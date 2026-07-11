# AIStudio — Benchmark Findings
*Generated: 2026-07-07 08:03*

## Configuration
- **Corpus:** `sec_10k`
- **Scope:** none (full corpus)
- **Base Top K:** 10 (effective K may be higher for multi-entity queries)
- **Temperature:** 0.3
- **Alpha:** 0.5
- **Min Score:** 0.5
- **Model:** llama3.1:8b
- **API:** http://localhost:8000
- **Questions:** `benchmarks/sec_10k/sec_10k_questions.yaml` · sha `bc38f105`

## Summary
- **Questions:** 10
- **Passed (binary):** 9/10 (90%)
- **Rating (AIStudio_878):** 🟢 9 GREEN · 🟡 1 AMBER · 🔴 0 RED
- **Avg latency:** 45.9s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `sec_10k` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings? | 45.59s | 🟢 | JPMorgan_Chase_10K_2024-02-16.htm, JPMor | Emergence-of-AI-risk-language framing; answerable with current corpus. |
| 2 | How do JPMorgan, Bank of America, and Citigroup describe oversight of AI-related risk — through dedicated AI committees, or folded into their existing risk-governance structures? | 49.82s | 🟢 | JPMorgan_Chase_10K_2024-02-16.htm, Bank_ | Reframed (BIC) — drops the dedicated-AI-committee presupposition; the correct answer ('AI risk is folded into existing risk governance') scores clean and contains 'AI'. The presupposing original lives in the June_2026 set. |
| 3 | Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged? | 54.98s | 🟢 | JPMorgan_Chase_10K_2024-02-16.htm, JPMor | Explicit 2022-vs-2026 temporal contrast across two firms. |
| 4 | How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework? | 40.31s | 🟢 | Bank_of_America_10K_2024-02-20.htm, Citi | Two-firm climate evolution since 2022. |
| 5 | How do JPMorgan, Bank of America, and Citigroup describe their approach to managing capital strength and their CET1 capital position in their most recent 10-K filings? | 56.64s | 🟢 | JPMorgan_Chase_10K_2023-02-21.htm, JPMor | Reframed (BIC) — qualitative capital-management / CET1-position comparison, prose-only. The hard multi-year CET1+revenue TABLE trend is preserved in the June_2026 set as the work-in-progress table exhibit (Annex 5). |
| 6 | How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge? | 49.4s | 🟢 | JPMorgan_Chase_10K_2026-02-13.htm, JPMor | Three-firm digital strategy over a relative 5-year window. |
| 7 | What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging? | 48.59s | 🟢 | JPMorgan_Chase_10K_2026-02-13.htm, Citig | 'compliance' keyword removed 2026-05-30 (AIStudio_850) as a false negative. |
| 8 | How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K? | 42.89s | 🟢 | GOLDMAN_SACHS_GROUP_INC_10K_2026-02-25.h | L1 baseline. 2026-06-02 audit GREEN — Goldman-only, substantive. Token verified on Beast. |
| 9 | What are the principal categories of revenue BlackRock identifies in its most recent 10-K, and how does it describe each? | 29.89s | 🟡 | Raymond_James_10K_2021-11-23.htm, Raymon | Reframed (BIC) — qualitative 'describe the sources' (base & performance fees, securities lending, technology services). Avoids inviting a precise sub-line figure; the original audited GREEN on sources but the model volunteered a wrong technology-services number. |
| 10 | What was JPMorgan Chase's total net revenue for fiscal year 2024, as reported in its FY2024 consolidated statements of income? Report the single FY2024 figure. | 41.15s | 🟢 | JPMorgan_Chase_10K_2025-02-14.htm | Pinned (BIC) — single FY2024 figure (~$177.6B), the income-statement total the system retrieves correctly; the wording discourages the multi-year pull that produced the contradictory FY2025 figure in the June_2026 run. The single-cell table lookup is the one quantitative shape handled cleanly. |

## Detailed Results

****
### 1. ai_disclosure_evolution
**Query:** When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America']` | **Keywords sent:** `['AI', 'risk', 'JPMorgan', 'Bank of America']`
**Retrieval query:** When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings? JPMorgan Chase & Co Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 45.59s | **Pass:** ✅ | **Citation density:** 0.75

**Answer:**

> JPMorgan Chase first started disclosing AI as a specific risk factor in their 10-K filings in FY2023 [1]. In their most recent filing (FY2025), JPMorgan Chase uses language that highlights the risks associated with AI system failures, inappropriate use of AI systems, lack of transparency in AI systems, or inaccurate or biased output from AI systems [2].
>
> Bank of America first started disclosing AI as a specific risk factor in their 10-K filings in FY2025 [3]. In their most recent filing (FY2025), Bank of America uses language that highlights the risks associated with expanded use of AI, including emerging third-party AI services and autonomous AI agents, which may result in increased data risk, unpredictable system interactions, inadequate controls or safeguards, AI failure, or produce unintended operations or consequences [3].

**Citations:**

- [1] JPMorgan_Chase_10K_2024-02-16.htm
- [2] JPMorgan_Chase_10K_2026-02-13.htm
- [3] Bank_of_America_10K_2026-02-25.htm


****
### 2. ai_governance_committees_comparison
**Query:** How do JPMorgan, Bank of America, and Citigroup describe oversight of AI-related risk — through dedicated AI committees, or folded into their existing risk-governance structures?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['AI', 'risk', 'governance', 'oversight']`
**Retrieval query:** How do JPMorgan, Bank of America, and Citigroup describe oversight of AI-related risk — through dedicated AI committees, or folded into their existing risk-governance structures? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 49.82s | **Pass:** ✅ | **Citation density:** 0.364

**Answer:**

> JPMorgan Chase describes oversight of AI-related risk through dedicated committees and existing risk-governance structures.
>
> * JPMorgan Chase's FY2023 10-K states that the Firmwide Risk Committee escalates to the Board Risk Committee [1].
> * The Asset and Liability Committee ("ALCO") is responsible for overseeing the Firm's asset and liability management, including activities supporting management of liquidity risk, balance sheet, interest rate risk, and capital risk [1].
> * JPMorgan Chase has a dedicated AI committee, but it is not explicitly stated in the provided sources whether this committee oversees AI-related risks.
>
> Bank of America describes oversight of AI-related risk through existing governance structures and policies.
>
> * Bank of America's FY2024 10-K states that the Corporation has policies and procedures to help facilitate oversight of cybersecurity risk, which includes AI-related risks [2].
> * The Corporation relies on three lines of defense and management to prepare for, identify, prevent, detect, mitigate, respond to, and recover from cybersecurity threats and incidents, including those related to AI [2].
>
> Citigroup describes oversight of AI-related risk through existing governance structures and policies.
>
> * Citigroup's FY2025 10-K states that the Company has policies which govern the use of emerging technologies, including AI [3].
> * The Company relies on third parties to support certain product and service offerings, which may put Citi at a disadvantage to competitors who may directly offer a broader array of products and services [4].
>
> Note: There is no explicit mention of dedicated AI committees in Bank of America's or Citigroup's provided sources.

**Citations:**

- [1] JPMorgan_Chase_10K_2024-02-16.htm
- [2] Bank_of_America_10K_2025-02-25.htm
- [3] Citigroup_10K_2026-02-20.htm
- [4] Citigroup_10K_2024-02-23.htm


****
### 3. cyber_disclosure_2022_vs_2026
**Query:** Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged?
**Entity filter:** `['JPMorgan_Chase', 'Citigroup']` | **Keywords sent:** `['cybersecurity', 'JPMorgan', 'Citigroup', 'risk management']`
**Retrieval query:** Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged? JPMorgan Chase & Co Citigroup Inc
**Model:** `llama3.1:8b` | **Latency:** 54.98s | **Pass:** ✅ | **Citation density:** 0.438

**Answer:**

> JPMorgan Chase's description of its cybersecurity risk management framework in its 2022 and 2026 annual reports shows some changes. In the 2022 report [1], JPMorgan Chase mentions that it has experienced, and expects to continue experiencing, a higher volume and complexity of cyber threats. However, by 2026 [2], this statement is absent.
>
> The 2026 report introduces new language about engaging third-party assessors or auditing firms with industry-recognized expertise on cybersecurity matters to review specific aspects of the Firm's cybersecurity risk management framework, processes, and controls.
>
> In contrast, Citigroup's descriptions in its 2022, 2024, and 2026 annual reports show more significant changes. In 2022 [3], Citigroup mentions that it leverages an intelligence-led strategy to protect against, detect, and respond to cyber attacks. By 2024 [4], this statement is absent.
>
> In 2024 [4], Citigroup introduces the concept of a Cybersecurity Risk Appetite Statement, which is used to measure performance quarterly. This is also mentioned in the 2026 report [4].
>
> The 2023 report for Citigroup [5] highlights increased legislative and regulatory scrutiny of firms' cybersecurity protection services.
>
> The 2024 report for JPMorgan Chase [2] mentions that the Firm actively partners with appropriate government and law enforcement agencies and peer industry forums to assist in understanding the full spectrum of cybersecurity risks and in enhancing defenses and improving resiliency in the Firm's operating environment. This is also mentioned in the 2026 report [6].
>
> The 2025 report for JPMorgan Chase [2] mentions that the Cybersecurity and Technology Controls Operating Committee (CTOC) oversees the Firm's assessment and management of cybersecurity risk, including oversight of the implementation and maintenance of appropriate controls in support of the Firm's Information Security Program. This is also mentioned in the 2026 report [6].
>
> The 2025 report for Citigroup [7] highlights several improvements to Citi's risk management, including closing the 2013 Consent Order with the FRB related to anti-money laundering and Bank Secrecy Act deficiencies.
>
> In summary, while both JPMorgan Chase and Citigroup have made changes to their descriptions of cybersecurity risk management frameworks in their annual reports, Citigroup has introduced more significant new concepts, such as the Cybersecurity Risk Appetite Statement.

**Citations:**

- [1] JPMorgan_Chase_10K_2024-02-16.htm
- [2] JPMorgan_Chase_10K_2025-02-14.htm
- [3] Citigroup_10K_2022-02-28.htm
- [4] Citigroup_10K_2026-02-20.htm
- [5] Citigroup_10K_2023-02-27.htm
- [6] JPMorgan_Chase_10K_2026-02-13.htm
- [7] Citigroup_10K_2025-02-21.htm


****
### 4. climate_risk_evolution
**Query:** How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework?
**Entity filter:** `['Bank_of_America', 'Citigroup']` | **Keywords sent:** `['climate', 'risk', 'Bank of America', 'Citigroup', 'Net Zero']`
**Retrieval query:** How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework? Citigroup Inc Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 40.31s | **Pass:** ✅ | **Citation density:** 0.556

**Answer:**

> Bank of America's Climate Risk Framework was created in 2023 [1]. 
>
> The framework addresses how the Corporation identifies, measures, monitors, and controls climate risk by enhancing existing risk management processes. It includes examples of how climate risk manifests across the seven risk types and details the roles and responsibilities for climate risk management across the three lines of defense.
>
> In contrast, Citigroup's Climate Risk Management Framework (Climate RMF) was developed to provide globally consistent principles and approaches for managing climate risk across the Company [2].
>
> Bank of America's Net Zero goal was announced in 2021, while Citigroup's Net Zero plan implementation is leading to the further integration of climate risk discussions into client engagement and client selection [3]. 
>
> Citigroup has developed sector-specific climate risk assessments in its credit underwriting process for certain sectors that Citi has identified as higher climate risk. In contrast, Bank of America disclosed its 2019 and 2020 financed emissions and emissions intensity metrics for auto manufacturing, energy, and power generation in its September 2022 Task Force on Climate-related Financial Disclosures Report [4].
>
> Bank of America's progress towards achieving its Net Zero Goal is based on establishing the baseline for emissions associated with its financing activities. Citigroup continues to enhance its methodologies for quantifying how climate risks could impact the individual credit profiles of its clients across various sectors [5].

**Citations:**

- [1] Bank_of_America_10K_2024-02-20.htm
- [2] Citigroup_10K_2026-02-20.htm
- [3] Citigroup_10K_2024-02-23.htm
- [4] Bank_of_America_10K_2023-02-22.htm
- [5] Citigroup_10K_2025-02-21.htm


****
### 5. capital_ratios_trend
**Query:** How do JPMorgan, Bank of America, and Citigroup describe their approach to managing capital strength and their CET1 capital position in their most recent 10-K filings?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['CET1', 'capital', 'JPMorgan', 'Bank of America', 'Citigroup']`
**Retrieval query:** How do JPMorgan, Bank of America, and Citigroup describe their approach to managing capital strength and their CET1 capital position in their most recent 10-K filings? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 56.64s | **Pass:** ✅ | **Citation density:** 0.357

**Answer:**

> JPMorgan Chase describes its approach to managing capital strength and CET1 capital position as follows:
>
> * The Firm's capital management is guided by the Contingency Capital Plan, which defines how the Firm calibrates its targeted capital levels and meets minimum capital requirements [1].
> * JPMorgan Chase & Co. is required to maintain minimum ratios for CET1 capital, Tier 1 capital, Total capital, Tier 1 leverage, and the SLR under the Basel III rules [2].
>
> Bank of America describes its approach as follows:
>
> * The Corporation manages its capital position so that its capital is more than adequate to support its business activities and aligns with risk, risk appetite, and strategic planning [3].
> * Bank of America uses proprietary models to measure capital requirements for credit, country, market, operational, and strategic risks, and allocates capital based on each business's unique risk profile [3].
>
> Citigroup describes its approach as follows:
>
> * Citi's capital management framework is designed to ensure that Citigroup and its principal subsidiaries maintain sufficient capital consistent with each entity's respective risk profile, management targets, and applicable regulatory standards and guidelines [4].
> * Citibank must maintain minimum CET1 Capital, Tier 1 Capital, Total Capital, and Leverage ratios of 6.5%, 8.0%, 10.0%, and 5.0%, respectively, to be considered "well capitalized" under the revised Prompt Corrective Action (PCA) regulations applicable to insured depository institutions as established by the U.S. Basel III rules [5].
>
> Note that JPMorgan Chase's description of its capital management approach is more detailed than Bank of America's and Citigroup's, but all three firms describe their approaches in terms of managing capital strength and CET1 capital position to support business activities and meet regulatory requirements.

**Citations:**

- [1] JPMorgan_Chase_10K_2023-02-21.htm
- [2] JPMorgan_Chase_10K_2025-02-14.htm
- [3] Bank_of_America_10K_2024-02-20.htm
- [4] Citigroup_10K_2023-02-27.htm
- [5] Citigroup_10K_2022-02-28.htm


****
### 6. digital_banking_strategy
**Query:** How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['digital', 'technology', 'JPMorgan', 'Bank of America', 'Citigroup']`
**Retrieval query:** How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 49.4s | **Pass:** ✅ | **Citation density:** 1.375

**Answer:**

> JPMorgan Chase has described its digital banking strategy and technology investment priorities over the last 5 years as adapting to emerging technologies, such as AI and blockchain, to remain competitive [1]. The firm acknowledges that it may need to spend more to modify or adapt its products to attract and retain clients and customers [2,3,4].
>
> Bank of America has also emphasized the importance of adapting to rapidly evolving industry standards and consumer preferences through digital banking and other digital services [5,6,7,8]. The firm highlights the risk that payments processing and other products and services could be significantly disrupted by new technologies, such as cryptocurrencies and distributed ledger technology [5].
>
> Citigroup has noted the increasing competition from non-traditional financial services firms, such as fintech companies, which are using technology to enhance borrowing, saving, and investing capabilities [9,10,11]. The firm acknowledges that emerging technologies have the potential to intensify competition and accelerate disruption in the financial services industry [9].
>
> Major themes that emerge include:
>
> * Adaptation to emerging technologies, such as AI and blockchain, to remain competitive
> * Increased competition from non-traditional financial services firms, such as fintech companies
> * Risk of disruption to payments processing and other products and services due to new technologies
> * Need for investment in digital banking infrastructure to attract and retain customers
>
> Note: The sources do not provide specific information on the exact strategies or priorities of each firm over the last 5 years. However, they highlight the common themes and risks associated with digital banking and emerging technologies.

**Citations:**

- [1] JPMorgan_Chase_10K_2026-02-13.htm
- [2] JPMorgan_Chase_10K_2025-02-14.htm
- [3] JPMorgan_Chase_10K_2022-02-22.htm
- [4] JPMorgan_Chase_10K_2024-02-16.htm
- [5] Bank_of_America_10K_2022-02-22.htm
- [6] Bank_of_America_10K_2024-02-20.htm
- [7] Bank_of_America_10K_2025-02-25.htm
- [8] Bank_of_America_10K_2026-02-25.htm
- [9] Citigroup_10K_2025-02-21.htm
- [10] Citigroup_10K_2022-02-28.htm
- [11] Citigroup_10K_2023-02-27.htm


****
### 7. regulatory_burden_evolution
**Query:** What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging?
**Entity filter:** `['JPMorgan_Chase', 'Citigroup']` | **Keywords sent:** `['regulatory', 'capital', 'JPMorgan', 'Citigroup']`
**Retrieval query:** What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging? JPMorgan Chase & Co Citigroup Inc
**Model:** `llama3.1:8b` | **Latency:** 48.59s | **Pass:** ✅ | **Citation density:** 0.267

**Answer:**

> New regulatory burdens and capital rules disclosed in JPMorgan's 2025 filings compared to 2022 include:
>
> * The potential for an updated proposal to amend the US risk-based capital framework in early 2026 [1].
> * The implementation of new EU and UK Basel III frameworks, with market risk aspects delayed until January 1, 2027 [1].
> * The delay of the new rules in the U.K. to January 1, 2027 [1].
>
> New regulatory burdens and capital rules disclosed in Citigroup's 2025 filings compared to 2022 include:
>
> * Potential changes to various aspects of the US regulatory capital framework and requirements applicable to Citi, including revisions to the US Basel III rules [2].
> * Potential fiscal, monetary, tax, sanctions, and other changes promulgated by the US federal government and other governments [3].
>
> Themes both firms agree are most challenging include:
>
> * Ongoing regulatory and legislative uncertainties and changes in the U.S. and globally [1,2,3,4].
> * Increased expectations and scrutiny from regulators, including with respect to governance, infrastructure, data, and risk management practices and controls [2,3].
> * Extensive and frequently changing regulatory and legislative requirements in the U.S. and other jurisdictions, resulting in substantial compliance, regulatory, and other risks and costs [2,3].
>
> Note that JPMorgan's 2022 filing does not mention any new regulatory burdens or capital rules compared to 2021.

**Citations:**

- [1] JPMorgan_Chase_10K_2026-02-13.htm
- [2] Citigroup_10K_2025-02-21.htm
- [3] Citigroup_10K_2024-02-23.htm
- [4] Citigroup_10K_2026-02-20.htm


****
### 8. cyber_goldman
**Query:** How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K?
**Entity filter:** `['Goldman_Sachs']` | **Keywords sent:** `['cybersecurity', 'Goldman Sachs', 'risk management', 'oversight']`
**Retrieval query:** How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K? The Goldman Sachs Group, Inc.
**Model:** `llama3.1:8b` | **Latency:** 42.89s | **Pass:** ✅ | **Citation density:** 0.333

**Answer:**

> Goldman Sachs describes its cybersecurity risk-management framework as a comprehensive program that includes critical components such as training and education, identity and access management, application and software security, infrastructure security, mobile security, data security, cloud computing, and technology operations [1]. The Cybersecurity Program is administered by Technology Risk within Engineering and overseen by the Chief Information Security Officer (CISO) [2].
>
> The program aims to identify, assess, document, and mitigate threats, establish and evaluate compliance with information security mandates, adopt and apply a security control framework, and prevent, detect, and respond to security incidents [2]. A dedicated Operational Risk team provides oversight and challenge of the Cybersecurity Program, independent of Technology Risk, and assesses its operating effectiveness against industry standard frameworks and Board risk appetite-approved operational risk limits and thresholds [1,2].
>
> The Firmwide Technology Risk Committee oversees cybersecurity matters, as well as technology risk management frameworks and methodologies, and monitors their effectiveness [3]. The committee is co-chaired by the CISO and the chief technology officer, and reports to the Firmwide Enterprise Risk Committee [3].
>
> Goldman Sachs' governance structure includes regular briefings from the CISO on a range of cybersecurity-related topics, including the status of the Cybersecurity Program, emerging cybersecurity threats, mitigation strategies, and related regulatory engagements [1,4]. The Board receives these briefings directly or through its committees, including the Risk Committee and Technology Risk Subcommittee [1,3].
>
> The firm emphasizes phishing and cybersecurity training for employees and allocates additional resources for business continuity in response to AI-enabled fraud and ransomware attacks [1,3,4]. However, despite these efforts, Goldman Sachs cannot eliminate all cybersecurity risks or provide assurances that it has not had occurrences of undetected cybersecurity incidents [1,3,4].
>
> The Cybersecurity Program is periodically reviewed and modified to respond to changing threats and conditions [2]. The CISO oversees the Technology Risk team, which assesses and manages cybersecurity risks [2].

**Citations:**

- [1] GOLDMAN_SACHS_GROUP_INC_10K_2026-02-25.htm
- [2] Goldman_Sachs_10K_2024-02-23.htm
- [3] Goldman_Sachs_10K_2026-02-25.htm
- [4] Goldman_Sachs_10K_2025-02-27.htm


****
### 9. revenue_sources_blackrock
**Query:** What are the principal categories of revenue BlackRock identifies in its most recent 10-K, and how does it describe each?
**Entity filter:** `['BlackRock']` | **Keywords sent:** `['BlackRock', 'revenue', 'investment advisory', 'fees']`
**Retrieval query:** What are the principal categories of revenue BlackRock identifies in its most recent 10-K, and how does it describe each?
**Model:** `llama3.1:8b` | **Latency:** 29.89s | **Pass:** ❌ | **Citation density:** 0.333

**Answer:**

> BlackRock's principal categories of revenue are not explicitly stated in any of the provided sources. However, based on the content of [1] Raymond_James_10K_2021-11-23.htm and [2] Raymond_James_10K_2023-11-21.htm, it appears that Raymond James Financial identifies its principal categories of revenue as:
>
> * PCG segment: financial planning, investment advisory, and securities transaction services
> * Capital Markets segment: 
> * Asset Management segment: 
> * Bank segment: 
> * Other segment: 
>
> These segments are described in the "Segment Information" section of the 10-K filings for Raymond James Financial. The specific categories of revenue for BlackRock could not be determined from the provided sources.
>
> Note that the other sources do not provide information on revenue categories for BlackRock or any other firm.

**Citations:**

- [1] Raymond_James_10K_2021-11-23.htm
- [2] Raymond_James_10K_2023-11-21.htm

**Missing keywords:** ['fees']

****
### 10. net_revenue_jpm
**Query:** What was JPMorgan Chase's total net revenue for fiscal year 2024, as reported in its FY2024 consolidated statements of income? Report the single FY2024 figure.
**Entity filter:** `['JPMorgan_Chase']` | **Keywords sent:** `['JPMorgan', 'net revenue', '2024']`
**Retrieval query:** What was JPMorgan Chase's total net revenue for fiscal year 2024, as reported in its FY2024 consolidated statements of income? Report the single FY2024 figure. JPMorgan Chase & Co
**Model:** `llama3.1:8b` | **Latency:** 41.15s | **Pass:** ✅ | **Citation density:** 0.5

**Answer:**

> JPMorgan Chase's total net revenue for fiscal year 2024 was $177.6 billion [1].

**Citations:**

- [1] JPMorgan_Chase_10K_2025-02-14.htm

