# AIStudio Benchmark Audit — SEC 10-K Corpus
## Run B · Frontier Question Set (`sec_10k_frontier`) · 2026-06-26

**Run ID:** benchmark_sec_10k_gemma3-27b_june_2026_top_k10_2026-06-26_0122
**Auditor:** Claude (Opus) · audited against SEC EDGAR primary filings
**Corpus:** sec_10k · 100+ filings / 21 firms (FY2021–FY2025) · scope: none (full corpus)
**Config:** Top-K=10 · T=0.3 · α=0.5 · gemma3:27b · entity-filter:auto · keywords:on
**Questions:** frontier set · 10 questions
**Companion:** Run A (`sec_10k`, calibrated set) — same corpus, the dependable-surface counterpart

---

> **Companion reading** — this report is part of the canonical benchmark suite. Read it alongside [TUTORIAL.md](../../TUTORIAL.md) §5 (how to read a benchmark) and Annex 4 (the table-cell frontier), and see the suite synthesis: [BENCH - Canonical Suite - README and Synthesis](BENCH%20-%20Canonical%20Suite%20-%20README%20and%20Synthesis.md). The reports carry the data and the audit; the *method* lives in the Tutorial, the *mechanism* in its Annexes.

## Executive Summary

**Mechanical: 10/10 GREEN · Calibrated: ~6.5–7/10 · 0 fabrications · Avg latency 49.7s**

Run B is the **frontier** set — the same SEC-10-K corpus pushed to the question shapes Run A deliberately defers: multi-year quantitative-table synthesis, 2022-vs-2026 temporal contrasts, and a question that presupposes a governance structure the filings don't contain. The mechanical scorer rates B a perfect 10/10. On a calibrated read against the primary filings, B is **~6.5–7**: six answers are correct, two are mechanically-GREEN-but-wrong on the substance, one is quantitatively wrong while GREEN, and one is a fair answer to an unfair question.

B is the most important run in the suite for one reason: it is the cleanest demonstration that **mechanical pass ≠ correct** (Tutorial §5.3). Every defect here scores GREEN — the keyword and citation checks pass while the figure-to-year binding, the temporal span, or the question's own premise is wrong. None of these is visible in the green number; each was found by reading the answer against the filing. This is the frontier the suite exists to keep measured.

---

## Results at a Glance

| # | ID | Mech | Calibrated | One-line |
|---|---|---|---|---|
| 1 | ai_disclosure_evolution | 🟢 | ✅ | JPM + BofA AI-risk emergence, real quoted language, correct |
| 2 | ai_governance_committees | 🟢 | ◑ fair-answer | Filings disclose no dedicated AI committee; model answers with the real (general) structure |
| 3 | cyber_disclosure_2022_vs_2026 | 🟢 | ⚠ temporal | Compares 2024-vs-2025, not the asked 2022-vs-2026; JPM half states the span isn't covered |
| 4 | climate_risk_evolution | 🟢 | ✅ | BofA + Citi 2022→2024 evolution, named frameworks, correct |
| 5 | capital_ratios_trend | 🟢 | ✗ year-misbind | CET1 numbers bound to wrong years (15.7% labeled FY2021); revenue punted — the table frontier |
| 6 | digital_banking_strategy | 🟢 | ✅ | Three firms, density 1.0, genuine multi-firm synthesis |
| 7 | regulatory_burden_evolution | 🟢 | ✅ | Basel III / SCB changes, JPM + Citi, correct |
| 8 | cyber_goldman | 🟢 | ✅ | Goldman-only, substantive, L1 baseline |
| 9 | revenue_sources_blackrock | 🟢 | ✅ | BlackRock revenue categories correct (figure unit dropped — minor) |
| 10 | net_revenue_jpm | 🟢 | ✅ | FY2024 net revenue $177.6B from the income-statement table |

---

## Notable Per-Question Findings

### Q5 ✗ capital_ratios_trend — the table-cell frontier (Annex 4) at full scale
The headline failure, and the clearest *mechanical-pass-≠-correct* case in the suite. The answer returns a confident, fully-formatted CET1 table with 10 citations — and scores GREEN — but the figures are **bound to the wrong years**: it reports JPMorgan's CET1 as "15.7% FY2021" when 15.7% is the FY2024 figure (FY2021 was ~13%), and it openly punts on revenue ("total revenues are not directly provided in a consolidated format"). This is exactly the failure Annex 4 documents: financial ratios live in multi-year, multi-column tables, and a chunk can sever a cell from the column-header (the year) that gives it meaning. Maximally fluent, citation-rich, wrong in the cells. **See Annex 4 for the mechanism; this is that mechanism at three-firm × five-year scale.**

### Q3 ⚠ cyber_disclosure_2022_vs_2026 — temporal-span collapse (distinct from Q5)
The ask is 2022-vs-2026. The Citi half is strong and concrete; the **JPM half compares 2024-vs-2025 and openly states the sources don't cover the asked span.** The requested temporal contrast isn't delivered for JPM, and the anchors drift. This is a *temporal-synthesis* frontier — **not** a table problem (keep it distinct from Q5): the failure is in spanning two time-points, not in reading a table cell. Honest about the gap (no fabrication), but incomplete versus the ask.

### Q2 ◑ ai_governance_committees — fair answer to an unfair question
The question presupposes *dedicated AI governance committees*. We verified directly against the corpus (primary-retrieval probe): the filings contain **no dedicated-AI-committee content** — only general risk/operating committees plus one Citi "Generative AI" risk-factor mention. So the model answering with the firms' general risk-governance structure is the **correct available answer to a question that assumes something not in the filings** — an honest response, not a drift defect. (Run A's calibrated set reframes this exact question for the same reason.)

### Where B is genuinely solid (Q1, Q4, Q6, Q8, Q9, Q10)
Single-firm factual (Q8 Goldman, Q9 BlackRock, Q10 JPM net revenue $177.6B) and qualitative multi-firm synthesis (Q1 AI emergence, Q4 climate, Q6 digital strategy) all come back correct and grounded. Q10 is notable: the single-cell income-statement lookup is the one quantitative shape the system handles cleanly — the contrast with Q5's multi-cell table is the whole point of pairing them in one run.

---

## Synthesis

Run B maps the **synthesis/temporal frontier** of the SEC-10-K corpus on clean English text. Retrieval is healthy and single-firm/qualitative-multi-firm answers are correct; the frontier is **binding values to their coordinates** — Q5 binds CET1 figures to the wrong years, Q3 fails to span the asked two time-points. Both score GREEN, which is the lesson: the mechanical score rewards confident, citation-rich output regardless of whether the cells are right. Read against the primary filings, B is ~6.5–7, not 10.

Critically, **no fabrication appears anywhere** — where coverage is thin (Q3 JPM span, Q5 revenue) the model states the gap rather than inventing one. The frontier is precision-under-synthesis, not honesty. The active build that addresses it — binding each number to its row, year, and basis — is the structured-data and table-recognition work of Annex 4; B exists to keep that boundary measured rather than discovered live in front of a reader.

Paired with Run A (the calibrated, dependable surface of the same corpus), the A↔B contrast is one axis of the suite: A is what the system reliably does, B is where it strains, both on English. The esef runs (C/D) map the orthogonal language axis.

**Claims this run supports:**
- The clearest *mechanical-pass-≠-correct* evidence in the suite: GREEN answers that are wrong in the table cells (Q5) and the temporal span (Q3)
- Single-cell numeric retrieval (Q10) and qualitative multi-firm synthesis (Q1/Q4/Q6) are reliable on the same corpus
- Zero fabrication; honest abstention where coverage is thin (Q3, Q5 revenue)
- The residual is value-to-coordinate binding under multi-year/multi-firm synthesis — the table frontier (Annex 4) and temporal synthesis, both deliberately isolated here

---

*Report basis: benchmark_sec_10k_gemma3-27b_june_2026_top_k10_2026-06-26_0122.{md,json} · "dedicated AI committee" premise verified absent via primary retrieval · audited against SEC EDGAR · 2026-06-26*

<div align="center">✻✻✻  ✻✻✻</div>
