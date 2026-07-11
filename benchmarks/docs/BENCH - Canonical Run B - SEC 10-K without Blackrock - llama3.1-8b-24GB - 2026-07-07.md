# AIStudio Benchmark — Canonical Run B · Suzanne-Class Edition
## SEC 10-K Frontier Set, without BlackRock (`sec_10k` · 20 firms / 100 filings) · llama3.1:8b · 24 GB · 2026-07-07

*Type: NOTES | Domain: AIS | Status: internal provenance — hardware-tier edition. Intrinsic analysis of a single run. Cross-run comparison and trajectory belong to the Suite Synthesis, not here.*

**Machine:** Suzanne / MacBook-Pro-2 · 24 GB unified memory
**Config:** Top-K=10 · T=0.3 · α=0.5 · **llama3.1:8b** · entity-filter:auto · keywords:on · min_score=0.5 · **system_prompt_tier=small (uniform)**
**Corpus:** `sec_10k` at HEAD `093fabc`, 20 firms × 5 years = 100 filings. **BlackRock not ingested** (added after this run).
**Run:** `benchmark_sec_10k_llama3.1-8b_frontier_top_k10_2026-07-07_0827` · questions `frontier` (10)
**Reproduce:** `ais_bench --corpus sec_10k --model llama3.1:8b --questions frontier --full`

---

## Executive Summary

**6🟢 · 3🟡 · 1🔴 (BlackRock, out-of-scope) · avg 53.0s · every question tier=small. Mechanical 7/10 — the calibrated read is lower, and the reason is one question.**

Run B is the frontier: multi-year quantitative-table synthesis, temporal contrasts, and premise-testing questions. Its intrinsic value is the sharpest demonstration in this run that **a mechanical pass is not a correct answer** — concentrated in Q5.

**The finding is Q5, the three-firm × five-year CET1-and-revenue table.** It returns **GREEN with 10 citations at 89.95s** and is wrong in three distinct, verifiable ways visible in the answer text:
1. **Basis-confusion** — JPMorgan's CET1 is pulled on the *Basel III Advanced* basis, not the Standardized figure the question implies, with a self-contradicting narrative ("consistently above 13%… but decreased to 15.3%").
2. **Cell-duplication** — Citigroup's FY2022 revenue figure ($45,686M) is copied verbatim into FY2025.
3. **Wrong-row fabrication** — Bank of America's "total revenue" is actually *Total common shareholders' equity* summed with itself ($272,400 + $263,249 = $535,649M): a revenue answer manufactured from equity rows.

This is table-collapse: chunking severs the value from its row / year / basis header, and the model patches the gaps with plausible-looking arithmetic on the wrong cells. The failure mode on this run is **fabrication** — inventing a number from the wrong row — not merely omission.

**The control within the same run holds: Q10 (single-cell net revenue) is correct** — "$177.6 billion," one clean source. Same corpus, same model, same run: the *single-cell* shape is exact, the *multi-cell table* shape shatters. The determinant is entirely whether the number's coordinates (row, year, basis) survived chunking.

---

## Results at a Glance (audited calibrated read)

| # | ID | Rating | Cite density | Calibrated | One-line |
|---|---|---|---|---|---|
| 1 | ai_disclosure_evolution | 🟢 | 0.30 | ✅ | JPM + BofA AI-risk emergence, correct |
| 2 | ai_governance_committees_comparison | 🟢 | 0.50 | ◑ | No dedicated AI committee in filings; model answers the real (general) structure |
| 3 | cyber_disclosure_2022_vs_2026 | 🟢 | 0.43 | ✅ | JPM + Citi cyber framework changes, correct |
| 4 | climate_risk_evolution | 🟢 | 0.31 | ✅ | BofA + Citi 2022→ evolution, named frameworks |
| 5 | **capital_ratios_trend** | 🟢 | 0.56 | **✗ table-collapse** | **CET1 basis-confusion + revenue cell-duplication + equity-as-revenue fabrication** |
| 6 | digital_banking_strategy | 🟢 | 0.44 | ✅ | Three-firm digital strategy, 10 cites, genuine synthesis |
| 7 | regulatory_burden_evolution | 🟡 | 0.083 | ✅⁻ | Basel III / capital-rule changes correct; amber is sparse attribution only (read up) |
| 8 | cyber_goldman | 🟡 | 0.57 | ✅⁻ | Goldman cyber framework correct; amber is missing literal token "oversight" (read up) |
| 9 | revenue_sources_blackrock | 🔴 | 0.0 | **⊘ out-of-scope** | BlackRock not ingested — 0 citations, clean refusal (no backfill on this phrasing) |
| 10 | net_revenue_jpm | 🟡 | 0.50 | ✅ | FY2024 net revenue **$177.6B**, correct single figure; amber is missing token "JPMorgan" only (read up) |

**Effective in-scope calibrated:** of the 9 in-scope questions — **6 clean (✅/✅⁻), 1 fair-answer (◑, Q2), 1 confidently-wrong-in-cells (✗, Q5), and the single-cell numeric (Q10) correct.** Q9 dropped (corpus gap). The three mechanical AMBERs (Q7/Q8/Q10) are keyword/density artifacts on correct answers — read up. The one that matters is Q5, and it reads down.

---

## Findings

1. **Table-collapse produces fabrication (fileable, high priority).** Q5's failure is not omission but invention: the model built a revenue figure by summing two equity rows (BofA), duplicated a cell across years (Citi), and bound CET1 to the wrong basis (JPM Advanced vs Standardized). Root cause is chunking severing value from row/year/basis header; the answer-side symptom is fabricated arithmetic on wrong cells. **Table-aware chunking** (bind value → row → year → basis) is the capability lever this run points to.
2. **CET1 basis is a required coordinate (sharpens Finding 1).** Even with perfect chunking, a CET1 answer must bind to its *basis* (Advanced vs Standardized), not just its year. Q5 conflated the two. Basis is a second coordinate table-aware retrieval must preserve.
3. **Entity-filter-miss refused cleanly on this phrasing.** Q9's BlackRock question returned 0 citations and no answer (RED) rather than backfilling — the correct no-info behavior. (Whether this is deterministic vs phrasing-sensitive is a question for the entity-filter-miss work; recorded here as the observed behavior on this run.)

---

## Intrinsic Read

This run's own signal: **the frontier questions expose a single, decisive capability limit — the multi-cell quantitative table.** Everything qualitative (disclosure, cyber, climate, digital strategy) is correct; the single-cell numeric (Q10) is correct; only the multi-year, multi-firm, multi-basis *table* (Q5) fails — and it fails by fabrication, the most dangerous mode, because the output looks authoritative and is cited. The gap between Q5 (table) and Q10 (single cell) inside one run isolates the cause to coordinate-preservation under chunking, nothing else. The mechanical AMBERs are measurement artifacts, not answer defects — the instrument is trustworthy; the finding is capability.

---

## Claims Supported

- On the frontier set, this run is correct on all qualitative synthesis and on single-cell numeric lookup ($177.6B), and fails only on the multi-cell quantitative table (Q5).
- The table failure mode on this run is **fabrication** — a revenue figure built from equity rows, a duplicated cell, a wrong CET1 basis — not omission.
- The Q5-vs-Q10 split within one run isolates the cause to **coordinate-preservation (row/year/basis) under chunking**; **table-aware chunking** is the capability lever indicated.
- Citations engage uniformly (`tier=small`); the mechanical ambers (Q7/Q8/Q10) are keyword/density artifacts on correct answers — the measurement is sound.
