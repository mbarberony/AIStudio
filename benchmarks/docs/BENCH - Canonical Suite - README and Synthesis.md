# AIStudio — Canonical Benchmark Suite
## README & Synthesis · gemma3:27b · 2026-06-26

all figures audited against primary filings (SEC EDGAR / ESEF filings.xbrl.org)
**Model:** gemma3:27b · Top-K=10 · T=0.3 · α=0.5
**Reproduce:** `ais_bench --batch` (runs the pinned set from `benchmarks/batch/bench_canonical.yaml`)
**Read alongside:** Tutorial §5 (how to read a benchmark) · Annex 3 (language) · Annex 4 (tables)

---

> **Companion file** — [TUTORIAL.md](../../TUTORIAL.md) is the companion to this suite: §5 teaches *how to read* a benchmark (mechanical vs calibrated), and Annexes 3 (language) and 4 (tables) carry the failure mechanisms these runs surface. This README is the evidence layer; the Tutorial is the method and mechanism layer. Read together.

## What this suite is

Four benchmark runs across the two shipped corpora, each read the way Tutorial §5 prescribes: **start at the mechanical score, audit the answers against the primary filings, then state the calibrated read.** The mechanical score is a keyword-and-citation signal — it is easy to run and easy to misread, and its failure mode is to reward confident wrongness. The calibrated read is what the answers actually say when you scroll the cited chunk. The gap between the two is the entire reason this suite exists.

The four runs are designed as two pairs that vary one thing each:
- **A vs B** — same corpus (SEC 10-K), different question difficulty. Isolates the *synthesis/temporal* frontier.
- **C vs D** — same corpus (ESEF banks), scoped to control language. Isolates the *language* frontier.

Together they map two orthogonal frontiers and the solid ground between them — with, across all four runs, **zero fabrications.**

---

## The four runs at a glance

| Run | Set | Corpus · scope | Mechanical | Calibrated | What it proves |
|---|---|---|---|---|---|
| **A** | `sec_10k` | SEC 10-K · full | 10/10 | **9/10** | Dependable surface — qualitative + single-cell, soft spots are temporal-label only |
| **B** | `sec_10k_frontier` | SEC 10-K · full | 10/10 | **~6.5–7** | Synthesis ceiling — GREEN table answers wrong in the cells (Q5), temporal span collapse (Q3) |
| **C** | `esef_blended` | ESEF · 12 firms | 8/12 | **~8–9/12** | Blended baseline — every soft spot on a non-English firm, never fabrication |
| **D** | `esef_english` | ESEF · 5 EN firms | 6/8 | **~7–8/8** | Language-controlled — effectively clean; ambers are keyword artifacts only |

*Mechanical scores carry run-to-run noise at non-zero temperature; a one-point delta between runs is not a finding. The stable signal is the audit, not the number.*

---

## The two frontiers (the synthesis)

### Frontier 1 — Synthesis & temporal binding (the A↔B axis, on clean English)
On the US corpus, retrieval is healthy and the system is solid where the audits say it is: single-firm factual lookups, qualitative multi-firm comparison, and single-cell numeric retrieval all come back grounded and correctly cited (Run A, 9/10). The frontier appears when a question demands **binding a value to its coordinates** — Run B's three-firm × five-year CET1 table returns a confident, citation-rich answer with the figures bound to the *wrong years* (15.7% labeled FY2021 when it is the FY2024 value), and the 2022-vs-2026 cyber question answers a 2024-vs-2025 span instead. Both score GREEN. This is the table-cell frontier of **Annex 4** at scale: maximally fluent, citation-rich, wrong in the cells — the clearest case in the suite of *mechanical pass ≠ correct.* The active build is structured-data and table-recognition handling that binds each number to its row, year, and basis.

### Frontier 2 — Language (the C↔D axis, on the European corpus)
The ESEF corpus carries seven non-English filers (Swedish, German, Dutch, French, Italian) alongside five English ones. Run C (blended, all 12) scores ~8–9/12 — and **every single soft spot falls on a non-English firm**: a Swedish leverage question the model honestly abstains on, a Dutch NII question that retrieves the wrong (ESG) section, a German risk question answered sparsely. Run D removes the variable — scope the corpus to its five English filers, match the questions — and the run is **effectively clean** (~7–8/8, the two ambers a single missing keyword). The C↔D delta is the language axis isolated: retrieval and synthesis are sound; the frontier is specifically the non-English filing, documented in **Annex 3** (the glossary bridges acronym↔full-form within English but does not translate).

### The constant across all four — graceful failure, no fabrication
The single most important property the suite establishes is what the system does when it *can't* answer: it says less, points at less, retrieves the wrong section, or explicitly declines — it **never invents a plausible number.** Run C's Nordea abstention, Run B's "revenue not available," Run A's "sources don't cover that span" are all the same discipline: honest about the gap. This is why gemma3:27b is the synthesis model, and why the audit method (verify the cited chunk, §5.6) is the contract rather than the green number.

**But this holds under *normal* querying — not under adversarial contradiction.** The four runs ask honest questions and get honest answers; the [companion case study](BENCH%20-%20Canonical%20Companion%20-%20AIS%20vs%20Google%20vs%20Reality.md) is the harder test they cannot reach. Fed a *conflicting* figure and pressed to reconcile it, AIS abandoned a correct, filing-backed answer and confabulated a cross-firm explanation — while Google manufactured a page-cited precision the filing does not support. Graceful abstention when an answer is *absent* is not the same as holding ground when an answer is *challenged*: the suite proves the first, the case study exposes the gap in the second. Even a well-grounded system can be talked out of the truth — which is exactly why the audit, not the green number, is the contract, and why the citation-grounding guard is the build that closes the gap.

---

## How to read these reports

Each per-run report (`BENCH - Canonical Run {A,B,C,D} - …`) follows the same shape: executive summary → results at a glance → notable per-question findings → synthesis → claims supported. The scoring notation:
- **✅** correct, grounded, right firm · **✅⁻** correct but keyword/density artifact (read up) · **◑** fair-answer-to-unfair-question or hidden abstention · **⚠** mechanically passing but incomplete/wrong-span · **✗** confidently wrong (read down)

The four-state discipline behind these (✅ Good / ⚠ Partial / ❌ Miss / 🔍 Grading artifact) and the objective-% metric are defined in Tutorial §5.5. The reports carry the *data and the audit*; the *mechanism* lives in the annexes (Annex 3 language, Annex 4 tables); the *method* lives in §5. This README is the evidence layer that ties them together.

---

## Files in this suite

- `BENCH - Canonical Run A - SEC 10-K Calibrated Set` — the dependable surface
- `BENCH - Canonical Run B - SEC 10-K Frontier Set` — the synthesis/table frontier
- `BENCH - Canonical Run C - ESEF Banks Blended Corpus` — the blended-language baseline
- `BENCH - Canonical Run D - ESEF Banks English Matched` — the language-controlled clean cut
- `reports/` — the raw, machine-generated `bench.py` reports for all four runs (provenance; regenerated by `ais_bench --batch`)
- [`BENCH - Canonical Companion - AIS vs Google vs Reality`](BENCH%20-%20Canonical%20Companion%20-%20AIS%20vs%20Google%20vs%20Reality.md) — the AIG-revenue trap: the same question put to AIS and to Google, each answer scored against the primary filing ("Reality"), then **pushed back on** with a conflicting figure. The adversarial counterpart to these four runs — where the no-fabrication discipline they measure meets the one test they cannot reach.

---

*Generated 2026-06-26 · gemma3:27b · audited against SEC EDGAR + ESEF primary filings · reproduce with `ais_bench --batch`*

<div align="center">✻✻✻  ✻✻✻</div>
