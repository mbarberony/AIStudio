# AIStudio Benchmark — Canonical Run A · Suzanne-Class Edition
## SEC 10-K Calibrated Set, with BlackRock (`sec_10k` · 21 firms / 102 filings) · llama3.1:8b · 24 GB · 2026-07-07

*Type: NOTES | Domain: AIS | Status: internal provenance — hardware-tier edition. Intrinsic analysis of a single run. Cross-run comparison and trajectory belong to the Suite Synthesis, not here.*

**Machine:** Suzanne / MacBook-Pro-2 · 24 GB unified memory
**Config:** Top-K=10 · T=0.3 · α=0.5 · **llama3.1:8b** · entity-filter:auto · keywords:on · min_score=0.5 · **system_prompt_tier=small (uniform)**
**Corpus:** `sec_10k` at HEAD `093fabc`, 21 firms incl. **BlackRock** (BLK, 2 filings FY2024–FY2025, LEI-resolved).
**Run:** `benchmark_sec_10k_llama3.1-8b_top_k10_2026-07-07_0917`
**Reproduce:** `ais_bench --corpus sec_10k --model llama3.1:8b --full`

---

## Executive Summary

**9🟢 · 1🟡 · 0🔴 · avg 44.4s · every question tier=small.**

Run A — the dependable-surface calibrated set — returns **9🟢 of 10** on the full 21-firm corpus. Qualitative synthesis, disclosure-emergence, cross-firm comparison, and single-cell numeric lookup are all grounded and correct, several at perfect citation density (Q1, Q2 at cd=1.0). The single-cell numeric case is exact: FY2024 JPMorgan net revenue returns **$177.6B** from one clean source (Q10). Citations engage uniformly (`tier=small` on all 10).

The lone AMBER is Q9 (BlackRock revenue categories). BlackRock is now ingested, yet the model's retrieval surfaced Goldman and Raymond James chunks rather than BlackRock's own, and it narrated around them — hedging correctly ("not explicitly stated") but missing the categories. This is a retrieval-scoping failure on a thinly-represented firm (2 filings), not a corpus gap — see Findings.

---

## Results at a Glance (audited)

| # | ID | Rating | Cite density | Calibrated | One-line |
|---|---|---|---|---|---|
| 1 | ai_disclosure_evolution | 🟢 | 1.00 | ✅ | AI-risk emergence, correct firms, fully cited |
| 2 | ai_governance_committees_comparison | 🟢 | 1.00 | ✅ | AI risk folded into existing governance, fully cited |
| 3 | cyber_disclosure_2022_vs_2026 | 🟢 | 0.46 | ✅ | JPM cyber framework evolution, correct |
| 4 | climate_risk_evolution | 🟢 | 0.55 | ✅ | BofA + Citi 2022→ evolution |
| 5 | capital_ratios_trend | 🟢 | 0.40 | ✅ | Qualitative capital-management approach, prose, clean |
| 6 | digital_banking_strategy | 🟢 | 0.58 | ✅ | Digital strategy synthesis |
| 7 | regulatory_burden_evolution | 🟢 | 0.30 | ✅ | Basel III / capital-rule changes |
| 8 | cyber_goldman | 🟢 | 0.33 | ✅ | Goldman cyber framework + oversight, correct |
| 9 | revenue_sources_blackrock | 🟡 | 0.30 | **✗ retrieval-scope** | BlackRock ingested but retrieval surfaced Goldman/RJF; model backfilled (see Findings) |
| 10 | net_revenue_jpm | 🟢 | 0.50 | ✅ | FY2024 net revenue **$177.6B**, single figure, correct |

**9/10 correct.** Q9 is now in-scope (BlackRock present) and is a genuine miss — a retrieval-scoping failure, not a corpus gap.

---

## Findings

1. **Entity-scoped retrieval fails on a thin firm (fileable).** BlackRock is ingested (2 filings) but Q9's retrieval returned Goldman and Raymond James chunks instead of BlackRock's, and the model backfilled from them while hedging. With only 2 filings, BlackRock's revenue-category chunk did not rank into the top-K under `entity-filter:auto`. Two levers: (a) hard-scope retrieval to the named entity when one is detected (return no-info rather than backfill on zero in-scope hits); (b) ensure thin-firm chunks are reachable (per-entity K floor).
2. **Calibrated surface is otherwise spotless.** 9/10 with two perfect-density answers and exact single-cell numeric; the citation mechanism is uniform (`tier=small`).

---

## Intrinsic Read

On the full 21-firm corpus, this run's calibrated surface is grounded, cited, and correct at 9/10, with exact single-cell numeric lookup and uniform citation engagement. The single defect is isolated and diagnosable: retrieval did not scope to the named entity when that entity is thinly represented, so a BlackRock question was answered from other firms' chunks. Nothing in the qualitative or numeric-single-cell surface fails.

---

## Claims Supported

- On a 24 GB machine at the 8b tier with the full 21-firm corpus, the calibrated SEC-10-K surface is correct at **9/10**, single-cell numeric exact ($177.6B), citations uniform (`tier=small`).
- The one defect is **entity-scoped retrieval on a thinly-represented firm** (BlackRock, 2 filings) — retrieval surfaced other firms and the model backfilled; a retrieval-scoping issue, cleanly separable from RAG quality on the rest.
