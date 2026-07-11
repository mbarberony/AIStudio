# AIStudio — Benchmark Findings
*Generated: 2026-07-07 09:49*

## Configuration
- **Corpus:** `sec_10k`
- **Scope:** none (full corpus)
- **Base Top K:** 10 (effective K may be higher for multi-entity queries)
- **Temperature:** 0.3
- **Alpha:** 0.5
- **Min Score:** 0.5
- **Model:** gemma3:12b
- **API:** http://localhost:8000
- **Questions:** `frontier`

## Summary
- **Questions:** 10
- **Passed (binary):** 9/10 (90%)
- **Rating (AIStudio_878):** 🟢 9 GREEN · 🟡 1 AMBER · 🔴 0 RED
- **Avg latency:** 49.9s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `sec_10k` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings? | 20.77s | 🟢 | JPMorgan_Chase_10K_2024-02-16.htm, Bank_ | Emergence-of-AI-risk-language framing; answerable with current corpus. |
| 2 | Which of JPMorgan, Bank of America, or Citigroup have established dedicated AI governance committees, and how do their oversight structures differ? | 61.54s | 🟢 | Citigroup_10K_2026-02-20.htm, JPMorgan_C | 3-firm comparison. 2026-06-02 audit AMBER — answers drift to general risk committees; missing 'AI' is a genuine drift signal, not a phrasing artifact. Keyword retained deliberately. |
| 3 | Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged? | 35.7s | 🟢 | JPMorgan_Chase_10K_2024-02-16.htm, JPMor | Explicit 2022-vs-2026 temporal contrast across two firms. |
| 4 | How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework? | 39.36s | 🟢 | Bank_of_America_10K_2024-02-20.htm, Bank | Two-firm climate evolution since 2022. |
| 5 | How have CET1 capital ratios and total revenues trended at JPMorgan, Bank of America, and Citigroup from FY2021 through FY2025? Identify any consistent leaders or laggards. | 108.81s | 🟢 | Citigroup_10K_2023-02-27.htm, Citigroup_ | The stacked case — 3 firms × FY2021-FY2025 × quantitative table. Heaviest question (~114s). |
| 6 | How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge? | 59.77s | 🟢 | JPMorgan_Chase_10K_2022-02-22.htm, JPMor | Three-firm digital strategy over a relative 5-year window. |
| 7 | What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging? | 35.49s | 🟢 | JPMorgan_Chase_10K_2026-02-13.htm, JPMor | 'compliance' keyword removed 2026-05-30 (AIStudio_850) as a false negative. |
| 8 | How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K? | 28.28s | 🟢 | GOLDMAN_SACHS_GROUP_INC_10K_2026-02-25.h | L1 baseline. 2026-06-02 audit GREEN — Goldman-only, substantive. Token verified on Beast. |
| 9 | What does BlackRock identify as its principal sources of revenue in its most recent 10-K? | 38.48s | 🟡 | BlackRock,_Inc._10K_2026-02-25.htm | L1 baseline. 2026-06-02 audit GREEN — BlackRock-only. Token verified on Beast. |
| 10 | What was JPMorgan Chase's total net revenue for fiscal 2024 as reported in its consolidated statements of income? | 70.69s | 🟢 | JPMorgan_Chase_10K_2025-02-14.htm | L2 — the table-location ∂. 2026-06-02 audit AMBER→fixed — pulled $177.6B FY2024 from the income-statement table; keyword 'total revenue' → 'net revenue' (answer says "total net revenue"). derived=false (figure is stated, not computed — contrast L7). |

## Detailed Results

****
### 1. ai_disclosure_evolution
**Query:** When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America']` | **Keywords sent:** `['AI', 'risk', 'JPMorgan', 'Bank of America']`
**Retrieval query:** When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings? JPMorgan Chase & Co Bank of America Corporation
**Model:** `gemma3:12b` | **Latency:** 20.77s | **Pass:** ✅ | **Citation density:** 0.4

**Answer:**

> JPMorgan Chase first started disclosing AI as a specific risk factor in its 2024 filing [1]. In that filing, JPMorgan Chase noted risks associated with AI systems including failures, inappropriate use, lack of transparency, inaccurate or biased output, increased exposure to cyber attacks, and potential workforce planning challenges [1].
>
> Bank of America first disclosed AI as a risk factor in its 2025 filing [2]. The filing states that increasing scrutiny regarding AI governance and risk management is occurring [2]. It also notes risks associated with expanded use of AI, including increased data risk, unpredictable system interactions, inadequate controls, potential for AI failure, and operational, legal, regulatory, and reputational harm [2].

**Citations:**

- [1] JPMorgan_Chase_10K_2024-02-16.htm
- [2] Bank_of_America_10K_2026-02-25.htm


****
### 2. ai_governance_committees_comparison
**Query:** Which of JPMorgan, Bank of America, or Citigroup have established dedicated AI governance committees, and how do their oversight structures differ?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['AI', 'governance', 'committee', 'JPMorgan']`
**Retrieval query:** Which of JPMorgan, Bank of America, or Citigroup have established dedicated AI governance committees, and how do their oversight structures differ? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `gemma3:12b` | **Latency:** 61.54s | **Pass:** ✅ | **Citation density:** 0.444

**Answer:**

> Citigroup has established a Transformation Oversight Committee that reviews actions related to Citi’s risk and control environment [1]. Additionally, the Citigroup CEO has established four standing Executive Management Governance Committees that cover primary risks, including one overseeing liquidity and market risk [1]. These committees review policies and programs [1].
>
> JPMorgan Chase's Board of Directors actively oversees the business through principal standing committees [2]. The Firmwide Risk Committee escalates to the Board Risk Committee [2]. JPMorgan Chase’s filings do not describe a dedicated AI governance committee, but mention that risk governance supports escalation of risks and issues to senior management and the Board of Directors [2].
>
> Bank of America states that it has policies and procedures to help facilitate oversight of cybersecurity risk, with reporting to executive management and committees [3]. They also note increasing scrutiny regarding sustainability-related policies, goals, targets, and disclosure could result in litigation [4]. Bank of America's filings do not describe a dedicated AI governance committee.

**Citations:**

- [1] Citigroup_10K_2026-02-20.htm
- [2] JPMorgan_Chase_10K_2026-02-13.htm
- [3] Bank_of_America_10K_2025-02-25.htm
- [4] Bank_of_America_10K_2026-02-25.htm


****
### 3. cyber_disclosure_2022_vs_2026
**Query:** Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged?
**Entity filter:** `['JPMorgan_Chase', 'Citigroup']` | **Keywords sent:** `['cybersecurity', 'JPMorgan', 'Citigroup', 'risk management']`
**Retrieval query:** Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged? JPMorgan Chase & Co Citigroup Inc
**Model:** `gemma3:12b` | **Latency:** 35.7s | **Pass:** ✅ | **Citation density:** 0.364

**Answer:**

> In 2022, JPMorgan Chase’s cybersecurity risk management framework was described as being integrated into the firm's operational risk management framework [1]. The governance structure for the Global Cybersecurity and Technology Controls organization was designed to identify, escalate, and mitigate cybersecurity risks [1]. The CISO reported to the Global Chief Information Officer and led the Global Cybersecurity and Technology Controls organization responsible for identifying technology and cybersecurity risks [1].
>
> In 2026, JPMorgan Chase’s description of its cybersecurity risk management framework remains integrated into the firm's operational risk management framework [2]. The governance structure continues to be designed to identify, escalate, and mitigate cybersecurity risks [2]. A key change is that the Cybersecurity and Technology Controls Operating Committee (CTOC) now oversees the implementation and maintenance of appropriate controls in support of the Firm’s Information Security Program [2].
>
> In 2022, Citigroup described its cybersecurity risk management program as being built on three lines of defense [3]. The Chief Information Security Officer (CISO) led the first line of defense, providing frontline business, operational and technical controls [3]. Citi actively participated in knowledge-sharing groups to enhance preparedness and resilience [3].
>
> In 2026, Citigroup's cybersecurity risk management continues to be overseen by the Risk Management Committee, which monitors performance against a Cybersecurity Risk Appetite Statement quarterly [4]. A key change is that the Board would now be made aware of potentially material cybersecurity incidents via communication lines from the Chief Information Security Office to senior management and the Board [4].

**Citations:**

- [1] JPMorgan_Chase_10K_2024-02-16.htm
- [2] JPMorgan_Chase_10K_2026-02-13.htm
- [3] Citigroup_10K_2024-02-23.htm
- [4] JPMorgan_Chase_10K_2025-02-14.htm


****
### 4. climate_risk_evolution
**Query:** How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework?
**Entity filter:** `['Bank_of_America', 'Citigroup']` | **Keywords sent:** `['climate', 'risk', 'Bank of America', 'Citigroup', 'Net Zero']`
**Retrieval query:** How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework? Citigroup Inc Bank of America Corporation
**Model:** `gemma3:12b` | **Latency:** 39.36s | **Pass:** ✅ | **Citation density:** 0.455

**Answer:**

> Bank of America’s disclosures regarding climate risk evolved since 2022; in 2023, they created an internal Climate Risk Framework that addresses how the corporation identifies, measures, monitors, and controls climate risk [1]. This framework enhances existing risk management processes and details roles and responsibilities across different lines of defense [1]. In 2021, Bank of America publicly announced a commitment to achieve net zero emissions by 2050 [2]. They also announced targets in 2022 to reduce emissions associated with financing activities related to auto manufacturing, energy, and power generation by 2030 [2].
>
> Citigroup’s disclosures regarding climate risk have also evolved since 2022; in 2023, they developed a Climate Risk Management Framework (Climate RMF) that provides information on governance, roles, responsibilities, and principles for managing climate risks [3]. In 2024, Citi continued to enhance methodologies for quantifying how climate risks could impact the credit profiles of its clients [4]. They also stated that climate risk is an overarching risk that can act as a driver of other categories of risk [5].
>
> Bank of America has a more detailed Net Zero or transition risk framework. In 2021, they announced a commitment to achieve net zero emissions by 2050 and set 2030 targets for emissions related to financing activities [2]. They also released an "Approach to Zero" framework in 2022 [1]. Citigroup's disclosures mention a Net Zero plan implementation leading to integration of climate risk discussions into client engagement [3], but lack the specificity of Bank of America’s published framework and targets [2,1].

**Citations:**

- [1] Bank_of_America_10K_2024-02-20.htm
- [2] Bank_of_America_10K_2023-02-22.htm
- [3] Citigroup_10K_2024-02-23.htm
- [4] Citigroup_10K_2025-02-21.htm
- [5] Citigroup_10K_2026-02-20.htm


****
### 5. capital_ratios_trend
**Query:** How have CET1 capital ratios and total revenues trended at JPMorgan, Bank of America, and Citigroup from FY2021 through FY2025? Identify any consistent leaders or laggards.
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['CET1', 'capital', 'JPMorgan', 'Bank of America', 'revenue']`
**Retrieval query:** How have CET1 capital ratios and total revenues trended at JPMorgan, Bank of America, and Citigroup from FY2021 through FY2025? Identify any consistent leaders or laggards. JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `gemma3:12b` | **Latency:** 108.81s | **Pass:** ✅ | **Citation density:** 0.471

**Answer:**

> Here's a summary of the CET1 capital ratios and total revenues trends for JPMorgan Chase, Bank of America, and Citigroup from FY2021 through FY2025, based solely on the provided sources.
>
> **Citigroup**
>
> *   **CET1 Capital Ratio:** As of December 31, 2021, Citi’s CET1 Capital ratio was 13.0% [1]. It increased to 13.4% as of December 31, 2023 [2], and decreased to 13.2% as of December 31, 2025 [3]. The decrease in 2025 was primarily driven by common share repurchases, an increase in RWA, and the payment of dividends [3].
> *   **Total Revenues:** Total revenues were $15,665 in 2022 [1], $18,102 in 2023 [4], and $19,649 in 2024 [4].
>
> **Bank of America**
>
> *   **CET1 Capital Ratio:** Bank of America’s CET1 capital ratio was 11.8% as of December 31, 2023 [5].
> *   **Total Revenues:** Total revenue information is not provided in the sources.
>
> **JPMorgan Chase**
>
> *   **CET1 Capital Ratio:** As of December 31, 2021, JPMorgan Chase’s CET1 capital ratio was 13.8% [6]. It increased to 13.6% as of December 31, 2023 [7], and decreased slightly to an unspecified value as of December 31, 2024 [8].
> *   **Total Revenues:** Total revenue information is not provided in the sources.
>
> **Consistent Leaders/Laggards**
>
> Based solely on the available data, it's difficult to definitively identify consistent leaders or laggards across all three banks for either CET1 capital ratios or total revenues due to limited data points and varying reporting methodologies.

**Citations:**

- [1] Citigroup_10K_2023-02-27.htm
- [2] Citigroup_10K_2024-02-23.htm
- [3] Citigroup_10K_2026-02-20.htm
- [4] Citigroup_10K_2025-02-21.htm
- [5] Bank_of_America_10K_2024-02-20.htm
- [6] JPMorgan_Chase_10K_2022-02-22.htm
- [7] JPMorgan_Chase_10K_2024-02-16.htm
- [8] JPMorgan_Chase_10K_2025-02-14.htm


****
### 6. digital_banking_strategy
**Query:** How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['digital', 'technology', 'JPMorgan', 'Bank of America', 'Citigroup']`
**Retrieval query:** How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `gemma3:12b` | **Latency:** 59.77s | **Pass:** ✅ | **Citation density:** 0.786

**Answer:**

> JPMorgan Chase, Bank of America, and Citigroup have consistently highlighted the impact of emerging technologies on their digital banking strategies and technology investment priorities over the last five years (2021-2025).
>
> **JPMorgan Chase:** From 2022 to 2026, JPMorgan Chase’s filings repeatedly mention non-depository institutions offering traditional banking products due to technological advances [1,2,3]. They specifically note the rise of electronic securities trading, cryptocurrency trading, and online algorithmic investment advice [1,2,3]. In 2026, they emphasize the need to keep pace with rapidly changing technologies, including generative AI, to avoid losing market share [4].
>
> **Bank of America:** Bank of America’s filings from 2022 and 2024 highlight increased reliance on digital banking services due to the pandemic [5,6]. They note that emerging technologies like analytic capabilities, self-service digital trading platforms, and automated trading markets are impacting the competitive landscape [5,6]. In 2025, they specifically mention AI and machine learning as key areas of investment and acknowledge the potential for disruption from nonbank digital asset ecosystems [7,8].
>
> **Citigroup:** Citigroup’s filings from 2021 to 2026 consistently address competition from non-traditional financial services firms, particularly fintech companies offering technology-driven solutions [9,10,11]. They acknowledge the increasing interest in digital assets and cryptocurrencies among clients and investors [9,11]. Citigroup’s 2026 filing specifically mentions that emerging technologies like AI and digital assets could make certain products less competitive [11].
>
> **Major Themes:**
> *   **Competition from Fintech:** All three firms consistently acknowledge the growing competition from fintech companies leveraging technology to offer financial services.
> *   **Digital Asset Evolution:** The evolving landscape of digital assets, including cryptocurrencies and stablecoins, is a recurring theme across all filings.
> *   **AI Integration:** Artificial intelligence (AI) and machine learning are increasingly recognized as critical areas for investment and potential disruption.
> *   **Need for Adaptation:** Each firm emphasizes the need to adapt products and services to rapidly evolving industry standards and consumer preferences.

**Citations:**

- [1] JPMorgan_Chase_10K_2022-02-22.htm
- [2] JPMorgan_Chase_10K_2024-02-16.htm
- [3] JPMorgan_Chase_10K_2023-02-21.htm
- [4] JPMorgan_Chase_10K_2026-02-13.htm
- [5] Bank_of_America_10K_2022-02-22.htm
- [6] Bank_of_America_10K_2024-02-20.htm
- [7] Bank_of_America_10K_2025-02-25.htm
- [8] Bank_of_America_10K_2026-02-25.htm
- [9] Citigroup_10K_2022-02-28.htm
- [10] Citigroup_10K_2023-02-27.htm
- [11] Citigroup_10K_2026-02-20.htm


****
### 7. regulatory_burden_evolution
**Query:** What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging?
**Entity filter:** `['JPMorgan_Chase', 'Citigroup']` | **Keywords sent:** `['regulatory', 'capital', 'JPMorgan', 'Citigroup']`
**Retrieval query:** What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging? JPMorgan Chase & Co Citigroup Inc
**Model:** `gemma3:12b` | **Latency:** 35.49s | **Pass:** ✅ | **Citation density:** 0.467

**Answer:**

> JPMorgan Chase disclosed in its 2025 filing that the Federal Reserve’s Vice Chair for Supervision indicated potential updates to the U.S. risk-based capital framework may be issued in early 2026 [1]. Additionally, JPMorgan noted finalized rules implementing Basel III frameworks became effective in the EU beginning January 1, 2025, with market risk aspects expected to be delayed until January 1, 2027, and a similar delay announced for the U.K. [2]. In contrast, the 2022 filing highlighted that maintaining regulatory capital equal to or in excess of minimums would result in limitations on distributions like dividends and share repurchases [3].
>
> Citigroup’s 2025 filing mentions potential changes to U.S. laws or regulations regarding credit cards, including a possible interest rate cap, alongside ongoing developments with the U.S. regulatory capital framework [4]. Their 2023 filing indicated that Citi faces "ongoing regulatory and legislative uncertainties and changes" [5]. In 2022, Citigroup noted an increase in their required CET1 Capital ratio due to a GSIB surcharge and paused common share repurchases [6].
>
> A shared challenge for both firms appears to be the ongoing interpretation and implementation of extensive and frequently changing regulatory and legislative requirements [7,5,4].

**Citations:**

- [1] JPMorgan_Chase_10K_2026-02-13.htm
- [2] JPMorgan_Chase_10K_2025-02-14.htm
- [3] JPMorgan_Chase_10K_2023-02-21.htm
- [4] Citigroup_10K_2026-02-20.htm
- [5] Citigroup_10K_2024-02-23.htm
- [6] Citigroup_10K_2023-02-27.htm
- [7] Citigroup_10K_2025-02-21.htm


****
### 8. cyber_goldman
**Query:** How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K?
**Entity filter:** `['Goldman_Sachs']` | **Keywords sent:** `['cybersecurity', 'Goldman Sachs', 'risk management', 'oversight']`
**Retrieval query:** How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K? The Goldman Sachs Group, Inc.
**Model:** `gemma3:12b` | **Latency:** 28.28s | **Pass:** ✅ | **Citation density:** 0.571

**Answer:**

> Goldman Sachs describes its cybersecurity risk-management framework as including preventive and detective controls and processes to mitigate emerging threats [1,2]. The Cybersecurity Program is administered by Technology Risk within Engineering and overseen by the Chief Information Security Officer (CISO) [3,4]. A dedicated Operational Risk team, reporting to the chief risk officer, provides oversight of the Cybersecurity Program and assesses its effectiveness against industry standards and Board-approved limits [1,2,3,4].
>
> The firm’s process for managing cybersecurity risk includes training and education, identity and access management, application security, infrastructure security, mobile security, data security, cloud computing governance, and technology operations [2,3]. Technology Risk monitors threats and allocates resources to mitigate risks, including emphasizing phishing and cybersecurity training for employees in response to AI-enabled fraud and ransomware attacks [1,2,3].
>
> Board oversight is provided through the Risk Committee and Technology Risk Subcommittee, which receive periodic briefings from the CISO, chief information officer, and chief technology officer on operational and technology risks, including cybersecurity risks [1,2,3,4]. The Firmwide Artificial Intelligence Risk and Controls Committee also assists the Firmwide Technology Risk Committee [1,2].

**Citations:**

- [1] GOLDMAN_SACHS_GROUP_INC_10K_2026-02-25.htm
- [2] Goldman_Sachs_10K_2026-02-25.htm
- [3] Goldman_Sachs_10K_2025-02-27.htm
- [4] Goldman_Sachs_10K_2024-02-23.htm


****
### 9. revenue_sources_blackrock
**Query:** What does BlackRock identify as its principal sources of revenue in its most recent 10-K?
**Entity filter:** `['BlackRock']` | **Keywords sent:** `['BlackRock', 'revenue', 'investment advisory', 'fees']`
**Retrieval query:** What does BlackRock identify as its principal sources of revenue in its most recent 10-K?
**Model:** `gemma3:12b` | **Latency:** 38.48s | **Pass:** ❌ | **Citation density:** 1.0

**Answer:**

> BlackRock identifies its principal sources of revenue as asset management, performance fees, and securities lending [1].

**Citations:**

- [1] BlackRock,_Inc._10K_2026-02-25.htm

**Missing keywords:** ['investment advisory']

****
### 10. net_revenue_jpm
**Query:** What was JPMorgan Chase's total net revenue for fiscal 2024 as reported in its consolidated statements of income?
**Entity filter:** `['JPMorgan_Chase']` | **Keywords sent:** `['JPMorgan', 'net revenue']`
**Retrieval query:** What was JPMorgan Chase's total net revenue for fiscal 2024 as reported in its consolidated statements of income? JPMorgan Chase & Co
**Model:** `gemma3:12b` | **Latency:** 70.69s | **Pass:** ✅ | **Citation density:** 0.5

**Answer:**

> JPMorgan Chase reported total net revenue of $177.6 billion for fiscal year 2024, up 12% [1].

**Citations:**

- [1] JPMorgan_Chase_10K_2025-02-14.htm

