# AIStudio Benchmark Audit — SEC 10-K Corpus
## Run A · Calibrated Question Set (default) · 2026-06-26

**Run ID:** benchmark_sec_10k_gemma3-27b_top_k10_2026-06-26_0029
**Auditor:** Claude (Opus) · audited against SEC EDGAR primary filings
**Corpus:** sec_10k · 100+ filings / 21 firms (FY2021–FY2025) · scope: none (full corpus)
**Config:** Top-K=10 · T=0.3 · α=0.5 · gemma3:27b · entity-filter:auto · keywords:on
**Questions:** `benchmarks/sec_10k/sec_10k_questions.yaml` (sha bc38f105) · 10 questions

---

> **Companion reading** — this report is part of the canonical benchmark suite. Read it alongside [TUTORIAL.md](../../TUTORIAL.md) §5 (how to read a benchmark) and §5.6 (verify the cited chunk), and see the suite synthesis: [BENCH - Canonical Suite - README and Synthesis](BENCH%20-%20Canonical%20Suite%20-%20README%20and%20Synthesis.md). The reports carry the data and the audit; the *method* lives in the Tutorial, the *mechanism* in its Annexes.

## Executive Summary

**Mechanical: 10/10 GREEN · Calibrated: 9/10 (8 clean + 2 half-credit) · 0 fabrications · Avg latency 50.9s**

Run A is the **calibrated** SEC-10-K set — the questions a user can ask and trust the answer to. The set was deliberately framed (BIC = best-in-class reframing) to the shapes the system handles dependably: qualitative cross-firm comparisons, emergence-of-disclosure narratives, and single-cell numeric lookups. The hard multi-year quantitative-table and 2022-vs-2026 temporal shapes are *not* dropped — they are preserved in Run B (the frontier set) as the work-in-progress exhibit, so A measures the dependable surface and B measures the frontier.

The mechanical scorer rates A 10/10. On a calibrated read against the primary filings, A scores **9/10**: eight answers are clean and correctly grounded; two (Q1, Q3) lose a half-point each for temporal-label imperfections on otherwise-correct, well-cited answers. **No fabrication anywhere** — where coverage is thin the model abstains or states the gap rather than inventing.

---

## Results at a Glance

| # | ID | Mech | Calibrated | One-line |
|---|---|---|---|---|
| 1 | ai_disclosure_evolution | 🟢 | ✅⁻ ½ | Correct firms + real risk language; minor "first-disclosed" year-label softness |
| 2 | ai_oversight_bic | 🟢 | ✅ | Correctly answers "AI risk is folded into existing risk governance" — the true state |
| 3 | cyber_disclosure_2022_vs_2026 | 🟢 | ✅⁻ ½ | Citi half strong; JPM half compares 2024-vs-2025 and flags it doesn't cover the asked span |
| 4 | climate_risk_evolution | 🟢 | ✅ | BofA + Citi 2022→2024 evolution, named frameworks, correct |
| 5 | capital_management_bic | 🟢 | ✅ | Qualitative CET1-position comparison, prose-only, clean (hard table trend → Run B) |
| 6 | digital_banking_strategy | 🟢 | ✅ | Three-firm digital strategy, broad correct synthesis |
| 7 | regulatory_burden_evolution | 🟢 | ✅ | Basel III / capital-rule changes, JPM + Citi, correct |
| 8 | cyber_goldman | 🟢 | ✅ | Goldman-only, substantive, L1 baseline |
| 9 | revenue_sources_blackrock_bic | 🟢 | ✅ | Qualitative revenue-category description (reframed to avoid the wrong sub-line figure) |
| 10 | net_revenue_jpm | 🟢 | ✅ | Single FY2024 figure ~$177.6B from the income-statement table — the one quantitative shape handled cleanly |

---

## Notable Per-Question Findings

### Q2 ✅ ai_oversight_bic — the reframe that tells the truth
The original question presupposed *dedicated AI committees*. The filings largely do **not** describe dedicated AI-governance bodies — AI risk is folded into existing risk-governance structures. The BIC reframe drops the presupposition, and the model answers correctly: AI oversight sits inside the existing firmwide/board risk committees. This is the right answer to a fair question; the presupposing original is preserved in Run B precisely to show what happens when a question assumes something the corpus doesn't contain.

### Q3 ✅⁻ cyber_disclosure_2022_vs_2026 — the temporal-label half-point
The Citi half is strong and concrete (three-lines-of-defense, Cybersecurity Risk Appetite Statement, consent-order closure, cloud risk-compute). The ask is 2022-vs-2026; the **JPM half compares 2024 vs 2025 and openly states the sources don't cover JPM's 2024→2025 changes** — the requested contrast isn't fully delivered for JPM, and the temporal anchors drift (Citi "2022" resolves to the 2022-02-28 / FY2021 filing). Honest about the gap, no fabrication, but incomplete versus the ask → half-credit.

### Q10 ✅ net_revenue_jpm — the quantitative shape that works
Single FY2024 figure (~$177.6B), pulled from the income-statement total, cited to the FY2024 filing. The wording pins a single cell and discourages the multi-year pull that produces year-misbinding in Run B. The single-cell table lookup is the one quantitative shape the system handles cleanly and repeatably.

---

## Synthesis

Run A establishes the **dependable surface** of the SEC-10-K corpus: qualitative cross-firm comparison, disclosure-emergence narrative, and single-cell numeric retrieval, at 21-firm / 100+-filing scale, with gemma3:27b at K=10. Nine of ten answers are correct and correctly grounded; the two half-points are **temporal label-binding** softness (Q1 "first-disclosed" year, Q3 JPM span) — never retrieval failure and never fabrication. Where the corpus lacks coverage (Q3 JPM 2024→2025), the model states the gap rather than inventing one — the epistemic discipline that is the standing reason gemma3:27b is the synthesis model.

The single pattern across every soft spot is **value-to-label binding on temporal questions** — the same frontier Run B probes deliberately. A is calibrated to stay on the right side of that frontier; B crosses it on purpose. Read together, A is "what the system reliably does" and B is "where it strains," on one axis (synthesis/temporal); the esef runs (C/D) map the orthogonal language axis.

**Claims this run supports:**
- SEC-10-K qualitative multi-firm comparison is reliable at 21-firm scale (8/10 clean, 9/10 calibrated)
- Single-cell numeric retrieval from XBRL income-statement tables is clean and repeatable (Q10)
- Zero cross-firm contamination; zero fabrication; honest abstention where coverage is thin (Q3)
- The residual is temporal label-binding on multi-firm/multi-year questions — a known, deliberately-isolated frontier (see Run B)

---

*Report basis: benchmark_sec_10k_gemma3-27b_top_k10_2026-06-26_0029.{md,json} · audited against SEC EDGAR primary filings · 2026-06-26*

<div align="center">✻✻✻  ✻✻✻</div>
