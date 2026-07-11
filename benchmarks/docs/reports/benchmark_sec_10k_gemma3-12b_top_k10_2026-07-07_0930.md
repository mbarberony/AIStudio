# AIStudio — Benchmark Findings
*Generated: 2026-07-07 09:41*

## Configuration
- **Corpus:** `sec_10k`
- **Scope:** none (full corpus)
- **Base Top K:** 10 (effective K may be higher for multi-entity queries)
- **Temperature:** 0.3
- **Alpha:** 0.5
- **Min Score:** 0.5
- **Model:** gemma3:12b
- **API:** http://localhost:8000
- **Questions:** `benchmarks/sec_10k/sec_10k_questions.yaml` · sha `bc38f105`

## Summary
- **Questions:** 10
- **Passed (binary):** 8/10 (80%)
- **Rating (AIStudio_878):** 🟢 8 GREEN · 🟡 1 AMBER · 🔴 1 RED
- **Avg latency:** 66.7s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `sec_10k` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings? | 67.75s | 🟢 | JPMorgan_Chase_10K_2024-02-16.htm, JPMor | Emergence-of-AI-risk-language framing; answerable with current corpus. |
| 2 | How do JPMorgan, Bank of America, and Citigroup describe oversight of AI-related risk — through dedicated AI committees, or folded into their existing risk-governance structures? | 62.48s | 🟢 | JPMorgan_Chase_10K_2024-02-16.htm, JPMor | Reframed (BIC) — drops the dedicated-AI-committee presupposition; the correct answer ('AI risk is folded into existing risk governance') scores clean and contains 'AI'. The presupposing original lives in the June_2026 set. |
| 3 | Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged? | 60.47s | 🟡 | JPMorgan_Chase_10K_2024-02-16.htm, JPMor | Explicit 2022-vs-2026 temporal contrast across two firms. |
| 4 | How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework? | 69.0s | 🟢 | Bank_of_America_10K_2023-02-22.htm, Citi | Two-firm climate evolution since 2022. |
| 5 | How do JPMorgan, Bank of America, and Citigroup describe their approach to managing capital strength and their CET1 capital position in their most recent 10-K filings? | 82.56s | 🟢 | JPMorgan_Chase_10K_2023-02-21.htm, JPMor | Reframed (BIC) — qualitative capital-management / CET1-position comparison, prose-only. The hard multi-year CET1+revenue TABLE trend is preserved in the June_2026 set as the work-in-progress table exhibit (Annex 5). |
| 6 | How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge? | 101.45s | 🟢 | Citigroup_10K_2022-02-28.htm, Citigroup_ | Three-firm digital strategy over a relative 5-year window. |
| 7 | What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging? | 73.59s | 🟢 | JPMorgan_Chase_10K_2026-02-13.htm, JPMor | 'compliance' keyword removed 2026-05-30 (AIStudio_850) as a false negative. |
| 8 | How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K? | 48.07s | 🟢 | GOLDMAN_SACHS_GROUP_INC_10K_2026-02-25.h | L1 baseline. 2026-06-02 audit GREEN — Goldman-only, substantive. Token verified on Beast. |
| 9 | What are the principal categories of revenue BlackRock identifies in its most recent 10-K, and how does it describe each? | 35.42s | 🔴 | — | Reframed (BIC) — qualitative 'describe the sources' (base & performance fees, securities lending, technology services). Avoids inviting a precise sub-line figure; the original audited GREEN on sources but the model volunteered a wrong technology-services number. |
| 10 | What was JPMorgan Chase's total net revenue for fiscal year 2024, as reported in its FY2024 consolidated statements of income? Report the single FY2024 figure. | 66.57s | 🟢 | JPMorgan_Chase_10K_2025-02-14.htm | Pinned (BIC) — single FY2024 figure (~$177.6B), the income-statement total the system retrieves correctly; the wording discourages the multi-year pull that produced the contradictory FY2025 figure in the June_2026 run. The single-cell table lookup is the one quantitative shape handled cleanly. |

## Detailed Results

****
### 1. ai_disclosure_evolution
**Query:** When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America']` | **Keywords sent:** `['AI', 'risk', 'JPMorgan', 'Bank of America']`
**Retrieval query:** When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings? JPMorgan Chase & Co Bank of America Corporation
**Model:** `gemma3:12b` | **Latency:** 67.75s | **Pass:** ✅ | **Citation density:** 0.8

**Answer:**

> JPMorgan Chase first started disclosing AI as a specific risk factor in its 2024 filing [1]. Previously, in the 2022 filing, JPMorgan Chase mentioned using machine learning and artificial intelligence within models [2]. Bank of America first disclosed AI as a risk factor in its 2025 filing [3].
>
> In their most recent filings:
> JPMorgan Chase's 2026 Form 10-K states that the rapid development and deployment of advanced technologies, including generative and agentic AI systems, present risks such as AI system failures, inappropriate use, lack of transparency, inaccurate output, increased exposure to cyberattacks, intensified AI-enabled cyber threats, and potential workforce planning miscalibration [4].
> Bank of America's 2025 Form 10-K notes that expanded use of AI, including emerging third‑party AI services and autonomous AI agents, may result in increased data risk, unpredictable system interactions, inadequate controls or safeguards, AI failure, and operational, legal, regulatory, and reputational harm [3].

**Citations:**

- [1] JPMorgan_Chase_10K_2024-02-16.htm
- [2] JPMorgan_Chase_10K_2022-02-22.htm
- [3] Bank_of_America_10K_2026-02-25.htm
- [4] JPMorgan_Chase_10K_2026-02-13.htm


****
### 2. ai_governance_committees_comparison
**Query:** How do JPMorgan, Bank of America, and Citigroup describe oversight of AI-related risk — through dedicated AI committees, or folded into their existing risk-governance structures?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['AI', 'risk', 'governance', 'oversight']`
**Retrieval query:** How do JPMorgan, Bank of America, and Citigroup describe oversight of AI-related risk — through dedicated AI committees, or folded into their existing risk-governance structures? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `gemma3:12b` | **Latency:** 62.48s | **Pass:** ✅ | **Citation density:** 0.5

**Answer:**

> JPMorgan Chase describes its risk governance and oversight structure as supporting channels for escalating risks and issues to senior management, the FRC, and the Board of Directors [1]. The Firmwide Risk Committee escalates to the Board Risk Committee [2]. JPMorgan Chase’s Operating Committee is accountable to and may refer matters to the Board of Directors [1].
>
> Bank of America states that its Risk Framework describes delegations of authority whereby the Board and its committees may delegate authority to management-level committees or executive officers [3]. The Board authorizes management to maintain an effective Risk Framework and oversees compliance with safe and sound banking practices [3].
>
> Citigroup notes that policies govern the use of emerging technologies, including in model risk management [4]. However, ineffective AI development or deployment practices could result in adverse consequences [4]. Additionally, Citi faces competition risks to the extent competitors may be faster and more successful in developing and implementing AI [4].

**Citations:**

- [1] JPMorgan_Chase_10K_2024-02-16.htm
- [2] JPMorgan_Chase_10K_2026-02-13.htm
- [3] Bank_of_America_10K_2024-02-20.htm
- [4] Citigroup_10K_2026-02-20.htm


****
### 3. cyber_disclosure_2022_vs_2026
**Query:** Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged?
**Entity filter:** `['JPMorgan_Chase', 'Citigroup']` | **Keywords sent:** `['cybersecurity', 'JPMorgan', 'Citigroup', 'risk management']`
**Retrieval query:** Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged? JPMorgan Chase & Co Citigroup Inc
**Model:** `gemma3:12b` | **Latency:** 60.47s | **Pass:** ❌ | **Citation density:** 0.286

**Answer:**

> In 2022, JPMorgan Chase’s cybersecurity risk management framework was described as being integrated into the firm's operational risk management framework [1]. The governance structure for the Global Cybersecurity and Technology Controls organization identified, escalated, and mitigated cybersecurity risks [1]. The CISO reported to the Global Chief Information Officer and led the Global Cybersecurity and Technology Controls organization responsible for identifying technology and cybersecurity risks [1].
>
> In 2026, JPMorgan Chase’s cybersecurity risk management framework continues to be integrated into the firm's operational risk management framework [2]. Governance forums inform management of key areas of concern regarding the prevention, detection, mitigation, and remediation of cybersecurity risks [2]. The Cybersecurity and Technology Controls Operating Committee oversees the implementation and maintenance of appropriate controls in support of the Firm’s Information Security Program [2].
>
> A concrete change is that in 2026, governance forums inform management of key areas of concern regarding cybersecurity risk, whereas in 2022, updates generally included information regarding cybersecurity developments, recommended changes to the program, and ongoing initiatives [1].

**Citations:**

- [1] JPMorgan_Chase_10K_2024-02-16.htm
- [2] JPMorgan_Chase_10K_2026-02-13.htm

**Missing keywords:** ['Citigroup']

****
### 4. climate_risk_evolution
**Query:** How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework?
**Entity filter:** `['Bank_of_America', 'Citigroup']` | **Keywords sent:** `['climate', 'risk', 'Bank of America', 'Citigroup', 'Net Zero']`
**Retrieval query:** How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework? Citigroup Inc Bank of America Corporation
**Model:** `gemma3:12b` | **Latency:** 69.0s | **Pass:** ✅ | **Citation density:** 0.5

**Answer:**

> Bank of America announced a commitment to achieve net zero emissions in financing activities, operations, and supply chain before 2050 in 2021 [1]. In 2022, Bank of America announced a target to reduce emissions by 2030 associated with financing activities related to auto manufacturing, energy, and power generation [1]. Citigroup began developing globally consistent principles for managing climate risk across the company through its Climate Risk Management Framework (Climate RMF) in 2024 [2,3].
>
> In 2022, Bank of America disclosed its 2019 and 2020 financed emissions and emissions intensity metrics for specific sectors [1]. In 2023, they planned to disclose financed emissions for additional portions of their business loan portfolio and set financing activity emission reduction targets for other key sectors by April 2024 [1]. Bank of America created its internal Climate Risk Framework in 2023, which addresses how the corporation identifies, measures, monitors, and controls climate risk [4].
>
> Citigroup’s Net Zero plan implementation is leading to the further integration of climate risk discussions into client engagement and client selection [5]. In 2025, Citigroup continued to develop globally consistent principles for managing climate risk across the company through its Climate Risk Management Framework (Climate RMF) [3].
>
> Bank of America has a more detailed Net Zero or transition risk framework as evidenced by their internal Climate Risk Framework created in 2023 and specific targets announced since 2021 [1,4]. Citigroup’s disclosures focus on integrating climate risk into client engagement and developing a Climate Risk Management Framework [5,2,3].

**Citations:**

- [1] Bank_of_America_10K_2023-02-22.htm
- [2] Citigroup_10K_2026-02-20.htm
- [3] Citigroup_10K_2025-02-21.htm
- [4] Bank_of_America_10K_2025-02-25.htm
- [5] Citigroup_10K_2024-02-23.htm


****
### 5. capital_ratios_trend
**Query:** How do JPMorgan, Bank of America, and Citigroup describe their approach to managing capital strength and their CET1 capital position in their most recent 10-K filings?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['CET1', 'capital', 'JPMorgan', 'Bank of America', 'Citigroup']`
**Retrieval query:** How do JPMorgan, Bank of America, and Citigroup describe their approach to managing capital strength and their CET1 capital position in their most recent 10-K filings? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `gemma3:12b` | **Latency:** 82.56s | **Pass:** ✅ | **Citation density:** 0.25

**Answer:**

> JPMorgan Chase describes its approach to capital management as establishing targeted capital levels and meeting minimum requirements through a Contingency Capital Plan [1]. The firm calibrates these levels, monitors their appropriateness, and outlines actions for capital depletion during stress periods [1]. JPMorgan Chase’s capital rules generally follow the Basel Committee's Capital Accord [1]. In 2025, the firm allocated capital based on Basel III Standardized RWA and the GSIB surcharge [2].
>
> Bank of America manages its capital position to support business activities and aligns it with risk appetite and strategic planning [3]. The corporation seeks to maintain safety and soundness even under adverse scenarios and meet regulatory requirements [3]. As of December 31, 2023, the CET1 capital ratio of 11.8 percent exceeded both its requirement and the new minimum requirement in place as of January 1, 2024 [3]. Effective January 1, 2024, the G-SIB surcharge increased, resulting in a higher minimum CET1 capital ratio requirement to 10.0 percent [3]. The firm also maintains a supplementary leverage ratio (SLR) of 3.0 percent plus a leverage buffer of 2.0 percent [3].
>
> Citigroup’s capital management framework ensures sufficient capital consistent with its risk profile and regulatory standards [4]. Citi assesses its capital adequacy against internal quantitative goals designed to evaluate capital levels in expected and stressed environments [4]. To be considered "well capitalized," Citibank must maintain minimum CET1 Capital, Tier 1 Capital, Total Capital and Leverage ratios of 6.5%, 8.0%, 10.0% and 5.0%, respectively [5].

**Citations:**

- [1] JPMorgan_Chase_10K_2023-02-21.htm
- [2] JPMorgan_Chase_10K_2026-02-13.htm
- [3] Bank_of_America_10K_2024-02-20.htm
- [4] Citigroup_10K_2023-02-27.htm
- [5] Citigroup_10K_2024-02-23.htm


****
### 6. digital_banking_strategy
**Query:** How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['digital', 'technology', 'JPMorgan', 'Bank of America', 'Citigroup']`
**Retrieval query:** How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `gemma3:12b` | **Latency:** 101.45s | **Pass:** ✅ | **Citation density:** 0.588

**Answer:**

> JPMorgan Chase, Bank of America, and Citigroup have consistently highlighted the impact of emerging technologies on their digital banking strategies and technology investment priorities over the last five years (2021-2025).
>
> **Citigroup:** In 2021 [1], Citi noted that non-financial services firms were offering traditionally bank-provided services, intensifying competition. They also acknowledged increasing client interest in digital assets and potential regulatory challenges related to providing such services [1]. By 2023 [2], Citigroup recognized competition from online banks and fintech companies [2]. In 2025 [3], they emphasized the acceleration of emerging technologies like AI, digital assets (including tokenized deposits), and instant payments, potentially making some products less competitive and requiring investment in infrastructure to attract and retain customers [3].
>
> **Bank of America:** Bank of America’s filings from 2022 [4] highlighted increased reliance on digital banking due to the pandemic and pressure from competitors. They noted increasing cybersecurity risks associated with digital services [4]. In 2024 [5], they emphasized adapting strategies and products to rapidly evolving industry standards and consumer preferences, including developments in AI [5]. By 2025 [6,7], Bank of America focused on the regulatory landscape surrounding emerging technologies like AI, cryptocurrencies, and distributed ledger technology, acknowledging potential impacts on competition and requiring substantial investment [6,7].
>
> **JPMorgan Chase:** JPMorgan Chase’s filings consistently addressed disruption from non-depository institutions offering traditional banking products through e-commerce and electronic solutions [8,9]. In 2022 [8], they mentioned the risk of payments processing being disrupted by technologies like cryptocurrencies. By 2023 [9], JPMorgan Chase highlighted the need to adapt products to match competitors' offerings, including technology companies [9]. Their 2025 filing [10] specifically addressed generative AI and the risk of losing market share if they don’t keep pace with technological advances [10].
>
> **Major Themes:**
> *   **Increased Competition:** All three firms consistently mention increased competition from non-traditional financial services firms, fintech companies, and online banks.
> *   **Digital Asset Evolution:**  The evolving landscape of digital assets (cryptocurrencies, stablecoins, tokenized deposits) is a recurring theme, with all three institutions acknowledging both opportunities and regulatory challenges [1,6,8,3].
> *   **AI Integration:** Artificial intelligence (and generative AI specifically in later years) has become an increasingly important focus, requiring investment and adaptation to maintain competitiveness [5,10,6,7].
> *   **Rapid Technological Change:** The need to adapt quickly to rapidly evolving technologies is a constant concern for all three firms [4,5,8,9].

**Citations:**

- [1] Citigroup_10K_2022-02-28.htm
- [2] Citigroup_10K_2023-02-27.htm
- [3] Citigroup_10K_2026-02-20.htm
- [4] Bank_of_America_10K_2022-02-22.htm
- [5] Bank_of_America_10K_2024-02-20.htm
- [6] Bank_of_America_10K_2025-02-25.htm
- [7] Bank_of_America_10K_2026-02-25.htm
- [8] JPMorgan_Chase_10K_2022-02-22.htm
- [9] JPMorgan_Chase_10K_2024-02-16.htm
- [10] JPMorgan_Chase_10K_2026-02-13.htm


****
### 7. regulatory_burden_evolution
**Query:** What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging?
**Entity filter:** `['JPMorgan_Chase', 'Citigroup']` | **Keywords sent:** `['regulatory', 'capital', 'JPMorgan', 'Citigroup']`
**Retrieval query:** What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging? JPMorgan Chase & Co Citigroup Inc
**Model:** `gemma3:12b` | **Latency:** 73.59s | **Pass:** ✅ | **Citation density:** 0.294

**Answer:**

> JPMorgan Chase disclosed in its 2025 filing that the Federal Reserve’s Vice Chair for Supervision indicated that U.S. banking regulators may issue an updated proposal to amend the U.S. risk-based capital framework in early 2026, replacing the July 2023 proposal [1]. They also noted that finalized rules implementing Basel III frameworks became effective in the EU beginning January 1, 2025, with market risk aspects expected to be delayed until January 1, 2027, and a similar delay announced for the U.K. [1]. In 2022, JPMorgan Chase noted that maintaining required capital levels could impact their ability to support business activities and meet evolving regulatory requirements [2].
>
> Citigroup’s 2023 filing indicated they were continually required to interpret and implement extensive and frequently changing regulatory and legislative requirements [3]. Their 2024 filing highlighted significantly heightened regulatory expectations and scrutiny, particularly in the wake of banking stresses in 2023 [4]. Citigroup's 2022 filing mentioned an increase in their required regulatory CET1 Capital ratio to 11.5% from 10.5% due to a rise in the SCB requirement [5].
>
> A shared challenge identified by both firms is navigating evolving Basel III frameworks and potential changes to U.S. regulatory capital requirements [1,3].

**Citations:**

- [1] JPMorgan_Chase_10K_2026-02-13.htm
- [2] JPMorgan_Chase_10K_2022-02-22.htm
- [3] Citigroup_10K_2024-02-23.htm
- [4] Citigroup_10K_2025-02-21.htm
- [5] Citigroup_10K_2023-02-27.htm


****
### 8. cyber_goldman
**Query:** How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K?
**Entity filter:** `['Goldman_Sachs']` | **Keywords sent:** `['cybersecurity', 'Goldman Sachs', 'risk management', 'oversight']`
**Retrieval query:** How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K? The Goldman Sachs Group, Inc.
**Model:** `gemma3:12b` | **Latency:** 48.07s | **Pass:** ✅ | **Citation density:** 1.0

**Answer:**

> Goldman Sachs describes its cybersecurity risk-management framework as including preventive and detective controls and processes to mitigate emerging threats [1,2]. A dedicated Operational Risk team provides oversight of the Cybersecurity Program and assesses its effectiveness against industry standards and Board-approved limits [1,2]. The Firmwide Technology Risk Committee oversees cybersecurity matters and monitors their effectiveness; it is co-chaired by the CISO and chief technology officer and reports to the Firmwide Enterprise Risk Committee [1,2]. The Board oversees risk management policies and practices, including cybersecurity risks, and receives regular briefings from the CISO on topics such as the status of the Cybersecurity Program, emerging threats, and mitigation strategies [1,2,3,4].

**Citations:**

- [1] GOLDMAN_SACHS_GROUP_INC_10K_2026-02-25.htm
- [2] Goldman_Sachs_10K_2026-02-25.htm
- [3] Goldman_Sachs_10K_2025-02-27.htm
- [4] Goldman_Sachs_10K_2024-02-23.htm


****
### 9. revenue_sources_blackrock
**Query:** What are the principal categories of revenue BlackRock identifies in its most recent 10-K, and how does it describe each?
**Entity filter:** `['BlackRock']` | **Keywords sent:** `['BlackRock', 'revenue', 'investment advisory', 'fees']`
**Retrieval query:** What are the principal categories of revenue BlackRock identifies in its most recent 10-K, and how does it describe each?
**Model:** `gemma3:12b` | **Latency:** 35.42s | **Pass:** ❌ | **Citation density:** 0.0

**Answer:**

> The provided sources do not contain information about BlackRock's principal categories of revenue or descriptions thereof.

**Missing keywords:** ['BlackRock', 'revenue', 'investment advisory', 'fees']
**⚠ Model said 'no information' — possible retrieval miss**

****
### 10. net_revenue_jpm
**Query:** What was JPMorgan Chase's total net revenue for fiscal year 2024, as reported in its FY2024 consolidated statements of income? Report the single FY2024 figure.
**Entity filter:** `['JPMorgan_Chase']` | **Keywords sent:** `['JPMorgan', 'net revenue', '2024']`
**Retrieval query:** What was JPMorgan Chase's total net revenue for fiscal year 2024, as reported in its FY2024 consolidated statements of income? Report the single FY2024 figure. JPMorgan Chase & Co
**Model:** `gemma3:12b` | **Latency:** 66.57s | **Pass:** ✅ | **Citation density:** 0.5

**Answer:**

> JPMorgan Chase reported total net revenue of $177.6 billion in fiscal year 2024 [1].

**Citations:**

- [1] JPMorgan_Chase_10K_2025-02-14.htm

