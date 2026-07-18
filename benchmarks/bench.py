#!/usr/bin/env python3
# Changelog: 2.17.0 — review pass: (1) the corpus-failure usage line now points at `ais_bench --help`;
#   (2) 'passed (binary)' → 'passed (binary test)'; (3) Query-expansion renders on/off, not 1/0;
#   (4) NEW --mem-track / --no-mem-track (default ON while _1037 is open) gates the PER-QUESTION
#   memory column only — the run-tail recap and the JSON record are unconditional, because a memory
#   warning must never hide behind a flag nobody passed; (5) the recap now reports the LOWEST point
#   seen during the run, not just the end value — a transient dip is what trips the guard mid-sweep
#   and it can recover before the run ends.
# Changelog: 2.16.4 — removed an orphaned blank-line print before the fit check: it dated from when
#   the fit gate opened its OWN --- Preflight bundle, and after the sections were unified it left a
#   gap in the middle of the checks.
# Changelog: 2.16.3 — Preflight's informational lines moved from stderr to stdout. Mixing streams
#   inside one section interleaved unpredictably (a phantom blank line after the corpus check) and
#   non-error output does not belong on stderr. Errors still go to stderr.
# Changelog: 2.16.2 — batch output polish: `--- Batch` section header re-homed here (it was the
#   wrapper's until v1.10.1); the run-count line uses `•` (section-level) with no leading blank;
#   the runtime estimate now prints INSIDE --dry-run, which is when the hours are being decided.
# Changelog: 2.16.1 — ruff SIM102: flatten the nested preflight guard into one condition.
# Changelog: 2.16.0 — AIStudio_1040: --batch is now machine-adaptive and --canonical is the exact
#   reproduction verb (they were the same flag; --canonical was a deprecated alias).
#     --canonical            reproduce the audited runs with their PINNED models (comparability)
#     --batch                every set twice: smallest INSTALLED + largest that FITS (the 4x2)
#     --batch --model X      X for every set (per-run fit gate still applies)
#     --batch --model largest|smallest   explicit tier selection
#   Rationale: a 24GB box could not run the reference suite AT ALL (pinned 27b wedges), while the
#   pinned spec is exactly what makes published numbers comparable — so the two needs got two verbs.
#   Adds an order-of-magnitude runtime estimate before execution (bare --batch is 8 runs = hours)
#   and reports the resolved model set; --dry-run shows the expanded run list.
# Changelog: 2.15.0 — (1) BUG: Preflight lived inside _resolve_fit_policy(), which only runs when
#   --model is passed — so `ais_bench --corpus nonexistent` ran EIGHT default questions against a
#   corpus that does not exist instead of aborting. Preflight now opens in main() right after the
#   banner, unconditionally. (2) The 'no questions file — using defaults' line is now a `·`
#   sub-detail under ▶ Checking questions..., not a stray pre-section print. (3) Bullet split per
#   CLI-Output review: `•` = section-level supplementary info, `·` = indented sub-detail.
# Changelog: 2.14.1 — (1) reverted the blank line before each section separator (reviewed live:
#   denser reads better). (2) The corpus/questions preflight MOVED here from ais_bench.sh: the
#   wrapper aborted before python ran, so a bad --corpus printed ❌ with NO identity banner,
#   violating CLI-Output STD §2 ('very first line, unconditionally'). bench.py now owns banner +
#   every check, and failures render as ❌ + guidance inside --- Preflight. (3) pandoc note back
#   to ⚠ per Manuel (the real fix is install-side: weasyprint is pip-installable, pandoc is brew).
# Changelog: 2.14.0 — CLI-Output conformance pass (Manuel review 2026-07-18): (a)(d) `_sep()` now
#   emits a blank line before every section separator except the first, so the banner and each
#   block get air; (b) write_markdown no longer prints the .md filename mid-Summary (it was
#   duplicating the --- Reports listing); (e) NEW `--- Reports` section with an `✅` parent line;
#   (c) the pandoc nag is no longer a per-run `⚠` — a missing optional PDF toolchain is not a
#   warning, and months of crying wolf trains the eye to skip real ones. It is now a neutral `·`
#   sub-detail inside --- Reports.
# Changelog: 2.13.1 — AIStudio_1037: the drift footer no longer counts the one-time MODEL LOAD as
#   accumulation. Q1's before-sample precedes residency, so an 8B on 128GB showed a fixed ~-5 that
#   looked like a leak. Now reports `load -5 · steady 91% → 91% at end (+0 over N questions after
#   load)` and only warns on a post-load slide (>=2 measured questions, <=-10 points).
# Changelog: 2.13.0 — AIStudio_1037 INSTRUMENTATION: per-question free-memory sampling.
#   Each question now prints `mem <before>%→<after>%` and the run tail prints the total drift
#   (`52% at start → 23% at end (-29 points)`) with a warning when the slide is large or the
#   run ends low on headroom. Both values persist to the JSON (`memory.free_pct_before/after`).
#   Reads macOS `memory_pressure` — the same source api._available_memory_bytes uses, so the
#   printed number is what the fit guard decides on. Diagnostic only: no behaviour change, and
#   it degrades silently (None) off-macOS. Purpose: distinguish a genuine content miss from a
#   fit-guard BLOCK caused by the sweep starving itself, and to choose between the candidate
#   fixes (release per-question KV vs clean baseline at launch) from data rather than guesswork.
# Changelog: 2.12.4 — fixed double period ("hang..", "right now..") — _fit_warn/_fit_err already
#   append the period; callers no longer pass their own. (Text-only.)
# Changelog: 2.12.3 — Fit gate rebuilt as a count-based picker (Manuel, 2026-07-17), conforming to
#   CLI Output STD §10.3-D. When the chosen model is BLOCKed and --fit-policy is absent, the gate now
#   branches on how many OTHER models fit: 0 → dead-end (free memory / Tutorial §2.5 / restart);
#   1 → lettered inline "(r)un <model>, (f)ree memory & restart, (Enter) cancel"; ≥2 → uniform numbered
#   list (models largest-fitting-first with "run on this", then Free-memory-&-restart, then Cancel;
#   Enter = Cancel). New _fetch_fitting_models() returns the FIT/WARN generative set from /models. The
#   old (r)etry-that-re-polls-in-process is GONE — "free memory" now directs to ais_restart (state
#   change realized by restart, not a live poll). All non-run exits end "❌ Stopped — no benchmark run."
# Changelog: 2.12.2 — CLI Output STD §10 conformance: options comma-separated (not 3-space), cursor is
#   ❯ (U+276F) inline, unrecognized input reprompts once ("· didn't catch that") then falls to the Enter
#   default. No logic change.
# Changelog: 2.12.1 — Fit-gate polish (Manuel, 2026-07-16): (a) fixed double-period ("hang..") by
#   stripping the trailing "." from the server reason before formatting; (b) retry no longer restates
#   the full warning — it prints one concise "still doesn't fit — <reason>" line; (c) NO-MODEL-FITS
#   dead-end: when nothing generative fits (rec is None), the gate says "No model fits this machine
#   right now / free memory or see Tutorial §2.5 / then restart: ais_start" instead of offering a
#   downgrade that doesn't exist. No logic change to the fit decision.
# Changelog: 2.12.0 — Interactive fit gate reworked (Manuel, 2026-07-16): when --fit-policy is absent
#   and a run is BLOCKed, bench no longer offers a [YES/n] "proceed anyway" — it never silently runs
#   the too-big model. Instead: `(r)etry after closing other apps` (re-reads free memory and
#   re-evaluates — the run proceeds if it now fits), `(d)owngrade to <rec>` (run the fitting model),
#   or Enter/anything-else → stop (fail-closed). Retry loops until fit, downgrade, or stop. This makes
#   the memory-headroom path actionable (close apps → retry) rather than binary. --help updated.
# Changelog: 2.11.1 — CLI Output STD §2 conformance for the fit gate: _resolve_fit_policy now emits a
#   `--- Preflight` section label + a `▶ Checking model fit...` action line, with the verdict/skip as
#   `⚠`/`ℹ` detail lines under it (was two bare `⚠` lines with no section header). Single-run site drops
#   its redundant post-skip warning (the resolver already prints the reason). No fit-logic change.
# Changelog: 2.11.0 — AIStudio_1012: --dry-run. With --batch, prints the resolved run set (id · corpus
#   · model · scope · questions · top_k · timeout) from bench_canonical.yaml and EXITS without running
#   the multi-hour suite. Guarded: --dry-run WITHOUT --batch stops with a notice rather than silently
#   executing a single run (anti-silent-failure). Preview → stdout; the notice → stderr.
# Changelog: 2.10.0 — AIStudio_1020: --fit-policy {skip,downshift,force}. Before a run dispatches a
#   model, bench asks the API's /models `fit` field (the ONE guard policy in app/model_fit.py — no
#   divergent bench-side arithmetic) whether it fits this box. On a BLOCK (e.g. 27b on 24GB, which
#   loads then hangs): skip → don't run, log a loud partial SKIP (never a silent gap in the summary);
#   downshift → auto-switch to the recommended fitting model, annotated; force → run anyway with a
#   warning. If --fit-policy is ABSENT and a run is BLOCKed, bench STOPS and confirms [YES/n] before
#   continuing (per Manuel) — TTY-gated on stdin: with no terminal to answer (fully non-interactive)
#   it FAILS CLOSED (❌, exit 1) rather than guess. FIT/WARN/unknown and unspecified --model run as
#   before. Conforms to STD - AIStudio - CLI Output (⚠/❌/·/ℹ symbols, prompt+warnings to stderr so a
#   tee'd report stays clean). NOTE: the [YES/n] gate has no CLI-Output-STD precedent — flagged.
# Changelog: 2.9.5 — A19-adjacent: PDF generation weasyprint step made reliable. The html→pdf
#   render previously wrote a temp .py and ran it via subprocess under sys.executable — if that
#   interpreter differed from the one running bench.py (common: bench under venv, sys.executable
#   pointing elsewhere), the weasyprint import failed and printed "install weasyprint" even when
#   it WAS installed. Now imports weasyprint in-process (same env as bench.py), so a present
#   weasyprint is always found; ImportError → the honest install hint, other errors → a distinct
#   weasyprint-error message (no longer mislabeled as not-installed). pandoc step (md→html)
#   unchanged; its FileNotFoundError → brew install pandoc hint unchanged. temp-file cleanup now
#   in a finally so it runs on both success and failure.
# Changelog: 2.9.4 — A18 (operator-workflow leaks in civilian output). (1) Report footer printed
#   "Upload zip and say 'audit that report' for qualitative review" — a urCrew/Claude-session
#   instruction meaningless to a public user; replaced with a real hint (open the .md report).
#   (2) --scope --help string named _scope_common_ops (a gitignored operator file); dropped the
#   operator-file name, kept the resolved-path explanation. Same reverse-leak class as A1/A2.
# Changelog: 2.9.3 — A2 fix: `--batch-id <ID>` alone now triggers batch mode. --batch-id sets
#   dest `canonical_id`, but the dispatch gate only checked `canonical` (set by --batch) — so
#   `ais_bench --batch-id D` (no --batch) silently fell through to a single run on the DEFAULT
#   corpus (demo) instead of running canonical run D. Now the gate fires on either flag.
# Changelog: 2.8.4 — Batch mode: child runs spawned by run_canonical now suppress their own
#   [ais_bench v… ] header (env AIS_BENCH_CHILD=1 on the child; main() skips the header when set).
#   The parent prints one header + the ▶ banner IDs each run — kills the N+1 header repetition in
#   --batch output. Added module-level `import os` (was only a local import in the PDF block).
# Changelog: 2.8.3 — VERSION constant synced 2.7.3 → 2.8.3 (was lagging the 2.8.2 changelog
#   head — the T2.52 trap: bump the field the tool reads, not just the comment). CLI Output STD:
#   batch banner de-bolded to a `·` info line (was a competing [ ] header); per-run ──► → ▶
#   (──► not in the §1 symbol table). Docstring: stale --subset → --scope (removed 2.8.0).
# Changelog: 2.8.2 — Flag rename: --batch is now the primary flag for the pinned run set
#            (--canonical kept as a silent deprecated alias; same dest, so behavior identical).
#            --batch-id mirrors --canonical-id. NOTE: ais_bench.sh wrapper still keys its
#            preflight-skip on --canonical — wrapper update to also skip on --batch is OWED.
# Changelog: 2.8.1 — Canonical/batch spec relocated: --canonical now reads
#            benchmarks/batch/bench_canonical.yaml (was flat benchmarks/bench_canonical.yaml);
#            legacy flat path kept as fallback. Help strings updated.
# Changelog: 2.8.0 — Questions resolver: named subsets now live in benchmarks/<corpus>/questions/
#            (mirrors data/corpora/<corpus>/scopes/). load_questions tries questions/ first, flat
#            <corpus>/ kept for back-compat. A NAMED --questions stem that does not resolve is now a
#            HARD ERROR (SystemExit) — never silent-falls-back to defaults (silent-failure HALT rule).
#            Empty --questions still resolves the corpus default superset benchmarks/<corpus>/<corpus>_
#            questions.yaml. Stale June_2026 help-ref updated to questions/sec_10k_frontier_questions.yaml.
# Changelog: 2.7.0 — report now records the actual run manifest: scope name + resolved firm
#            universe, and the questions file path + content SHA-8 (pins the exact question
#            set, label-drift-proof). Written to BOTH the JSON config block (recorded) and the
#            MD Configuration section (shown). Closes the "report must show the scope manifest" TODO.
# Changelog: 2.6.0 — add --timeout flag (default 120s); threaded through run_query to the
#            per-question urlopen. Slow large models (gemma3:27b) need --timeout 300 on heavy
#            multi-firm questions that otherwise hit the 120s wall with 0 citations.
# Changelog: 2.4.0 — Unified-scope wiring (step 3). --scope now LOADS + validates a scope
#              via scripts/_scope_common_ops (hard-error on a missing named scope, AIStudio_882)
#              and exposes its firm-token universe (retrieval restriction is the paired step,
#              pending the --scope ↔ /ask source_path mechanism). --scope no longer resolves
#              question filenames. --lang → --lang_questions (filters question_language, not the
#              firm filing-language; the EN/non-EN firm split is --scope's job now). Added
#              --keywords {on,off} (keyword-channel ablation; off = old no_keyword_hint). Removed
#              --subset + the hardcoded FIRM_SUBSETS registry (firm grouping is a scope file now).
# Changelog: 2.0.12 — Remove --difficulty flag (redundant — difficulty is encoded
#              in questions filename; --questions basic implies difficulty:basic).
#              Add --scope flag. Fix stem resolution to try corpus_scope_stem,
#              corpus_stem, stem_questions patterns before falling back to stem.yaml.
# Changelog: 2.0.11 — Fix stem expansion: try {corpus}_{stem}_questions.yaml and
#              {stem}_questions.yaml before {stem}.yaml. Enables --questions basic
#              to resolve esef_banks_basic_questions.yaml. Also adds scope-aware
#              resolution: {corpus}_{scope}_{stem}_questions.yaml when --scope active.
# Changelog: 2.0.10 — AIStudio_840 addendum: entity_count field added to
#              load_questions() (v1.2 schema). Captures number of distinct entities
#              needed to answer — analytical field complementing entity_filter.
# Changelog: 2.0.9 — AIStudio_840: questions schema v1.2 support. load_questions() now reads question_language, answer_location, section_count, data_type, difficulty fields (all optional, backward compatible). filter_questions() gains difficulty= parameter. --difficulty flag added (basic|standard|complex). Per-question verbose output shows difficulty + answer_location.
# Changelog: 2.0.8 — AIStudio_841: implement --verbose (-v) and --super-verbose (-vv).
#             --verbose: chunks_retrieved, entity_filter, first_source per question.
#             --super-verbose: retrieval_query, entity_tokens, keywords, model_used, answer preview.
#             Requires api.py v1.8.8 (chunks_retrieved in AskResponse).
# Changelog: 2.0.7 — AIStudio_841 TODO: --verbose (chunks_retrieved, effective_k, entity_filter,
#             first source per question) and --super-verbose (retrieval_query, entity tokens,
#             keywords, model_used, full answer, all citations). Requires AskResponse to return
#             chunks_retrieved + effective_k. Filed HIGH/WEEK.
# Changelog: 2.0.6 — MD report shows retrieval_query (post-expansion), model_used,
#             entity_filter, keywords per question. Replaces firm/year placebo fields.
# Changelog: 2.0.5 — AIStudio_840: wire keywords from YAML through run_query() to
#             /ask payload. Previously keywords were evaluation-only (used by evaluate()
#             for mechanical scoring) but never sent to the API for BM25 boosting.
#             All 17 previous runs had keywords=None reaching retrieve().
# Changelog: 2.0.4 — fix evaluate() failure return missing citation_count and other keys;
#             bench.py crashed with KeyError when API request failed mid-run.
# Changelog: 2.0.3 — move bold bracketed header to Python per STD §7. Shell wrapper
#             no longer prints version header. bench.py main() prints it as first line.
# Changelog: 2.0.2 — AIStudio_829: benchmark reports bundled as zip (json+md+pdf).
#             Audit trigger: "audit that report" — Claude reads zip, adds qualitative
#             ratings + comments, produces _audited_ zip. Protocol in THINK Master T2.47.
# Changelog: 2.0.1 — AIStudio_828: accent + hyphen normalization in evaluate().
#             flag if < 0.1 on non-trivial questions. Language marker (*) for non-English
#             questions via YAML language field. Remove "all keywords found" from terminal
#             output — keyword pass is the pass condition, not a separate signal.
#             Base Top K label in Configuration section (effective K per AIStudio_825).
# Changelog: 1.9.9 — fix keywords field: read "keywords" first, fall back to "expected_keywords";
#             add Alpha and Min Score to report Configuration markdown section.
# Changelog: 1.9.8 — CRITICAL: entity_filter field was not extracted from YAML
#             questions during load_questions() — q.get("entity_filter") always
#             returned None. Added entity_filter to the question dict.
# Changelog: 1.9.7 — auto-copy .md report to ~/Downloads/ at end of run
#             so urc_deploy --last picks it up immediately.
# Changelog: 1.9.6 — fix evaluate() over-aggressive no_info_signal:
#             only penalize no_info when citation_count == 0. When model has
#             citations it is answering substantively — hedging about missing
#             firms is honest, not a failure.
# Changelog: 1.9.5 — corpus metadata defaults applied for top_k/temperature/alpha/min_score
#             when not explicitly passed via CLI. Uses None sentinel.
# Changelog: 1.9.4 — --questions accepts stem (no path, no .yaml extension);
#             auto-expands to benchmarks/<corpus>/<stem>.yaml.
#             Example: --questions sec_10k_questions_no_filter
# Changelog: 1.9.3 — Fix evaluate() false positives/negatives:
#             (a) 0 citations always fails regardless of keyword pass
#             (b) keyword check restricted to substantive answer only —
#             keywords found in refusal phrases no longer count as keyword pass
#             (c) no_info_signal phrases expanded with observed patterns
# Changelog: 1.8.1 — AIStudio_752: add --alpha flag for hybrid retrieval; pass hybrid_alpha
#            to /ask payload. Removes env var workaround.
"""
AIStudio RAG Benchmark Script
Usage:
    ais_bench                                            # demo corpus, defaults
    ais_bench --corpus sec_10k --top-k 10               # SEC corpus
    ais_bench --corpus demo --model llama3.1:70b        # 70b model

Question scope filtering (sec_10k):
    ais_bench --corpus sec_10k --topics "AI Risk Evolution"
    ais_bench --corpus sec_10k --scope big_banks
    ais_bench --corpus sec_10k --question-ids capital_ratios_trend,latency_test
    ais_bench --corpus sec_10k --topics "Capital & Financial Position" --scope big_banks

Flags:
    --corpus        Corpus name to query (default: demo)
    --top-k         Number of chunks to retrieve (default: 5)
    --temperature   LLM temperature (default: 0.3)
    --model         Model to use (default: from API config)
    --questions     Path to YAML question file (auto-detected from corpus name if omitted)
    --api           API base URL (default: http://localhost:8000)
    --timeout       Per-question HTTP timeout in seconds (default: 120; raise for slow large models)
    --no-markdown   Skip writing .md report
    --full          Include full answers in report (default: first 4 paragraphs)
    --firm          Inject firm filter into all queries (overrides YAML firm fields)
    --scope         Restrict the retrieval firm-universe to a named scope file:
                    benchmarks resolve <corpus>_<scope>_scope.yaml (e.g. big_banks, bulge_bracket,
                    asset_managers, exchanges, insurance, custody, boutiques). Missing scope = hard error.
    --topics        Filter questions by topic name (comma-separated, AND with --scope)
    --question-ids  Filter to specific question IDs (comma-separated, AND with other filters)
    --alpha         Hybrid retrieval alpha: 0.0=pure vector, 1.0=pure BM25, None=backend default

Output files (in benchmarks/<corpus>/reports/):
    benchmark_<corpus>_<model>_<descriptors>_<YYYY-MM-DD_HHMM>.json
    benchmark_<corpus>_<model>_<descriptors>_<YYYY-MM-DD_HHMM>.md
    benchmark_<corpus>_<model>_<descriptors>_<YYYY-MM-DD_HHMM>.pdf  (if pandoc + weasyprint installed)
    (descriptors: scope/questions/top_k/etc.; datetime is always the last field — Naming STD §2)

Question file auto-detection (in order):
    benchmarks/<corpus>/<corpus>_questions.yaml
    data/corpora/<corpus>/<corpus>_questions.yaml
    Built-in defaults (SEC 10-K questions — fallback only)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import time

try:
    import yaml as _yaml

    _YAML_AVAILABLE = True
except ImportError:
    _YAML_AVAILABLE = False
import sys
from datetime import datetime
from pathlib import Path

# Shared scope resolver (scripts/_scope_common_ops.py). bench lives in benchmarks/,
# the resolver in ../scripts/ — prepend it to the path before import. Single source of
# truth for scope load/validate + entity selection (AIStudio_882 hard-error contract).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import _scope_common as _scope  # noqa: E402

# Version — single source of truth for urc_deploy and runtime display.
# Must be within first 8KB (extract_version limit). No # Version: comment.
# Changelog: 2.7.3 — Naming STD §2 conformance: timestamp moved to the END of base_name,
#            after all descriptors (was mid-string). New: benchmark_{corpus}_{model}{suffix}_{ts}.
#            Legacy reports keep their old mid-string order on disk; new reports are datetime-last.
# Changelog: 2.7.2 — Naming STD §2 descriptor ordering: filter_suffix fields now ordered
#            LEAST-VOLATILE-FIRST (questions → scope → sub-selectors → ablations → top_k),
#            and a `questions` stem descriptor was added (non-default sets self-label; the
#            default set stays unlabelled). Run B (June_2026) no longer collides with run A.
# Changelog: 2.7.1 — AIStudio_931 correction (Naming STD §14 / Command Dev §3a). --canonical is now
#            pure orchestration: sub-runs write standard benchmark_{corpus}_{model}_{timestamp}{suffix}
#            reports into benchmarks/<corpus>/reports/ — no copy, no rename, no sample_reports/ dir
#            (removed the fragile newest-by-mtime heuristic, the AIStudio_930 clock trap). Added a
#            top_k{N} descriptor to filter_suffix so runs differing only by K are distinguishable.
# Changelog: 2.7.0 — AIStudio_931 (provisional #): --canonical mode. Runs the pinned set from
#            benchmarks/bench_canonical.yaml (the four TUTORIAL §5.9 runs) via the normal
#            single-run path. +--canonical-id to run one. Inert (graceful exit) when the spec yaml
#            is absent — ships safe before the apparatus is finalized.
# Changelog: 2.5.0 — AIStudio_882 (scope application): --scope now RESTRICTS retrieval.
#            scope_tokens ride the /ask allowed_source_paths field (server ANDs them with
#            each question's entity logic — intersect). Closes the 2.4.0 deferred seam.
# Changelog: 2.4.0 — Unified-scope wiring (step 3): --scope loads+validates via
#            _scope_common_ops (hard-error 882) and exposes the firm-token universe;
#            --lang→--lang_questions (question_language, not firm filing-language);
#            +--keywords {on,off} (keyword ablation); −--subset/FIRM_SUBSETS.
# Changelog: 2.3.0 — AIStudio_878: amber rating. evaluate() returns rating ∈ {GREEN,AMBER,RED}
#            + weighted score, demoting keyword_pass from the binary verdict to a soft signal.
#            RED = no citations / honest-empty / wrong firm (entity_coverage==0 with filter active);
#            GREEN = cited + right-firm + honest + keywords ok + adequate density;
#            AMBER = cited + plausibly right but a soft weakness (keyword miss, low density,
#            partial coverage) → audit. Binary "pass" retained for back-compat. Console + summary
#            + report surface the tri-state. Thresholds are v1 defaults — calibrate vs audited runs.
# Changelog: 2.2.1 — AIStudio_875 lint fixes: F821 _eff_kw→_q_kw straggler (super-verbose path),
#            SIM108 ternary for _eff_ef.
# Changelog: 2.2.0 — AIStudio_875: REPLACE --augment-from with --query-expansion N (default 1) +
#            --entity-filter {none,yaml,auto} (default auto). Two orthogonal axes the conflated
#            --augment-from could not express (F8 finding). Maps: scaffold≡--query-expansion 1 --entity-filter yaml;
#            auto≡--query-expansion 1 --entity-filter auto; none≡--query-expansion 0 --entity-filter none.
#            Server (api.py v1.9.0) does the auto entity→source_path filter wiring.
# Changelog: 2.1.0 — AIStudio_867: add --augment-from {scaffold,ui,auto,none} (default ui).
#            Controls which hint source bench forwards to retrieval, isolating the
#            scaffold-vs-auto frontier. DEFAULT CHANGE: un-flagged ais_bench now forwards
#            UI keywords only (no hand-fed entity_filter) — was implicit scaffold. Pass
#            --augment-from scaffold for the prior entity-isolation behavior. 'auto' forwards
#            no hints and forces hybrid so server query-analysis (GLEIF/glossary) expansion
#            fires. Verbose/config output reflects EFFECTIVE sent hints, not YAML values.
# Changelog: 2.9.2 — AIStudio_941: batch runner reads a top-level `timeout:` in bench_canonical.yaml
#            (mirrors top-level `model:`). Resolution per-run spec timeout → top-level spec timeout →
#            parent --timeout → 120. A canonical run now carries its own timeout; no --timeout 300 needed.
# Changelog: 2.9.1 — AIStudio_941: evaluate() failed-request branch now returns rating="RED" + the
#            5 keys it previously omitted (score/keyword_pass/entity_coverage/entities_missing/rating),
#            so timed-out questions score as RED instead of blank-undercounting, and the report renderer
#            can't KeyError on a failed row (the mid-run crash noted in the 2.x history).
# Changelog: 2.9.0 — AIStudio_940: --batch/--canonical now propagates --timeout to sub-runs (per-run
#            spec `timeout` wins, else inherit the parent's --timeout). Fixes `ais_bench --canonical
#            --timeout 300` silently not reaching children — heavy questions on the larger _958 window
#            could hit the 120s wall → HTTP fail → mechanical RED.
VERSION = "2.17.0"

# ── CLI ───────────────────────────────────────────────────────────────────────


def _sep(label: str) -> None:
    """Print a dim italic section separator per STD - AIStudio - CLI Output."""
    print(f"\033[2m\033[3m--- {label}\033[0m")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="AIStudio RAG Benchmark")
    p.add_argument("--corpus", default="demo", help="Corpus name")
    p.add_argument(
        "--scope",
        default=None,
        help=(
            "Scope stem naming a firm subset, resolved to "
            "data/corpora/<corpus>/scopes/<corpus>_<scope>_scope.yaml (e.g. "
            "--scope esef_banks_lang_noen, or the bare stem 'lang_noen'). LOADED + "
            "validated at startup — a missing named scope is a hard error (AIStudio_882), "
            "never a silent fallback. Restricts the retrieval firm-universe to the scope's "
            "firms; does NOT filter questions (use --questions / --question-ids / "
            "--lang-questions for that)."
        ),
    )
    p.add_argument("--top-k", type=int, default=None, help="Top K chunks to retrieve (default: corpus metadata or 5)")
    p.add_argument("--temperature", type=float, default=None, help="LLM temperature (default: corpus metadata or 0.3)")
    p.add_argument("--model", default=None, help="Model ID (default: API default)")
    p.add_argument("--questions", default=None,
                    help="Path to questions YAML file, or bare stem (e.g. sec_10k_questions_no_filter). "
                         "Stem auto-expands to benchmarks/<corpus>/<stem>.yaml.")
    p.add_argument("--api", default="http://localhost:8000", help="API base URL")
    p.add_argument("--timeout", type=int, default=120,
                   help="Per-question HTTP timeout in seconds (default: 120; raise for slow large models, e.g. gemma3:27b)")
    p.add_argument("--no-markdown", action="store_true", help="Skip writing .md report")
    p.add_argument("--full", action="store_true", help="Include full answers in report")
    p.add_argument(
        "--firm",
        default=None,
        help=(
            "Firm name to inject into all queries (e.g. 'Wells Fargo'). "
            "Overrides any per-question 'firm' field in the YAML. Caller is "
            "responsible for spelling and firm selection."
        ),
    )
    p.add_argument(
        "--topics",
        default=None,
        help=(
            "Filter questions by topic name (comma-separated). "
            "Example: --topics 'AI Risk Evolution,Capital & Financial Position'"
        ),
    )
    p.add_argument(
        "--question-ids",
        default=None,
        help=(
            "Filter to specific question IDs (comma-separated). "
            "Example: --question-ids capital_ratios_trend,latency_test"
        ),
    )

    p.add_argument(
        "--alpha",
        type=float,
        default=None,
        help="Hybrid retrieval alpha: 0.0=pure vector, 1.0=pure BM25. None=corpus metadata or backend default.",
    )
    p.add_argument(
        "--min-score",
        type=float,
        default=None,
        dest="min_score",
        help="Minimum chunk score threshold. None=corpus metadata or backend default.",
    )
    p.add_argument(
        "--lang-questions",
        dest="lang_questions",
        nargs="+",
        default=None,
        metavar="LANG",
        help=(
            "Filter questions by the language the QUESTION is phrased in "
            "(question_language field; space-separated). Example: --lang-questions en. "
            "NOTE: this is NOT the firm filing-language — the EN/non-EN firm split is now "
            "done with --scope (e.g. --scope esef_banks_lang_noen). Questions without a "
            "question_language field default to 'en'."
        ),
    )
    p.add_argument(
        "--keywords",
        choices=["on", "off"],
        default="on",
        help=(
            "Keyword (BM25) channel toggle. 'on' (default) forwards each question's keywords "
            "to retrieval; 'off' suppresses them — the keyword-channel ablation (the old "
            "no_keyword_hint variant). Independent of --entity-filter (the entity ablation). "
            "no_scaffold ≡ --entity-filter none --keywords off."
        ),
    )
    p.add_argument(
        "--verbose", "-v",
        action="store_true",
        help=(
            "Per-question: show chunks_retrieved, effective entity_filter, first source. "
            "AIStudio_841."
        ),
    )
    p.add_argument(
        "--super-verbose", "-vv",
        action="store_true",
        dest="super_verbose",
        help=(
            "Per-question: show retrieval_query (post-expansion), entity tokens, "
            "keywords sent, model_used, and full answer text. Implies --verbose. "
            "AIStudio_841."
        ),
    )

    p.add_argument(
        "--query-expansion",
        dest="query_expansion",
        type=int,
        default=1,
        metavar="N",
        help=(
            "Entity-name expansion repeat count (AIStudio_875). 0 = off (raw query); "
            "1 = each recognized entity's canonical name appended once (DEFAULT); "
            "N>1 = appended N times to weight BM25. Affects the retrieval query only, "
            "never the query sent to the LLM."
        ),
    )

    p.add_argument(
        "--entity-filter",
        dest="entity_filter_mode",
        default="auto",
        choices=["none", "yaml", "auto"],
        help=(
            "Source of the Qdrant source_path retrieval filter (AIStudio_875). Governs the "
            "ENTITY filter only — `keywords` are an independent BM25 channel forwarded in ALL modes. "
            "none = no filter (all firms eligible); "
            "yaml = use the question file's entity_filter field (hand-fed scaffold); "
            "auto = IGNORE the question file's entity_filter and instead detect entities from the "
            "query, mapping them to source_path tokens via the entity KB (DEFAULT). Requires a "
            "reachable KB for the corpus; if none loads, auto applies no filter. Replaces --augment-from."
        ),
    )

    p.add_argument(
        "--canonical",
        dest="canonical_exact",
        action="store_true",
        help=(
            "EXACT REPRODUCTION of the audited reference runs: every run in "
            "benchmarks/batch/bench_canonical.yaml with its PINNED model, unchanged. This is the "
            "comparability path — use it to reproduce or extend published numbers. On a machine that "
            "cannot fit the pinned model the fit gate applies (see --fit-policy)."
        ),
    )
    p.add_argument(
        "--batch",
        dest="canonical",
        action="store_true",
        help=(
            "Run the reference question sets against THIS machine. Bare --batch runs every set twice "
            "— once on the smallest installed model and once on the largest that fits — so a machine "
            "is characterised across its own tier range. Narrow it with --model <name|largest|smallest>. "
            "Reports are written per run into benchmarks/<corpus>/reports/ and name their model."
        ),
    )
    p.add_argument(
        "--batch-id",
        "--canonical-id",
        dest="canonical_id",
        default=None,
        metavar="ID",
        help="With --batch, run only the single run whose id matches (e.g. --batch-id C).",
    )

    p.add_argument(
        "--mem-track",
        dest="mem_track",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "Show free memory per question (`mem 91%%=91%%`). Default ON while AIStudio_1037 (sweep "
            "self-starvation) is open; --no-mem-track hides the column. The run-tail memory recap and "
            "the JSON record are written regardless — a memory warning must never hide behind a flag."
        ),
    )
    p.add_argument(
        "--fit-policy",
        dest="fit_policy",
        default=None,
        choices=["skip", "downshift", "force"],
        help=(
            "AIStudio_1020 — what to do when a run's model WON'T FIT this machine's memory (the API "
            "fit guard returns BLOCK; e.g. gemma3:27b on a 24GB box loads then hangs). "
            "skip = do not run it (logged as a loud SKIP, never a silent gap); "
            "downshift = auto-switch to the recommended fitting model; "
            "force = run anyway (you accept the wedge risk). "
            "If OMITTED and a run is BLOCKed, bench stops and offers (r)etry-after-freeing-memory, "
            "(d)owngrade-to-a-fitting-model, or Enter=stop — it never silently runs the too-big model "
            "(requires a terminal; a fully non-interactive run fails closed). FIT/WARN models, and "
            "runs with no explicit --model, are unaffected."
        ),
    )

    p.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help=(
            "AIStudio_1012 — with --batch, print the resolved run set (corpus × model × scope × "
            "questions) from bench_canonical.yaml and exit WITHOUT executing the suite. Use it to "
            "confirm what a batch will run before committing the hours. (Without --batch it stops "
            "with a notice rather than running a single job.)"
        ),
    )

    return p.parse_args()


# ── Load questions ────────────────────────────────────────────────────────────

DEFAULT_QUESTIONS = [
    {
        "id": "goldman_ai_risk",
        "description": "Goldman Sachs AI risk — firm filter",
        "query": "What does Goldman Sachs say about the risks of artificial intelligence?",
        "corpus": None,  # uses CLI --corpus
        "firm": "Goldman Sachs",
        "year": None,
        "expected_keywords": ["artificial intelligence", "AI", "risk", "Goldman"],
        "notes": "Should return Goldman-specific AI risk disclosure",
    },
    {
        "id": "jpmorgan_cybersecurity",
        "description": "JPMorgan cybersecurity risk — firm filter",
        "query": "How does JPMorgan Chase describe their cybersecurity risk management?",
        "corpus": None,
        "firm": "JPMorgan Chase",
        "year": None,
        "expected_keywords": ["cybersecurity", "JPMorgan", "risk"],
        "notes": "Should return JPMorgan cybersecurity section",
    },
    {
        "id": "morgan_stanley_model_risk",
        "description": "Morgan Stanley model risk — firm filter",
        "query": "What is Morgan Stanley's approach to model risk?",
        "corpus": None,
        "firm": "Morgan Stanley",
        "year": None,
        "expected_keywords": ["model risk", "Morgan Stanley"],
        "notes": "Should return model risk governance section",
    },
    {
        "id": "goldman_ai_committee",
        "description": "Goldman AI governance committee — firm filter",
        "query": "Does Goldman Sachs have an AI governance committee and what does it do?",
        "corpus": None,
        "firm": "Goldman Sachs",
        "year": None,
        "expected_keywords": ["Artificial Intelligence", "committee", "governance"],
        "notes": "Should mention Firmwide Artificial Intelligence Risk and Controls Committee",
    },
    {
        "id": "cross_corpus_ai_governance",
        "description": "Cross-corpus AI governance — no filter",
        "query": "Which financial firms have dedicated AI governance committees?",
        "corpus": None,
        "firm": None,
        "year": None,
        "expected_keywords": ["AI", "committee", "governance"],
        "notes": "No firm filter — tests cross-corpus retrieval quality",
    },
    {
        "id": "bofa_climate_risk",
        "description": "Bank of America climate risk — firm filter",
        "query": "How does Bank of America describe climate risk in their annual report?",
        "corpus": None,
        "firm": "Bank of America",
        "year": None,
        "expected_keywords": ["climate", "risk", "Bank of America"],
        "notes": "Should return climate risk section",
    },
    {
        "id": "goldman_2026_revenue",
        "description": "Goldman 2025 revenue — firm + year filter",
        "query": "What were Goldman Sachs total revenues in 2025?",
        "corpus": None,
        "firm": "Goldman Sachs",
        "year": "2026",  # filing year
        "expected_keywords": ["revenue", "billion", "2025"],
        "notes": "Tests year filter combined with firm filter",
    },
    {
        "id": "latency_test",
        "description": "Simple factual — latency baseline",
        "query": "What is Goldman Sachs?",
        "corpus": None,
        "firm": "Goldman Sachs",
        "year": None,
        "expected_keywords": ["Goldman Sachs", "bank", "financial"],
        "notes": "Simple query for latency baseline measurement",
    },
]


def load_questions(path: str | None, corpus: str = "sec_10k") -> list[dict]:
    """
    Load benchmark questions from a file or auto-detect based on corpus name.

    Priority:
    1. Explicit --questions path (JSONL or JSON)
    2. Auto-detect: data/demo/demo_questions.json for demo corpus
    3. Fallback: DEFAULT_QUESTIONS (sec_10k hardcoded set)
    """
    # AIStudio_618b (v2.0.11): stem expansion — try multiple filename patterns.
    # Allows short stems: --questions basic → esef_banks_basic_questions.yaml
    # Resolution order (first match wins):
    #   1. {corpus}_{stem}_questions.yaml          — corpus-prefixed shorthand
    #   2. {stem}_questions.yaml                   — bare stem with _questions suffix
    #   3. {stem}.yaml                             — literal (legacy, full filename stem)
    # (v2.4.0: dropped the scope-keyed candidate — --scope is a firm filter, not a
    #  question-file selector.)
    if path is not None and "/" not in path and "\\" not in path and "." not in path:
        script_dir_stem = Path(__file__).parent
        # v2.8.0: named question subsets live in benchmarks/<corpus>/questions/ (mirrors
        # data/corpora/<corpus>/scopes/). Search there first; flat <corpus>/ kept for
        # back-compat. Empty stem (path is None) is handled below → corpus default superset.
        candidates = [
            script_dir_stem / corpus / "questions" / f"{corpus}_{path}_questions.yaml",
            script_dir_stem / corpus / "questions" / f"{path}_questions.yaml",
            script_dir_stem / corpus / f"{corpus}_{path}_questions.yaml",
            script_dir_stem / corpus / f"{path}_questions.yaml",
            script_dir_stem / corpus / f"{path}.yaml",
        ]
        matched = next((c for c in candidates if c.exists()), None)
        if matched:
            path = str(matched)
        else:
            # v2.8.0: a NAMED stem that does not resolve is a HARD ERROR — never silently
            # fall back to the default set (silent-failure HALT rule). Empty stem still
            # resolves to the corpus default superset via the path-is-None branch below.
            tried = "\n      ".join(str(c) for c in candidates)
            raise SystemExit(
                f"  \u2717 Questions stem '{path}' did not resolve for corpus '{corpus}'.\n"
                f"    Named question sets live in benchmarks/{corpus}/questions/ "
                f"as {corpus}_<stem>_questions.yaml.\n"
                f"    Tried:\n      {tried}"
            )

    # Auto-detect corpus question file if no explicit path given
    # Priority: {corpus}_questions.yaml > {corpus}_questions.json > DEFAULT_QUESTIONS
    if path is None:
        script_dir = Path(__file__).parent
        repo_root = script_dir.parent
        # Search order: benchmarks/{corpus}/ first, then data/corpora/{corpus}/
        search_roots = [
            script_dir / corpus,  # benchmarks/{corpus}/
            repo_root / "data" / "corpora" / corpus,  # data/corpora/{corpus}/
        ]
        found = None
        for search_root in search_roots:
            for ext in (".yaml", ".yml", ".json"):
                candidate = search_root / f"{corpus}_questions{ext}"
                if candidate.exists():
                    found = candidate
                    break
            if found:
                break
        if found:
            path = str(found)
            pass  # path shown in header
        else:
            _QUESTIONS_NOTE.append(f"No questions file for '{corpus}' — using built-in defaults.")
            return DEFAULT_QUESTIONS

    if path is None:
        return DEFAULT_QUESTIONS

    p = Path(path)
    if not p.exists():
        print(f"Questions file not found: {path} — using defaults")
        return DEFAULT_QUESTIONS

    questions = []
    with p.open() as f:
        content_str = f.read().strip()

    # Support YAML, JSON array, and JSONL formats
    if p.suffix.lower() in (".yaml", ".yml"):
        # YAML format: list of topic blocks with questions
        if not _YAML_AVAILABLE:
            print("   pyyaml not installed — pip install pyyaml")
            return DEFAULT_QUESTIONS
        raw = _yaml.safe_load(content_str)
        # ── Schema validation guard ──────────────────────────────────────────────
        # Expected: list of topic-blocks, each: {topic: str, questions: [...]}
        # Common mistake: flat list of question dicts (topic as a field, not a wrapper).
        _schema_ok = (
            isinstance(raw, list)
            and len(raw) > 0
            and isinstance(raw[0], dict)
            and "questions" in raw[0]
        )
        if not _schema_ok:
            _hint = ""
            if isinstance(raw, list) and len(raw) > 0 and isinstance(raw[0], dict) and "question" in raw[0]:
                _hint = (
                    "\n   Hint: your file looks like a flat list of question dicts. "
                    "Wrap them in topic blocks:\n"
                    "     - topic: \"My Topic\"\n"
                    "       questions:\n"
                    "         - id: my_q\n"
                    "           question: \"...\"\n"
                    "           keywords: [kw1, kw2]"
                )
            _ref = "benchmarks/sec_10k/questions/sec_10k_frontier_questions.yaml"
            print(
                f"\n❌  Questions file schema error: {p}\n"
                f"    Expected a list of topic-blocks:\n"
                f"      - topic: \"Topic Name\"\n"
                f"        questions:\n"
                f"          - id: question_id\n"
                f"            question: \"Your question text?\"\n"
                f"            keywords: [kw1, kw2]\n"
                f"    Reference: {_ref}{_hint}\n"
            )
            return DEFAULT_QUESTIONS
        # ────────────────────────────────────────────────────────────────────────
        for topic_block in raw:
            topic = topic_block.get("topic", "General")
            for q in topic_block.get("questions", []):
                qid = q.get("id", q.get("question", "")[:40].lower().replace(" ", "_"))
                questions.append(
                    {
                        "id": qid,
                        "description": q.get("question", ""),
                        "query": q.get("question", ""),
                        "corpus": q.get("corpus", None),
                        "firm": q.get("firm", None),
                        "year": q.get("year", None),
                        "keywords": q.get("keywords", []),
                        "entity_filter": q.get("entity_filter", None),
                        "notes": q.get("notes", topic),
                        "topic": topic,
                        "language": q.get("language", "en"),
                        # v1.2 fields (optional, backward compatible)
                        "question_language": q.get("question_language", "en"),
                        "answer_location": q.get("answer_location", None),
                        "section_count": q.get("section_count", None),
                        "data_type": q.get("data_type", None),
                        "difficulty": q.get("difficulty", None),
                        "entity_count": q.get("entity_count", None),
                    }
                )
    elif content_str.startswith("["):
        # JSON array format: [{topic, questions: [...]}, ...]
        raw = json.loads(content_str)
        for topic_block in raw:
            topic = topic_block.get("topic", "General")
            for q in topic_block.get("questions", []):
                questions.append(
                    {
                        "id": q.lower().replace(" ", "_")[:40],
                        "description": q,
                        "query": q,
                        "corpus": None,
                        "firm": None,
                        "year": None,
                        "keywords": [],
                        "notes": topic,
                    }
                )
    else:
        # JSONL format: one question object per line
        for line in content_str.splitlines():
            line = line.strip()
            if line:
                questions.append(json.loads(line))

    pass  # count shown in header
    return questions


# ── Run single benchmark query ────────────────────────────────────────────────


def run_query(
    *,
    api: str,
    query: str,
    corpus: str,
    top_k: int,
    temperature: float,
    model: str | None,
    firm: str | None,
    year: str | None,
    hybrid_alpha: float | None = None,
    min_score: float | None = None,
    entity_filter: list[str] | None = None,
    allowed_source_paths: list[str] | None = None,
    keywords: list[str] | None = None,
    query_expansion: int = 1,
    entity_filter_mode: str = "auto",
    timeout: int = 120,
) -> dict:
    import urllib.request

    payload: dict = {
        "query": query,
        "corpus": corpus,
        "top_k": top_k,
        "temperature": temperature,
        "query_expansion": query_expansion,
        "entity_filter_mode": entity_filter_mode,
    }
    if model:
        payload["model"] = model
    if firm:
        payload["firm"] = firm
    if year:
        payload["year"] = year
    if min_score is not None:
        payload["min_score"] = min_score
    if entity_filter:
        payload["entity_filter"] = entity_filter
    if allowed_source_paths:
        payload["allowed_source_paths"] = allowed_source_paths  # AIStudio_882: scope firm-boundary
    if hybrid_alpha is not None:
        payload["hybrid_alpha"] = hybrid_alpha
    if keywords:
        payload["keywords"] = keywords

    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{api}/ask",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            elapsed = time.perf_counter() - t0
            data = json.loads(resp.read())
            return {"ok": True, "elapsed_sec": round(elapsed, 2), "data": data}
    except Exception as e:
        elapsed = time.perf_counter() - t0
        return {"ok": False, "elapsed_sec": round(elapsed, 2), "error": str(e)}


# ── Evaluate result ───────────────────────────────────────────────────────────


# Refusal phrases — keywords found inside these do not count as substantive keyword hits.
# Expanded from observed benchmark failures where model says "no information about X"
# and X happens to be a required keyword — mechanically passing but substantively failing.
_REFUSAL_PHRASES = [
    "no information available",
    "no relevant information",
    "sources do not contain",
    "sources do not address",
    "cannot find any information",
    "not found in the provided",
    "no data available",
    "unfortunately, there is no",
    "no direct mention of",
    "the documents primarily discuss",
    "i cannot find specific information",
    "based on general knowledge",
    "based on my general knowledge",
    "is not mentioned in",
    "i do not see any information about",
    "there is no mention of",
    "purely speculative and not based on actual data",
    "the available sources do not",
    "absent from the available sources",
    "does not contain information about",
    "no sources provided",
    "not explicitly stated",
    "not explicitly mentioned",
    "the provided sources do not",
    "the sources do not provide",
    "based on the provided",
]


def _strip_refusal_context(answer: str) -> str:
    """
    Remove sentences containing refusal phrases from the answer before keyword
    checking. This prevents keywords that appear in 'no information about X'
    phrases from counting as substantive keyword hits.
    """
    sentences = answer.split(".")
    clean = []
    for sentence in sentences:
        if not any(phrase in sentence.lower() for phrase in _REFUSAL_PHRASES):
            clean.append(sentence)
    return ".".join(clean)


def _normalize_text(s: str) -> str:
    """
    Normalize text for keyword matching:
    - Strip accents (Société → Societe, Crédit → Credit)
    - Normalize hyphens (non-performing → non performing)
    - Lowercase
    Applied to both answer text and keywords before comparison.
    Prevents false negatives from accent/hyphen variants (AIStudio_828).
    """
    import unicodedata
    # Strip accents
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    # Normalize hyphens to spaces
    s = s.replace("-", " ")
    return s.lower()


def evaluate(result: dict, expected_keywords: list[str],
             entity_filter: list[str] | None = None) -> dict:
    if not result["ok"]:
        return {
            "pass": False,
            "rating": "RED",          # AIStudio_941: a failed/timed-out request is a RED, not a blank — the old branch omitted rating (+ score/keyword_pass/entity_coverage/entities_missing), so timeouts undercounted in reports and any renderer reading result["score"] KeyError'd
            "score": 0.0,
            "reason": f"Request failed: {result['error']}",
            "keyword_pass": False,
            "citation_count": 0,
            "citation_pass": False,
            "citation_density": 0.0,
            "low_citation_density": False,
            "no_info_signal": False,
            "missing_keywords": [],
            "entity_coverage": None,
            "entities_missing": [],
            "cited_sources": [],
        }

    data = result["data"]
    answer = (data.get("answer") or "").lower()
    answer_normalized = _normalize_text(data.get("answer") or "")
    citations = data.get("citations") or []
    has_citations = data.get("has_citations", False)

    # AIStudio_796 fix (a): 0 citations always fails — no citation means either
    # hallucination or refusal. Never pass a 0-citation answer regardless of keywords.
    citation_pass = has_citations and len(citations) > 0

    # Check for no-information signal
    no_info_signal = any(phrase in answer_normalized for phrase in _REFUSAL_PHRASES)

    # AIStudio_796 fix (b): keyword check on substantive content only.
    # Strip sentences containing refusal phrases before checking keywords —
    # prevents "no information about JPMorgan" from counting as a JPMorgan keyword hit.
    # AIStudio_828: normalize accents + hyphens before comparison.
    substantive_normalized = _normalize_text(_strip_refusal_context(data.get("answer") or ""))
    missing = [kw for kw in expected_keywords if _normalize_text(kw) not in substantive_normalized]
    keyword_pass = len(missing) == 0

    # AIStudio_813: citation density = citations / answer sentences.
    answer_sentences = max(1, len([s for s in answer.split(".") if s.strip()]))
    citation_density = round(len(citations) / answer_sentences, 3)
    low_density = citation_density < 0.1 and answer_sentences > 3

    # AIStudio_813: entity coverage = fraction of entity_filter tokens that appear
    # in at least one cited source filename. Catches "passes on keyword but wrong firm cited".
    # entity_filter tokens are source_path substrings (e.g. "JPMorgan", "Citigroup").
    # cited_sources are bare filenames. Match: any token in any filename (case-insensitive).
    if entity_filter and citations:
        cited_fnames = " ".join(c.get("source", "").split("/")[-1] for c in citations).lower()
        covered = sum(1 for token in entity_filter if token.lower() in cited_fnames)
        entity_coverage = round(covered / len(entity_filter), 2)
        entities_missing = [t for t in entity_filter if t.lower() not in cited_fnames]
    else:
        entity_coverage = None
        entities_missing = []

    # AIStudio_796 fix (a): explicit 0-citation guard — belt and suspenders.
    if not citation_pass:
        return {
            "pass": False,
            "rating": "RED",          # AIStudio_878: no citations → always RED
            "score": 0.0,
            "keyword_pass": keyword_pass,
            "citation_pass": False,
            "no_info_signal": no_info_signal,
            "missing_keywords": missing,
            "citation_count": 0,
            "citation_density": 0.0,
            "low_citation_density": False,
            "entity_coverage": entity_coverage,
            "entities_missing": entities_missing,
            "cited_sources": [],
        }

    # AIStudio_796 fix (c): no_info_signal only penalizes when citations are absent.
    # When the model has citations it found substantive content — hedging about
    # missing firms ("sources do not address Wells Fargo") is honest partial coverage,
    # not a failure. Only fire no_info_signal as a hard fail when citation_count == 0.
    effective_no_info = no_info_signal and not citation_pass

    # AIStudio_878 — amber rating + weighted score (keyword demoted from verdict to signal).
    _ec = entity_coverage if entity_coverage is not None else 1.0  # no filter active → neutral
    if (not citation_pass) or effective_no_info or (entity_coverage is not None and entity_coverage == 0.0):
        rating = "RED"
    elif keyword_pass and not low_density and _ec >= 0.5:
        rating = "GREEN"
    else:
        rating = "AMBER"
    score = round(max(0.0,
        0.45 * (1.0 if citation_pass else 0.0)
        + 0.25 * _ec
        + 0.15 * (1.0 if keyword_pass else 0.0)
        + 0.15 * (0.0 if low_density else 1.0)
        - (0.5 if effective_no_info else 0.0)), 3)

    return {
        "pass": keyword_pass and citation_pass and not effective_no_info,
        "rating": rating,
        "score": score,
        "keyword_pass": keyword_pass,
        "citation_pass": citation_pass,
        "no_info_signal": effective_no_info,
        "missing_keywords": missing,
        "citation_count": len(citations),
        "citation_density": citation_density,
        "low_citation_density": low_density,
        "entity_coverage": entity_coverage,
        "entities_missing": entities_missing,
        "cited_sources": [c.get("source", "").split("/")[-1] for c in citations],
    }


# ── Write BENCHMARK_FINDINGS.md ───────────────────────────────────────────────


def _file_sha8(path) -> str:
    """Short content hash of the question file — pins the exact set used (label-drift-proof)."""
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:8]
    except Exception:
        return "—"


def write_markdown(results: list[dict], args: argparse.Namespace, output_path: Path,
                   *, scope_firms: list[str] | None = None,
                   questions_label: str | None = None,
                   questions_sha: str | None = None) -> None:
    md_path = output_path.with_suffix(".md")
    passed = sum(1 for r in results if r["eval"]["pass"])
    total = len(results)
    avg_latency = sum(r["result"]["elapsed_sec"] for r in results if r["result"]["ok"]) / max(
        1, total
    )

    lines = [
        "# AIStudio — Benchmark Findings",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
        "## Configuration",
        f"- **Corpus:** `{args.corpus}`",
        f"- **Scope:** {(args.scope + f' — {len(scope_firms or [])} firm(s): ' + ', '.join(scope_firms or [])) if args.scope else 'none (full corpus)'}",
        f"- **Base Top K:** {args.top_k} (effective K may be higher for multi-entity queries)",
        f"- **Temperature:** {args.temperature}",
        *([ f"- **Alpha:** {args.alpha}" ] if args.alpha is not None else []),
        *([ f"- **Min Score:** {args.min_score}" ] if args.min_score is not None else []),
        f"- **Model:** {args.model or 'API default'}",
        f"- **API:** {args.api}",
        f"- **Questions:** `{questions_label or '(default)'}`" + (f" · sha `{questions_sha}`" if questions_sha and questions_sha != '—' else ''),
        "",
        "## Summary",
        f"- **Questions:** {total}",
        f"- **Passed (binary):** {passed}/{total} ({round(100 * passed / total)}%)",
        f"- **Rating (AIStudio_878):** 🟢 {sum(1 for r in results if r['eval'].get('rating')=='GREEN')} GREEN · 🟡 {sum(1 for r in results if r['eval'].get('rating')=='AMBER')} AMBER · 🔴 {sum(1 for r in results if r['eval'].get('rating')=='RED')} RED",
        f"- **Avg latency:** {round(avg_latency, 1)}s",
        "",
        "## Infrastructure",
        "- Vector store: Qdrant 1.17.0 (Apple Silicon, local)",
        "- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)",
        "- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2",
        f"- Corpus: `{args.corpus}` (see corpus stats in UI)",
        "",
        "## Results",
        "",
        "| # | Description | Latency | Pass | Citations | Notes |",
        "|---|-------------|---------|------|-----------|-------|",
    ]

    for i, r in enumerate(results, 1):
        q = r["question"]
        ev = r["eval"]
        res = r["result"]
        status = {"GREEN": "🟢", "AMBER": "🟡", "RED": "🔴"}.get(ev.get("rating"), "✅" if ev["pass"] else "❌")
        latency = f"{res['elapsed_sec']}s"
        cites = ", ".join(ev.get("cited_sources", []))[:40] or "—"
        _lang = q.get("language", "en")
        _lang_marker = " (*)" if _lang and _lang != "en" else ""
        _density_flag = " ⚠low-density" if ev.get("low_citation_density") else ""
        desc = q["description"] + _lang_marker
        lines.append(
            f"| {i} | {desc} | {latency} | {status} | {cites}{_density_flag} | {q.get('notes', '')} |"
        )

    lines += ["", "## Detailed Results", ""]

    for question_num, r in enumerate(results, 1):
        q = r["question"]
        ev = r["eval"]
        res = r["result"]
        _lang = q.get("language", "en")
        _lang_marker = " (*)" if _lang and _lang != "en" else ""
        lines += [
            "****",
            f"### {question_num}. {q['id']}{_lang_marker}",
            f"**Query:** {q['query']}",
            f"**Entity filter:** `{q.get('entity_filter') or 'none'}` | **Keywords sent:** `{q.get('keywords') or 'none'}`",
            f"**Retrieval query:** {res['data'].get('retrieval_query', q['query']) if res['ok'] else q['query']}",
            f"**Model:** `{res['data'].get('model_used', 'unknown') if res['ok'] else 'unknown'}` | **Latency:** {res['elapsed_sec']}s | **Pass:** {'✅' if ev['pass'] else '❌'} | **Citation density:** {ev.get('citation_density', '—')}{'  ⚠ low' if ev.get('low_citation_density') else ''}",
            "",
        ]
        if res["ok"]:
            answer = res["data"].get("answer", "")
            if args.full:
                display_answer = answer
            else:
                paragraphs = [p.strip() for p in answer.split("\n\n") if p.strip()]
                display_answer = "\n\n".join(paragraphs[:4])
                if len(paragraphs) > 4:
                    display_answer += "\n\n*[truncated — use --full for complete answer]*"
            lines += ["**Answer:**", ""]
            for line in display_answer.split("\n"):
                lines.append(f"> {line}" if line.strip() else ">")
            lines.append("")
        if res["ok"] and res["data"].get("citations"):
            lines += ["**Citations:**", ""]
            for c in res["data"].get("citations") or []:
                src = c.get("source", "").split("/")[-1]
                page = f" p.{c['page']}" if c.get("page") else ""
                lines.append(f"- [{c.get('index', '?')}] {src}{page}")
            lines.append("")
        if ev.get("missing_keywords"):
            lines.append(f"**Missing keywords:** {ev['missing_keywords']}")
        if ev.get("no_info_signal"):
            lines.append("**⚠ Model said 'no information' — possible retrieval miss**")
        if ev.get("low_citation_density"):
            lines.append(f"**⚠ Low citation density:** {ev['citation_density']} (correct answer, sparse attribution)")
        if ev.get("entity_coverage") is not None and ev["entity_coverage"] < 1.0:
            lines.append(f"**⚠ Entity coverage:** {ev['entity_coverage']} — uncited firms: {', '.join(ev.get('entities_missing', []))}")
        lines.append("")

    with open(md_path, "w") as f:
        f.write("\n".join(lines))
    # (No print here — the file is listed once, in the --- Reports section at the end.
    #  It used to print its own name mid-Summary, duplicating that listing.)


# ── Question filtering ────────────────────────────────────────────────────────


def filter_questions(
    questions: list[dict],
    *,
    topics: str | None,
    question_ids: str | None,
    lang_questions: list[str] | None,
) -> tuple[list[dict], list[str]]:
    """Filter questions by topics, question IDs, and/or question-language codes.

    All filters compose with AND. Returns (filtered_questions, applied_filter_descriptions).
    (v2.4.0: --subset/FIRM_SUBSETS removed — firm grouping is a --scope file now.
     --lang→--lang_questions: filters question_language, not the firm filing-language.)
    """
    applied: list[str] = []
    filtered = list(questions)

    # Filter by question IDs (most specific — apply first)
    if question_ids:
        wanted_ids = {qid.strip() for qid in question_ids.split(",") if qid.strip()}
        filtered = [q for q in filtered if q.get("id") in wanted_ids]
        applied.append(f"--question-ids ({len(wanted_ids)} IDs)")

    # Filter by the language the QUESTION is phrased in (question_language; default 'en').
    # NOT the firm filing-language — the EN/non-EN firm split is --scope's job.
    if lang_questions:
        wanted_langs = {lc.strip().lower() for lc in lang_questions if lc.strip()}
        filtered = [
            q for q in filtered
            if (q.get("question_language") or "en").lower() in wanted_langs
        ]
        applied.append(f"--lang-questions {' '.join(sorted(wanted_langs))}")

    # Filter by topics
    if topics:
        wanted_topics = {t.strip().lower() for t in topics.split(",") if t.strip()}
        filtered = [
            q for q in filtered
            if (q.get("topic", "") or q.get("notes", "")).lower() in wanted_topics
            or any(t in (q.get("topic", "") or q.get("notes", "")).lower() for t in wanted_topics)
        ]
        applied.append(f"--topics ({len(wanted_topics)} topics)")

    return filtered, applied


# ── Main ──────────────────────────────────────────────────────────────────────





def _installed_generative(api: str) -> list[dict]:
    """Every installed generative model, largest-footprint first, each annotated with its fit verdict.

    Superset of _fetch_fitting_models: this one keeps models that do NOT fit, because `smallest`
    is defined as the smallest INSTALLED model (the floor tier we want to measure), not the
    smallest that happens to fit right now.
    """
    try:
        import json as _json
        import urllib.request

        with urllib.request.urlopen(f"{api}/models", timeout=5) as resp:
            models = _json.loads(resp.read())
    except Exception:
        return []
    out = []
    for m in models:
        mid = m.get("id", "")
        if m.get("is_generative") is False or "embed" in mid.lower():
            continue
        fit = m.get("fit") or {}
        fp = fit.get("footprint_bytes") or 0
        out.append({"id": mid, "gb": (fp / 1e9 if fp else None), "verdict": fit.get("verdict")})
    out.sort(key=lambda x: (x["gb"] or 0), reverse=True)
    return out


def _resolve_batch_models(api: str, selector: str | None) -> list[str]:
    """Which model(s) a --batch invocation should run on. AIStudio_1040.

    None      → the 4x2 matrix: [smallest installed, largest that fits] (deduped if they coincide)
    'largest' → largest generative model that fits now
    'smallest'→ smallest INSTALLED generative model (deliberately not smallest-that-fits)
    <name>    → that model, verbatim; the existing per-run fit gate still applies
    """
    if selector and selector not in ("largest", "smallest"):
        return [selector]
    installed = _installed_generative(api)
    if not installed:
        return []
    fitting = [m for m in installed if m.get("verdict") in ("FIT", "WARN")]
    largest = fitting[0]["id"] if fitting else None
    smallest = installed[-1]["id"]
    if selector == "largest":
        return [largest] if largest else []
    if selector == "smallest":
        return [smallest]
    picks = [m for m in (smallest, largest) if m]
    return list(dict.fromkeys(picks))   # dedupe, preserve order


def _announce_runtime(n_runs: int, models: list[str], api: str) -> None:
    """Order-of-magnitude runtime estimate before committing hours. AIStudio_1040.

    ~10 s/question on a small model, ~60 s on a large one. Real spread is wide (retrieval size,
    thermal state, what else is resident), so this is announced as a RANGE (50-200%) and framed as
    an order of magnitude — the point is 'minutes or hours?', not a promise.
    """
    _sizes = {m["id"]: (m["gb"] or 0) for m in _installed_generative(api)}
    per_q = sum(60.0 if _sizes.get(m, 0) >= 9 else 10.0 for m in models) / max(len(models), 1)
    total_s = per_q * 10 * n_runs          # ~10 questions per run
    lo, hi = total_s * 0.5, total_s * 2.0

    def _fmt(sec: float) -> str:
        return f"{sec / 60:.0f} min" if sec < 5400 else f"{sec / 3600:.1f} h"

    print(f"• Estimated runtime: {_fmt(lo)}-{_fmt(hi)} (order of magnitude, ~10 questions/run).")


def run_canonical(args: argparse.Namespace) -> int:
    """Run the pinned canonical benchmark set (AIStudio_931).

    Reads benchmarks/batch/bench_canonical.yaml and executes each defined run via the
    normal single-run path (subprocess re-invocation of this script). Each sub-run
    writes its own report into benchmarks/<corpus>/reports/ under the standard
    benchmark_{corpus}_{model}_{timestamp}{filter_suffix} name (Naming STD §14) —
    nothing is renamed or copied. The canonical layer is pure orchestration: it only
    decides *which* runs execute. Returns a process exit code (0 = all runs ok).

    Ships safe: if the spec yaml is absent, prints guidance and returns 1 without side effects.
    """
    import subprocess

    import yaml

    script_dir = Path(__file__).resolve().parent
    # v2.8.1: canonical/batch spec relocated to benchmarks/batch/. Fall back to the legacy
    # flat benchmarks/bench_canonical.yaml so an un-migrated tree still runs.
    spec_path = script_dir / "batch" / "bench_canonical.yaml"
    if not spec_path.exists():
        legacy = script_dir / "bench_canonical.yaml"
        if legacy.exists():
            spec_path = legacy
    if not spec_path.exists():
        print(f"❌ Canonical spec not found: {spec_path}")
        print("   Create benchmarks/batch/bench_canonical.yaml (see TUTORIAL §5.9), then retry.")
        return 1

    spec = yaml.safe_load(spec_path.read_text()) or {}
    runs = spec.get("runs", []) or []
    default_model = spec.get("model")
    default_timeout = spec.get("timeout")   # AIStudio_941: top-level spec timeout default (mirrors default_model)

    if args.canonical_id is not None:
        runs = [r for r in runs if str(r.get("id")) == str(args.canonical_id)]
        if not runs:
            print(f"❌ No canonical run with id={args.canonical_id!r} in {spec_path.name}")
            return 1

    if not runs:
        print(f"❌ No runs defined in {spec_path.name}")
        return 1

    # AIStudio_1040 — model resolution.
    #   --canonical : reproduce EXACTLY (each run keeps its pinned model). Comparability path.
    #   --batch     : characterise THIS machine — bare = every run twice (smallest installed +
    #                 largest that fits); --model narrows it (name | largest | smallest).
    _sep("Batch")
    _exact = getattr(args, "canonical_exact", False)
    _batch_models: list[str] = []
    if not _exact:
        _batch_models = _resolve_batch_models(args.api, getattr(args, "model", None))
        if not _batch_models:
            print("❌ No generative model available to run the batch.")
            print("· Free memory, or install one:  ollama pull gemma3:4b")
            return 1
        _expanded = []
        for _r in runs:
            for _m in _batch_models:
                _rr = dict(_r)
                _rr["model"] = _m
                _rr["id"] = f"{_r.get('id', '?')}·{_m}"
                _expanded.append(_rr)
        runs = _expanded
        if len(_batch_models) == 1:
            _sel = getattr(args, "model", None)
            if _sel is None:
                print("• Smallest and largest resolve to the same model — running each set once.")
            print(f"• Model: {_batch_models[0]}")
        else:
            print(f"• Models: {' · '.join(_batch_models)}  (smallest installed + largest that fits)")

    # AIStudio_1012 — --dry-run: show the resolved run set and exit without executing the suite.
    if getattr(args, "dry_run", False):
        print(f"• dry-run — {len(runs)} run(s) resolved from {spec_path.name} (NOT executed):")
        for r in runs:
            _rid = r.get("id", "?")
            _m = r.get("model", default_model) or "API default"
            _bits = [f"corpus={r.get('corpus', '?')}", f"model={_m}"]
            if r.get("scope"):
                _bits.append(f"scope={r['scope']}")
            if r.get("questions"):
                _bits.append(f"questions={r['questions']}")
            if r.get("top_k") is not None:
                _bits.append(f"top_k={r['top_k']}")
            _t = r.get("timeout", default_timeout if default_timeout is not None else args.timeout)
            if _t is not None:
                _bits.append(f"timeout={_t}")
            print(f"  · {_rid}: " + "  ".join(_bits))
        if not _exact and _batch_models:
            _announce_runtime(len(runs), _batch_models, args.api)
        print(f"• {len(runs)} run(s) would execute → benchmarks/<corpus>/reports/. Re-run without --dry-run to execute.")
        return 0

    print(f"• batch — {len(runs)} run(s) → benchmarks/<corpus>/reports/")
    if not _exact and _batch_models:
        _announce_runtime(len(runs), _batch_models, args.api)

    failures = 0
    skipped = 0
    for r in runs:
        rid = r.get("id", "?")
        corpus = r.get("corpus")
        if not corpus:
            print(f"  ❌ run {rid}: missing 'corpus' — skipped")
            failures += 1
            continue
        model = r.get("model", default_model)

        # AIStudio_1020: memory-fit gate per run. The PARENT owns the decision (skip / downshift /
        # force / confirm) so the run is resolved once; the child then runs the resolved model with
        # --fit-policy force so it does not re-evaluate or re-prompt.
        if model:
            _fit_action, _fit_model = _resolve_fit_policy(args.api, str(model), args.fit_policy, context=f"run {rid}")
            if _fit_action == "skip":
                print(f"  ⚠ run {rid}: SKIPPED — {model} won't fit this machine (--fit-policy).", file=sys.stderr)
                skipped += 1
                continue
            model = _fit_model

        # Build the single-run argv — reuses the full single-run path verbatim.
        argv = [sys.executable, str(Path(__file__).resolve()), "--corpus", str(corpus)]
        if model:
            argv += ["--model", str(model)]
            argv += ["--fit-policy", "force"]  # AIStudio_1020: parent already applied the policy — child must not re-gate
        if r.get("top_k") is not None:
            argv += ["--top-k", str(r["top_k"])]
        if r.get("questions"):
            argv += ["--questions", str(r["questions"])]
        if r.get("scope"):
            argv += ["--scope", str(r["scope"])]
        if r.get("alpha") is not None:
            argv += ["--alpha", str(r["alpha"])]
        if r.get("min_score") is not None:
            argv += ["--min-score", str(r["min_score"])]
        # AIStudio_940/_941: propagate timeout to sub-runs. A bigger num_ctx (_958) slows generation, so
        # the 120s default can time out heavy multi-firm questions → HTTP failure → mechanical fail
        # (the likely cause of the Run C/D drop). Resolution mirrors model:: per-run spec `timeout:` wins,
        # else the top-level spec `timeout:`, else the parent invocation's --timeout (default 120) — so a
        # canonical run carries its own timeout without needing --timeout 300 on every invocation.
        _run_timeout = r.get("timeout", default_timeout if default_timeout is not None else args.timeout)
        if _run_timeout is not None:
            argv += ["--timeout", str(_run_timeout)]

        print(f"\n\033[1m▶ canonical {rid}: {r.get('label', corpus)}\033[0m")
        print("    " + " ".join(argv[2:]))
        # AIS_BENCH_CHILD=1 → child suppresses its own header (▶ banner IDs the run);
        # env spread inherits the parent's PYTHONPATH/venv. Output streams through.
        result = subprocess.run(argv, env={**os.environ, "AIS_BENCH_CHILD": "1"})
        if result.returncode != 0:
            print(f"  ❌ run {rid} failed (exit {result.returncode})")
            failures += 1
            continue
        print(f"  ✅ {rid} done → benchmarks/{corpus}/reports/")

    ok = len(runs) - failures - skipped
    mark = "✅" if failures == 0 else "⚠"
    _skip_note = f", {skipped} skipped (won't fit)" if skipped else ""
    print(f"\n{mark} batch: {ok}/{len(runs)} run(s) ok{_skip_note} → benchmarks/<corpus>/reports/")
    return 1 if failures else 0


# ── AIStudio_1020: memory-fit policy for bench runs ──────────────────────────────────────────
# bench asks the API's /models for the model's fit verdict (the ONE guard policy lives in
# app/model_fit.py — bench never re-derives the threshold) and applies --fit-policy. All advisory
# output goes to stderr so a `... | tee report.md` capture stays clean (CLI-Output STD precedent).
def _fetch_model_fit(api: str, model: str) -> dict | None:
    """The server-computed fit verdict {verdict, recommendation, reason} for `model`, or None when
    the API is unreachable / the model isn't listed / fit wasn't evaluated (guard then no-ops)."""
    if not model:
        return None
    try:
        import json as _json
        import urllib.request

        with urllib.request.urlopen(f"{api}/models", timeout=5) as resp:
            models = _json.loads(resp.read())
        for m in models:
            if m.get("id") == model:
                return m.get("fit")
    except Exception:
        return None
    return None


def _fetch_fitting_models(api: str, exclude: str = "") -> list[dict]:
    """Generative models that currently FIT (or WARN) this machine, largest-footprint first —
    the candidate set for the fit gate's downgrade picker. Each dict: {id, gb}. Embedding-only
    models and the too-big model itself (`exclude`) are omitted. [] on any API failure."""
    try:
        import json as _json
        import urllib.request

        with urllib.request.urlopen(f"{api}/models", timeout=5) as resp:
            models = _json.loads(resp.read())
    except Exception:
        return []
    out = []
    for m in models:
        mid = m.get("id", "")
        if mid == exclude or m.get("is_generative") is False or "embed" in mid.lower():
            continue
        fit = m.get("fit") or {}
        if fit.get("verdict") in ("FIT", "WARN"):
            fp = fit.get("footprint_bytes") or 0
            out.append({"id": mid, "gb": fp / 1e9 if fp else None})
    out.sort(key=lambda x: (x["gb"] or 0), reverse=True)  # largest-fitting-first
    return out


def _free_memory_pct() -> float | None:
    """System-wide free memory as a percentage, or None when unavailable.

    AIStudio_1037 instrumentation. Reads macOS `memory_pressure` — the SAME source the API's
    fit guard uses (api._available_memory_bytes), so the number printed here is the number the
    guard will decide on. Deliberately NOT psutil: psutil.available under-reports ~2.5x on
    macOS, which is the bug that made the guard false-block in the first place.

    Cheap enough to call per question (one subprocess, ~10ms). Returns None off-macOS or on any
    failure — instrumentation must never break a benchmark run.
    """
    try:
        out = subprocess.run(
            ["memory_pressure"], capture_output=True, text=True, timeout=5
        ).stdout
        m = re.search(r"free percentage:\s*(\d+)%", out, re.IGNORECASE)
        return float(m.group(1)) if m else None
    except Exception:
        return None


_QUESTIONS_NOTE: list[str] = []   # deferred note, rendered under ▶ Checking questions...


def _preflight_corpus(corpus: str) -> None:
    """Corpus + questions-file checks, INSIDE the Preflight section.

    These used to live in the wrapper (ais_bench.sh), which meant a failure aborted before
    bench.py ever ran — so the identity banner never printed, violating CLI-Output STD §2
    ("the very first line, unconditionally"). Owning them here keeps one banner, one
    Preflight section, and gives failures the same ❌ + guidance treatment as any other check.
    """
    repo = Path(__file__).resolve().parent.parent
    print("▶ Checking corpus...")
    uploads = repo / "data" / "corpora" / corpus / "uploads"
    if not uploads.is_dir():
        print(f"  ❌ Corpus '{corpus}' has no uploads/ directory — not yet ingested.", file=sys.stderr)
        print("  · Ingest documents first via the UI, then re-run.", file=sys.stderr)
        print("  · Usage: ais_bench --corpus <name> [--model <name>]  ·  ais_bench --help for all options", file=sys.stderr)
        sys.exit(1)
    docs = [f for f in uploads.iterdir() if f.is_file() and not f.name.startswith(".")]
    if not docs:
        print(f"  ❌ Corpus '{corpus}' has no documents in uploads/.", file=sys.stderr)
        print("  · Ingest documents first via the UI or an ais_ingest_* command.", file=sys.stderr)
        sys.exit(1)
    qfile = repo / "benchmarks" / corpus / f"{corpus}_questions.yaml"
    if not qfile.is_file():
        print(f"  ❌ No questions file for corpus '{corpus}'.", file=sys.stderr)
        print(f"  · Expected: benchmarks/{corpus}/{corpus}_questions.yaml", file=sys.stderr)
        _avail = sorted({p.parent.name for p in (repo / "benchmarks").glob("**/*_questions.yaml")})
        if _avail:
            print(f"  · Corpora with question sets: {', '.join(_avail)}", file=sys.stderr)
        sys.exit(1)
    print(f"  ✅ {corpus} ready — {len(docs)} document(s).")


def _fit_err(msg: str) -> None:
    print(f"❌ {msg}.", file=sys.stderr)


def _fit_warn(msg: str) -> None:
    print(f"⚠ {msg}.", file=sys.stderr)


def _fit_info(msg: str) -> None:
    print(f"ℹ {msg}", file=sys.stderr)


def _resolve_fit_policy(api: str, model: str, policy: str | None, *, context: str = "") -> tuple[str, str | None]:
    """Decide whether/how a run proceeds given its model's fit verdict and --fit-policy.

    Returns (action, effective_model): action 'run' → proceed (model may be a downshift substitute);
    action 'skip' → do not run this one. Only BLOCK triggers policy/gate; FIT/unknown → run; WARN →
    run with an advisory. Absent policy + BLOCK → [YES/n] gate on stdin; no terminal → fail closed.

    Output conforms to STD - AIStudio - CLI Output §2 (Activity Bundles): a `--- Preflight` section
    label, a `▶` action line, then `⚠`/`·`/`ℹ`/`❌` detail lines under it.
    """
    # --- Preflight  (section label per CLI Output STD §2). The wrapper (ais_bench.sh v1.10.0)
    # runs the corpus/questions checks SILENTLY and exports the resolved facts, so this single
    # section owns the whole preflight rather than the wrapper printing a competing one before
    # the identity banner.
    print(f"▶ Checking model fit ({model} vs available memory)...")
    fit = _fetch_model_fit(api, model)
    verdict = (fit or {}).get("verdict")
    if verdict == "WARN":
        _fit_warn(f"{model} is a tight fit for this machine's memory{(' (' + context + ')') if context else ''}; may slow or swap")
        return ("run", model)
    if verdict != "BLOCK":
        print(f"  ✅ {model} fits.")
        return ("run", model)  # FIT or unknown — fail-open; the API's own /ask preflight still backstops

    rec = (fit or {}).get("recommendation")
    reason = ((fit or {}).get("reason") or "won't fit this machine's memory").rstrip(".")
    label = f"{model}{(' [' + context + ']') if context else ''}"

    if policy == "force":
        _fit_warn(f"{label} {reason}; --fit-policy force → running anyway (may hang)")
        return ("run", model)
    if policy == "skip":
        _fit_warn(f"{label} {reason}; --fit-policy skip → SKIPPED")
        return ("skip", None)
    if policy == "downshift":
        if rec:
            _fit_info(f"{label} {reason}; --fit-policy downshift → running on {rec} instead")
            return ("run", rec)
        _fit_warn(f"{label} {reason}, and no smaller model fits; --fit-policy downshift → SKIPPED")
        return ("skip", None)

    # policy is None → interactive gate. Needs a terminal to answer.
    # The form depends on how many OTHER models currently fit (STD §10.3):
    #   0 fit  → dead-end: free memory / Tutorial / restart
    #   1 fit  → lettered inline: (r)un <model>, (f)ree memory & restart, (Enter) cancel
    #   ≥2 fit → uniform numbered list: 1..N models (largest-first) + Free-memory + Cancel
    # A "retry" that needs the operator to free memory does NOT re-poll in-process — it directs
    # to ais_restart (state change realized by the restart, not a racing live poll). STD §10.5.
    if not sys.stdin.isatty():
        _fit_warn(f"{label} {reason}, and --fit-policy was not set")
        _fit_err("no terminal to confirm — pass --fit-policy {skip,downshift,force} for non-interactive runs")
        sys.exit(1)

    fitting = _fetch_fitting_models(api, exclude=model)

    # Reply helpers shared by both forms (STD §10.5).
    def _reply_run(chosen: str) -> tuple[str, str]:
        print(f"  \u00b7 Running on {chosen}...", file=sys.stderr)
        return ("run", chosen)

    def _reply_free_and_stop() -> None:
        print('  \u00b7 Close the apps you don\'t need, then run: ais_restart in Terminal '
              '(Cmd+Space \u2192 "Terminal") before choosing a model.', file=sys.stderr)
        _fit_err("Stopped — no benchmark run.")
        sys.exit(1)

    def _reply_cancel() -> None:
        _fit_err("Stopped — no benchmark run.")
        sys.exit(1)

    # 0 fit → dead-end.
    if not fitting:
        _fit_warn(f"{label} {reason}")
        _fit_err("No model fits this machine right now")
        print("  \u00b7 Free memory (close other apps), or see the Tutorial (Module 2.5) for options.", file=sys.stderr)
        print("  \u00b7 Then restart: ais_start", file=sys.stderr)
        sys.exit(1)

    _fit_warn(f"{label} {reason}")

    # 1 fit → lettered inline (STD §10.3-A).
    if len(fitting) == 1:
        only = fitting[0]
        gb = f" (~{only['gb']:.0f} GB)" if only["gb"] else ""
        reprompted = False
        while True:
            print(f"  (r)un {only['id']}{gb}, (f)ree memory & restart, (Enter) cancel \u276f ",
                  file=sys.stderr, end="")
            try:
                ans = input().strip().lower()
            except EOFError:
                ans = ""
            if ans == "r":
                return _reply_run(only["id"])
            if ans == "f":
                _reply_free_and_stop()
            if ans == "":
                _reply_cancel()
            if not reprompted:
                print("  \u00b7 didn't catch that — enter r, f, or press Enter to cancel", file=sys.stderr)
                reprompted = True
                continue
            _reply_cancel()

    # ≥2 fit → uniform numbered list (STD §10.3-D).
    n = len(fitting)
    free_idx = n + 1   # "Free memory & restart"
    cancel_idx = n + 2  # "Cancel"
    total = n + 2
    reprompted = False
    while True:
        print(f"  Choose an option [1-{total}], or (Enter) to cancel:", file=sys.stderr)
        for i, m in enumerate(fitting, start=1):
            gb = f"(~{m['gb']:.0f} GB)" if m["gb"] else ""
            print(f"    {i}. {m['id']:<14} {gb:<10} run on this", file=sys.stderr)
        print(f"    {free_idx}. Free memory & restart", file=sys.stderr)
        print(f"    {cancel_idx}. Cancel", file=sys.stderr)
        print("  \u276f ", file=sys.stderr, end="")
        try:
            ans = input().strip()
        except EOFError:
            ans = ""
        if ans == "":
            _reply_cancel()
        if ans.isdigit():
            choice = int(ans)
            if 1 <= choice <= n:
                return _reply_run(fitting[choice - 1]["id"])
            if choice == free_idx:
                _reply_free_and_stop()
            if choice == cancel_idx:
                _reply_cancel()
        if not reprompted:
            print(f"  \u00b7 didn't catch that — enter 1-{total}, or press Enter to cancel", file=sys.stderr)
            reprompted = True
            continue
        _reply_cancel()


def main() -> None:
    args = parse_args()
    # Child runs spawned by run_canonical suppress their own header (the parent
    # already printed one + the ▶ banner IDs each run); see AIS_BENCH_CHILD below.
    if not os.environ.get("AIS_BENCH_CHILD"):
        print(f"\033[1m[ais_bench v{VERSION} — AIStudio RAG Benchmark]\033[0m")

    # --- Preflight opens HERE, unconditionally. It used to live inside _resolve_fit_policy(),
    # which only runs when --model is given — so `ais_bench --corpus nonexistent` skipped every
    # check and happily benchmarked 8 default questions against a corpus that does not exist.
    _is_batch = (getattr(args, "canonical", False) or getattr(args, "canonical_exact", False)
                 or getattr(args, "canonical_id", None) is not None)
    if not _is_batch and not os.environ.get("AIS_BENCH_CHILD"):
        _sep("Preflight")
        _preflight_corpus(getattr(args, "corpus", None) or "demo")

    # AIStudio_931 — canonical/batch mode short-circuits the single-run path.
    # A2 (2026-07-05): --batch-id alone must also trigger it. --batch-id sets
    # `canonical_id` (a different dest than --batch's `canonical`), so `ais_bench
    # --batch-id D` without --batch used to fall through to a single run on the
    # DEFAULT corpus (demo) — a silent-wrong-result trap. Trigger on either.
    if (getattr(args, "canonical", False) or getattr(args, "canonical_exact", False)
            or getattr(args, "canonical_id", None) is not None):
        raise SystemExit(run_canonical(args))

    # AIStudio_1012: --dry-run only previews a --batch run set. Without --batch there is nothing to
    # preview, and silently executing a single run would defeat the flag — stop with a notice instead.
    if getattr(args, "dry_run", False):
        print("⚠ --dry-run applies to --batch (it previews the resolved run set). Add --batch, or drop --dry-run to run a single job.", file=sys.stderr)
        return

    # ── Scope (AIStudio_882): load + validate the firm-universe up front ─────────
    # --scope names a firm subset; the resolver hard-errors on a missing named scope
    # (never a silent fallback). We surface the firm-token universe here. Applying it as
    # a retrieval source_path restriction is the paired sub-step (the --scope ↔ /ask
    # firm-allowlist mechanism, deferred per design #3). --scope does NOT filter questions.
    scope_firms: list[str] = []
    scope_tokens: list[str] = []
    if args.scope:
        _stem = args.scope
        if _stem.startswith(args.corpus + "_"):
            _stem = _stem[len(args.corpus) + 1:]  # tolerate a corpus-prefixed stem
        try:
            _rows = _scope.load_entities(args.corpus, _stem)
        except _scope.ScopeError as e:
            print(f"❌ --scope {args.scope!r} could not be resolved:\n{e}")
            sys.exit(2)
        scope_firms = [n for n in (_scope.entity_name(r) for r in _rows) if n]
        scope_tokens = [f.replace(" ", "_") for f in scope_firms]
        print(f"· --scope {args.scope} → {len(scope_firms)} firm(s): {', '.join(scope_firms)}")
        # AIStudio_882 (scope application): scope_tokens ride the /ask `allowed_source_paths`
        # field — the server ANDs them with each question's entity logic (intersect). An
        # out-of-scope question retrieves nothing; a scope-only run retrieves across the scope.

    # ── Fetch corpus metadata defaults ───────────────────────────────────────
    # Apply corpus metadata defaults for params not explicitly set via CLI.
    # CLI flag → corpus metadata default → hardcoded fallback.
    try:
        import urllib.request
        info_url = f"{args.api}/corpus/{args.corpus}/info"
        with urllib.request.urlopen(info_url, timeout=5) as resp:
            _info = __import__("json").loads(resp.read())
        _corpus_top_k = _info.get("default_top_k")
        _corpus_temp  = _info.get("default_temperature")
        _corpus_alpha = _info.get("default_hybrid_alpha")
        _corpus_min   = _info.get("default_min_score")
    except Exception:
        _corpus_top_k = _corpus_temp = _corpus_alpha = _corpus_min = None

    if args.top_k is None:
        args.top_k = _corpus_top_k if _corpus_top_k is not None else 5
    if args.temperature is None:
        args.temperature = _corpus_temp if _corpus_temp is not None else 0.3
    if args.alpha is None and _corpus_alpha is not None:
        args.alpha = _corpus_alpha
    if args.min_score is None and _corpus_min is not None:
        args.min_score = _corpus_min

    # AIStudio_1020: memory-fit gate for this single run. Only when an explicit --model was given
    # (a default-model run is backstopped by the API's own /ask preflight). May skip the run or
    # downshift args.model to a model that fits. Emits its own `--- Preflight` bundle (CLI Output §2).
    if args.model:
        # (No separator print here: Preflight is now one unified section opened in main(), so the
        #  blank line this used to emit orphaned itself in the middle of the checks.)
        _fit_action, _fit_model = _resolve_fit_policy(args.api, args.model, args.fit_policy)
        if _fit_action == "skip":
            return  # skip reason already printed under --- Preflight by _resolve_fit_policy
        args.model = _fit_model

    # Resolve paths — output to benchmarks/{corpus}/reports/ with timestamp
    script_dir = Path(__file__).parent
    reports_dir = script_dir / args.corpus / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    # STD - General - Naming Conventions: time component is HHMM (no hyphen)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")

    # Model slug for filename — shorten to filesystem-safe form
    # e.g. "gemma3:27b" → "gemma3-27b", "llama3.1:8b" → "llama3.1-8b", None → "default"
    _model_raw = args.model or "default"
    _model_slug = _model_raw.replace(":", "-").replace("/", "-")[:20]

    # Build filter suffix for filename so scope/lang/ablation runs are distinguishable
    # Descriptor ordering: LEAST-VOLATILE FIRST (Naming STD §2). Fields that rarely
    # change for a corpus lead; the dial you sweep most (top_k) sits last, just before
    # the timestamp. Order: questions → scope → question sub-selectors → ablations → top_k.
    filter_parts = []
    # questions: the named set/stem (the default set is unlabelled, so a baseline run
    # stays clean and a non-default set self-identifies in the filename).
    if args.questions and "/" not in str(args.questions) and "\\" not in str(args.questions):
        _q_stem = str(args.questions).strip().lower().replace(" ", "_")[:24]
        filter_parts.append(_q_stem)
    if args.scope:
        filter_parts.append(args.scope)
    if args.topics:
        first_topic = args.topics.split(",")[0].strip().lower().replace(" ", "_").replace("&", "and")[:20]
        filter_parts.append(f"topics_{first_topic}")
    if args.question_ids:
        filter_parts.append("qids")
    if args.lang_questions:
        filter_parts.append("langq_" + "_".join(sorted(args.lang_questions)))
    # Ablation markers — keep entity/keyword-ablated runs distinguishable in report names
    if args.entity_filter_mode != "auto":
        filter_parts.append(f"ef-{args.entity_filter_mode}")
    if args.keywords == "off":
        filter_parts.append("kwoff")
    # Top-K descriptor (Naming STD §14: fields that describe the report). Most-swept dial
    # → last before the timestamp. Makes runs differing only by K distinguishable.
    filter_parts.append(f"top_k{args.top_k}")
    filter_suffix = ("_" + "_".join(filter_parts)) if filter_parts else ""

    # Naming STD §2: datetime is ALWAYS the last field, after all descriptors.
    # base_name = benchmark_{corpus}_{model}_{descriptors}_{timestamp}
    base_name = f"benchmark_{args.corpus}_{_model_slug}{filter_suffix}_{timestamp}"
    output_path = reports_dir / f"{base_name}.json"
    questions_path = args.questions

    # Preflight header printed by ais_bench.sh shell wrapper

    questions = load_questions(questions_path, corpus=args.corpus)
    questions_label = (
        str(questions_path)
        if questions_path
        else f"benchmarks/{args.corpus}/{args.corpus}_questions.yaml"
    )
    questions_sha = _file_sha8(questions_label)
    total_loaded = len(questions)

    # Apply filters
    if args.topics or args.question_ids or args.lang_questions:
        questions, applied_filters = filter_questions(
            questions,
            topics=args.topics,
            question_ids=args.question_ids,
            lang_questions=args.lang_questions,
        )
        if not questions:
            print(f"❌ No questions matched filters: {', '.join(applied_filters)}")
            print(f"   Loaded {total_loaded} from {questions_label}, filtered to 0.")
            return
        print("▶ Checking questions...")
        for _n in _QUESTIONS_NOTE:
            print(f"  · {_n}")
        print(f"  ✅ {len(questions)} of {total_loaded} loaded after filters.")
        _q_filter_note = f"{questions_label} ({', '.join(applied_filters)})"
    else:
        print("▶ Checking questions...")
        for _n in _QUESTIONS_NOTE:
            print(f"  · {_n}")
        print(f"  ✅ {len(questions)} loaded.")
        _q_filter_note = str(questions_label)

    model_label = args.model if args.model else "API default (llama3.1:8b)"
    # --- Input Parameters (after Preflight: only worth printing for a run that will happen)
    _sep("Input Parameters")
    _params: list[tuple[str, str]] = [
        ("Questions", _q_filter_note),
        ("Corpus", str(args.corpus)),
        ("Model", model_label),
        ("Top K", str(args.top_k)),
        ("Temperature", str(args.temperature)),
    ]
    if args.alpha is not None:
        _params.append(("Alpha", str(args.alpha)))
    if args.min_score is not None:
        _params.append(("Min Score", str(args.min_score)))
    if args.scope:
        _params.append(("Scope", f"{args.scope} ({len(scope_firms)} firms)"))
    _params += [
        ("Query-expansion", "on" if args.query_expansion else "off"),
        ("Entity-filter", str(args.entity_filter_mode)),
        ("Keywords", str(args.keywords)),
    ]
    _w = max(len(k) for k, _ in _params)
    for _k, _v in _params:
        print(f"• {_k.ljust(_w)} : {_v}")

    # --- Firm override message
    if args.firm:
        print(f"• --firm '{args.firm}' active — applied to all queries (overriding YAML firm fields)")

    # --- Running
    _sep("Running")

    results = []
    for i, q in enumerate(questions, 1):
        corpus = q.get("corpus") or args.corpus
        # CLI --firm overrides per-question firm field; otherwise use YAML's firm
        effective_firm = args.firm if args.firm else q.get("firm")
        print(f"▶ [{i}/{len(questions)}] {q['description']}...")
        _mem_before = _free_memory_pct()  # AIStudio_1037

        # AIStudio_875: --query-expansion and --entity-filter map directly to server request
        # fields. --entity-filter yaml forwards the question's entity_filter; none/auto leave it
        # to the server (auto self-populates from detected entities). hybrid_alpha enables the
        # hybrid path the server expansion uses.
        # v2.4.0: --keywords off suppresses the (independent) BM25 keyword channel — the
        # keyword-channel ablation (old no_keyword_hint).
        _q_ef = q.get("entity_filter") or None
        _q_kw = (q.get("keywords") or None) if args.keywords == "on" else None
        _mode = args.entity_filter_mode
        # yaml → hand-feed the question's entity_filter; none/auto → server decides (auto self-populates)
        _eff_ef = _q_ef if _mode == "yaml" else None
        _eff_alpha = args.alpha if args.alpha is not None else 0.5  # hybrid on so expansion/BM25 fire

        result = run_query(
            api=args.api,
            query=q.get("query") or q.get("question", ""),
            corpus=corpus,
            top_k=args.top_k,
            temperature=args.temperature,
            model=args.model,
            firm=effective_firm,
            year=q.get("year"),
            hybrid_alpha=_eff_alpha,
            min_score=args.min_score,
            entity_filter=_eff_ef,
            allowed_source_paths=scope_tokens or None,
            keywords=_q_kw,
            query_expansion=args.query_expansion,
            entity_filter_mode=_mode,
            timeout=args.timeout,
        )

        ev = evaluate(result, q.get("expected_keywords", []) or q.get("keywords", []),
                      entity_filter=_eff_ef)
        status = {"GREEN": "🟢", "AMBER": "🟡", "RED": "🔴"}.get(ev.get("rating"), "✅" if ev["pass"] else "❌")
        _lang = q.get("language", "en")
        _lang_marker = " (*)" if _lang and _lang != "en" else ""
        _missing_str = f" | missing: {', '.join(ev['missing_keywords'])}" if ev.get("missing_keywords") else ""
        _density_str = f" | density: {ev['citation_density']}⚠" if ev.get("low_citation_density") else ""
        # AIStudio_1037: memory at question boundaries — the curve that reveals sweep starvation.
        _mem_after = _free_memory_pct()
        _mem_str = ""
        if not getattr(args, "mem_track", True):
            _mem_before = _mem_before  # still recorded to JSON, just not displayed
        elif _mem_before is not None and _mem_after is not None:
            _arrow = "→" if _mem_after != _mem_before else "="
            _mem_str = f" | mem {_mem_before:.0f}%{_arrow}{_mem_after:.0f}%"
        elif getattr(args, "mem_track", True) and _mem_after is not None:
            _mem_str = f" | mem {_mem_after:.0f}%"
        print(
            f"  {status} {result['elapsed_sec']}s | {ev['citation_count']} citation(s){_missing_str}{_density_str}{_lang_marker}{_mem_str}"
        )

        # AIStudio_841: --verbose and --super-verbose output
        _verbose = getattr(args, 'verbose', False) or getattr(args, 'super_verbose', False)
        _super = getattr(args, 'super_verbose', False)
        if _verbose and result["ok"]:
            _data = result["data"]
            _ef = _eff_ef or []  # AIStudio_867: show what was actually sent, not the YAML value
            _chunks = _data.get("chunks_retrieved", "?")
            _first_src = ""
            if (_data.get("citations") or []):
                _first_src = (_data["citations"][0].get("source") or "").split("/")[-1]
            _diff = q.get("difficulty") or ""
            _aloc = q.get("answer_location") or ""
            _meta = f" | difficulty: {_diff}" if _diff else ""
            _meta += f" | answer_loc: {_aloc}" if _aloc else ""
            print(f"    · chunks_retrieved: {_chunks} | entity_filter: {_ef or 'none'} | first_source: {_first_src or 'none'}{_meta}")
        if _super and result["ok"]:
            _data = result["data"]
            _rq = _data.get("retrieval_query") or q.get("query", "")
            _model = _data.get("model_used", "?")
            _kw = _q_kw or []   # effective sent keywords (always forwarded)
            _ef = _eff_ef or []   # AIStudio_867: effective sent entity_filter
            print(f"    · original_query:   {q.get('query', '')[:100]}")
            print(f"    · retrieval_query:  {_rq[:100]}")
            print(f"    · entity_tokens:    {_ef}")
            print(f"    · keywords_sent:    {_kw}")
            print(f"    · model_used:       {_model}")
            _ans = (_data.get("answer") or "").strip()
            print(f"    · answer:           {_ans[:200]}{'...' if len(_ans) > 200 else ''}")

        results.append({"question": q, "result": result, "eval": ev,
                        "memory": {"free_pct_before": _mem_before,  # AIStudio_1037
                                   "free_pct_after": _mem_after}})

    # Summary
    passed = sum(1 for r in results if r["eval"]["pass"])
    total = len(results)
    avg_latency = sum(r["result"]["elapsed_sec"] for r in results if r["result"]["ok"]) / max(
        1, total
    )

    _sep("Summary")
    _greens = sum(1 for r in results if r["eval"].get("rating") == "GREEN")
    _ambers = sum(1 for r in results if r["eval"].get("rating") == "AMBER")
    _reds = sum(1 for r in results if r["eval"].get("rating") == "RED")
    print(f"• {passed}/{total} passed (binary test) | 🟢 {_greens}  🟡 {_ambers}  🔴 {_reds} | avg latency: {round(avg_latency, 1)}s")

    # AIStudio_1037: sweep memory drift — the headline diagnostic for self-starvation.
    # A sweep should hold memory roughly constant; a monotonic slide means per-question working
    # memory (KV cache / retrieval context) is not being released, and on a constrained box the
    # /ask fit guard will start BLOCKing the tail of the run (0.02s + 0 citations).
    # The FIRST question's drop is dominated by loading the model into memory (a one-time cost,
    # e.g. ~5 points for an 8B on 128GB), which is NOT accumulation. Report it separately and
    # measure drift from the post-load steady state (after Q1) so the warning tracks the real
    # signal — memory that keeps sliding once the model is already resident.
    _mem_pts = [(r.get("memory") or {}).get("free_pct_after") for r in results]
    _mem_pts = [m for m in _mem_pts if m is not None]
    _mem_pre = (results[0].get("memory") or {}).get("free_pct_before") if results else None
    if _mem_pts:
        _mem_end = _mem_pts[-1]
        _load_cost = (_mem_pre - _mem_pts[0]) if _mem_pre is not None else None
        _steady = _mem_pts[0]
        _drift = _mem_end - _steady          # post-load drift — the accumulation signal
        _n_after = max(len(_mem_pts) - 1, 0)  # questions measured after the load
        _flag = ""
        if _n_after >= 2 and _drift <= -10:
            _flag = "  ⚠ memory keeps sliding after load — suspect sweep accumulation (AIStudio_1037)"
        elif _mem_end <= 25:
            _flag = "  ⚠ low headroom at run end — later questions may have been fit-guard BLOCKED"
        _load_str = f"load {_load_cost:+.0f} · " if _load_cost is not None else ""
        # The LOWEST point matters more than the end value: a transient dip is what actually trips
        # the fit guard mid-sweep, and it can recover before the run finishes.
        _low = min(_mem_pts)
        _low_str = f" · low {_low:.0f}%" if _low < _steady else ""
        print(
            f"• memory: {_load_str}steady {_steady:.0f}% → {_mem_end:.0f}% at end{_low_str} "
            f"({_drift:+.0f} points over {_n_after} question(s) after load){_flag}"
        )
    for r in results:
        status = {"GREEN": "🟢", "AMBER": "🟡", "RED": "🔴"}.get(r["eval"].get("rating"), "✅" if r["eval"]["pass"] else "❌")
        _lang = r["question"].get("language", "en")
        _lang_marker = " (*)" if _lang and _lang != "en" else ""
        print(f"  {status} {r['question']['id']}{_lang_marker}")
        if r["eval"].get("no_info_signal"):
            print(
                f"  ⚠ {r['question']['id']}: model said 'no information' — possible retrieval miss."
            )
        if r["eval"].get("low_citation_density"):
            print(
                f"  ⚠ {r['question']['id']}: low citation density ({r['eval']['citation_density']}) — correct answer, sparse attribution."
            )
        if r["eval"].get("entity_coverage") is not None and r["eval"]["entity_coverage"] < 1.0:
            missing_e = r["eval"].get("entities_missing", [])
            print(
                f"  ⚠ {r['question']['id']}: entity coverage {r['eval']['entity_coverage']} — uncited: {', '.join(missing_e)}"
            )

    # Write JSON results
    with open(output_path, "w") as f:
        json.dump(
            {
                "run_at": datetime.now().isoformat(),
                "config": {
                    "corpus": args.corpus,
                    "scope": args.scope,
                    "scope_firms": scope_firms,
                    "top_k": args.top_k,
                    "temperature": args.temperature,
                    "alpha": args.alpha,
                    "min_score": args.min_score,
                    "model": args.model,
                    "api": args.api,
                    "questions_file": questions_label,
                    "questions_sha8": questions_sha,
                },
                "summary": {
                    "total": total,
                    "passed": passed,
                    "avg_latency_sec": round(avg_latency, 2),
                },
                "results": results,
            },
            f,
            indent=2,
        )

    # Write markdown
    _wm_kwargs = dict(scope_firms=scope_firms, questions_label=questions_label, questions_sha=questions_sha)
    if not args.no_markdown:
        write_markdown(results, args, output_path, **_wm_kwargs)

    _pdf_note: list[str] = []   # (c) deferred, non-nagging PDF notes — surfaced in --- Reports
    # Write PDF via pandoc (always attempted)
    if args.no_markdown:
        write_markdown(results, args, output_path, **_wm_kwargs)
    md_path = output_path.with_suffix(".md")
    pdf_path = output_path.with_suffix(".pdf")
    html_path = output_path.with_suffix(".html")
    import subprocess

    try:
        r1 = subprocess.run(
            ["pandoc", str(md_path), "-o", str(html_path), "--standalone"],
            capture_output=True,
            text=True,
        )
        if r1.returncode != 0:
            print(f"  ⚠ PDF skipped: pandoc error: {r1.stderr.strip()[:80]}")
        else:
            # Render HTML → PDF in-process. Previously this shelled out to a temp
            # script under sys.executable, which could be a different interpreter than
            # the one bench.py runs in — so a weasyprint installed in bench.py's env
            # still reported "install weasyprint". Importing here uses the SAME env.
            try:
                from weasyprint import HTML

                HTML(filename=str(html_path)).write_pdf(str(pdf_path))
            except ImportError:
                print(
                    "  ⚠ PDF skipped — install weasyprint: pip3 install weasyprint --break-system-packages"
                )
            except Exception as e:
                print(f"  ⚠ PDF skipped — weasyprint error: {str(e)[:80]}")
            finally:
                if html_path.exists():
                    html_path.unlink()
    except FileNotFoundError:
        # (c) The PDF step is optional. Nagging every run for months trained the eye to skip
        # warnings, which is exactly how a real ⚠ gets missed. State it once per run as a
        # neutral sub-detail, not a warning, and only when a PDF was actually wanted.
        _pdf_note.append("⚠ PDF skipped — pandoc not installed: brew install pandoc")

    # Bundle reports as zip for upload + audit workflow (AIStudio_829)
    # zip contains: json + md + pdf (if exists). Copied to ~/Downloads/.
    import zipfile as _zipfile

    downloads = Path.home() / "Downloads"
    downloads.mkdir(exist_ok=True)
    zip_name = f"{base_name}.zip"
    zip_dest = downloads / zip_name

    _files_to_zip = [f for f in [output_path, md_path, pdf_path] if f.exists()]
    with _zipfile.ZipFile(zip_dest, "w", _zipfile.ZIP_DEFLATED) as zf:
        for fpath in _files_to_zip:
            zf.write(fpath, fpath.name)

    _sep("Reports")
    print(f"✅ Reports written to {reports_dir}/")
    print(f"  · {output_path.name}")
    if md_path.exists():
        print(f"  · {md_path.name}")
    if pdf_path.exists():
        print(f"  · {pdf_path.name}")
    print(f"  · Bundled: ~/Downloads/{zip_name} ({len(_files_to_zip)} files)")
    print("  · Open the .md report for the full per-question breakdown and citations.")
    for _n in _pdf_note:
        print(f"  {_n}")


if __name__ == "__main__":
    main()
