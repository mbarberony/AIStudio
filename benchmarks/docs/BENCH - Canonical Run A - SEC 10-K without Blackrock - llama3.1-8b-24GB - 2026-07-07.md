# AIStudio Benchmark — Canonical Run A · Suzanne-Class Edition
## SEC 10-K Calibrated Set, without BlackRock (`sec_10k` · 20 firms / 100 filings) · llama3.1:8b · 24 GB · 2026-07-07

*Type: NOTES | Domain: AIS | Status: internal provenance — hardware-tier edition. Intrinsic analysis of a single run. Cross-run comparison and trajectory belong to the Suite Synthesis, not here.*

**Machine:** Suzanne / MacBook-Pro-2 · 24 GB unified memory
**Config:** Top-K=10 · T=0.3 · α=0.5 · **llama3.1:8b** · entity-filter:auto · keywords:on · min_score=0.5 · **system_prompt_tier=small (uniform)**
**Corpus:** `sec_10k` at HEAD `093fabc`, 20 firms × 5 years = 100 filings, 99,944 chunks. **BlackRock not ingested** (21st-firm exercise deferred).
**Run:** `benchmark_sec_10k_llama3.1-8b_top_k10_2026-07-07_0755` · questions sha `bc38f105`
**Reproduce:** `ais_bench --corpus sec_10k --model llama3.1:8b --full`

---

## Executive Summary

**9🟢 · 1🟡 (BlackRock, out-of-scope) · 0🔴 · avg 45.9s · every question tier=small. Effective in-scope read: 9/9 clean.**

Run A is the calibrated set: the dependable-surface questions — disclosure-emergence narratives, qualitative cross-firm comparison, single-cell numeric lookup. On this machine and model the run returns **9🟢 of 10**, the single non-green being the un-ingested BlackRock firm (a corpus gap, not a system failure). On the in-scope 20 firms the run is **effectively spotless**: every answer is grounded, cited, and correct.

Two intrinsic properties define the run. First, the **`_956` slim system prompt engaged uniformly — `tier=small` on all 10 questions** — and citations are present on every answer; on this 24 GB machine, which is the box that historically returned zero citations, the citation mechanism is now fully reliable. Second, the **quantitative single-cell shape is correct**: FY2024 JPMorgan net revenue returns **$177.6B** from a single clean source (Q10), the numeric-lookup case handled precisely.

The one behavioral finding is on the out-of-scope question (Q9): with no BlackRock chunks to retrieve, entity-filter returned nothing and the model **backfilled from Raymond James** while correctly hedging "not explicitly stated for BlackRock." Faithful in prose, unfaithful in control flow — see Findings.

---

## Results at a Glance (audited · in-scope = 20 firms)

| # | ID | Rating | Cite density | Calibrated | One-line |
|---|---|---|---|---|---|
| 1 | ai_disclosure_evolution | 🟢 | 0.75 | ✅ | JPM FY2023 / BofA FY2025 AI-risk emergence, real quoted language, correct firms |
| 2 | ai_governance_committees_comparison | 🟢 | 0.36 | ✅ | "AI risk folded into existing risk governance" — the true state |
| 3 | cyber_disclosure_2022_vs_2026 | 🟢 | 0.44 | ✅ | JPM + Citi cyber framework evolution, 7 cites, correct |
| 4 | climate_risk_evolution | 🟢 | 0.56 | ✅ | BofA + Citi 2022→ evolution, named Net-Zero frameworks |
| 5 | capital_ratios_trend | 🟢 | 0.36 | ✅ | Qualitative CET1-position comparison, prose-only, clean |
| 6 | digital_banking_strategy | 🟢 | 1.38 | ✅ | Three-firm digital strategy, 11 cites, genuine multi-firm synthesis |
| 7 | regulatory_burden_evolution | 🟢 | 0.27 | ✅ | Basel III / capital-rule changes, JPM + Citi, correct |
| 8 | cyber_goldman | 🟢 | 0.33 | ✅ | Goldman board oversight: Firmwide Technology Risk Committee co-chaired CISO+CTO, correct |
| 9 | revenue_sources_blackrock | 🟡 | 0.33 | **⊘ out-of-scope** | **BlackRock not ingested** — entity-filter empty, model backfilled Raymond James (see Findings) |
| 10 | net_revenue_jpm | 🟢 | 0.50 | ✅ | FY2024 net revenue **$177.6B**, single figure, single clean source |

**Effective in-scope: 9/9 ✅.** Q9 is dropped from the scored read because its target firm is absent from the corpus by design; it measures a corpus-completeness gap, not RAG quality.

---

## Findings

1. **Entity-filter-miss → cross-firm backfill (faithfulness, fileable).** Q9 named BlackRock; `entity_filter=['BlackRock']` matched nothing (firm not ingested); retrieval fell back to unfiltered results and surfaced Raymond James chunks; the model narrated RJF's segments while hedging "not explicitly stated for BlackRock." `no_info_signal=false` — the system did not classify this as a no-info case. **Correct behavior:** when the named entity yields zero filtered hits, hard-stop / return no-info rather than backfill from other firms and cite them.
2. **Corpus-completeness gap (data, not RAG).** `sec_10k_questions.yaml` (sha `bc38f105`) asks about BlackRock, which is not in the ingested 20 firms. Resolve by either (a) adding BlackRock as the 21st firm, or (b) marking Q9 out-of-scope in the question set.

---

## Intrinsic Read

This run's own signal, independent of any other: **on a 24 GB machine at the small-model tier, the calibrated SEC-10-K surface is grounded, cited, and correct at 9/9 in-scope.** Citations engage uniformly (`tier=small`), qualitative cross-firm comparison holds without starvation, and single-cell numeric lookup is exact. The two blemishes are cleanly separable and neither is a RAG-quality defect: one is a corpus-completeness gap (BlackRock absent), the other a faithfulness control-flow issue (entity-filter-miss backfill) surfaced only *because* of that gap. Nothing in the in-scope set fails.

---

## Claims Supported

- On a 24 GB machine at the 8b tier, the calibrated SEC-10-K surface — qualitative cross-firm comparison, disclosure-emergence, single-cell numeric — is **grounded, cited, and correct at 9/9 in-scope**.
- The `_956` slim system prompt engages **uniformly (`tier=small`)** with citations present on every answer — the citation mechanism is reliable on this machine.
- Single-cell numeric lookup is exact (FY2024 net revenue $177.6B, single source).
- The one behavioral defect is an **entity-filter-miss backfill** on an out-of-scope firm; the one score gap is a **corpus-completeness** issue — both cleanly separable, neither a RAG-quality regression.
