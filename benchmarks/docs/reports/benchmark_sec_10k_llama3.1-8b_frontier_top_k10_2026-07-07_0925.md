# AIStudio — Benchmark Findings
*Generated: 2026-07-07 09:30*

## Configuration
- **Corpus:** `sec_10k`
- **Scope:** none (full corpus)
- **Base Top K:** 10 (effective K may be higher for multi-entity queries)
- **Temperature:** 0.3
- **Alpha:** 0.5
- **Min Score:** 0.5
- **Model:** llama3.1:8b
- **API:** http://localhost:8000
- **Questions:** `frontier`

## Summary
- **Questions:** 10
- **Passed (binary):** 6/10 (60%)
- **Rating (AIStudio_878):** 🟢 6 GREEN · 🟡 2 AMBER · 🔴 2 RED
- **Avg latency:** 29.1s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `sec_10k` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings? | 14.81s | 🟢 | JPMorgan_Chase_10K_2026-02-13.htm, Bank_ | Emergence-of-AI-risk-language framing; answerable with current corpus. |
| 2 | Which of JPMorgan, Bank of America, or Citigroup have established dedicated AI governance committees, and how do their oversight structures differ? | 41.88s | 🟢 | JPMorgan_Chase_10K_2022-02-22.htm, Bank_ | 3-firm comparison. 2026-06-02 audit AMBER — answers drift to general risk committees; missing 'AI' is a genuine drift signal, not a phrasing artifact. Keyword retained deliberately. |
| 3 | Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged? | 16.32s | 🟢 | JPMorgan_Chase_10K_2025-02-14.htm, Citig | Explicit 2022-vs-2026 temporal contrast across two firms. |
| 4 | How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework? | 19.44s | 🟢 | Bank_of_America_10K_2022-02-22.htm, Bank | Two-firm climate evolution since 2022. |
| 5 | How have CET1 capital ratios and total revenues trended at JPMorgan, Bank of America, and Citigroup from FY2021 through FY2025? Identify any consistent leaders or laggards. | 76.56s | 🟢 | Citigroup_10K_2023-02-27.htm, Citigroup_ | The stacked case — 3 firms × FY2021-FY2025 × quantitative table. Heaviest question (~114s). |
| 6 | How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge? | 16.1s | 🔴 | — | Three-firm digital strategy over a relative 5-year window. |
| 7 | What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging? | 20.76s | 🟢 | JPMorgan_Chase_10K_2026-02-13.htm, Citig | 'compliance' keyword removed 2026-05-30 (AIStudio_850) as a false negative. |
| 8 | How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K? | 19.96s | 🔴 | — | L1 baseline. 2026-06-02 audit GREEN — Goldman-only, substantive. Token verified on Beast. |
| 9 | What does BlackRock identify as its principal sources of revenue in its most recent 10-K? | 24.94s | 🟡 | BlackRock,_Inc._10K_2026-02-25.htm | L1 baseline. 2026-06-02 audit GREEN — BlackRock-only. Token verified on Beast. |
| 10 | What was JPMorgan Chase's total net revenue for fiscal 2024 as reported in its consolidated statements of income? | 40.44s | 🟡 | JPMorgan_Chase_10K_2025-02-14.htm | L2 — the table-location ∂. 2026-06-02 audit AMBER→fixed — pulled $177.6B FY2024 from the income-statement table; keyword 'total revenue' → 'net revenue' (answer says "total net revenue"). derived=false (figure is stated, not computed — contrast L7). |

## Detailed Results

****
### 1. ai_disclosure_evolution
**Query:** When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America']` | **Keywords sent:** `['AI', 'risk', 'JPMorgan', 'Bank of America']`
**Retrieval query:** When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings? JPMorgan Chase & Co Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 14.81s | **Pass:** ✅ | **Citation density:** 0.333

**Answer:**

> JPMorgan Chase first started disclosing AI as a specific risk factor in their 10-K filings in FY2023 [1]. In the most recent filing (FY2025), JPMorgan Chase mentions that the rapid development and deployment of advanced technologies, including generative and agentic AI systems, present a range of risks to its businesses and operations [1].
>
> Bank of America first started disclosing AI as a specific risk factor in their 10-K filings in FY2025 [2]. In the most recent filing (FY2025), Bank of America mentions that expanded use of AI, including emerging third-party AI services and autonomous AI agents, may result in increased data risk, unpredictable system interactions, inadequate controls or safeguards, AI failure, or produce unintended operations or consequences [2].
>
> Both JPMorgan Chase and Bank of America mention the risks associated with AI, including AI system failures, inappropriate use of AI systems, lack of transparency in AI systems, or inaccurate or biased output from AI systems. They also mention the increased exposure to cyber attacks, system manipulation, or data loss if AI systems are not designed and implemented with appropriate safeguards [1,2].

**Citations:**

- [1] JPMorgan_Chase_10K_2026-02-13.htm
- [2] Bank_of_America_10K_2026-02-25.htm


****
### 2. ai_governance_committees_comparison
**Query:** Which of JPMorgan, Bank of America, or Citigroup have established dedicated AI governance committees, and how do their oversight structures differ?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['AI', 'governance', 'committee', 'JPMorgan']`
**Retrieval query:** Which of JPMorgan, Bank of America, or Citigroup have established dedicated AI governance committees, and how do their oversight structures differ? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 41.88s | **Pass:** ✅ | **Citation density:** 0.5

**Answer:**

> JPMorgan Chase has established a dedicated AI governance committee, the Board Risk Committee [1], which assists the Board in its oversight of management's responsibility to implement a global risk management framework reasonably designed to identify, assess, and manage the Firm's risks. This committee is responsible for approving policies and procedures related to risk management.
>
> Bank of America has not established a dedicated AI governance committee, but it does have a Governance structure that includes policies and procedures to help facilitate oversight of cybersecurity risk [2]. The Corporation's three lines of defense, and management, strive to prepare for, identify, prevent, detect, mitigate, respond to, and recover from cybersecurity threats and incidents.
>
> Citigroup has not established a dedicated AI governance committee. However, it does have an Asset and Liability Committee (ALCO) that oversees the Firm's asset and liability management, including the activities and frameworks supporting management of the balance sheet, liquidity risk, interest rate risk, and capital [3]. Additionally, Citi has policies that govern the use of emerging technologies, including AI [4].
>
> It is worth noting that while JPMorgan Chase has a dedicated AI governance committee, its oversight structure differs from Citigroup's in that it has a more formalized risk management framework with multiple committees overseeing different aspects of risk.

**Citations:**

- [1] JPMorgan_Chase_10K_2022-02-22.htm
- [2] Bank_of_America_10K_2025-02-25.htm
- [3] Citigroup_10K_2026-02-20.htm
- [4] Citigroup_10K_2025-02-21.htm


****
### 3. cyber_disclosure_2022_vs_2026
**Query:** Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged?
**Entity filter:** `['JPMorgan_Chase', 'Citigroup']` | **Keywords sent:** `['cybersecurity', 'JPMorgan', 'Citigroup', 'risk management']`
**Retrieval query:** Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged? JPMorgan Chase & Co Citigroup Inc
**Model:** `llama3.1:8b` | **Latency:** 16.32s | **Pass:** ✅ | **Citation density:** 0.333

**Answer:**

> Comparing JPMorgan Chase's and Citigroup's descriptions of their cybersecurity risk management frameworks in their 2022 versus 2026 annual reports reveals the following changes:
>
> JPMorgan Chase:
> - In 2025, the Firm engages third-party assessors or auditing firms with industry-recognized expertise on cybersecurity matters to review specific aspects of the Firm’s cybersecurity risk management framework, processes and controls [1].
> - The Cybersecurity and Technology Controls Operating Committee (“CTOC”) is the principal management committee that oversees the Firm’s assessment and management of cybersecurity risk [1].
>
> Citigroup:
> - In 2026, Citi's Board would be made aware of a potentially material cybersecurity incident via lines of communication that run from the Chief Information Security Office to senior management and also to the Board [2].
> - The Risk Management Committee (RMC) oversees Citi’s risk profile, which includes cybersecurity risk, and monitors whether Citi is operating within its cybersecurity risk appetite under its mandate to review key operational risks [2].
>
> These changes indicate that both firms have enhanced their cybersecurity risk management frameworks in recent years. JPMorgan Chase has increased the use of third-party assessors and established a more prominent role for the Cybersecurity and Technology Controls Operating Committee, while Citigroup has improved communication with its Board regarding potential cybersecurity incidents and strengthened oversight through the Risk Management Committee.

**Citations:**

- [1] JPMorgan_Chase_10K_2025-02-14.htm
- [2] Citigroup_10K_2026-02-20.htm


****
### 4. climate_risk_evolution
**Query:** How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework?
**Entity filter:** `['Bank_of_America', 'Citigroup']` | **Keywords sent:** `['climate', 'risk', 'Bank of America', 'Citigroup', 'Net Zero']`
**Retrieval query:** How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework? Citigroup Inc Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 19.44s | **Pass:** ✅ | **Citation density:** 0.429

**Answer:**

> Climate Risk Disclosure Evolution:
>
> Bank of America's climate risk disclosure has evolved since 2022. In FY2022, Bank of America publicly announced a goal to achieve net zero greenhouse gas emissions in their financing activities, operations, and supply chain before 2050 [1]. They also released their Approach to Zero TM framework for achieving this goal [2]. By FY2023, Bank of America created an internal Climate Risk Framework that addresses climate risk identification, measurement, monitoring, and control [2].
>
> In contrast, Citigroup's climate risk disclosure has not shown significant evolution since 2022. In FY2022, Citigroup discussed the importance of considering climate-related risks in their credit underwriting process and mentioned developing sector-specific climate risk assessments [3]. However, by FY2023, they were still discussing the challenges of quantifying climate-related risks due to limited data availability [4].
>
> Net Zero or Transition Risk Framework:
>
> Bank of America has a more detailed Net Zero or transition risk framework. In FY2024, Bank of America described their Climate and Environmental Risk Management function, which oversees climate risk management and provides an independent assessment of enterprise-wide climate risks [5]. They also created an internal Climate Risk Framework that addresses various global climate-related laws, rules, regulations, and guidance [5].
>
> In comparison, Citigroup's framework is less detailed. In FY2025, Citigroup mentioned developing globally consistent principles and approaches for managing climate risk through their Climate Risk Management Framework (Climate RMF) [6]. However, the details of this framework are not provided in the sources.
>
> Overall, Bank of America appears to have a more comprehensive approach to climate risk management and disclosure.

**Citations:**

- [1] Bank_of_America_10K_2022-02-22.htm
- [2] Bank_of_America_10K_2024-02-20.htm
- [3] Citigroup_10K_2023-02-27.htm
- [4] Citigroup_10K_2024-02-23.htm
- [5] Bank_of_America_10K_2025-02-25.htm
- [6] Citigroup_10K_2025-02-21.htm


****
### 5. capital_ratios_trend
**Query:** How have CET1 capital ratios and total revenues trended at JPMorgan, Bank of America, and Citigroup from FY2021 through FY2025? Identify any consistent leaders or laggards.
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['CET1', 'capital', 'JPMorgan', 'Bank of America', 'revenue']`
**Retrieval query:** How have CET1 capital ratios and total revenues trended at JPMorgan, Bank of America, and Citigroup from FY2021 through FY2025? Identify any consistent leaders or laggards. JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 76.56s | **Pass:** ✅ | **Citation density:** 0.423

**Answer:**

> CET1 capital ratios:
>
> * Citigroup:
> 	+ FY2021: 12.2% [1]
> 	+ FY2022: 13.0% [1]
> 	+ FY2023: 13.4% [2]
> 	+ FY2024: 13.6% [3]
> 	+ FY2025: 13.2% [4]
> * Bank of America:
> 	+ FY2021: absent
> 	+ FY2022: absent
> 	+ FY2023: 11.8% [5]
> 	+ FY2024: 12.0% [6]
> 	+ FY2025: 11.7% [7]
> * JPMorgan Chase:
> 	+ FY2021: CET1 capital ratio (Basel III Advanced, JPMorgan Chase & Co.): 13.8% [8]
> 	+ FY2022: CET1 capital ratio (Basel III Advanced, JPMorgan Chase & Co.): 15.9% [9]
> 	+ FY2023: CET1 capital ratio (Basel III Advanced, JPMorgan Chase & Co.): 15.3% [10]
> 	+ FY2024: CET1 capital ratio (Basel III Advanced, JPMorgan Chase & Co.): 13.6% [11]
>
> Total revenues:
>
> * Citigroup:
> 	+ FY2021: absent
> 	+ FY2022: $19,645M [3]
> 	+ FY2023: $18,102M [3]
> 	+ FY2024: $19,649M [3]
> 	+ FY2025: absent
> * Bank of America:
> 	+ FY2021: absent
> 	+ FY2022: absent
> 	+ FY2023: $44.8B [6]
> 	+ FY2024: $47.6B [6]
> 	+ FY2025: $49.1B [7]
> * JPMorgan Chase:
> 	+ FY2021: absent
> 	+ FY2022: absent
> 	+ FY2023: absent
> 	+ FY2024: absent
>
> Consistent leaders or laggards:
>
> * Citigroup's CET1 capital ratio has been consistently above 13% from FY2021 to FY2025.
> * Bank of America's CET1 capital ratio has been below the regulatory minimum in FY2022 and FY2023, but increased to 12.0% in FY2024.
> * JPMorgan Chase's CET1 capital ratio has fluctuated between 13.8% and 15.9% from FY2021 to FY2022.
>
> Note: The total revenues for JPMorgan Chase are absent in the provided sources.

**Citations:**

- [1] Citigroup_10K_2023-02-27.htm
- [2] Citigroup_10K_2024-02-23.htm
- [3] Citigroup_10K_2025-02-21.htm
- [4] Citigroup_10K_2026-02-20.htm
- [5] Bank_of_America_10K_2024-02-20.htm
- [6] Bank_of_America_10K_2025-02-25.htm
- [7] Bank_of_America_10K_2026-02-25.htm
- [8] JPMorgan_Chase_10K_2022-02-22.htm
- [9] JPMorgan_Chase_10K_2023-02-21.htm
- [10] JPMorgan_Chase_10K_2024-02-16.htm
- [11] JPMorgan_Chase_10K_2025-02-14.htm


****
### 6. digital_banking_strategy
**Query:** How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['digital', 'technology', 'JPMorgan', 'Bank of America', 'Citigroup']`
**Retrieval query:** How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 16.1s | **Pass:** ❌ | **Citation density:** 0.0

**Answer:**

> JPMorgan Chase has described its digital banking strategy and technology investment priorities over the last 5 years as adapting to emerging technologies, including AI and blockchain, to remain competitive. The firm acknowledges that new competitors in the financial services industry continue to emerge, driven by technological advances and e-commerce growth.
>
> Bank of America's approach focuses on timely adaptation to rapidly evolving industry standards and consumer preferences through a diversified mix of businesses delivering a broad range of financial products and services. The firm recognizes the risk of disruption from emerging technologies, including AI, digital assets, and distributed ledger technology.
>
> Citigroup has emphasized the need to change or adapt its products and services in response to increased competition and emerging technologies. The firm notes that non-traditional financial services firms are expanding their offerings, using technology and mobile platforms to enhance borrowing, saving, and investing capabilities.
>
> Major themes emerging from these descriptions include:
>
> - Adaptation to rapidly evolving industry standards and consumer p


****
### 7. regulatory_burden_evolution
**Query:** What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging?
**Entity filter:** `['JPMorgan_Chase', 'Citigroup']` | **Keywords sent:** `['regulatory', 'capital', 'JPMorgan', 'Citigroup']`
**Retrieval query:** What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging? JPMorgan Chase & Co Citigroup Inc
**Model:** `llama3.1:8b` | **Latency:** 20.76s | **Pass:** ✅ | **Citation density:** 0.389

**Answer:**

> JPMorgan Chase disclosed that it continues to monitor developments and potential impacts related to an updated proposal to amend the U.S. risk-based capital framework, which is expected to be issued by banking regulators in early 2026 [1]. 
>
> Citigroup disclosed that it faces ongoing regulatory and legislative uncertainties and changes, including potential changes to various aspects of the U.S. regulatory capital framework and requirements applicable to Citi [2].
>
> Both firms have not disclosed new regulatory burdens or capital rules in their 2025 filings compared to 2022.
>
> JPMorgan Chase has phased out the CECL capital transition provisions as of January 1, 2025 [1]. 
>
> Citigroup disclosed that it paused common share repurchases beginning as of the third quarter of 2022 due to an increase in the SCB requirement and macroeconomic uncertainty [3].
>
> There are no themes both firms agree are most challenging.
>
> JPMorgan Chase is subject to various regulatory capital requirements, including leverage- and risk-based capital requirements [4]. 
>
> Citigroup's required regulatory CET1 Capital ratio increased to 12% from 11.5% under the Standardized Approach as of January 1, 2023 due to an increase in the GSIB surcharge [3].
>
> JPMorgan Chase is subject to a Stress Capital Buffer (“SCB”) requirement for the coming year, which forms part of the Firm’s applicable capital buffers [5]. 
>
> Citigroup's ability to return capital to shareholders may be impacted by regulatory and legislative uncertainties and changes [6].
>
> Both firms are required to interpret and implement extensive and frequently changing regulatory and legislative requirements in the U.S. and other jurisdictions in which they do business, resulting in substantial compliance, regulatory and other risks and costs [7].

**Citations:**

- [1] JPMorgan_Chase_10K_2026-02-13.htm
- [2] Citigroup_10K_2026-02-20.htm
- [3] Citigroup_10K_2023-02-27.htm
- [4] JPMorgan_Chase_10K_2022-02-22.htm
- [5] JPMorgan_Chase_10K_2025-02-14.htm
- [6] Citigroup_10K_2024-02-23.htm
- [7] Citigroup_10K_2025-02-21.htm


****
### 8. cyber_goldman
**Query:** How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K?
**Entity filter:** `['Goldman_Sachs']` | **Keywords sent:** `['cybersecurity', 'Goldman Sachs', 'risk management', 'oversight']`
**Retrieval query:** How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K? The Goldman Sachs Group, Inc.
**Model:** `llama3.1:8b` | **Latency:** 19.96s | **Pass:** ❌ | **Citation density:** 0.0

**Answer:**

> Goldman Sachs describes its cybersecurity risk-management framework in its most recent 10-K (FY2025) as including critical components of its risk management framework and the following key areas:
>
> • Training and education to enable employees to recognize information and cybersecurity threats
> • Identity and access management, including entitlement management and production access
> • Application and software security, including software change management, open source software, and backup and restoration
> • Infrastructure security, including monitoring for known vulnerabilities and signs of unauthorized attempts to access data and systems
> • Mobile security, including mobile applications
> • Data security, including cryptography and encryption, database security, data erasure, and media disposal
> • Cloud computing, including governance and security of cloud applications, and software-as-a-service data onboarding
> • Technology operations, including change management
>
> The firm's board-level oversight is provided by the Board, which oversees risk management policies and practices, including cybersecurity risks, through its committees, including the Risk Committee and Technology Risk Subcommittee. The chief risk officer, chief information officer, and chief technology officer periodically brief the Board on operational and technology risks, including cybersecurity risks.
>
> In FY2024, Goldman Sachs' board-level oversight was also provided by the Board, which received regular briefings from the CISO on a range of cybersecurity-related topics.
>
> In FY2023, the firm's Cybersecurity Program was overseen by the CISO, who reported directly to the chief information officer. The CISO was responsible for managing and implementing the program and overseeing the Technology Risk team, which assessed and managed cybersecurity risks.
>
> Note that Goldman Sachs' description of its cybersecurity risk-management framework and board-level oversight is consistent across FY2023, FY2024, and FY2025 filings, with some minor variations in language.


****
### 9. revenue_sources_blackrock
**Query:** What does BlackRock identify as its principal sources of revenue in its most recent 10-K?
**Entity filter:** `['BlackRock']` | **Keywords sent:** `['BlackRock', 'revenue', 'investment advisory', 'fees']`
**Retrieval query:** What does BlackRock identify as its principal sources of revenue in its most recent 10-K?
**Model:** `llama3.1:8b` | **Latency:** 24.94s | **Pass:** ❌ | **Citation density:** 0.333

**Answer:**

> BlackRock identifies its principal sources of revenue as management fees from its investment products and services, including exchange-traded funds (ETFs), mutual funds, and separately managed accounts [1].
>
> Note that there is no information on BlackRock's principal sources of revenue in the provided sources for FY2026. The statement above only includes information from the FY2025 filing.

**Citations:**

- [1] BlackRock,_Inc._10K_2026-02-25.htm

**Missing keywords:** ['investment advisory']

****
### 10. net_revenue_jpm
**Query:** What was JPMorgan Chase's total net revenue for fiscal 2024 as reported in its consolidated statements of income?
**Entity filter:** `['JPMorgan_Chase']` | **Keywords sent:** `['JPMorgan', 'net revenue']`
**Retrieval query:** What was JPMorgan Chase's total net revenue for fiscal 2024 as reported in its consolidated statements of income? JPMorgan Chase & Co
**Model:** `llama3.1:8b` | **Latency:** 40.44s | **Pass:** ❌ | **Citation density:** 0.5

**Answer:**

> Total net revenue for fiscal 2024 was $177.6 billion [1].

**Citations:**

- [1] JPMorgan_Chase_10K_2025-02-14.htm

**Missing keywords:** ['JPMorgan']
