# AIStudio Benchmark Audit — ESEF Banks Corpus
## Run C · Full Corpus, Blended Language (`esef_blended`) · 2026-06-26

**Run ID:** benchmark_esef_banks_gemma3-27b_top_k10_2026-06-26_2222
**Auditor:** Claude (Opus) · audited against ESEF primary filings (filings.xbrl.org)
**Corpus:** esef_banks · 12 firms · scope: none (full corpus) · 5 EN-filing + 7 non-EN-filing
**Config:** Top-K=10 · T=0.3 · α=0.5 · gemma3:27b · entity-filter:auto · keywords:on
**Questions:** default set · 12 questions
**Companion:** Run D (`esef_english`) — the same corpus restricted to the 5 English filers with matched questions

---

> **Companion reading** — this report is part of the canonical benchmark suite. Read it alongside [TUTORIAL.md](../../TUTORIAL.md) §5 (how to read a benchmark) and Annex 3 (the language ceiling), and see the suite synthesis: [BENCH - Canonical Suite - README and Synthesis](BENCH%20-%20Canonical%20Suite%20-%20README%20and%20Synthesis.md). The reports carry the data and the audit; the *method* lives in the Tutorial, the *mechanism* in its Annexes.

## Executive Summary

**Mechanical: 8/12 (6 🟢 · 6 🟡 · 0 🔴) · Calibrated: ~8–9/12 · 0 fabrications · Avg latency 62.4s**

Run C is the **blended-language baseline**: all 12 ESEF banks, default questions, no scope filter — the number a user sees querying the full European corpus without knowing which filings are in English. Five firms file in English (ING, Barclays, HSBC, Standard Chartered, BBVA); seven file in their domestic language (Nordea/SEB Swedish, Erste German, KBC Dutch, BNP/Société Générale French, UniCredit Italian). The run's defining feature: **every soft spot falls on a non-English firm, and not one is a fabrication.** Where the system can't ground an answer in a foreign-language filing, it returns a sparse-but-correct answer, drifts to an adjacent section, or — in the cleanest case — explicitly abstains. It never invents.

The mechanical 8/12 both *under-* and *over-*states quality in different places, which is why it is audited rather than trusted: three ambers are correct answers with sparse attribution (read up), one GREEN hides an abstention (read down).

---

## Results at a Glance

| # | ID | Firm (filing lang) | Mech | Calibrated | One-line |
|---|---|---|---|---|---|
| 1 | cet1_ing_group | ING (en) | 🟡 | ✅ | Correct CET1 13.1%/buffer; amber is low density only |
| 2 | tier1_capital_barclays | Barclays (en) | 🟢 | ✅ | Full capital stack, correct figures |
| 3 | leverage_ratio_hsbc | HSBC (en) | 🟡 | ✅ | 5.3% + UK 3.25% + buffers — primary-verified correct; "regulatory" keyword artifact |
| 4 | cet1_cross_firm_en | ING/HSBC/Barclays (en) | 🟢 | ✅ | Three-firm CET1, correct, no contamination |
| 5 | nordea_leverage_ratio | Nordea (sv) | 🟢 | ◑ abstain | GREEN hides an abstention: "sources do not directly address this" |
| 6 | kbc_nii_sensitivity | KBC (nl) | 🟡 | ❌ wrong-topic | Answered ESG/climate credit risk, not the asked NII sensitivity |
| 7 | climate_risk_bbva | BBVA (en) | 🟡 | ✅ | TCFD/GFANZ transition plan, correct; low density |
| 8 | climate_standard_chartered | Std Chartered (en) | 🟢 | ✅ | Net-zero ops by 2025, scenario analysis, correct |
| 9 | digital_ing | ING (en) | 🟢 | ✅ | Four-enabler tech strategy, correct |
| 10 | digital_nordea | Nordea (sv) | 🟡 | ✅⁻ | Correct (top-3 digital, app awards); "technology" keyword artifact |
| 11 | barclays_holdco_sub | Barclays (en) | 🟢 | ✅ | Holdco/sub structure, FHC status, correct |
| 12 | erste_whitespace_collapse | Erste (de) | 🟡 | ✅⁻ | Sparse but real risk-profile answer; "framework" keyword artifact |

---

## Notable Per-Question Findings

### The language pattern (the run's thesis)
Sort the soft spots by filing language and the result is unambiguous: **all four English firms with a flagged question (Q1 ING, Q3 HSBC, Q7 BBVA) amber only on keyword/density technicalities while answering correctly; the genuine quality problems are on non-English firms** — Q5 (Nordea, sv), Q6 (KBC, nl), Q10 (Nordea, sv), Q12 (Erste, de). This is the language ceiling of **Annex 3** at corpus scale: retrieval quality is not language-neutral, and a question in English against a filing written in Swedish/Dutch/German retrieves worse.

### Q5 ◑ nordea_leverage_ratio — the GREEN that hides an abstention (read down)
Scored GREEN 1.0, but the answer is: *"The available sources do not directly address this question…"* — an honest abstention on a Swedish filing, scored as a pass because the citation and topical keywords matched. This is the mirror of B's false-GREENs: here the mechanical score *over*-credits a non-answer. The right read is "could not ground the specific leverage figure across the language gap" — a known non-English limitation, correctly handled by abstaining rather than inventing.

### Q6 ❌ kbc_nii_sensitivity — wrong-section retrieval (the one real miss)
The ask is net-interest-income sensitivity and interest-rate-risk management. The answer describes KBC's **ESG/climate credit-risk** framework instead — a wrong-section retrieval on a Dutch filing. This is the genuine miss of the run: not a fabrication, but the wrong part of the document surfaced because the English query matched the wrong Dutch passage.

### Q3 ✅ leverage_ratio_hsbc — primary-verified, amber is a keyword artifact (read up)
HSBC 5.3% (from 5.6%), UK minimum 3.25%, 0.9% buffer (0.7% ALRB + 0.2% CCLB), exceeded throughout 2025 — every figure verified against HSBC's Pillar 3 disclosure. The amber is solely the missing literal token "regulatory"; the answer is fully correct. Read up.

---

## Synthesis

Run C is the **honest blended baseline** for the European corpus: 8/12 mechanical, ~8–9/12 calibrated, on a 12-firm portfolio where seven firms file in a non-English language. Its value is in *where* the soft spots fall — exclusively on the non-English firms, and exclusively as sparse-attribution, wrong-section, or honest-abstention, **never fabrication.** The system degrades gracefully across the language gap: it says less, points at less, or declines — it does not invent a plausible foreign-sourced number.

The cross-firm English questions (Q4, and the single-firm English Q1/Q2/Q3/Q7/Q8/Q9/Q11) are correct, confirming entity isolation holds at 12-firm scale with no contamination. The European-specific frontier is the language one, documented in **Annex 3**: the glossary bridges acronym↔full-form within English but does not translate, so an English question against a Swedish or Dutch filing retrieves worse. Run D isolates the clean half of this corpus to show what the system does when language is controlled.

**Claims this run supports:**
- Entity isolation holds at 12-firm scale; zero cross-firm contamination, zero fabrication
- The system degrades *gracefully* on non-English filings — sparse, wrong-section, or honest abstention (Q5/Q6/Q10/Q12), never invention
- English-firm answers are correct and primary-verifiable (HSBC leverage, ING CET1, three-firm cross-CET1)
- The frontier is language, not retrieval mechanics (Annex 3); Run D tests the language-controlled cut directly

---

*Report basis: benchmark_esef_banks_gemma3-27b_top_k10_2026-06-26_2222.{md,json} · audited against ESEF primary filings + HSBC Pillar 3 · filing languages verified by chunk-content read · 2026-06-26*

<div align="center">✻✻✻  ✻✻✻</div>
