#!/usr/bin/env python3
"""
update_help_corpus.py — AIStudio Help Corpus PDF Generator
Called by ais_update_help.sh. Do not run directly.
"""

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path


def fix_links(text: str, repo_root: Path) -> str:
    def rewrite(m):
        label, href = m.group(1), m.group(2)
        if href.startswith(("http", "mailto", "#", "file://")):
            return m.group(0)
        anchor = ""
        if "#" in href:
            href, anchor = href.split("#", 1)
            anchor = f"#{anchor}"
        pdf_href = href.replace(".md", ".pdf")
        if (repo_root / pdf_href).exists():
            return f"[{label}](file://{repo_root}/{pdf_href}{anchor})"
        if (repo_root / href).exists():
            return f"[{label}](file://{repo_root}/{href}{anchor})"
        return label

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", rewrite, text)


def generate_pdf(subject: dict, repo_root: Path, uploads_dir: Path) -> bool:
    import markdown as md_lib
    from weasyprint import HTML

    today = date.today().strftime("%B %d, %Y")
    source = repo_root / subject["source_md"]
    pdf_path = repo_root / subject["pdf"]
    pdf_name = Path(subject["pdf"]).name
    corpus_dest = uploads_dir / pdf_name

    if not source.exists():
        print(f"  ⚠  Source not found: {subject['source_md']} — skipping")
        return False

    print(f"  Generating {pdf_name} from {subject['source_md']}...")

    md_text = source.read_text()
    md_text = re.sub(
        r"```mermaid.*?```",
        '<div class="mermaid-placeholder"><em>[Architecture diagram]</em></div>',
        md_text,
        flags=re.DOTALL,
    )
    md_text = re.sub(r"\[!\[CI\].*?\]\(.*?\)\n?", "", md_text)
    md_text = fix_links(md_text, repo_root)

    md = md_lib.Markdown(extensions=["tables", "fenced_code", "toc"])
    body = md.convert(md_text)

    css = f"""
  @page {{ margin: 2cm 2cm 2.8cm 2cm; @bottom-center {{ content: "{pdf_name}    |    AIStudio    |    {today}    |    Page " counter(page) " of " counter(pages); font-family: Arial, Helvetica, sans-serif; font-size: 9pt; color: #999999; }} }}
  body {{ font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.6; color: #1a1a1a; }}
  h1 {{ font-size: 22pt; color: #1a1a2e; border-bottom: 2px solid #4a90d9; padding-bottom: 6px; margin-top: 24px; }}
  h2 {{ font-size: 16pt; color: #16213e; border-bottom: 1px solid #ddd; padding-bottom: 4px; margin-top: 20px; }}
  h3 {{ font-size: 13pt; color: #333; margin-top: 16px; }}
  p {{ margin: 6px 0; }}
  strong em, em strong {{ color: #4a90d9; font-style: italic; font-weight: bold; }}
  a {{ color: #4a90d9; text-decoration: none; }}
  code {{ background: #f4f4f4; padding: 1px 4px; border-radius: 3px; font-family: 'Courier New', monospace; font-size: 9.5pt; }}
  pre {{ background: #1a1a2e; color: #e0e0e0; padding: 12px 16px; border-radius: 6px; font-size: 9pt; line-height: 1.4; }}
  pre code {{ background: none; color: inherit; padding: 0; }}
  table {{ border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 10pt; }}
  th {{ background: #1a1a2e; color: white; padding: 8px 12px; text-align: left; }}
  td {{ border: 1px solid #ddd; padding: 7px 12px; }}
  tr:nth-child(even) td {{ background: #f9f9f9; }}
  blockquote {{ border-left: 4px solid #4a90d9; margin: 12px 0; padding: 8px 16px; background: #f0f6ff; font-style: italic; }}
  hr {{ border: none; border-top: 1px solid #ddd; margin: 24px 0; }}
  .mermaid-placeholder {{ background: #f0f6ff; border: 1px solid #4a90d9; border-radius: 6px; padding: 12px 16px; color: #555; font-style: italic; margin: 12px 0; }}
  .doc-header {{ text-align: center; margin-bottom: 32px; padding-bottom: 16px; border-bottom: 2px solid #4a90d9; }}
  .logo {{ font-size: 26pt; font-weight: bold; letter-spacing: -1px; font-family: Arial, sans-serif; }}
  .logo-ai {{ color: #1a1a1a; }}
  .logo-studio {{ color: #4a90d9; }}
"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>{css}</style></head>
<body>
<div class="doc-header">
  <div class="logo"><span class="logo-ai">AI</span><span class="logo-studio">Studio</span></div>
</div>
{body}
</body></html>"""

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    html_tmp = pdf_path.with_suffix(".gen.html")
    html_tmp.write_text(html)
    HTML(filename=str(html_tmp)).write_pdf(str(pdf_path))
    html_tmp.unlink()

    uploads_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(pdf_path), str(corpus_dest))
    print(f"  ✓ {pdf_name} → {corpus_dest}")

    # Also copy to ~/Downloads for manual testing and UI re-ingestion
    downloads_dest = Path.home() / "Downloads" / pdf_name
    shutil.copy2(str(pdf_path), str(downloads_dest))
    print(f"  ✓ {pdf_name} → ~/Downloads/")
    return True


def main():
    parser = argparse.ArgumentParser(description="AIStudio Help Corpus PDF Generator")
    parser.add_argument("--repo-root", required=True, help="Repo root path")
    parser.add_argument("--subject", default=None, help="Single subject to update (optional)")
    args = parser.parse_args()

    import yaml

    repo_root = Path(args.repo_root)
    # Manifest lives in meta/ — survives corpus deletion
    manifest_path = repo_root / "meta" / "help_manifest.yaml"
    uploads_dir = repo_root / "data" / "corpora" / "help" / "uploads"

    if not manifest_path.exists():
        print(f"❌ Manifest not found: {manifest_path}")
        print("   Deploy it first: ais_deploy help_manifest.yaml")
        sys.exit(1)

    # Create corpus directory structure if it doesn't exist
    uploads_dir.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ Corpus directory ready: {uploads_dir}")

    with open(manifest_path) as f:
        manifest = yaml.safe_load(f)

    subjects = manifest.get("subjects", [])
    updated = []

    for s in subjects:
        if args.subject and s["subject"] != args.subject:
            continue
        print(f"\n── {s['subject']} ──────────────────────────────────")
        if generate_pdf(s, repo_root, uploads_dir):
            updated.append(s["subject"])

    # Update last_updated in manifest
    if updated:
        raw = manifest_path.read_text()
        today = date.today().isoformat()
        for subj in updated:
            raw = re.sub(
                rf'(subject: {subj}.*?last_updated: ")[^"]*(")',
                rf"\g<1>{today}\g<2>",
                raw,
                flags=re.DOTALL,
            )
        manifest_path.write_text(raw)

    print("\n── Summary ──────────────────────────────────")
    print(f"  Updated: {len(updated)}")
    for s in updated:
        print(f"    ✓ {s}")
    print("\n  Next step — re-ingest help corpus via the UI:")
    print("    1. Open AIStudio")
    print("    2. Select the 'help' corpus")
    print("    3. Click Add and select all PDFs from ~/Downloads/")


if __name__ == "__main__":
    main()
