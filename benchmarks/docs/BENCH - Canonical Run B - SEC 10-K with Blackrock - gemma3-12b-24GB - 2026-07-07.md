# AIStudio Benchmark — Canonical Run B · Suzanne-Class Edition
## SEC 10-K Frontier Set, with BlackRock (`sec_10k` · 21 firms / 102 filings) · gemma3:12b · 24 GB · 2026-07-07

*Type: NOTES | Domain: AIS | Status: internal provenance — hardware-tier edition. Intrinsic analysis of a single run. Cross-run comparison and trajectory belong to the Suite Synthesis, not here.*

**Machine:** Suzanne / MacBook-Pro-2 · 24 GB unified memory
**Config:** Top-K=10 · T=0.3 · α=0.5 · **gemma3:12b** · entity-filter:auto · keywords:on · min_score=0.5 · **system_prompt_tier=small (12B < 20B threshold)**
**Corpus:** `sec_10k` at HEAD `093fabc`, 21 firms incl. **BlackRock**.
**Run:** `benchmark_sec_10k_gemma3-12b_frontier_top_k10_2026-07-07_0941`
**Reproduce:** `ais_bench --corpus sec_10k --model gemma3:12b --questions frontier --full`

---

## Executive Summary

**9🟢 · 1🟡 · 0🔴 · avg 49.9s · tier=small. The strongest frontier run in the set — and the reason is how it handles the table.**

Run B on the mid tier returns **9🟢 of 10** on the frontier set, and its defining property is Q5. The three-firm × five-year CET1-and-revenue table is handled **honestly**: the answer opens "based solely on the provided sources," reports the CET1 figures it can support, attributes Citigroup's FY2025 decrease to a correct causal read ("common share repurchases, an increase in RWA, and the payment of dividends"), and where a value is absent — Bank of America total revenue — it **states the value is not provided rather than fabricating one.** No equity-as-revenue arithmetic, no cross-year cell duplication. The frontier's hardest question is answered without invention.

BlackRock (Q9) resolves **correctly and fully cited** (cd=1.0): "asset management, performance fees, and securities lending" — the best BlackRock answer in the set; the AMBER is only a missing keyword token ("investment advisory"). The qualitative core (Q1–Q8) is uniformly green.

---

## Results at a Glance (audited)

| # | ID | Rating | Cite density | Calibrated | One-line |
|---|---|---|---|---|---|
| 1 | ai_disclosure_evolution | 🟢 | 0.40 | ✅ | AI-risk emergence, correct |
| 2 | ai_governance_committees_comparison | 🟢 | 0.44 | ✅ | Governance structure, correct |
| 3 | cyber_disclosure_2022_vs_2026 | 🟢 | 0.36 | ✅ | JPM + Citi cyber framework changes |
| 4 | climate_risk_evolution | 🟢 | 0.46 | ✅ | BofA + Citi evolution |
| 5 | **capital_ratios_trend** | 🟢 | 0.47 | **✅ honest table** | Hedged, correct causal read on Citi 2025; **absent cells declared absent — no fabrication** |
| 6 | digital_banking_strategy | 🟢 | 0.79 | ✅ | Three-firm digital strategy, strong synthesis |
| 7 | regulatory_burden_evolution | 🟢 | 0.47 | ✅ | Capital-rule changes |
| 8 | cyber_goldman | 🟢 | 0.57 | ✅ | Goldman cyber framework, correct |
| 9 | revenue_sources_blackrock | 🟡 | 1.00 | ✅ | **"Asset management, performance fees, securities lending"** — correct, fully cited; amber is missing token "investment advisory" |
| 10 | net_revenue_jpm | 🟢 | 0.50 | ✅ | FY2024 net revenue **$177.6B** (+12%), correct |

**9/10 correct**, including an honestly-handled quantitative table and a correct, fully-cited BlackRock answer. The lone amber (Q9) is a keyword-token artifact on a correct answer.

---

## Findings

1. **The multi-cell quantitative table is handled without fabrication (Q5, the key intrinsic result).** The answer hedges to available sources, gives a correct causal explanation for the one trend it reports, and explicitly declares absent values absent (BofA revenue "not provided") rather than manufacturing them. The table-coordinate limit still bounds *how much* it can report, but it does not produce wrong numbers.
2. **BlackRock resolves correctly and fully cited (Q9, cd=1.0).** "Asset management, performance fees, securities lending" — real BlackRock revenue categories, every claim cited. The AMBER is purely a missing keyword token, a grader artifact, not an answer defect.
3. **Longer table synthesis under a generous timeout.** Q5 ran 108.8s and completed cleanly under the 300s per-query timeout — the frontier table needs the headroom, and the timeout provides it.

---

## Intrinsic Read

This run's signal is honest handling of the hardest material. On the quantitative table (Q5) it reports what the sources support, explains the trend it reports correctly, and declares absent cells absent — the safe, faithful failure mode when coordinate-preservation limits reach are hit. BlackRock (Q9) is answered correctly and fully cited. The qualitative core is uniformly green. The frontier set, which stresses table synthesis and thin-firm retrieval, is handled here without fabrication and without ungrounded prose — the reliability the frontier is designed to test holds on this run.

---

## Claims Supported

- On the frontier set at the mid (12b) tier, this run is correct at **9/10**, including an honestly-handled multi-cell quantitative table and a correct, fully-cited BlackRock answer.
- The Q5 table is reported without fabrication: available cells cited, one trend explained with a correct causal read, absent cells declared absent — the faithful failure mode at the coordinate limit.
- BlackRock (Q9) resolves to correct, fully-cited revenue categories; the AMBER is a keyword-token grader artifact.
- Single-cell numeric ($177.6B) correct; the table question required ~109s and completed under the 300s timeout.
