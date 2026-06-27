# AIStudio Benchmark Audit — ESEF Banks Corpus
## Run D · English Matched (`esef_english`) · 2026-06-26

**Run ID:** benchmark_esef_banks_gemma3-27b_lang_en_lang_en_top_k10_2026-06-26_2235
**Auditor:** Claude (Opus) · audited against ESEF primary filings (filings.xbrl.org)
**Corpus:** esef_banks · scope: `lang_en` (5 English filers: ING, Barclays, HSBC, Standard Chartered, BBVA)
**Config:** Top-K=10 · T=0.3 · α=0.5 · gemma3:27b · entity-filter:auto · keywords:on · scope: lang_en (5 firms)
**Questions:** `lang_en` set · 8 questions (the English-firm subset of the default 12)
**Companion:** Run C (`esef_blended`) — the same corpus un-scoped, all 12 firms, blended language

---

> **Companion reading** — this report is part of the canonical benchmark suite. Read it alongside [TUTORIAL.md](../../TUTORIAL.md) §5.8 (scope + questions pairing) and Annex 3 (the language ceiling), and see the suite synthesis: [BENCH - Canonical Suite - README and Synthesis](BENCH%20-%20Canonical%20Suite%20-%20README%20and%20Synthesis.md). The reports carry the data and the audit; the *method* lives in the Tutorial, the *mechanism* in its Annexes.

## Executive Summary

**Mechanical: 6/8 (6 🟢 · 2 🟡 · 0 🔴) · Calibrated: ~7–8/8 · 0 fabrications · Avg latency 62.7s**

Run D is the **language-controlled** benchmark: the ESEF corpus restricted to its five verified English filers, paired with the eight questions that target those firms. It is the matched, apples-to-apples counterpart to Run C's blended baseline — and it answers the question C raises ("how much of C's soft scoring is language?") by removing the variable. The result is decisive: with language controlled, the run is **effectively clean.** Both ambers are pure keyword artifacts — the literal token "regulatory" missing from otherwise-correct answers — and there are zero wrong-topic answers, zero abstentions, zero contamination, and zero fabrication. Every one of the eight answers is substantively correct against the primary filings.

This pairing is the methodological point of the suite: **scope picks the firms, questions picks the set, and pairing them correctly isolates one variable.** D over C is the language axis measured cleanly.

---

## Results at a Glance

| # | ID | Firm | Mech | Calibrated | One-line |
|---|---|---|---|---|---|
| 1 | cet1_ing_group | ING | 🟡 | ✅ | CET1 13.1% (from 13.6%), 11.09% requirement, ~195bp buffer — correct; "regulatory" keyword artifact |
| 2 | tier1_capital_barclays | Barclays | 🟢 | ✅ | CET1 12.7%, T1 16.1%, total 19.0%, full £-figures — correct |
| 3 | leverage_ratio_hsbc | HSBC | 🟡 | ✅ | 5.3%, UK 3.25%, 0.9% buffer — primary-verified; "regulatory" keyword artifact |
| 4 | cet1_cross_firm_en | ING/HSBC/Barclays | 🟢 | ✅ | Three-firm CET1 with full SREP breakdown, correct, no contamination |
| 5 | climate_risk_bbva | BBVA | 🟢 | ✅ | TCFD + GFANZ-aligned transition plan, correct |
| 6 | climate_standard_chartered | Std Chartered | 🟢 | ✅ | Net-zero ops by 2025, position statements, correct |
| 7 | digital_ing | ING | 🟢 | ✅ | Four-enabler tech strategy under the CTO, correct |
| 8 | barclays_holdco_sub | Barclays | 🟢 | ✅ | Barclays PLC 100% of Barclays Bank PLC, FHC status, correct |

---

## Notable Per-Question Findings

### The clean result (the run's thesis)
Every question that was a *genuine* problem in Run C is **absent here** — because every genuine C problem was a non-English firm (Nordea Q5/Q10, KBC Q6, Erste Q12), and the `lang_en` scope drops all of them. What remains are the five English firms, and against them the system answers correctly on capital ratios, leverage, cross-firm CET1, climate, digital strategy, and holdco structure. The two ambers (Q1 ING, Q3 HSBC) are the *identical* keyword artifact — the scorer wants the literal token "regulatory" and the answer phrases the regulatory minimum without that exact word. Read up: both are correct.

### Q3 ✅ leverage_ratio_hsbc — primary-verified
HSBC 5.3% (down from 5.6%), UK minimum 3.25%, 0.9% buffer (0.7% ALRB + 0.2% CCLB), exceeded throughout 2025 — matches HSBC's Pillar 3 disclosure exactly. The only mark against it is the missing literal "regulatory" keyword. This is a benchmark-calibration artifact, not a retrieval or generation failure.

### Q4 ✅ cet1_cross_firm_en — three-firm synthesis, clean
ING/HSBC/Barclays CET1 with ING's full SREP requirement breakdown (4.5% Pillar 1 + 0.93% Pillar 2 + 2.5% conservation + 0.93% countercyclical + 0.16% SyRB + 2.0% O-SII), three citations, correct firms, no contamination. The multi-firm path that strains on the blended corpus works cleanly when the firms are language-matched.

---

## Synthesis

Run D is the **clean English benchmark**: with the corpus scoped to its five verified English filers and the questions matched to those firms, the system is effectively flawless — 6/8 mechanical, ~7–8/8 calibrated, the two-point gap entirely a single missing keyword. There are no wrong-topic answers, no abstentions, no contamination, no fabrication; every answer is correct against the primary filings.

The value of D is in the **C↔D contrast**. Run C (blended, 12 firms) scores ~8/12 with every soft spot on a non-English firm; Run D (English-only, matched) is clean. The delta is the language axis, isolated by controlling scope and questions together — exactly the methodology the suite is built to demonstrate (Tutorial §5.8). The reading is direct: AIStudio's retrieval and synthesis are sound; the European frontier is specifically the non-English filing (Annex 3), and on English-filing firms the same machinery returns grounded, correctly-cited, primary-verifiable answers at K=10.

A note on K and multi-firm load: the canonical depth for these multi-firm corpora is K=10 because effective retrieval depth must accommodate several firms competing for slots — a per-entity quota raises the effective K so one firm doesn't crowd out the others. D's clean three-firm Q4 confirms that depth is sufficient for the language-controlled cut.

**Claims this run supports:**
- With language controlled, ESEF retrieval + synthesis is effectively clean (~7–8/8); the gap is keyword calibration, not capability
- Multi-firm synthesis (Q4) is correct and contamination-free when firms are language-matched
- The C↔D delta isolates the language axis as the European frontier (Annex 3)
- K=10 is the correct multi-firm default; the scope+questions pairing is the methodology that makes the comparison honest (§5.8)

---

*Report basis: benchmark_esef_banks_gemma3-27b_lang_en_lang_en_top_k10_2026-06-26_2235.{md,json} · audited against ESEF primary filings + HSBC Pillar 3 · 2026-06-26*

<div align="center">✻✻✻  ✻✻✻</div>
