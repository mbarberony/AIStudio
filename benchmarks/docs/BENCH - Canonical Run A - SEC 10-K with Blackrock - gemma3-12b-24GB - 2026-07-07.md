# AIStudio Benchmark — Canonical Run A · Suzanne-Class Edition
## SEC 10-K Calibrated Set, with BlackRock (`sec_10k` · 21 firms / 102 filings) · gemma3:12b · 24 GB · 2026-07-07

*Type: NOTES | Domain: AIS | Status: internal provenance — hardware-tier edition. Intrinsic analysis of a single run. Cross-run comparison and trajectory belong to the Suite Synthesis, not here.*

**Machine:** Suzanne / MacBook-Pro-2 · 24 GB unified memory
**Config:** Top-K=10 · T=0.3 · α=0.5 · **gemma3:12b** · entity-filter:auto · keywords:on · min_score=0.5 · **system_prompt_tier=small (12B < 20B threshold)**
**Corpus:** `sec_10k` at HEAD `093fabc`, 21 firms incl. **BlackRock**.
**Run:** `benchmark_sec_10k_gemma3-12b_top_k10_2026-07-07_0930`
**Reproduce:** `ais_bench --corpus sec_10k --model gemma3:12b --full`

---

## Executive Summary

**8🟢 · 1🟡 · 1🔴 · avg 66.7s · tier=small.**

Run A at the mid model tier returns **8🟢 of 10** on the full 21-firm corpus, with a **disciplined** character: where information is present it answers correctly and cites well (Q8 at cd=1.0, Q1 at cd=0.80); where information is absent it **declines cleanly rather than fabricating.** The single-cell numeric is exact ($177.6B, Q10). Latency is notably higher than the small tier (avg 66.7s; Q6 at 101s), the cost of the larger model on a 24 GB machine.

The two non-green results are both conservative failures: **Q9 (BlackRock) is a clean RED refusal** — "the provided sources do not contain information" — no backfill, no fabrication, but no answer (retrieval did not surface BlackRock's 2 filings). **Q3 (cyber 2022-vs-2026) is AMBER for incomplete coverage** — it answered for JPMorgan but omitted Citigroup. Both are under-answering, not wrong-answering.

---

## Results at a Glance (audited)

| # | ID | Rating | Cite density | Calibrated | One-line |
|---|---|---|---|---|---|
| 1 | ai_disclosure_evolution | 🟢 | 0.80 | ✅ | AI-risk emergence, well cited |
| 2 | ai_governance_committees_comparison | 🟢 | 0.50 | ✅ | Governance structure, correct |
| 3 | cyber_disclosure_2022_vs_2026 | 🟡 | 0.29 | ◑ | JPM covered, **Citigroup omitted** — incomplete coverage |
| 4 | climate_risk_evolution | 🟢 | 0.50 | ✅ | BofA + Citi evolution |
| 5 | capital_ratios_trend | 🟢 | 0.25 | ✅ | Qualitative capital approach; Basel III Standardized RWA + GSIB surcharge — correct, no fabrication |
| 6 | digital_banking_strategy | 🟢 | 0.59 | ✅ | Three-firm digital strategy, correct (101s) |
| 7 | regulatory_burden_evolution | 🟢 | 0.29 | ✅ | Capital-rule changes |
| 8 | cyber_goldman | 🟢 | 1.00 | ✅ | Goldman cyber framework, fully cited |
| 9 | revenue_sources_blackrock | 🔴 | 0.00 | **◑ clean refusal** | "Sources do not contain information" — no backfill, no answer |
| 10 | net_revenue_jpm | 🟢 | 0.50 | ✅ | FY2024 net revenue **$177.6B**, correct |

**8/10 correct**, both misses conservative (Q9 refusal, Q3 incomplete) — no wrong-answering, no fabrication.

---

## Findings

1. **Conservative failure mode (intrinsic characterization).** Both non-green results under-answer rather than mis-answer: Q9 refuses cleanly when retrieval misses BlackRock's thin filings; Q3 omits a firm rather than inventing coverage. On Q5 (qualitative capital) the answer stays grounded in correct Basel-Standardized language with no fabricated figures.
2. **Retrieval still misses the thin firm (Q9).** BlackRock is ingested but its 2-filing revenue chunk did not rank into top-K; here the model declined rather than backfilled. Same retrieval-scoping gap as the small tier, safer downstream behavior.
3. **Latency cost.** Avg 66.7s (Q6 101s) — the mid model roughly doubles per-question time on this 24 GB machine.

---

## Intrinsic Read

This run's character is discipline: 8/10 correct, and the two misses are conservative — a clean refusal and an incomplete answer, never a fabricated one. On the quantitative-adjacent question (Q5) the model stays grounded in correct regulatory language rather than manufacturing figures. The cost is latency: roughly double the small tier's per-question time. The one capability gap is retrieval scoping on the thin BlackRock firm, which here produces a safe refusal rather than a wrong answer.

---

## Claims Supported

- On a 24 GB machine at the mid (12b) tier with the full 21-firm corpus, the calibrated surface is correct at **8/10**, single-cell numeric exact ($177.6B).
- Both misses are **conservative** — a clean no-info refusal (Q9) and an incomplete-coverage answer (Q3) — not wrong-answering or fabrication.
- Retrieval still misses the thinly-represented BlackRock firm; the model's response to that miss is a safe refusal.
- Latency is materially higher (avg 66.7s, up to 101s) — the mid model's cost on this hardware.
