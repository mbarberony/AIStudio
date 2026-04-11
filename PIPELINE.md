# AIStudio — Pipeline
*Last updated: 2026-04-07*
*Version: 1.0.0*

---

## 1. Purpose of This Document

This document records thinking about how AIStudio is and will evolve. It serves three purposes:

**Product thinking:** What needs to ship, in what order, and why. The wave structure reflects a deliberate build sequence — each wave unlocks the next. Beta Gate must ship before the LinkedIn story can be told. Wave 2 RAG quality improvements make the demo more credible. Wave 3 (urCrew) depends on Wave 2 infrastructure being stable.

**Session planning:** The top of the Next Session section answers the question "what do we do today?" without re-reading everything. Items are ordered by urgency, not by category.

**Decision log:** Architecture decisions, naming conventions, and protocol choices are recorded here when they don't warrant a full STD document. Implementation considerations that might change are noted inline.

- [ ] Naming convention review — as exempt files and operator/user split patterns accumulate, review STD - General - Naming Conventions for patterns worth codifying as first-class rules. Trigger: when exempt list exceeds ~15 entries or a third structural exception type appears. Current candidates: extensionless files (`install_ops`), `_ops` suffix files, repo fixtures with no date. (Added 2026-03-31)

---

## 2. Next Session — Do First

*These are urgent, blocking, or iron-is-hot items:*

*Weekend (Sat-Sun April 4-5) — 100% AIStudio, no job items:*

- [x] AIStudio_070 — 0 chunks display bug + AIStudio_109 conversation refresh — both in rag_studio.html, do together (Beta gate)
- [ ] AIStudio_111 — SEC corpus rename + re-ingest on M4 Air (deferred — use as M4 Air fresh install test, AIStudio_069)
- [ ] AIStudio_068 — System prompt hedging language — prompts/system.txt, 15 min (Beta gate)
- [x] AIStudio_106 — Create ais_restore_scripts — DONE (session summary 2026-04-05) — referenced in HOWTO_OPS but doesn't exist (Beta gate)
- [ ] AIStudio_066 — Qdrant WAL lock noise on restart — investigate stop.sh (Beta gate)
- [ ] AIStudio_101 + AIStudio_102 + AIStudio_103 — preflight check, llama model check, port conflict — install quality (Beta gate)
- [ ] AIStudio_060 + AIStudio_062 — repo cleanup + docs/ audit — sweep session (Beta gate)
- [ ] AIStudio_087 — test suite reassessment — run integration suite, assess gaps (Beta gate)
- [ ] AIStudio_069 — benchmark editorial pass → M4 Air fresh install test (Beta gate)
- [ ] AIStudio_075 + AIStudio_073 — Help button null polish + corpus selector height verify (Beta gate)
- [ ] AIStudio_079 — HOWTO troubleshooting note (Beta gate)

*Post-weekend (lower priority):*
- [ ] AIStudio_116 — ais_check_ops integrity test suite
- [ ] AIStudio_117 — HOWTO restructuring (A-I) — ~1-2 hour session
- [ ] AIStudio_118 — Rename generate_packet.sh → ais_packet_ops (post-Beta)
- [ ] AIStudio_119 — Design meta/ folder structure for full JOB + urCrew components (post-Beta)
- [ ] AIStudio_120 — urCrew activation session: repo decoupling, per-domain PIPELINE/manifest, job_packet/job_bundle commands (post-Beta, prerequisite: Beta declared)
- [ ] AIStudio_121 — Bootstrap EOS step: capture "other context" (boundary conditions) so Section 8 of New Thread Bootstrap is populated from previous session (post-Beta)
- [ ] AIStudio_122 — ais_deploy multi-file support: `ais_deploy file1 file2 file3` — sequential, fail-fast, summary at end. --to flag must work with multi-file syntax. Update manifest if new routing needed. Update --help. Post-Beta.
- [ ] AIStudio_123 — Remove live chunk count from ingest progress message — show 'X/Y files' only during ingest, consistent with final summary (Post-Beta)
- [ ] AIStudio_124 — v2.0: corpus metadata at creation time — UI fields for short_description, content_summary, search_guidance when creating a corpus. Persist to corpus_meta.yaml. Refactor corpus naming: implement CONF naming standard (AIStudio_093). System prompt loaded from system.txt not hardcoded in api.py.

- [x] Complete `ais_*` refactor — `.zshrc` dedup, add `ais_test`, `ais_check`, `ais_bench`, `ais_sec_download`, `ais_help`
- [x] Create `ais_help.sh` — prints all ais_* commands with descriptions
- [x] Codify `canonical_name` rule in HOWTO — always use `ais_deploy` to promote files from ~/Downloads, never bare `cp` (macOS appends `(N)` suffix breaking filenames)
- [x] HARNESS.md rewrite — point to `benchmarks/benchmark.py`, remove all `run_demo.py` references
- [x] CLAUDE.md update — replace `run_demo.py` command with `benchmarks/benchmark.py`
- [x] Trash `run_demo.py`, `run_demo_config.json`, root `BENCHMARK_FINDINGS.md`, `data/demo/` (after HARNESS.md + CLAUDE.md updated)
- [x] Move `data/demo/DEMO_CORPUS.md` → `docs/` — referenced in README
- [x] HOWTO — add corpus file recovery / trash folder section
- [x] QUICKSTART Step 7 — update tuning parameter names to match actual UI labels
- [ ] Extract principles (1-11) from `generate_packet.sh` into standalone `PRINC - AIStudio - Core Principles - YYYY-MM-DD.yaml`
- [x] Verify `ais_packet` and `ais_bundle` aliases survive cold shell sessions — superceded by --help requirement
- [ ] Add /epaves/ to .gitignore — epaves protocol requires this before first use. Also add epaves/ entry to bundle_manifest.yaml exclusion list.
- [ ] Consider PIPELINE public/private split — sanitized version at repo root vs full version in meta/
- [ ] Add `ais_ops_help.sh` to scripts/ — operator command reference (mirrors ais_help.sh)
- [ ] Move `download_sec_corpus.py` to `data/corpora/sec_10k/scripts/` — corpus-specific tooling
- [ ] Move user scripts from repo root to `ais_scripts/` subfolder (post-Beta polish)
- [x] Extend bundle_manifest.yaml to support repo-root-relative paths — deploy_to field added
- [x] Add filter-repo + .gitignore sequencing to HOWTO_OPS ✅ done this session

- [ ] AIStudio_041 — public_manifest.yaml at data/corpora/help/
- [ ] AIStudio_042 — ops_manifest.yaml at repo root + gitignore
- [ ] AIStudio_043 — Audit QUICKSTART.md — split operator content to QUICKSTART_ops.md
- [ ] AIStudio_044 — Audit HOWTO.md — split operator content to HOWTO_ops.md
- [ ] AIStudio_045 — Wire Help corpus ingest to read public_manifest.yaml
- [ ] AIStudio_046 — Rename HOWTO_OPS.md → HOWTO_ops.md
- [ ] AIStudio_047 — Add ops-leak checklist to pre-commit
- [x] AIStudio_052 — install.sh user-only, install_ops one-word operator install, auto-sources ~/.zshrc — 27c91d9
- [ ] AIStudio_053 — Implement manifest pattern for user vs ops separation. Apply to install, codify as standard. Connects to public_manifest.yaml / ops_manifest.yaml architecture.
- [ ] AIStudio_054 — Add --help to ais_* commands (POC)
- [ ] AIStudio_055 — Add install_ops deploy_to entry to bundle_manifest.yaml
- [x] AIStudio_048 — ais_sec_download alias fixed: correct path, --out ~/Downloads/sec_10k — ba2c0f6
- [x] AIStudio_049 — HOWTO.md SEC section fixed: UI-only ingest, correct path, narrative — ba2c0f6
- [x] AIStudio_050 — QUICKSTART.md SEC section fixed: ais_sec_download, UI ingest, cross-refs — ba2c0f6
- [x] AIStudio_051 — scripts/ais_commit.sh and ais_publish.sh created — ba2c0f6

---

## 3. Active Pipeline by Wave

### 🔴 BETA GATE — Must ship before Beta declaration

**Tests & Quality**
- [x] Run test suite — 31 passed, 0 failed ✅ 2026-04-06 (ais_test)

**UI Fixes**
- [x] Centered numbers in Top K and Temperature input fields — already in CSS, confirmed
- [x] Tooltips on Top K and Temperature — added title= attributes
- [ ] Help button in topbar — not built, separate from About
- [ ] Cold start protocol — when starting a session without a BUNDLE, Claude should: (1) ask Manuel to run `ls -la ~/Developer/AIStudio/meta/bundle_manifest.yaml` to confirm manifest is accessible, (2) ask Manuel to paste or upload the manifest before creating any new file types, (3) note which operator rules apply by asking "is there a recent PACKET I should read?" This closes the cold-start rule gap.

- [ ] PDF page numbers in footer — generated PDFs missing page N of N in footer. Add to PDF generation standard and update update_help_corpus.py.
- [ ] **Modal Window Standard** — all modals need: centered bold title describing the action (e.g. "Adding Files to Corpus 'help'", "Delete Corpus 'help'"), consistent styling. Apply to: file upload modal, corpus delete modal, about modal, YES confirmation modal. Create STD - AIStudio - Modal Window Standard.
- [x] AIStudio_076 — EOS protocol: transcript verification rule (rule d) + cp command rule for _session_summary.md. New STD version: STD - AIStudio - EOS Bundle - 2026-04-02.md
- [x] AIStudio_072 — EOS protocol: add PDF/MD sync step (Step 2b) to two places:
    (a) generate_packet.sh "How Manuel Works" section: add rule
        "PDF/MD sync: every .md with a companion PDF must be regenerated together.
        Run ais_update_help after any doc change. Never ship a stale PDF."
    (b) STD - AIStudio - EOS Bundle - 2026-03-31.md: add Step 2b between Step 2 and Step 3:
        "Verify PDF/MD sync — for every modified .md, confirm companion PDF regenerated.
        If not: run ais_update_help before proceeding."
    Files to check every EOS: HOWTO, QUICKSTART, README, architecture_decisions,
    HARNESS, DEMO_CORPUS, roadmap, dependencies (all have .md + .pdf pairs) (Step 2b):
    For every .md with companion PDF, verify both regenerated together before EOS.
    Update STD - AIStudio - EOS Bundle + generate_packet.sh "How Manuel Works".
    Also: add QUICKSTART.md to bundle_manifest.yaml deploy_to "./" — DONE this session.
    Also: add README.md deploy_to "./" to manifest — DONE this session.
- [x] AIStudio_071 — Help button implementation (Beta gate): SHIPPED
    Help button added to topbar [About][Help][● Connected].
    Switches to help corpus + welcome message if found.
    Fallback message with ais_update_help instructions if not found.
    Three follow-up items logged as AIStudio_073/074/075 below.
- [x] AIStudio_075 — Confirmed OK 2026-04-06
    Currently shows fallback text if help corpus missing — verify no 'null' displays
    anywhere in UI when corpus doesn't exist (broader check, not just Help button)
- [x] AIStudio_074 — Help corpus: hide 'help' from corpus selector dropdown
    Help is a system corpus — should not appear as a user-selectable option.
    Filter it out in the corpus list rendering: corpora.filter(c => c !== 'help')
    Also hide from New Corpus modal if name collision check includes it.
- [x] AIStudio_073 — Corpus selector height confirmed OK 2026-04-06
    Reported earlier: selector field height inconsistent. Check if still present
    after today's modal/UI changes.
    Add 'Help' button to header between About and Connected status.
    Behavior: switches corpus selector to 'help', sends a welcome message in chat:
    'Help mode — ask me anything about using AIStudio. Try: How do I create a corpus?'
    Restores previous corpus when user manually switches away.
    Fallback if help corpus not found: show message 'Help corpus not yet ingested —
    run ais_update_help then re-ingest the help corpus via Add.'
    Header order per UX STD: [About] [Help] [● Connected]
- [x] AIStudio_070 — Ingestion progress final summary shows wrong counts: "1280 files · 0 chunks" instead of "13 files · 1289 chunks". Root cause: _stream_stderr() returns last tqdm line overall, which is the Discover bar (fast file scan, no chunks) not the Process bar. Fix: cache last_process_line separately (lines containing "chunks=" or "%" with N/N pattern). Also: progress bar jumps 13%→100% because Process bar completes before first 2s poll interval on small corpora — cache counts on each line so status endpoint always returns last known good values even after process exits. (Added 2026-04-01)
- [x] "Ingestion failed — check server logs" — false negative UI bug. Ingestion succeeds but UI shows failure. Fix the status polling/display logic. PARTIAL: race condition fixed (single ingest endpoint), progress bar streaming fixed. Final summary counts still wrong (AIStudio_070). Also add to HOWTO: "If you see this message, check Stats — if chunk count > 0, ingestion succeeded."
- [ ] Integrate ais_update_help into EOS — when any help corpus source .md is modified, run ais_update_help as part of EOS Step 0 doc audit, then re-ingest help corpus via UI.
- [ ] ais_update_help + ingest — add post-generation message: "Re-ingest via UI: select help corpus → Delete all files → Add → select all PDFs from ~/Downloads/"
- [x] Delete confirmation modal — remove "This page says" browser default dialog. All four modals replaced with showModal() helper. Replace with custom modal: bold centered title "Removing File from Corpus", proper capitalization, corpus name in single quotes. Same pattern as YES confirmation modal.
- [ ] Remove automatic creation of chroma/ subfolder on corpus init — stale ChromaDB artifact, creates confusion.
- [ ] Auto-create questions/ subfolder in each new corpus with empty placeholder file — supports future benchmark question file per corpus.
- [ ] HOWTO.md — fix "How do I start AIStudio?" answer: remove confusing source/.zshrc chaining language, simplify to "run ais_start". Language should assume aliases are already loaded (install.sh handles this).
- [ ] QA_TESTING_LESSONS_LEARNED — removed from help corpus. Remove from help_manifest.yaml.
- [ ] ais_bench <corpus_name> — document in HOWTO_OPS and ais_help_ops. Add --help to ais_bench.
- [ ] **Source Dive** — click citation → PDF opens at exact page with relevant chunk highlighted. Requires pdfjs viewer + chunk position metadata. v2.0 roadmap item. Rename existing "Open ↗" to "Source Dive ↗" when implemented.
- [ ] AIStudio_060 — Corpus metadata + per-corpus system prompt: when creating a corpus, user can optionally provide (a) description, (b) prompt guidance that gets merged with base system prompt at query time. Store in corpus-level config file (e.g. data/corpora/{name}/corpus.yaml). UI: add optional description field to New Corpus modal. API: load corpus.yaml at query time, merge guidance into system prompt. Enables different query framing per corpus (architecture docs vs SEC filings vs help). (Added 2026-03-31)
- [x] AIStudio_061 — Audit and clean root-level files: epaved AIStudio-README.pdf (stale) and HOWTO_OPS.pdf (orphaned); moved QA_TESTING_LESSONS_LEARNED.md+.pdf to docs/; added to help_manifest.yaml and README. DONE eed9374 2026-04-03. delete HOW_TO.md (superseded by HOWTO.md), delete HOWTO_ops.md (wrong case, duplicate of HOWTO_OPS.md in meta/), delete deploy.sh (superseded by ais_deploy — references dead ~/code/AIStudio path), confirm prompts/system.txt is either wired into api.py or delete as orphan. Also confirm sec_10k corpus is ghost of SEC and clean up. (Added 2026-03-31)
- [ ] AIStudio_062 — Audit unknown docs/ files before Beta: EMBEDDING_TESTING_GUIDE.md, RAG_WEB_SEARCH_AND_OPTIMIZATION.md, data_model.md, ui_architecture.md, TESTS.md — decide: keep+review, archive, or delete. These are not in help corpus. (Added 2026-03-31)
- [ ] AIStudio_069 — Benchmark report editorial pass before external sharing:
    (a) Known Limitations section: remove developer jargon (XBRL stripping, CIK collision)
        or reframe as user-facing limitations
    (b) Roadmap section: remove items already shipped (CrossEncoder, page-aware chunking,
        PDF viewer, --force ingest) — stale vs README
    (c) Consider two report modes: --internal (full detail) vs --external (clean summary)
- [x] AIStudio_082 — Rename ais_update_help → ais_update_help_ops (operator-only, not user-facing). Add to install_ops, remove from install.sh. Update all references in HOWTO_OPS.md, bundle_manifest.yaml, EOS STD, generate_packet.sh. The help corpus re-generation is an operator task — users should never need to run it. (Beta gate)
- [ ] AIStudio_083 — Add auto re-ingest to ais_update_help_ops: after regenerating PDFs, automatically delete existing help corpus chunks in Qdrant and re-ingest all 8 PDFs without requiring UI interaction. This makes help corpus updates fully headless. Requires Qdrant Python client call to delete collection + re-run ingest pipeline programmatically. (Wave 2 — after Beta, but log now)
- [ ] AIStudio_084 — Corpus metadata modal (new feature): when creating a new corpus, show an optional metadata form with fields: Short description, Corpus content description (what's in it), Search guidance (how to look up content, what kinds of questions it answers), Other notes. Store in data/corpora/{name}/corpus_meta.yaml. At query time, prepend relevant metadata to system prompt to guide retrieval. For the help corpus: hardwire guidance to direct generic AIStudio questions toward README first. This directly fixes the README ranking problem observed today. (Wave 2 product feature — PIPELINE it now)
- [x] AIStudio_079 — Add "do not rename corpus files after ingestion" to HOWTO.md — DONE 2026-04-06 Troubleshooting section. Plain English, no Qdrant mention. Corpus records file/folder names at ingest time; renaming breaks citation lookup. Safe approach: delete via UI, recreate, re-ingest.
- [ ] AIStudio_095 — Define and document a standard for field ordering within file names. Current pattern has implicit ordering (TYPE - DOMAIN - Topic - Qualifier - Date) but the rules for what constitutes a Qualifier vs Topic are ambiguous. The WIP/Master issue in THINK files exposed this. Outcome: a clear decision table for when to use each position, with worked examples for all TYPE codes.
- [ ] AIStudio_096 — Review PIPELINE naming convention to enable tracking of multiple decoupled projects (AIStudio, JOB, urCrew, POS). Current convention uses AIStudio_NNN and JOB_NNN prefixes but these live in one file. As repos decouple, each project needs its own PIPELINE. Design: separate PIPELINE files per project with consistent item numbering, a master cross-project tracker, and naming convention for each. Prerequisite for repo decoupling (AIStudio_091).
- [ ] AIStudio_093 — Full manifest/config rename refactor. New naming convention: MAN - <COMMAND> - <SCOPE>.yaml and CONF - <SCOPE> - <Topic>.yaml. Rename: bundle_manifest.yaml → MAN - ais_deploy - Repo.yaml, help_manifest.yaml → MAN - ais_update_help_ops - Help Corpus.yaml, job_bundle_manifest → MAN - ais_bundle - Job Search.yaml, corpus_meta.yaml (help) → CONF - Help - Corpus Meta.yaml, corpus_meta.yaml (demo) → CONF - Demo - Corpus Meta.yaml. BEFORE STARTING: enumerate all first and second order consequences: (1st) files renamed, (2nd) deploy_files.sh hardcodes, bundle_session.sh hardcodes, update_help_corpus.py hardcodes, api.py hardcodes, generate_packet.sh references, STD files referencing old names, HOWTO_OPS references, PACKET template references, PIPELINE references, bundle_manifest.yaml self-referential entry. Do right, not convenient — T1.3a.
- [ ] AIStudio_094 — STD lifecycle status field. Add status field (INVESTIGATED/CANDIDATE/ACTIVE/DEPRECATED/ARCHIVED) to all STD file headers. Blocked on TH-017 (lifecycle state machine design). Option B — design first, apply after. See TH-019b.
- [x] AIStudio_092 — ais_deploy rename-on-deploy: no longer needed. Corpus meta files renamed to {corpus_name}_corpus_meta.yaml convention — unique names, routed via manifest static entries. --to flag no longer required. CLOSED 2026-04-06.
- [ ] AIStudio_101 — Add preflight check script scripts/check_env.sh: validates Python version (3.10+), PATH, Homebrew, Ollama, Qdrant binary presence before user starts install. Surfaced by QA_TESTING_LESSONS_LEARNED.md item #1/#8/#10. v1.1 target.
- [ ] AIStudio_102 — start.sh: check llama3.1:8b is available before starting. If not found, print clear error: "Required model not found. Run: ollama pull llama3.1:8b". Surfaced by QA_TESTING_LESSONS_LEARNED.md item #4. v1.1 target.
- [ ] AIStudio_103 — start.sh: port 8000 conflict handling. If port occupied, either kill old process or skip starting new one. Surfaced by QA_TESTING_LESSONS_LEARNED.md item #11. v1.1 target.
- [ ] AIStudio_104 — Reconcile demo_questions.yaml with DEMO_CORPUS.md and QA_TESTING_LESSONS_LEARNED.md. Three sources of demo questions exist — they should be consistent. DEMO_CORPUS.md is user-facing; demo_questions.yaml is machine-readable benchmark source; QA doc has validated subset. Add cross-reference in DEMO_CORPUS.md pointing to demo_questions.yaml. Add note in ais_bench.sh --help output referencing the questions file.
- [ ] AIStudio_107 — Clean stale files from help corpus uploads: README_1775177361.pdf and any other timestamp-named files appearing in corpus citations. These are leftover from earlier ingest runs. Delete via UI or truncate manifest.jsonl and re-ingest cleanly. Also: ais_update_help_ops should wipe stale PDFs before copying new ones.
- [x] AIStudio_109 — UI bug: conversation history lost on page refresh. The chat area shows "Conversation cleared" after refresh instead of restoring the previous conversation. Investigate: (a) is conversation state being saved to localStorage or session storage? (b) is the clear triggered by an event listener on page load? Expected behavior: conversation persists across refresh within the same session. Beta gate.
- [ ] AIStudio_108 — Conversation persistence (Wave 2): conversation history currently lives in browser memory only — cleared on refresh. Add server-side conversation storage per corpus session. Low priority until Beta is declared.
- [ ] AIStudio_100 — Add RAG Performance Findings to help corpus. Source .md file not found in repo (llm_analysis/ has no .md, only referenced PDF). Options: (A) write a new RAG Performance Findings .md from benchmark data and add to llm_analysis/, (B) extend ais_update_help_ops to support source_pdf field (skip .md→PDF generation, copy pre-built PDF directly). Option A preferred — creates a proper source document. Option B is an ais_update_help_ops enhancement.
- [x] AIStudio_106 — Create ais_restore_scripts — DONE (session summary 2026-04-05): extracts deploy_files.sh, generate_packet.sh, bundle_session.sh from latest BUNDLE zip in ~/Downloads and places them in scripts/. Referenced in HOWTO_OPS but script doesn't exist. Critical for post-filter-repo recovery. Also remove phantom alias from .zshrc if present.
- [ ] AIStudio_111 — All docs already use sec_10k consistently. On-disk folder is SEC/ and Qdrant collection is aistudio_SEC — mismatch is cosmetic. Deferred: rename + re-ingest to be done as part of M4 Air fresh install test (AIStudio_069). No doc changes needed.
- [ ] AIStudio_112 — Ingest from directory feature: allow user to specify a local directory path as a corpus source. Useful for SEC corpus (143 files). UI: add 'Ingest from folder' option. Backend: walk directory, filter by supported extensions, ingest all.
- [x] AIStudio_113 — Deploy ordering rule codified: bundle_manifest.yaml must be deployed before files whose entries it contains. Added as T2.1a in THINK Master and Section 2.2a in STD - General - Error Management and Prevention. DONE 2026-04-03: when bundle_manifest.yaml contains new glob entries, it must be deployed FIRST before deploying the files those entries cover. Otherwise ais_deploy loads the old manifest and prompts for destination. Corollary of T2.16d.
- [ ] AIStudio_114 — Define a standard for when and how to codify metadata in files (version, status, schema_version) vs in filenames vs in manifests vs in naming conventions. Questions to answer: when is a version number in a file header sufficient? when does the manifest need it? how do commands report version of what they read? See also T2.16c (schema versioning inside file). Outcome: a clear decision table codified in STD - General - Naming Conventions or a new STD - General - Metadata Standards.
- [ ] AIStudio_116 — Create ais_check_ops: shell-level integrity test suite for ops tooling. Tests: (1) .gitignore contains meta/, (2) git ls-files meta/ == 0, (3) all ais_* aliases defined, (4) bundle_manifest.yaml is valid YAML, (5) deploy_files.sh routes correctly using a temp mock file, (6) dotfile normalization works (gitignore.txt → .gitignore), (7) --to flag works. Run via ais_check_ops. Output: PASS/FAIL per test. Add to EOS checklist Step 1.
- [ ] AIStudio_118 — Rename generate_packet.sh → ais_packet_ops. Rationale: it is an operator script, must follow _ops convention. Before starting: enumerate all 1st and 2nd order consequences per T2.16b — (1st) file rename + manifest entry; (2nd) .zshrc alias, HOWTO_OPS.md references, STD - AIStudio - EOS Bundle, PACKET template self-references, PIPELINE references, bundle_manifest.yaml static entry. Post-Beta.
- [ ] AIStudio_119 — Design meta/ folder structure to accommodate full JOB bundle components in a structured, named way. Current state: job_hunting/ exists but is flat and mixed. Goal: define canonical subfolders (e.g. job_hunting/resumes/, job_hunting/tracker/, job_hunting/packets/, job_hunting/standards/, job_hunting/application_packages/), update bundle_manifest.yaml entries, update JOB bundle manifest, update ais_deploy routing. Prerequisite for JOB_020 meta cleanup and full decoupling. Post-Beta.
- [ ] AIStudio_120 — urCrew activation session: structured session to (1) finalize repo architecture (builds on AIStudio_091), (2) decouple PIPELINE.md into per-domain files (builds on AIStudio_096), (3) split bundle_manifest.yaml into per-domain manifests, (4) activate job_packet / job_bundle commands (JOB_002/003), (5) define urCrew repo structure and meta layout, (6) migrate meta/reference/ bootstrap infrastructure to correct home. Prerequisite: Beta declared. Trigger: "Let's think about this" → THINK - urCrew - Activation Session.
- [ ] AIStudio_121 — Add "other context" capture step to EOS protocol (and future ais_packet_ops). Goal: at EOS, Claude explicitly asks Manuel for boundary conditions (personal commitments, travel, other projects) and records them in the PACKET. This populates Section 8 of REF - urCrew - New Thread Bootstrap so the next Claude instance has it without asking. Update: STD - AIStudio - EOS Bundle, generate_packet.sh (and future ais_packet_ops) PACKET template. Post-Beta.
- [ ] AIStudio_122 — ais_deploy multi-file support: `ais_deploy file1 file2 file3` deploys each in sequence, stops on first failure, reports summary at end. Mirrors `&&` chain behavior but cleaner. --to flag must work with multi-file syntax (applies to all files in the batch, or per-file if mixed types). Update manifest if new routing needed. Update --help output. Codify in THINK Master: "batch where safe, flag where not — minimize operator friction." Post-Beta.
- [ ] AIStudio_123 — Remove live chunk count from ingest progress message. During ingest, status shows 'X/Y files · Z chunks' — chunk count mid-stream is unreliable. Simplify to 'X/Y files' only, consistent with final summary. One-liner in _stream_stderr() msg build block. Post-Beta.
- [ ] AIStudio_124 — v2.0 feature: corpus metadata at corpus creation time. UI: add optional fields to New Corpus modal (short_description, content_summary, search_guidance). Persist to data/corpora/{name}/corpus_meta.yaml on create. System prompt: load from prompts/system.txt at startup instead of hardcoding in api.py — prompt changes should not require code changes. Implement CONF naming standard for corpus_meta files (AIStudio_093). v2.0 milestone.
- [x] AIStudio_125 — Ingest header text: "✓ N files saved — being ingested into corpus 'demo'" never updated on completion. Fix: await pollIngestStatus result and update msgDiv header to "✓ N files ingested into corpus 'demo'" on done, "✗ Ingestion failed" on error. DONE 2026-04-05.
- [ ] AIStudio_126 — DEMO_SCRIPT_DAILY.md — new doc, video-script style walkthrough of day-to-day use: start AIStudio, select corpus, ask a question, interpret citations, open Source Dive, clear conversation, stop. Becomes reference for Beta acceptance testing AND eventual video script. Two demo routines total: QUICKSTART (install) + DEMO_SCRIPT_DAILY (usage).
- [ ] AIStudio_127 — Fresh install test on this Mac (~/Developer/AIStudio2 or similar different root), skipping dependency install (Ollama, Python already present). Validates install.sh path handling, alias setup, corpus init. Run both demo routines against it. Pre-M4 Air gate.
- [ ] AIStudio_128 — filter-repo pass to purge draft AI whitepaper PDFs (AI - August 2023 - 2024.pdf, barbero_ai_whitepaper.pdf) from git history. Files were in data/corpora/demo/uploads/trash/ in a transient commit. Must be done before any public repo sharing. Follow HOWTO_OPS filter-repo 5-step procedure exactly.
- [ ] AIStudio_129 — demo_corpus_meta.yaml: add article-level routing for remaining 3 journals (Strategy & Architecture 2006, Digitization, IT Infrastructure) once synopses available. Post-Beta.
- [ ] AIStudio_132 — Create ais_ignore: wrapper for the T2.5b gitignore exception pattern. Takes one or more filenames, adds each to .gitignore, runs git rm --cached if currently tracked, commits .gitignore only (never git add -A). Eliminates the manual multi-step process of gitignore + untrack. Usage: ais_ignore scripts/ais_backup.sh scripts/ais_commit.sh. Post-Beta.
- [ ] AIStudio_130 — Restructure operator scripts into scripts_ops/ directory. Gitignore scripts_ops/ as a whole (replaces per-file gitignore entries). Update all alias paths in .zshrc, bundle_manifest.yaml, HOWTO_OPS.md, ais_restore_scripts. Enumerate all 1st and 2nd order consequences per T2.16b before starting. Post-Beta.
- [x] AIStudio_136 — Individual file delete: keep original filename in trash, no epoch suffix. DONE 2026-04-06 — api.py.
- [x] AIStudio_140 — Remove chroma/ folder creation from corpus_paths.py. DONE 2026-04-06 — corpus_paths.py.
- [x] AIStudio_135 — Corpus doc/chunk count from live filesystem/Qdrant, not stale index. DONE 2026-04-06 — api.py get_corpus_info().
- [x] AIStudio_062 — Docs audit: epaved 5 stale docs, removed 4 superseded guides. DONE 2026-04-06 — commit d2971c6.
- [ ] AIStudio_133 — Known Limitation: complex multi-column PDF tables (tax forms) produce garbled extraction. Document in README Known Limitations + PRODUCT_ROADMAP. Fix path: improved PDF pre-processing (Wave 2+). Post-Beta.
- [ ] AIStudio_134 — Post-Beta: cross-document identity contamination within corpus. When multiple documents about different people share a corpus, retrieval does not respect document boundaries. Fix: per-document routing in corpus_meta.yaml. Post-Beta.
- [ ] AIStudio_137 — HOWTO corpus management section: remove terminal recovery commands, move to HOWTO_OPS only. HOWTO should be UI-only for all corpus operations. Post-Beta.
- [ ] AIStudio_138 — Frontend: render inline commands/code in RAG responses with monospace/italic styling. Detect backtick-wrapped strings in LLM output. Pointer: /howto endpoint anchor implementation. Post-Beta.
- [ ] AIStudio_139 — Decision: should scripts/start.sh and scripts/stop.sh be git-tracked and public? They contain no secrets. Currently gitignored by convention not necessity. Prerequisite: AIStudio_053, AIStudio_131. Post-Beta.
- [ ] AIStudio_141 — deploy_files.sh: manifest deploy_to should take precedence over find_in_repo to prevent routing to wrong file when duplicates exist (e.g. api.py in multiple locations). AIStudio_141.
- [ ] AIStudio_142 — ais_backup: add version info and key metrics to output — AIStudio version, repo file count, backup zip size, number of corpora. Makes each backup self-describing.
- [ ] AIStudio_143 — Pre-create uploads/trash/ subfolder on corpus creation in api.py create_corpus(). Currently created lazily on first file delete.
- [ ] AIStudio_144 — Orphaned Qdrant collection: aistudio_fr_10k exists in Qdrant but no fr_10k/ corpus folder on disk. Investigate origin, delete collection if orphaned. Run: curl -s http://localhost:6333/collections | python3 -m json.tool
- [ ] AIStudio_145 — New docs: CODEBASE_GUIDE.md (user-facing, docs/) + CODEBASE_GUIDE_OPS.md (operator, meta/reference/). Added to help corpus and bundle manifest. DONE 2026-04-06 — both files deployed.
- [ ] AIStudio_146 — help_manifest.yaml: remove stale roadmap entry (docs/roadmap.md was epaved 2026-04-06). DONE 2026-04-06.

- [ ] AIStudio_131 — Design and document full ops environment setup: what constitutes a complete ops environment, bootstrap path for a new operator from fresh clone + BUNDLE zip, whether ais_install_ops should exist as a script, role of BUNDLE in ops bootstrap. Companion STD stub: STD - AIStudio - Ops Environment Setup - 2026-04-06.md. Related: AIStudio_116 (ais_check_ops), AIStudio_130 (scripts_ops/). Post-Beta.
- [ ] AIStudio_110 — Add STD - General - Error Management and Prevention to generate_packet.sh PACKET template: (a) add to Bundle Contents read-first table, (b) add to "When to Consult" table with trigger "any file loss or recovery situation", (c) add trigger phrase "we better document that in the error management file" → updates the STD.
- [ ] AIStudio_105 — Add .gitignore safety guard to ais_commit: before running git add -A, check if .gitignore was modified in this session. If yes, prompt: "⚠️ .gitignore was modified — verify git status before proceeding (Y/N)?". This prevents the meta/ incident from recurring. Also add warning to EOS STD Step 2 checklist.
- [x] AIStudio_115 — Fix find_in_repo + dotfile normalization: v2.5.1 excluded hidden dirs from search; v2.5.2 auto-normalizes gitignore.txt → .gitignore. DONE 2026-04-03. Fix: add exclusions for hidden directories (.*/) in the find command. Also: dotfile deploy (AIStudio_099) should explicitly match root-level dotfiles only.
- [x] AIStudio_099 — Dotfile deploy solved by deploy_files.sh v2.5.2: gitignore.txt auto-normalized to .gitignore. No ais_dotfile_ops needed. DONE 2026-04-03. deploys a dotfile from Downloads to repo. macOS won't save dotfiles directly from Claude outputs — current workaround is save as plain name, mv in terminal, then ais_deploy. ais_dotfile_ops <plain_name> <dotfile_name> wraps the mv + ais_deploy in one command. Example: ais_dotfile_ops gitignore.txt .gitignore. Post-Beta.
- [x] AIStudio_098 — dotfile deploy: SOLVED. v2.5.2 gitignore.txt→.gitignore normalization; v2.5.3 --to flag properly parsed (no more basename error), all basename calls quoted. DONE 2026-04-03.: macOS won't save dotfiles (e.g. .gitignore) directly from Claude outputs panel. Current workaround: save as gitignore.txt, rename with mv in terminal, then ais_deploy. Better fix: add canonical_name override field to bundle_manifest.yaml static entries so deploy_files.sh can match 'gitignore.txt' → '.gitignore'. Design in AIStudio_093 refactor session.
- [ ] AIStudio_097 — Create ais_remove_ops utility: ais_remove_ops <filename>. Does: git rm the file, ais_commit with standard message. Consistent with ais_* operator utility model. Eliminates need for bare git rm commands. Companion to ais_rename_ops (AIStudio_090). Post-Beta.
- [ ] AIStudio_090 — Create ais_rename_ops utility: ais_rename_ops <old_name> <new_name>. Does: git rm old file, ais_deploy new file, search-replace references across HOWTO_OPS/generate_packet/bundle_manifest/.zshrc, ais_commit. Consistent with ais_* operator utility model. Post-Beta.
- [ ] AIStudio_091 — Publish standard for repo file structure and decoupling architecture. Brainstorming session needed to: (1) define canonical repo structure for AIStudio, (2) create separate job-search-docs repo, (3) create urCrew repo, (4) define a POS (Personal Operating System) meta-level repo that sits above all three, (5) document migration path. Prerequisite for Beta+1 work. Trigger: "Let's think about this" → THINK - urCrew - Repo Architecture session.
- [ ] AIStudio_087 — Reassess completeness of test suite at EOS Step 1. Currently 31 passed, 3 deselected, 1 xfailed. Verify: (a) what are the 3 deselected tests and should they run? (b) is 1 xfailed expected? (c) are all major features shipped this session (corpus_meta, manifest fix, corpus selector) covered by tests? Add missing coverage before Beta declaration.
- [ ] AIStudio_086 — manifest.jsonl append bug: help corpus manifest grows unboundedly across ingest runs — duplicate entries, trash references, historical log. Fix: rewrite manifest.jsonl atomically on each ingest. Medium priority.
- [x] AIStudio_085 — Corpus selector dropdown clips when 3+ corpora exist. Fixed with native dropdown + z-index wrapper (rag_studio.html). DONE 2026-04-02.
- [ ] AIStudio_080 — Help corpus: README.pdf not surfacing for "What is AIStudio?" query — HOWTO wins instead. README opening paragraph is the canonical answer. Investigate chunk scoring / retrieval for README content. May need README intro to be more prominent in chunking.
- [ ] AIStudio_081 — sec_10k corpus accidentally deleted — re-ingest needed next session (ais_sec_download + UI Add). Low priority but needed for demo corpus completeness.
- [ ] AIStudio_068 — System prompt tuning: remove hedging language from RAG answers.
    Current: 'appears to be', 'can be inferred', 'unfortunately there is no explicit info'
    Target: direct answers from evidence, acknowledge gaps briefly without hedging preamble.
    Edit: prompts/system.txt — add instruction to answer directly and confidently from
    provided sources, not to speculate but also not to preface with uncertainty disclaimers.
- [ ] AIStudio_067 — ais_bench positional arg: ais_bench demo should work as shorthand
    for ais_bench --corpus demo. Fix in ais_bench.sh: detect non-flag first arg and
    prepend --corpus. Also fix demo_questions.yaml usage comment: scripts/benchmark.py
    → benchmarks/benchmark.py (wrong path in YAML comment).
- [ ] AIStudio_066 — Qdrant WAL lock on aistudio_help collection: recurring panic on restart ('Can\'t init WAL: Resource temporarily unavailable'). Qdrant recovers but the error is noisy and suggests unclean shutdown is corrupting the WAL. Investigate: (a) add graceful Qdrant shutdown to stop.sh before kill, (b) or delete+rebuild aistudio_help on each restart since help corpus is re-ingested anyway. (Added 2026-04-01)
- [ ] AIStudio_060 — Repo cleanup (pre-delivery):
    (a) EPAVE HOW_TO.md (root) — superseded by HOWTO.md, PIPELINE already flagged
    (b) EPAVE HOWTO_ops.md (root, lowercase) — duplicate of HOWTO_OPS.md wrong case
    (c) EPAVE deploy.sh (root) — superseded by ais_deploy, no longer needed
    (d) CLEAN sec_10k corpus — no uploads/ folder, ghost of SEC corpus. Delete Qdrant
        collection aistudio_sec_10k, remove data/corpora/sec_10k/ folder
    (e) REVIEW QA_TESTING_LESSONS_LEARNED.md — keep in repo as dev record per PIPELINE,
        but remove .pdf companion (not user-facing)
    (f) DOCUMENT prompts/system.txt in HOWTO_OPS — this is the live LLM system prompt,
        operators should know it exists and where it is
    (g) MOVE docs/data_model.md → urCrew/ — it's target-state multi-user design, not
        current AIStudio state. Rename to CONCEPT - urCrew - Data Model - YYYY-MM-DD.md
    (h) REVIEW CLAUDE.md — update for ais_install, ais_restart, current alias set.
        This file is for Claude Code (IDE agent), must be current.
- [ ] AIStudio_059 — Pre-delivery doc consistency review
- [ ] AIStudio_061 — Classify docs/ for help corpus inclusion (per AIStudio_059 review):
    INCLUDE in help corpus (after update): HOWTO, QUICKSTART, README, HARNESS,
        DEMO_CORPUS, dependencies, roadmap, architecture_decisions, TESTS.md,
        ui_architecture.md (if current)
    EXCLUDE from help corpus (developer/stale): RAG_ACCURACY_ANALYSIS.md (ChromaDB era),
        CHUNKING_GUIDE.md (outdated), CITATIONS_MEMORY_GUIDE.md (early dev),
        EMBEDDING_TESTING_GUIDE.md (v2 Easter egg), RAG_WEB_SEARCH_AND_OPTIMIZATION.md
        (future/experimental), data_model.md (moving to urCrew/)
    UNKNOWN — needs review: docs/TESTS.md (looks current), docs/ui_architecture.md
    ACTION: after review, update help_manifest.yaml to match, re-run ais_update_help,
        re-ingest help corpus
- [ ] AIStudio_059 — Pre-delivery doc consistency review: audit ALL docs/ [PARTIAL: repo structure snapshot and legacy file identification completed in STD - General - Error Management and Prevention - 2026-04-03.md Section 3.6. Remaining: consistency fixes for each file, PDF regeneration, re-ingest.] and root .md files (HARNESS.md, RAG_ACCURACY_ANALYSIS.md, CHUNKING_GUIDE.md, CITATIONS_MEMORY_GUIDE.md, roadmap.md, QUICKSTART.md, README.md, HOWTO.md) for consistency with current stack (Qdrant, CrossEncoder, ais_install flow, new ingestion model, modal standards). Update each, regenerate PDFs, re-run ais_update_help, re-ingest help corpus. Gate: must complete before Beta declaration. (Added 2026-03-31)
- [ ] AIStudio_058 — Update QUICKSTART.md install step: replace `bash install.sh` with `./ais_install` throughout. Update README TL;DR same. New user flow: clone → `./ais_install` → `ais_start`. Nothing else.
- [ ] AIStudio_057 — install.sh --force flag: remove existing alias block from ~/.zshrc then re-append fresh block + source. Same for install_ops --force. Use case: redeploy updated aliases (e.g. new ais_* command) without manual ~/.zshrc editing. Guard: must remove old block cleanly, never append twice.
- [ ] ais_deploy extensionless file bug — `canonical_name()` in deploy_files.sh produces `install_ops.install_ops` for files with no extension (stem+ext both become the filename). Fix: detect no-extension case and return filename as-is. Also add `install_ops` to bundle_manifest.yaml `deploy_to: "./"` (done 2026-03-31).
- [ ] ais_deploy syntax extension — support `ais_deploy <file> in <path>` to specify destination inline without needing bundle_manifest.yaml entry first. E.g. `ais_deploy help_manifest.yaml in meta/`. Eliminates the manual prompt for new file types. Add to deploy_files.sh v2.5.0.
- [ ] --version flag on all ais_* scripts — mirrors --help requirement. Every script must support --version and print its version number. Add alongside --help in ais_command_help refactor.
- [ ] ais_command_help — single canonical .md file (or structured YAML) containing --help text for ALL ais_* scripts. Scripts refactored to read from this file first, fall back to inline text. Eliminates duplicate help maintenance. Create file, then refactor ais_start, ais_stop, ais_bench, ais_sec_download, ais_help, ais_update_help one by one.
- [ ] HOWTO.md — add granular TOC at top: list ALL questions as clickable links to their answers within the doc. Each Q becomes a named anchor. This is the primary navigation pattern for the help corpus.

- [ ] Build `ais_update_help.sh` — script that reads `help_manifest.yaml`, regenerates stale PDFs, copies to `data/corpora/help/uploads/`, updates `last_updated` in manifest. Alias: `ais_update_help`. Supports `ais_update_help <subject>` for single-subject refresh.
- [ ] Create `help_manifest.yaml` at `data/corpora/help/help_manifest.yaml` — inventory of all help corpus PDFs with subject, title, use, version, source_md, pdf path, corpus_path, last_updated.
- [ ] "Using the Interface" section in HOWTO.md — document every UI control: New Corpus, Upload File, Delete File, Inspect, Benchmark, About, Connected indicator, corpus selector, model selector, Top K, Temperature, Keywords, Clear Conversation. This is the primary source for corpus management UI questions and feeds directly into the help corpus. Required for Beta.
- [ ] UI Reference — standalone doc (or HOWTO section) covering every button, indicator, and control in the UI with description and behavior. Required for Beta.
- [ ] Quick Reference — REF - AIStudio - Quick Reference is gitignored (not public). For Beta, produce QUICKSTART.pdf (public tracked) OR promote REF to repo root as a tracked file.

**Doc inventory — files needing update before help corpus or public release:**

*User-facing (tracked, need PDF companions + review):*
- [ ] QUICKSTART.md — needs PDF companion (QUICKSTART.pdf). Step 7 tuning parameter names may be stale.
- [ ] DEMO_CORPUS.md — currently in docs/. Should be user-facing. Needs review and PDF.
- [ ] docs/roadmap.md — public, needs review for accuracy vs current state (some Beta items now done).
- [ ] docs/dependencies.md — public, accurate. Candidate for help corpus. Needs PDF.
- [ ] docs/HARNESS.md — public, accurate. User-facing benchmark guide. Needs PDF.

*Stale / pre-production — needs rewrite before any public use:*
- [ ] docs/RAG_ACCURACY_ANALYSIS.md — ChromaDB era, pre-reranker. Completely outdated. Rewrite as "RAG Quality and Retrieval Accuracy" covering current Qdrant+CrossEncoder stack.
- [ ] docs/CHUNKING_GUIDE.md — pre-production chunking implementation guide. Outdated code examples. Rewrite as user-friendly "How AIStudio chunks documents" explainer.
- [ ] docs/CITATIONS_MEMORY_GUIDE.md — implementation guide from early dev. Not user-facing. Either rewrite as "How citations and conversation memory work" or keep as internal dev doc.
- [ ] docs/EMBEDDING_TESTING_GUIDE.md — operator/developer doc. Review for accuracy, keep as internal reference only.
- [ ] docs/RAG_WEB_SEARCH_AND_OPTIMIZATION.md — review currency before including anywhere.

*Operator-only (gitignored, no action needed):*
- HOWTO_OPS.md, PIPELINE.md, all STDs, REF files, bundle_manifest.yaml

*Stubs / empty (fill or remove):*
- [ ] docs/TESTS.md — empty stub. Fill with testing guide or remove.
- [ ] docs/ui_architecture.md — 13KB, check currency vs current UI.
- [ ] docs/data_model.md — 4.5KB, check currency vs current Qdrant data model.

*No action needed (accurate and current):*
- README.md ✅, HOWTO.md ✅, architecture_decisions.md ✅, agentic_ai_pov.pdf ✅

*Newly classified after review:*
- [ ] CONTRIBUTING.md — developer-facing, public. Keep as-is. NOT in help corpus (no user value). Consider PDF for completeness later.
- [ ] HOW_TO.md — old version superseded by HOWTO.md. DELETE from repo root.
- [ ] QA_TESTING_LESSONS_LEARNED.md — operator/developer doc. Valuable lessons on OBE testing. NOT user-facing. Keep in repo for record but do NOT include in help corpus.
- [ ] tests/DEBUG_GUIDE.md — OLD, references ChromaDB era. DELETE or archive.
- [ ] tests/DEBUG_HINTS.md — CURRENT, accurate. Operator/developer tool. Move to docs/ or keep in tests/. NOT in user help corpus but consider for HOWTO_OPS content.
- [ ] AIStudio - README.pdf — old misnamed PDF at repo root. DELETE (README.pdf is current).
- [ ] meta/reference/REF - AIStudio - Bash Cheat Sheet - 2026-03-24.md — duplicate, older version. DELETE, keep 2026-03-27 only.
- [ ] docs/ui_architecture.md — target state design doc, partially implemented. NOT user-facing. Keep as internal reference. Update to reflect current implementation gaps.
- [ ] docs/data_model.md — future state schema. NOT user-facing. Keep as internal reference.
- [ ] docs/TESTS.md — CURRENT, accurate testing guide. Developer-facing. NOT in user help corpus.
- [ ] docs/RAG_WEB_SEARCH_AND_OPTIMIZATION.md — review before any use (not yet read fully).
- [ ] docs/EMBEDDING_TESTING_GUIDE.md — developer/operator tool. NOT in user help corpus.

**Help corpus — confirmed inclusions (need PDFs):**
- [ ] README.md → README.pdf ✅ exists
- [ ] HOWTO.md → HOWTO.pdf ✅ exists
- [ ] QUICKSTART.md → QUICKSTART.pdf ❌ generate
- [ ] docs/architecture_decisions.md → docs/architecture_decisions.pdf ✅ exists
- [ ] docs/DEMO_CORPUS.md → docs/DEMO_CORPUS.pdf ❌ generate
- [ ] docs/HARNESS.md → docs/HARNESS.pdf ❌ generate
- [ ] docs/dependencies.md → docs/dependencies.pdf ❌ generate
- [ ] docs/roadmap.md → docs/roadmap.pdf ❌ generate (after review/update)
- [ ] QA_TESTING_LESSONS_LEARNED.md → QA_TESTING_LESSONS_LEARNED.pdf ❌ generate (good for "what was tested" questions)

**Help corpus — confirmed exclusions:**
- docs/RAG_ACCURACY_ANALYSIS.md — stale ChromaDB era ❌
- docs/CHUNKING_GUIDE.md — stale implementation guide ❌
- docs/CITATIONS_MEMORY_GUIDE.md — implementation guide, not user-facing ❌
- docs/EMBEDDING_TESTING_GUIDE.md — developer only ❌
- docs/ui_architecture.md — future state, not current ❌
- docs/data_model.md — future state, not current ❌
- docs/TESTS.md — developer only ❌
- HOW_TO.md — superseded ❌
- tests/DEBUG_GUIDE.md — stale ❌
- [ ] README.pdf — internal links broken (e.g. QUICKSTART.md, benchmarks/ references). Rule: when generating PDF documentation, verify all links work before publishing.
- [x] Tooltips on Connected status indicator — title= attribute added
- [x] Tooltips on Top K and Temperature — descriptive title= attributes added
- [x] Add `/howto` endpoint to backend — serves HOWTO.md rendered as HTML with anchor IDs, enabling deep links like `http://localhost:8000/howto#installing-and-managing-llms` from About modal
- [ ] Update About modal "Updating LLM options" link to `http://localhost:8000/howto#installing-and-managing-llms` once /howto endpoint exists
- [ ] Define standard for About/README modal window — layout, sections, typography (prototype: current About modal)
- [ ] Capture key elements from About modal work as a pattern/STD — modal structure (title/stylized logo, sections, footer, resize), content sections (What it does, corpus description, components, contact), link rules (local-first, file:// rewrite in backend). Prototype artifact: current About modal + about.md. Add future STD - AIStudio - Modal Window Standard to pipeline.
- [ ] Add end-of-document marker ★★★  ★★★ (centered) to all user-facing PDFs: README.pdf, HOWTO.pdf, HOWTO_OPS.pdf, architecture_decisions.pdf, QUICKSTART.pdf. Rule defined in STD - INFO - Document Structure and Content - 2026-03-24.md line 204.
- [ ] STD - AIStudio - PDF Document Standard — formalize footer rule (doc name | product | date, Arial 9pt #999999), color palette choice (current vs experimental), link verification checklist, header style. Prototype: README.pdf and architecture_decisions.pdf.
- [ ] Standardize all user-facing PDF documents — footer standard from document_creation-Documentation_Standards-2026-03-21.md, links verified before publish. Prototype: README.pdf and architecture_decisions.pdf
- [ ] Architecture decisions PDF — generate docs/architecture_decisions.pdf using same standard as README.pdf (footer, verified links)
- [ ] Corpus description file — each corpus should have a `<name> - Description - YYYY-MM-DD.md` in uploads/ that describes the corpus and lists suggested keywords. Ingested automatically. Improves "what is this corpus about?" answers. User-editable.
- [ ] Add --help to all ais_* user scripts (ais_start, ais_stop, ais_bench, ais_sec_download) — required before Beta
- [ ] Verify ais_* aliases survive cold shell session (new terminal, no source ~/.zshrc)
- [ ] Visual inspection of 12 demo answers — citations render, links work, no regressions

**Help Corpus**
- [x] Update HELP - Using the UI doc — remove "no progress indicator yet", update for progress bar + About button
- [ ] Fix help corpus ingestion — rebuild as flat .md files in data/corpora/help/uploads/ (pipeline does not process zips)
- [ ] Add RAG Performance Findings to help corpus

**Docs**
- [ ] README — add self-referential corpus narrative
- [ ] QUICKSTART Step 7 — tuning parameter names (also in Next Session above)
- [ ] QUICKSTART — add `brew install pango` as prerequisite step (required for weasyprint/PDF generation)

**Gap Analysis Resolutions — docs to update:**

- [ ] Q44 Upgrade path — add to HOWTO.md: "git pull to upgrade; corpus data (Qdrant storage) persists across upgrades; re-ingestion only needed if chunk format changes (use --force); demo corpus auto-re-ingests on start."
- [ ] Q49 UI documentation — document every button in the UI (New Corpus, Upload File, Delete File, Inspect, Benchmark, About, Connected, Top K, Temperature, Keywords, Clear Conversation, corpus selector, model selector). Add to HOWTO.md as "Using the Interface" section. This answers all corpus management UI questions.
- [ ] Q56 Citations — copy citation explanation from README to HOWTO.md. Every user-facing feature in README should also be in HOWTO.
- [ ] Q60 Benchmark questions — add to HOWTO.md: derive test questions from benchmark reports; reports show which questions retrieve well and which don't. Point to HARNESS.md for full benchmark authoring guide.
- [ ] Q73 Connected indicator — add to README.md under "What you actually see and do": "A Connected indicator in the top bar shows backend status — green means all services running, grey/amber means backend is down; run ais_start to restore."
- [ ] Q81-85 License — add Creative Commons BY license section to README.md. Add license link to About modal (about.md footer). Add PIPELINE item to display license in About modal.
- [ ] Q38/37 Offline/air-gapped — already in README. Verify it's also in HOWTO.md "What it does" intro. If not, add explicit sentence: "AIStudio runs fully offline — no internet connection required after installation."

**Beta Validation**
- [ ] SEC 10-K corpus ingestion test on M4 Air — full 143 filing ingest, benchmark, latency baseline
- [ ] Fresh install test — clone repo on clean machine, follow QUICKSTART end-to-end
- [ ] Demo script polish — 12 questions, no dead ends, DEMO_SCRIPT.md
- [ ] Run test_aistudio.py --group all with backend live

**Beta Declaration**
- [ ] Update about.md version to confirmed Beta
- [ ] git tag beta-v1
- [ ] LinkedIn Beta announcement draft

---

### 🟡 WAVE 1 — Post-Beta Polish

**Ops & Dev Experience**
- [ ] ais_start should call ais_stop first — prevent port conflict on restart
- [ ] ais_status — show running services (ports, Ollama models, Qdrant collections)
- [ ] ais_test — runs make test from anywhere
- [ ] ais_ingest — runs ingest with corpus arg
- [ ] ais_bench — runs benchmark.py with defaults
- [ ] Update HOWTO.md and Bash Cheat Sheet with all ais_* commands
- [ ] deploy_files.sh --no-push flag for gitignored scripts

**Ingestion Lifecycle**
- [ ] Disable Remove/Add buttons while ingest running — prevent race condition
- [ ] Rename file-level "Delete" → "Remove"
- [ ] Stop ingestion — store proc handle, expose DELETE /corpus/{name}/ingest
- [ ] Wire actual chunks_written from subprocess stdout — currently shows 0
- [ ] Duplicate file detection on upload — JS check, prompt "Replace?"

**UI Polish**
- [ ] Date added in file list — upload timestamp in inspect panel
- [ ] Verify corpus file count excludes trash/ subdir contents

**Benchmark Improvements**
- [ ] Record machine hardware in benchmark.py report header
- [ ] Update RAG Performance Findings doc — add M4 Air data, finalize SEC 10-K numbers

**Repo Cleanup**
- [ ] Remove run_demo.py + run_demo_config.json — legacy harness (after HARNESS.md + CLAUDE.md updated)
- [ ] Root BENCHMARK_FINDINGS.md — references run_demo.py, trash after HARNESS.md update
- [ ] data/demo/ — legacy run_demo.py era reports + DEMO_CORPUS.md (move DEMO_CORPUS.md to docs/ first)
- [x] scripts/BENCHMARK_FINDINGS.md — trashed
- [x] scripts/benchmark_results.json — trashed
- [x] benchmarks/BENCHMARK_FINDINGS.md — trashed
- [x] benchmarks/benchmark_results.json — trashed
- [x] data/corpora/demo/demo_questions.yaml — duplicate of benchmarks/, trashed
- [x] data/corpora/fr_10k — experiment corpus, trashed
- [ ] Remove root deploy.sh — superseded by scripts/deploy_files.sh
- [ ] Assess src/agentic_lab/ — empty stub, keep or remove
- [ ] Remove or update docs/RAG_ACCURACY_ANALYSIS.md — references ChromaDB/JSONL (pre-Qdrant)
- [ ] Remove chroma_store.py — ChromaDB not fully excised
- [ ] Remove QuickReferenceGuide.docx — duplicate of .md

---

### 🟠 WAVE 2 — RAG Quality & PDF

**RAG Quality**
- [ ] Relevance threshold — discard chunks below similarity cutoff, expose in UI
- [ ] Query expansion / hybrid lexical+semantic retrieval — fix vocabulary mismatch failures
- [ ] XBRL stripping in HTML ingestion — SEC 10-K noise
- [ ] Embedding model comparison — nomic-embed-text vs bge-large

**PDF Viewer**
- [ ] PDF.js viewer with #page=N fragment support — page-accurate scroll
- [ ] Render source page as image in reference panel when chunk originates from PDF — include page number in citation metadata, enable click-to-page navigation (especially valuable for SEC filings)
- [ ] Scanned PDF / OCR support

**Benchmark Campaign (systematic)**
- [ ] Top K sensitivity — K=3,5,8,10,15
- [ ] Temperature sensitivity — T=0.1,0.3,0.5,0.7
- [ ] Model quality comparison — 8b vs 70b human eval (latency done, quality not compared)
- [ ] SEC 10-K corpus benchmark — 12 questions vs 105,964-chunk corpus
- [ ] M4 Air vs M4 Max systematic comparison
- [ ] Query complexity gradient — factual / synthesis / multi-hop

**API & Architecture**
- [ ] GET /corpus/{name}/files endpoint returning upload timestamps
- [ ] API_DOC.md — all endpoints, request/response, error codes
- [ ] Jira setup — one board, three epics: Beta Polish / v2.0 / urCrew

**Test Debt**
- [ ] Delete test_chroma_fallback_on_distance_filter.py — dead code
- [ ] Delete test_chroma_query_contract.py — dead code
- [ ] Move embedding_arithmetic.py to scripts/ or document it
- [ ] Fix test_api_integration.py — references llama3.2:3b not installed, always skips

---

### 🔵 WAVE 3 — urCrew

**Phase 0 — Foundation**
- [ ] Create separate urCrew GitHub repo — scaffold README, CONCEPT.md, ontology/, machines/
- [ ] YAML framework: PRINC/STD/IMPL_CONSIDERATION hierarchy
- [ ] PROT - AIStudio - Development Conventions YAML
- [ ] Codify "new artifact → prototype for pattern?" rule in packet template and HOWTO_OPS — when producing a new artifact or construct, ask if it deserves to be a pattern/STD — local-first links, deploy-before-create rule, operator/user separation (currently scattered in STDs, needs urCrew YAML home)
- [ ] linked_opportunity_management.yaml → email_management.yaml + linkedin_interaction.yaml → job_hunting.yaml
- [ ] Identity/preference ecosystem — codify how Manuel operates and responds to inbound

**Phase 1 — Integration**
- [ ] AIStudio /ask endpoint as tool available to CrewAI agents
- [ ] CrewAI as orchestration backbone
- [ ] AIStudio self-referential corpus — ingest docs/ as queryable help (30 min, zero new code)

**Phase 2 — Data**
- [ ] Gmail corpus ingestion — privacy architecture required first
- [ ] Wave 4: Email corpus ingestion (Yahoo → Zapier relay built Mar 27 — Phase 0 done)
- [ ] Gmail [For Claude] label triggers auto-ingestion into AIStudio job_search_emails corpus

**Phase 3 — Agents**
- [ ] Multi-agent Chief of Staff thread design
- [ ] Dalio machine construct as Pillar 5

---

---

## 3b. Job Search Pipeline

*Items prefixed JOB_ — will migrate to separate job-search-docs repo after Beta.*

### Standards & Infrastructure
- [ ] JOB_001 — Create separate git repo job-search-docs for bundle files [High]
- [ ] JOB_002 — Implement job_create_packet service [High]
- [ ] JOB_003 — Implement job_bundle service [High]

### Tech Addenda (all status: to_generate)
- [ ] JOB_004 — Tech addendum T01: Agentic AI POV [Critical — used across B, C2, C3]
- [ ] JOB_005 — Tech addendum T02: SDLC & Engineering Maturity [High]
- [ ] JOB_006 — Tech addendum T03: AWS vs Azure Comparison [High]
- [ ] JOB_007 — Tech addendum T04: Trading Reference Architecture [High — FinTech/AM roles]
- [ ] JOB_008 — Tech addendum T05: Governance & ARB Model [Medium]
- [ ] JOB_009 — Tech addendum T06: FinOps & Cloud Cost Management [Medium]
- [ ] JOB_010 — Tech addendum T07: AIStudio Demo Brief [High]

### Documents & Examples
- [ ] JOB_011 — Locate Chatterjee/MS CallPrep — add to bundle as C3 example [Medium]
- [ ] JOB_012 — Generate Wellington Study Guide from session notes [Medium]
- [ ] JOB_013 — Add resume + tracker to job-search-docs repo [High]
- [ ] JOB_014 — Version-stamp manifest on every update [Low]
- [ ] JOB_015 — Keep tracker Bucket/Prospect Type in sync with v1.1 taxonomy [Low]
- [ ] JOB_016 — Board-level 1-page intro bio [Medium]
- [x] JOB_017 — PDFs for all 4 active resume variants — 2026-03-31
- [ ] JOB_018 — Build inventory/manifest of call prep and cheatsheet formats
- [ ] JOB_019 — Add CxO titles to resume for Tier 1 HH use — BLOCKING Erin Maier send Thursday
- [ ] JOB_020 — Send Erin Maier email Thursday April 2 — attach Senior Technical Integrator resume. Gmail draft ID: r4676603611525648264
- [ ] JOB_021 — Re-engage Spencer Stuart (Lina Velcheva) and Heidrick (David Richardson) — Thursday April 2
- [ ] JOB_022 — Meta cleanup: move STD - OPS - * files from meta/ root → meta/standards/, rename to STD - JOB - * convention
- [ ] JOB_023 — Rename old standards files to proper convention (interview_preparation-... → STD - JOB - ...)
- [ ] JOB_024 — Remove duplicate STD - OPS - MANUEL - Standing Rules - 2026-03-30 (1).md
- [ ] JOB_025 — Codify JOB EOS as STD - JOB - EOS Protocol (7-step, mirrors AIStudio EOS)
- [ ] JOB_026 — Add meta/bundles/ glob to bundle_manifest.yaml for JOB bundles
- [ ] JOB_027 — Rename tracker: JOB_2026_Master_Tracker_BUCKETED.xlsx → JOB - 2026 - Master Tracker - BUCKETED - 2026-03-31.xlsx
- [ ] JOB_028 — Nick Boaknin intro: send Tier 1 plant emails after call with Nick (Tom, Erin, Chuck, Andrew, Lina)
- [ ] JOB_029 — BNY April 15 call prep session — Colin White strategy, consulting angle vs formal role
- [ ] JOB_030 — Rename BNY resume: Manuel_Barbero_BNY_Enterprise_Architect.docx → Manuel Barbero - BNY Enterprise Architect - 2026-03-31.docx, copy to meta/job_hunting/ via ais_deploy
- [ ] JOB_031 — Move stale job_bundle_manifest-2026-03-30.yaml from meta/ root → meta/job_hunting/
- [ ] JOB_032 — Add Barclays to tracker (LinkedIn job 4395174041) — review JD vs $700K target before applying
- [ ] JOB_033 — Add Schwab to tracker (info coming from Manuel)
- [ ] JOB_034 — Guardian Life / Michaela Alleyne-Kennedy: process PAUSED — JD not finalized, expect call in coming weeks. Status: On Hold.
- [ ] JOB_037 — Persist Anthropic application package as template under meta/job_hunting/application_packages/. The single-PDF format (resume + cover letter + why + transcript exhibit) may be the standard for future opportunities — especially roles where the Claude-as-author + live-session-proof angle is relevant. Consider as a reusable pattern, not a one-off.
- [ ] JOB_035 — Build STD - JOB - EOD Protocol (mirrors AIStudio EOS, 6 steps: tracker → meta/job_hunting/ → PACKET → manifest → bundle → verify). See Gmail draft.
- [ ] JOB_036 — Yann Jaffré: left voicemail April 1, postponed call to tomorrow (April 3). Follow up.
- [ ] AIStudio_077 — Fix JOB bundle deploy_to in bundle_manifest.yaml: glob patterns don't work for deploy routing at deploy time. Need static entries for JOB - BUNDLE - *.zip. Also: rename JOB bundle convention: BUNDLE - JOB - Job Search - HHMM - YYYY-MM-DD.zip (BUNDLE prefix takes precedence per naming convention update below).
- [ ] AIStudio_078 — Naming convention update: BUNDLE prefix takes precedence over activity name for easy re-ingestion in new thread. Applies to all bundle files. Document in STD - General - Naming Conventions. Old: JOB - BUNDLE - ... New: BUNDLE - JOB - ...

### Resume Taxonomy (rationalized 2026-03-31)
4 active variants:
1. Manuel_Barbero_-_Executive_Bio_-_March_2026.docx — warm contacts/HH, full narrative
2. Manuel_Barbero_-_Senior_Technical_Integrator.docx — player-coach, PE/advisory (default)
3. M_Barbero_Resume_Updated_Mar2026.docx — CTO/CAIO/AI Builder, Tier 1 HH
4. Manuel_Barbero.docx — Enterprise Chief Architect, Wealth & Investment

### 2-Pager Standards (established 2026-03-31)
- Use case: Intro Call — Senior Headhunter (Bucket B)
  Format: plain table, white background, dark gray headers, thin borders
  Example: JOB - Egon Zehnder - Intro Call Prep - 2026-03-31.docx
  Sections: WHO I AM paragraph, WHERE I AM IN MY SEARCH, MAKE HER REMEMBER, HOW TO OPEN,
            QUESTIONS TO ASK, PE ANGLE, CLOSE, DON'T, Page 2 Q&A grid

## 4. Linkage With Other Projects

**urCrew ↔ AIStudio:** urCrew is built on top of AIStudio (~70% UI reuse). AIStudio /ask becomes a tool in the CrewAI agent mesh. The current manual bundle/context packet workflow IS Phase 0 of urCrew.

**Job Search ↔ AIStudio:** AIStudio is the primary proof point in the job search. The README is a calling card. The GitHub repo is shared in outreach emails. Every architecture decision made in AIStudio development is a story for interviews.

**urCrew ↔ Job Search:** The YAML framework being designed for urCrew (PRINC/STD/IMPL) will eventually codify the job search playbook — linked_opportunity_management.yaml, linkedin_interaction.yaml, etc.

**Principles ↔ All Projects:** The 10 core principles codified in AIStudio apply to urCrew and job search equally. When urCrew formalizes the PRINC hierarchy, AIStudio principles will migrate there.

---

## 5. Gating Dependencies

```
Beta Declaration
    └── Beta Gate items complete (tests, UI fixes, help corpus, demo script)
    └── SEC 10-K corpus benchmarked on M4 Air
    └── Fresh install test passes

LinkedIn Post (Beta++ story)
    └── RAG Performance Findings doc complete (M4 Air ✅ + SEC 10-K data needed)
    └── Self-referential corpus live
    └── Demo script polished (12 questions, no dead ends)
    └── PDF viewer page-accurate (or documented workaround)

urCrew Phase 1
    └── AIStudio Beta stable
    └── /ask endpoint documented
    └── urCrew repo scaffolded

Email Corpus (Wave 4)
    └── Yahoo → Zapier relay ✅ (Phase 0 done Mar 27)
    └── Gmail [For Claude] label trigger (next)
    └── Privacy architecture for corpus ingestion
```

---

## 6. Annex — Completed Items


### EOS Process Fix (2026-03-31)
- [x] Identified gap: PIPELINE.md not being updated during sessions — items tracked in memory only
- [ ] Fix EOS procedure: before ais_packet, I must read current PIPELINE.md, add all new items,
      present via present_files for review, you deploy with ais_deploy PIPELINE.md, THEN ais_packet

### EOS / Bundle Infrastructure
- [x] Fix generate_packet.sh banner: "EOS Bundle Generator" → "EOS Packet Generator" — 979043c
- [x] bundle_session.sh v1.4.0 — manifest-driven, zip -@ handles spaces in filenames
- [x] bundle_manifest.yaml created — 80fd8f7
- [x] bundle_manifest.yaml added to bundle itself (self-referential entry) — 4859c0d
- [x] bundle_manifest.yaml descriptions — READ THIS FIRST generated dynamically from manifest
- [x] HOWTO — scripts/ gitignored, versioned via BUNDLE not git — 4859c0d
- [x] STD - General - Naming Conventions - 2026-03-27 — bundle_manifest.yaml added to Exempt Files
- [x] Principle 11 added: trace to root cause, update governing doc immediately — 4859c0d
- [x] META pipeline section added: decouple principles from script, refactor PACKET template
- [x] _session_summary.md convention — ephemeral, auto-consumed by ais_packet — a5b269f
- [x] ais_packet detects and inserts _session_summary.md automatically — a5b269f
- [x] EOS two-step protocol fully codified — PACKET template, HOWTO, STD - AIStudio - EOS Bundle
- [x] Principle 8: Never hand off incomplete work — f33117c
- [x] Principle 9: Fix process errors immediately — while the iron is hot — 2d7c7e8
- [x] Principle 10: Apply principles directionally, not dogmatically — 80fd8f7

### Bundle / Restore Infrastructure (session 2026-03-27 — late)
- [x] bundle_session.sh v1.6.0 — scripts/ copied to meta/scripts/ during bundle, included in zip
- [x] bundle_manifest.yaml — scripts/deploy_files.sh, generate_packet.sh, bundle_session.sh entries added
- [x] ais_restore_scripts — updated to restore from latest BUNDLE zip, falls back to Downloads
- [x] ais_help.sh — ais_restore_scripts documented
- [x] HOWTO_OPS.md — restore-from-bundle procedure, .deploy_map references removed
- [x] STD - AIStudio - EOS Bundle - 2026-03-27 — three non-negotiable EOS rules codified

### Deploy Infrastructure (session 2026-03-27)
- [x] deploy_files.sh v2.3.0 — find_in_manifest() uses deploy_to field, glob stem matching for dated files
- [x] deploy_files.sh v2.4.0 — .deploy_map removed, manifest-only destination resolution
- [x] deploy_files.sh v2.5.0 — version display ([vX.Y.Z] next to found files)
- [x] deploy_files.sh v2.5.1 — find_in_repo excludes .pytest_cache, .ruff_cache, .idea
- [x] deploy_files.sh v2.5.2 — gitignore.txt auto-normalized → .gitignore (macOS dotfile workaround)
- [x] deploy_files.sh v2.5.3 — --to flag properly parsed (basename error fixed), all basename calls quoted
- [x] ais_commit.sh v1.1.0 — .gitignore guard (refuses commit if meta/ missing), scripts/ tracking guard
- [x] bundle_manifest.yaml — THINK glob types fixed (glob → glob_latest), STD Error Management entry added
- [x] STD - General - Error Management and Prevention - 2026-04-03.md — created: repo structure, deploy workflow, what NOT to do, recovery procedure, repo snapshot April 2026
- [x] THINK Master — T1.18 (irreversible ops), T1.19 (persist artifacts), T1.20 (no repeat mistakes), T1.21 (waste no mistake), T1.22 (read file before editing), T2.1a (manifest first), T2.5b (gitignore check), T2.5c (grep meta/ before commit)
- [x] HOWTO_OPS.md — deploy ordering rule, ais_deploy gitignore.txt, --to flag, .gitignore verification, filter-repo full 5-step procedure, EOS STD ref updated to 2026-04-03
- [x] generate_packet.sh — Error Management trigger phrase added, STD in bundle contents table
- [x] filter-repo run clean — meta/ and operator scripts removed from git history. HEAD=9d29bd4
- [x] bundle_manifest.yaml — deploy_to field added to all entries, when_relevant field added
- [x] generate_packet.sh — "When to Consult" table now fully dynamic from manifest when_relevant
- [x] generate_packet.sh — both PACKET tables generated in one Python pass via JSON
- [x] ais_help.sh — ais_deploy documented as handling all file types (tracked, gitignored, meta/)
- [x] HOWTO_OPS.md — rule: add deploy_to to bundle_manifest.yaml before creating new file type
- [x] REF - AIStudio - Bash Cheat Sheet - 2026-03-27.md — new dated version, all ais_* commands
- [x] ais_restore_scripts — added to .zshrc, restores operator scripts after filter-repo

### EOS Infrastructure / DevOps (session 2026-03-27)
- [x] deploy_files.sh v2.2.0 — manifest-driven destination lookup, zsh glob (N) fix
- [x] deploy_files.sh v2.2.0 — `find_in_manifest()` checks bundle_manifest.yaml before repo search
- [x] ais_commit patched — guards against re-adding gitignored paths, --set-upstream fix
- [x] .gitignore rewritten correctly — meta/, benchmarks/reports/, operator scripts excluded
- [x] git filter-repo used to purge private data from history (3 passes, root cause resolved)
- [x] test_rag_core_jsonl.py marked @pytest.mark.integration — excluded from make test
- [x] pyproject.toml addopts — integration tests excluded from default run
- [x] make test: 31 passed, 0 failed, clean
- [x] HOWTO split → HOWTO.md (user) + HOWTO_OPS.md (operator, gitignored)
- [x] HOWTO_OPS.md — filter-repo + .gitignore sequencing lesson, .gitignore chaining warning
- [x] QUICKSTART — install.sh step (Step 7), corpus path fixed, tuning params updated, steps renumbered to 12
- [x] User scripts at repo root — install.sh, ais_help.sh, ais_start.sh, ais_stop.sh, ais_bench.sh, ais_sec_download.sh
- [x] HARNESS.md rewritten for benchmarks/benchmark.py
- [x] CLAUDE.md benchmark command updated
- [x] DEMO_CORPUS.md moved to docs/
- [x] run_demo.py, run_demo_config.json, BENCHMARK_FINDINGS.md (root), data/demo/ trashed
- [x] PACKET READ THIS FIRST — two-table format (Bundle Contents + When to Consult)
- [x] bundle_manifest.yaml descriptions — factual one-liners, PIPELINE.md entry added

### Repo Cleanup (partial — session 2026-03-27)
- [x] scripts/BENCHMARK_FINDINGS.md — trashed (legacy duplicate)
- [x] scripts/benchmark_results.json — trashed (legacy duplicate)
- [x] benchmarks/BENCHMARK_FINDINGS.md — trashed (superseded by timestamped reports/)
- [x] benchmarks/benchmark_results.json — trashed (superseded by timestamped reports/)
- [x] data/corpora/demo/demo_questions.yaml — trashed (identical duplicate of benchmarks/)
- [x] data/corpora/fr_10k — trashed (experiment corpus, no value)

### RAG Core & Quality
- [x] CrossEncoder ms-marco-MiniLM reranker wired into rag_core.py
- [x] Remove xfail from test_retrieve_finds_hits_jsonl — 33 passing — 33118f5
- [x] Run 5 benchmark: warm llama3.1:70b and 8b statistically indistinguishable on Apple Silicon
- [x] Prewarm endpoint (POST /prewarm, amber→green status pill)
- [x] 99.1% pass rate across 108 Q/A pairs documented
- [x] Vector arithmetic / analogy feature built (King - man + woman = Queen)
- [x] CI green with GitHub Actions PYTHONPATH fix, qdrant-client added to requirements.txt

### UI & UX
- [x] Progress bar during ingestion
- [x] Citation carry-over fix
- [x] File/corpus deletion to trash, Finder integration
- [x] UI ergonomics overhaul (corpus actions above dropdown, file actions below)
- [x] About modal, tooltips, custom delete confirmation modal (requires typed YES)
- [x] 14 new unit tests
- [x] Centered numbers in Top K and Temperature — text-align: center confirmed in CSS
- [x] Tooltips on Top K and Temperature — title= attributes added

### Infrastructure
- [x] SEC 10-K corpus ingested — 143 filings, 25 firms, 105,964 chunks
- [x] Metadata filtering (firm + year) working
- [x] Benchmark harness with timestamped reports
- [x] CI badge on README, pre-commit hooks, ruff
- [x] stop.sh, ais_start / ais_stop / ais_* aliases in ~/.zshrc
- [x] README.pdf deployed — architecture diagrams, footer, contact


## New Pipeline Items — 2026-04-06

### JOB — Process / Infrastructure
- [ ] JOB_029: Build STD - JOB - EOS Protocol — 6-step protocol defined April 6. Steps: (1) request manifest, (2) review transcript+verify files, (3) upload changed files, (4) session report, (5) present PACKET+BUNDLE+TRACKER, (6) cp commands. JOB EOS runs BEFORE AIStudio EOS.
- [ ] JOB_045: Clean up job_bundle_manifest.yaml — remove stale entries (CBRE resume, T01-T07 addenda all to_generate). Make it a reliable EOS checklist.
- [ ] JOB_046: Refactor meta/job_hunting/ flat files into subfolders:
  - Create: meta/job_hunting/resumes/ — move all resume .docx files there
  - Create: meta/job_hunting/call_prep/ — move all JOB - [Company] - * prep docs there
  - tracker/ already created ✅ — move JOB - 2026 - Master Tracker - 2026-03-24 - new.xlsx there
  - Update bundle_manifest.yaml glob entries: job_hunting/JOB - Morgan Stanley - *.docx, job_hunting/JOB - INFO - *.docx, job_hunting/M Barbero - Resume - *.docx etc to point to new subfolders
  - Write STD - JOB - Folder Structure documenting target architecture and urCrew project-level pattern
- [ ] JOB_047: Decide on job_bundle_manifest.yaml naming — remove date suffix (living doc). File now named job_bundle_manifest.yaml.
- [ ] JOB_048: Update PIPELINE entries for Yahoo context items — HH "A" identity, Two Sigma connection thread, real estate Texas firm details. Check Yahoo and add details here.
- [ ] JOB_049: Capco / Scott Claus — reboot email. Strong relationship equity. Queue for Wednesday.
- [ ] JOB_050: Will Grannis / Google — second try. Had 2017 interview loop. Queue for Tuesday.
- [ ] JOB_051: Two Sigma / Jeff Wecker (CTO, Bridgewater overlap 2012-2016) + Todd Bucello — use connection from HH "A". Check Yahoo thread.
- [ ] JOB_052: HH "A" — identify firm name and re-engage on 2 new mandates. Check Yahoo.
- [ ] JOB_053: Oakridge + Elevation Capital — tailored resume variants needed Tuesday before send.
- [ ] JOB_054: Mondrian Alpha — apply Tuesday. AIStudio as engineering proof point. Resume variant needed.
- [ ] JOB_055: Find Anthropic hiring contact for direct ping (beyond Greenhouse application).
- [ ] JOB_056: NFP VP Enterprise Architect NYC — assess JD, apply Wednesday if fit.
- [ ] JOB_057: Skaria Thomas / Millennium — ping this week using barbero_millennium_final.docx.
- [ ] JOB_058: Eileen Murray Anthropic angle letter — base text for Souheil (retiring) + Emilia pre-call note (April 15). Build Wednesday.
- [ ] JOB_059: PIPELINE naming convention — items below JOB_044 were added today. Reconcile numbering with tracker JOB items (JOB_033-044 in tracker vs pipeline numbering divergence).

### AIStudio — Process / Infrastructure  
- [ ] AIStudio_149: Update STD - General - Naming Conventions with: (1) {corpus_name}_corpus_meta.yaml convention, (2) CODEBASE_GUIDE / CODEBASE_GUIDE_OPS document pair pattern, (3) macOS Downloads wildcard verification command in HOWTO_OPS Shell & Terminal section. Add THINK items from April 6 session to THINK Master.
- [ ] AIStudio_150: bundle_manifest.yaml — remove stale static bootstrap entry for 2026-04-04 (replaced by glob_latest). Already fixed in April 6 update.
- [ ] AIStudio_151: ais_start.sh — fix multi-PID kill. `lsof -ti:8000` can return multiple PIDs; current code only kills first. Fix: `kill $(lsof -ti:8000 2>/dev/null) 2>/dev/null || true`
- [ ] AIStudio_152: Ingestion false-negative UI bug — "Ingestion failed" shows when all files skipped (already indexed). Root cause: `_run_ingest_background` sets status=error when returncode=0 but last tqdm line is empty (fast ingest with no Process bar output). Fix: check final chunk/file counts from cached best-seen values before declaring error. Medium priority.
- [x] AIStudio_153: CODEBASE_GUIDE not retrieved — FIXED 2026-04-07. Root cause was multi-layered: (1) pipeline.py ingested trash/CODEBASE_GUIDE.pdf instead of uploads/CODEBASE_GUIDE.pdf due to rglob recursing into trash/; (2) manifest-based skip logic caused re-uploads to be skipped; (3) stale trash/HOWTO.pdf chunks in Qdrant consumed 3 of top-10 retrieval slots. Fixes: trash/ moved outside uploads/, Qdrant-based skip logic, abs_file_path resolve() fix in delete endpoint, stale chunks deleted manually. Verified working at top-K=10.
- [ ] AIStudio_154: Citation duplicate numbering bug — same PDF appearing twice in references (HOWTO.pdf p.8 appears as both [4] and [5]). Pre-existing but surfaced April 6.
- [ ] AIStudio_155: Retrieval content-dominance problem — at top-K=5, documents with many chunks (HOWTO) drown out documents with fewer chunks (CODEBASE_GUIDE) even when the latter ranks #1 in vector search. The deduplication in generate_answer_with_citations merges all chunks from the same source, so HOWTO's 4-5 merged chunks dominate the LLM context. Fix options: (a) per-source chunk cap in retrieval, (b) query expansion / HyDE pre-retrieval, (c) corpus_meta routing injected into Qdrant query not just LLM prompt. Pipeline item — investigate.
- [ ] AIStudio_156: Doc update — CODEBASE_GUIDE.md corpus structure table still shows `uploads/trash/` as trash path. Update to `trash/` (sibling of uploads/). Regenerate CODEBASE_GUIDE.pdf via ais_update_help_ops. Re-ingest into help corpus.
- [ ] AIStudio_157: HOWTO_OPS.md — corpus file recovery procedure references `uploads/trash/<filename>`. Update to `trash/<filename>`. Also update any other path references to old trash location.
- [ ] AIStudio_158: Chroma eradication — remove all remaining chroma references: config.py (ChromaConfig, use_chroma field), rag_core.py (dead chroma import branch), api.py (use_chroma in response bodies), vectorstore/chroma_store.py (delete file), cli/corpus_stats.py (Chroma label), test_chroma_fallback_on_distance_filter.py (delete), test_chroma_query_contract.py (delete or convert), test_rag_core_jsonl.py (paths["chroma"] fixture), test_api_integration.py (AISTUDIO_USE_CHROMA env). Full session — do atomically.
- [ ] AIStudio_159: JSONL eradication — remove manifest.jsonl, index.jsonl, doc_chunk_map.json writes from pipeline.py and api.py. Clean corpus_paths.py of those keys. Update debug_stats.py and cli/corpus_stats.py. Do after AIStudio_158.
- [ ] AIStudio_160: THINK Master — add T1.23 (POD-Deploy), T1.24 (POD-Download), T1.25 (POS-Sent) rules. Promote via Scaffold first per T2.21.


### Documentation
- [x] STD - AIStudio - EOS Bundle - 2026-03-24.md
- [x] STD - General - Naming Conventions - 2026-03-24.md (4-segment pattern)
- [x] STD - General - Naming Conventions - 2026-03-27.md (bundle_manifest.yaml exempt)
- [x] STD - INFO - Document Structure and Content - 2026-03-24.md
- [x] REF - AIStudio - Bash Cheat Sheet - 2026-03-24.md
- [x] HOWTO.md updated with EOS protocol, _session_summary.md convention, scripts/ gitignore note
