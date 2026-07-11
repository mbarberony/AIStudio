# AIStudio Benchmark — Canonical Run B · Suzanne-Class Edition
## SEC 10-K Frontier Set, with BlackRock (`sec_10k` · 21 firms / 102 filings) · llama3.1:8b · 24 GB · 2026-07-07

*Type: NOTES | Domain: AIS | Status: internal provenance — hardware-tier edition. Intrinsic analysis of a single run. Cross-run comparison and trajectory belong to the Suite Synthesis, not here.*

**Machine:** Suzanne / MacBook-Pro-2 · 24 GB unified memory
**Config:** Top-K=10 · T=0.3 · α=0.5 · **llama3.1:8b** · entity-filter:auto · keywords:on · min_score=0.5 · **system_prompt_tier=small (uniform)**
**Corpus:** `sec_10k` at HEAD `093fabc`, 21 firms incl. **BlackRock**.
**Run:** `benchmark_sec_10k_llama3.1-8b_frontier_top_k10_2026-07-07_0925`
**Reproduce:** `ais_bench --corpus sec_10k --model llama3.1:8b --questions frontier --full`

---

## Executive Summary

**6🟢 · 2🟡 · 2🔴 · avg 29.1s · every question tier=small. This is the weakest run in the set, and for two distinct reasons.**

Run B is the frontier — multi-year quantitative-table synthesis and premise-testing. This run exhibits two intrinsic failure modes on top of the correct qualitative core:

**(1) Table fabrication (Q5).** The three-firm × five-year CET1-and-revenue table returns GREEN but is wrong in the cells: JPMorgan's CET1 pulled on the *Basel III Advanced* basis (not the Standardized figure implied), and Citigroup revenue figures shuffled across years ($19,645M / $18,102M / $19,649M bound to the wrong years). The model manufactures a plausible table from mis-coordinated cells.

**(2) Citation drop (Q6, Q8).** Two questions — digital-banking strategy and Goldman cybersecurity — returned **correct-looking prose with zero citations** (cd=0.0, both fast at 16–20s), scored RED. The answers read plausibly but are ungrounded: the citation mechanism, uniform elsewhere in this run, dropped out on these two. The short latencies suggest shallow/truncated retrieval feeding an ungrounded generation.

The qualitative core (Q1–Q4, Q7) is correct, and Q9 (BlackRock) partially resolves — "management fees from ETFs, mutual funds, and separately managed accounts," real but sparse.

---

## Results at a Glance (audited)

| # | ID | Rating | Cite density | Calibrated | One-line |
|---|---|---|---|---|---|
| 1 | ai_disclosure_evolution | 🟢 | 0.33 | ✅ | AI-risk emergence, correct |
| 2 | ai_governance_committees_comparison | 🟢 | 0.50 | ◑ | General governance structure (no dedicated AI committee in filings) |
| 3 | cyber_disclosure_2022_vs_2026 | 🟢 | 0.33 | ✅ | JPM + Citi cyber framework changes |
| 4 | climate_risk_evolution | 🟢 | 0.43 | ✅ | BofA + Citi evolution, correct |
| 5 | **capital_ratios_trend** | 🟢 | 0.42 | **✗ table-fabrication** | **CET1 basis-confusion + Citi revenue cell-shuffle** |
| 6 | digital_banking_strategy | 🔴 | 0.00 | **✗ citation-drop** | Correct-looking prose, **0 citations** — ungrounded |
| 7 | regulatory_burden_evolution | 🟢 | 0.39 | ✅ | Capital-rule changes, correct |
| 8 | cyber_goldman | 🔴 | 0.00 | **✗ citation-drop** | Correct-looking prose, **0 citations** — ungrounded |
| 9 | revenue_sources_blackrock | 🟡 | 0.33 | ◑ | Partial: "management fees from ETFs/mutual funds/SMAs" — real but sparse |
| 10 | net_revenue_jpm | 🟡 | 0.50 | ✅ | FY2024 net revenue **$177.6B** correct; amber is missing token "JPMorgan" |

**Effective:** 6 clean + 1 fair (Q2) + 1 correct-but-artifact numeric (Q10) — and **3 real defects: Q5 table fabrication, Q6/Q8 citation drop.**

---

## Findings

1. **Table fabrication on the multi-cell quantitative synthesis (Q5, fileable high-priority).** CET1 bound to the wrong basis (Advanced vs Standardized), Citi revenue figures shuffled across years. Root cause: chunking severs value from row/year/basis header; the model patches with mis-coordinated cells. Table-aware chunking is the lever.
2. **Citation drop on two frontier questions (Q6, Q8).** Both produced correct-looking, ungrounded prose with **0 citations** at short latency. On this run, the citation mechanism — uniform elsewhere — failed on two questions. Whether this is retrieval starvation (nothing to cite) or generation ignoring retrieved context needs a `/debug/retrieve` trace on these two queries.
3. **Q9 partial.** BlackRock now resolves to real revenue language (fees from ETFs/mutual funds/SMAs) but sparsely; the fuller category list ("investment advisory") is missing.

---

## Intrinsic Read

This run's signal is two failure modes co-occurring on the frontier set. The qualitative core is correct, but the *quantitative table* (Q5) fabricates mis-coordinated cells, and two questions (Q6, Q8) return ungrounded prose with no citations at all. The frontier set — harder retrieval, longer synthesis, multi-cell tables — is where this run's reliability frays: both the table-coordinate problem and the citation-grounding problem surface here and only here. The single-cell numeric (Q10) remains correct.

---

## Claims Supported

- On the frontier set, this run is correct on the qualitative core but exhibits **table fabrication** (Q5: wrong CET1 basis, shuffled revenue cells) and **citation drop** (Q6, Q8: correct-looking prose, zero citations).
- The table failure is coordinate-preservation under chunking (row/year/basis); **table-aware chunking** is the lever.
- The citation drop is isolated to two frontier questions and warrants a retrieval trace to separate starvation from generation-ignoring-context.
- Single-cell numeric ($177.6B) remains correct; Q9 BlackRock partially resolves.
