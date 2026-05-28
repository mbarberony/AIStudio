#!/usr/bin/env python3
"""
ais_enrich_qdrant.py — One-time Qdrant payload enrichment with alias prefixes.
Version: 1.0.0

Updates the `text` payload field of existing Qdrant chunks to inject
Wikidata natural query forms into the [Document:] prefix — without re-ingesting.

NOTE: This updates text payloads only. Vectors are NOT recomputed.
BM25 index benefits immediately. Vector recall improvement requires re-ingest.
Use this for fast validation; re-ingest both corpora for full benefit.

Usage:
  python3 scripts/ais_enrich_qdrant.py --corpus sec_10k [--dry-run]
  python3 scripts/ais_enrich_qdrant.py --corpus esef_banks [--dry-run]
  python3 scripts/ais_enrich_qdrant.py --corpus sec_10k --rollback

Rollback: stores original text in `text_pre_enrichment` payload field before
updating. --rollback restores from that field.
"""

import argparse
import sys
from pathlib import Path

SCRIPT_NAME = "ais_enrich_qdrant"
VERSION = "1.0.0"


def _bold(text: str) -> str:
    return f"\033[1m{text}\033[0m"


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not find repo root")


def _load_ks_alias_map(repo: Path, corpus: str) -> dict[str, list[str]]:
    """Load Wikidata natural query forms from entities YAML."""
    import yaml
    ks_dir = repo / "data" / "knowledge_sources" / "gleif"
    if not ks_dir.exists():
        return {}
    matches = sorted(ks_dir.glob(f"gleif_{corpus}_*_entities.yaml"))
    if not matches:
        return {}
    with open(matches[0], encoding="utf-8") as f:
        data = yaml.safe_load(f)
    import unicodedata

    def _normalize(s: str) -> str:
        """Strip accents and normalize to ASCII for fuzzy key matching."""
        return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii").strip()

    alias_map: dict[str, list[str]] = {}
    for entity in data.get("entities", []):
        canonical = entity.get("canonical", "")
        if not canonical:
            continue
        natural: list[str] = []
        scope_name = entity.get("scope_name", "")
        label = entity.get("wikidata_label", "")
        short = entity.get("wikidata_short_name", "")
        tickers = entity.get("wikidata_tickers", [])
        if scope_name and scope_name != canonical:
            natural.append(scope_name)
        if label and label != scope_name and label != canonical:
            natural.append(label)
        if short and short not in natural and short != canonical:
            natural.append(short)
        for t in (tickers or []):
            if t and len(t) <= 6 and t not in natural:
                natural.append(t)

        # Index by canonical AND all alias variants — XBRL EntityRegistrantName
        # uses the firm's self-reported name which may differ from GLEIF canonical
        # (e.g. "Société Générale" vs "SOCIETE GENERALE", "CRÉDIT AGRICOLE S.A."
        # vs "CREDIT AGRICOLE SA"). Index all forms so any variant matches.
        keys_to_index = {canonical}
        keys_to_index.add(_normalize(canonical))          # accent-stripped
        keys_to_index.add(canonical.title())              # Title Case
        keys_to_index.add(_normalize(canonical).title())  # Title Case accent-stripped
        for alias in entity.get("aliases", []):
            if alias and len(alias) > 3:
                keys_to_index.add(alias)
                keys_to_index.add(_normalize(alias))

        # Also index by xbrl_name if present — exact XBRL EntityRegistrantName
        # string that appears in [Document:] prefixes of existing chunks
        xbrl_name = entity.get("xbrl_name", "")
        if xbrl_name:
            keys_to_index.add(xbrl_name)
            keys_to_index.add(_normalize(xbrl_name))

        for key in keys_to_index:
            if key:
                alias_map[key] = natural

    return alias_map


def _enrich_prefix(text: str, alias_map: dict[str, list[str]]) -> tuple[str, bool]:
    """
    Inject aliases into [Document: <entity> ...] prefix if entity is in alias_map.
    Returns (new_text, was_changed).
    Only modifies chunks that have a [Document:] prefix — leaves others unchanged.
    Does not double-inject if aliases already present.
    """
    if not text.startswith("[Document: "):
        return text, False

    # Extract the prefix up to the first ]
    end = text.find("]")
    if end == -1:
        return text, False

    prefix_content = text[len("[Document: "):end]  # e.g. "THE GOLDMAN SACHS GROUP, INC. FY2025"
    rest = text[end + 1:]  # " chunk text..."

    # Check if already enriched (contains |)
    if " | " in prefix_content:
        return text, False

    # Split entity from FY year if present
    if " FY" in prefix_content:
        entity_part, fy_part = prefix_content.split(" FY", 1)
        fy_str = f" FY{fy_part}"
    else:
        entity_part = prefix_content
        fy_str = ""

    entity_part = entity_part.strip()
    # Try exact match first, then normalized variants
    aliases = (alias_map.get(entity_part)
               or alias_map.get(entity_part.upper())
               or alias_map.get(entity_part.title()))
    if not aliases:
        import unicodedata
        normalized = unicodedata.normalize("NFKD", entity_part).encode("ascii", "ignore").decode("ascii").strip()
        aliases = alias_map.get(normalized) or alias_map.get(normalized.upper())
    if not aliases:
        return text, False

    alias_str = " | " + " | ".join(aliases)
    new_prefix = f"[Document: {entity_part}{alias_str}{fy_str}]{rest}"
    return new_prefix, True


def run(corpus: str, dry_run: bool, rollback: bool) -> int:
    print(_bold(f"[{SCRIPT_NAME} v{VERSION} — Qdrant alias enrichment]"))

    try:
        import yaml  # noqa: F401
    except ImportError:
        print("  ✗ pyyaml not installed — pip3 install pyyaml --break-system-packages")
        return 1

    repo = _repo_root()
    sys.path.insert(0, str(repo / "src"))

    try:
        from qdrant_client import QdrantClient
        from qdrant_client.models import PayloadSelectorInclude
    except ImportError:
        print("  ✗ qdrant-client not installed")
        return 1

    collection_name = f"aistudio_{corpus}"
    client = QdrantClient(host="localhost", port=6333)

    # Verify collection exists
    try:
        info = client.get_collection(collection_name)
        total_points = info.points_count
    except Exception as e:
        print(f"  ✗ Collection {collection_name!r} not found: {e}")
        return 1

    print("--- Config")
    print(f"  · Corpus    : {corpus}")
    print(f"  · Collection: {collection_name} ({total_points:,} points)")
    print(f"  · Mode      : {'DRY RUN' if dry_run else 'ROLLBACK' if rollback else 'LIVE'}")

    if rollback:
        print("--- Rolling back to pre-enrichment text")
        offset = None
        rolled_back = 0
        while True:
            results, offset = client.scroll(
                collection_name=collection_name,
                scroll_filter=None,
                limit=200,
                offset=offset,
                with_payload=PayloadSelectorInclude(include=["text_pre_enrichment"]),
                with_vectors=False,
            )
            if not results:
                break
            updates = []
            for point in results:
                original = (point.payload or {}).get("text_pre_enrichment")
                if original:
                    updates.append((point.id, original))
            if updates and not dry_run:
                for point_id, orig_text in updates:
                    client.set_payload(
                        collection_name=collection_name,
                        payload={"text": orig_text},
                        points=[point_id],
                    )
            rolled_back += len(updates)
            if offset is None:
                break
        print(f"  ✅ Rolled back {rolled_back:,} points")
        return 0

    # Load alias map
    alias_map = _load_ks_alias_map(repo, corpus)
    if not alias_map:
        print(f"  ⚠ No knowledge sources found for corpus '{corpus}' — nothing to do")
        return 0
    print(f"  · Entities  : {len(alias_map)} in alias map")

    print("--- Scanning chunks")
    offset = None
    updated = 0
    skipped_no_prefix = 0
    skipped_already_enriched = 0
    skipped_no_match = 0

    while True:
        results, offset = client.scroll(
            collection_name=collection_name,
            scroll_filter=None,
            limit=200,
            offset=offset,
            with_payload=PayloadSelectorInclude(include=["text"]),
            with_vectors=False,
        )
        if not results:
            break

        # Accumulate updates for this page, then write in one batch per point
        # (Qdrant set_payload with multiple point IDs requires same payload value,
        # so we group by new_text and send one call per unique payload)
        page_updates: list[tuple[str, str, str]] = []  # (point_id, orig_text, new_text)

        for point in results:
            text = (point.payload or {}).get("text", "")
            if not text:
                skipped_no_prefix += 1
                continue

            new_text, changed = _enrich_prefix(text, alias_map)

            if not changed:
                if " | " in (text[:100] if text.startswith("[Document: ") else ""):
                    skipped_already_enriched += 1
                elif not text.startswith("[Document: "):
                    skipped_no_prefix += 1
                else:
                    skipped_no_match += 1
                continue

            page_updates.append((point.id, text, new_text))
            updated += 1

        if page_updates and not dry_run:
            # Send one set_payload per point — retry on connection error
            for point_id, orig_text, new_text in page_updates:
                for attempt in range(3):
                    try:
                        client.set_payload(
                            collection_name=collection_name,
                            payload={"text_pre_enrichment": orig_text, "text": new_text},
                            points=[point_id],
                        )
                        break
                    except Exception:  # noqa: BLE001
                        if attempt == 2:
                            raise
                        import time as _time
                        _time.sleep(1 + attempt)
                        # Reconnect
                        client = QdrantClient(host="localhost", port=6333)

        if offset is None:
            break

    print("--- Summary")
    print(f"  · Updated              : {updated:,}")
    print(f"  · Skipped (no prefix)  : {skipped_no_prefix:,}")
    print(f"  · Skipped (no match)   : {skipped_no_match:,}")
    print(f"  · Skipped (enriched)   : {skipped_already_enriched:,}")
    if dry_run:
        print("  ℹ Dry run — no changes written")
    else:
        print(f"  ✅ Done — {updated:,} chunks enriched in {collection_name}")
        print("  ℹ Rollback: python3 scripts/ais_enrich_qdrant.py"
              f" --corpus {corpus} --rollback")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Enrich Qdrant chunk text payloads with entity aliases"
    )
    parser.add_argument("--corpus", required=True, help="Corpus name (e.g. sec_10k)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Scan and report without writing")
    parser.add_argument("--rollback", action="store_true",
                        help="Restore text from text_pre_enrichment backup field")
    args = parser.parse_args(argv)
    return run(args.corpus, args.dry_run, args.rollback)


if __name__ == "__main__":
    sys.exit(main())
