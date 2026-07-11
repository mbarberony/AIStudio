# AIStudio — Benchmark Findings
*Generated: 2026-07-07 08:35*

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
- **Passed (binary):** 7/10 (70%)
- **Rating (AIStudio_878):** 🟢 6 GREEN · 🟡 3 AMBER · 🔴 1 RED
- **Avg latency:** 53.0s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `sec_10k` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings? | 57.55s | 🟢 | JPMorgan_Chase_10K_2026-02-13.htm, Bank_ | Emergence-of-AI-risk-language framing; answerable with current corpus. |
| 2 | Which of JPMorgan, Bank of America, or Citigroup have established dedicated AI governance committees, and how do their oversight structures differ? | 37.91s | 🟢 | JPMorgan_Chase_10K_2022-02-22.htm, Bank_ | 3-firm comparison. 2026-06-02 audit AMBER — answers drift to general risk committees; missing 'AI' is a genuine drift signal, not a phrasing artifact. Keyword retained deliberately. |
| 3 | Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged? | 44.52s | 🟢 | JPMorgan_Chase_10K_2026-02-13.htm, Citig | Explicit 2022-vs-2026 temporal contrast across two firms. |
| 4 | How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework? | 48.77s | 🟢 | Bank_of_America_10K_2022-02-22.htm, Bank | Two-firm climate evolution since 2022. |
| 5 | How have CET1 capital ratios and total revenues trended at JPMorgan, Bank of America, and Citigroup from FY2021 through FY2025? Identify any consistent leaders or laggards. | 89.95s | 🟢 | Citigroup_10K_2023-02-27.htm, Citigroup_ | The stacked case — 3 firms × FY2021-FY2025 × quantitative table. Heaviest question (~114s). |
| 6 | How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge? | 85.5s | 🟢 | JPMorgan_Chase_10K_2022-02-22.htm, JPMor | Three-firm digital strategy over a relative 5-year window. |
| 7 | What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging? | 65.52s | 🟡 | JPMorgan_Chase_10K_2026-02-13.htm, Citig ⚠low-density | 'compliance' keyword removed 2026-05-30 (AIStudio_850) as a false negative. |
| 8 | How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K? | 33.39s | 🟡 | GOLDMAN_SACHS_GROUP_INC_10K_2026-02-25.h | L1 baseline. 2026-06-02 audit GREEN — Goldman-only, substantive. Token verified on Beast. |
| 9 | What does BlackRock identify as its principal sources of revenue in its most recent 10-K? | 24.77s | 🔴 | — | L1 baseline. 2026-06-02 audit GREEN — BlackRock-only. Token verified on Beast. |
| 10 | What was JPMorgan Chase's total net revenue for fiscal 2024 as reported in its consolidated statements of income? | 42.25s | 🟡 | JPMorgan_Chase_10K_2025-02-14.htm | L2 — the table-location ∂. 2026-06-02 audit AMBER→fixed — pulled $177.6B FY2024 from the income-statement table; keyword 'total revenue' → 'net revenue' (answer says "total net revenue"). derived=false (figure is stated, not computed — contrast L7). |

## Detailed Results

****
### 1. ai_disclosure_evolution
**Query:** When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America']` | **Keywords sent:** `['AI', 'risk', 'JPMorgan', 'Bank of America']`
**Retrieval query:** When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings? JPMorgan Chase & Co Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 57.55s | **Pass:** ✅ | **Citation density:** 0.3

**Answer:**

> JPMorgan Chase first started disclosing AI as a specific risk factor in their 10-K filings in FY2023 [1]. In the most recent filing (FY2025), JPMorgan Chase mentions that the rapid development and deployment of advanced technologies, including generative and agentic AI systems, present a range of risks to its businesses and operations [1].
>
> Bank of America first started disclosing AI as a specific risk factor in their 10-K filings in FY2025 [2]. In the most recent filing (FY2025), Bank of America mentions that expanded use of AI, including emerging third-party AI services and autonomous AI agents, may result in increased data risk, unpredictable system interactions, inadequate controls or safeguards, AI failure, or produce unintended operations or consequences [2].
>
> In their FY2026 10-K filings, both JPMorgan Chase and Bank of America continue to discuss the risks associated with AI. JPMorgan Chase mentions that AI system failures, inappropriate use of AI systems, lack of transparency in AI systems, or inaccurate or biased output from AI systems could disrupt operations, cause erroneous transactions, compromise data privacy, infringe on intellectual property, harm clients and customers, or impair its ability to make sound business decisions [1]. Bank of America mentions that the proliferation of third-party financial data aggregators and emerging technologies, including AI (such as machine learning and generative AI) and robotics, increases their cybersecurity risks and exposure [3].
>
> In terms of language used in recent filings, JPMorgan Chase uses phrases such as "rapid development and deployment of advanced technologies, including generative and agentic AI systems" to describe the risks associated with AI [1]. Bank of America uses phrases such as "expanded use of AI, including emerging third-party AI services and autonomous AI agents" to describe the risks associated with AI [2].
>
> It is worth noting that neither JPMorgan Chase nor Bank of America mentions AI as a specific risk factor in their FY2021 or FY2022 10-K filings.

**Citations:**

- [1] JPMorgan_Chase_10K_2026-02-13.htm
- [2] Bank_of_America_10K_2026-02-25.htm
- [3] Bank_of_America_10K_2025-02-25.htm


****
### 2. ai_governance_committees_comparison
**Query:** Which of JPMorgan, Bank of America, or Citigroup have established dedicated AI governance committees, and how do their oversight structures differ?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['AI', 'governance', 'committee', 'JPMorgan']`
**Retrieval query:** Which of JPMorgan, Bank of America, or Citigroup have established dedicated AI governance committees, and how do their oversight structures differ? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 37.91s | **Pass:** ✅ | **Citation density:** 0.5

**Answer:**

> JPMorgan Chase has established a dedicated AI governance committee, the Board Risk Committee [1]. The Board Risk Committee assists the Board in its oversight of management's responsibility to implement a global risk management framework reasonably designed to identify, assess, and manage the Firm's risks.
>
> Bank of America has not explicitly mentioned establishing a dedicated AI governance committee. However, it mentions that the Corporation has policies and procedures to help facilitate oversight of cybersecurity risk [2], which includes the use of AI technologies.
>
> Citigroup has established a Transformation Oversight Committee, but its primary focus is on overseeing the actions of Citi's management to develop and execute a transformation of Citi's risk and control environment pursuant to the FRB and OCC Consent Orders [3]. It does not appear to have a dedicated AI governance committee.

**Citations:**

- [1] JPMorgan_Chase_10K_2022-02-22.htm
- [2] Bank_of_America_10K_2025-02-25.htm
- [3] Citigroup_10K_2026-02-20.htm


****
### 3. cyber_disclosure_2022_vs_2026
**Query:** Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged?
**Entity filter:** `['JPMorgan_Chase', 'Citigroup']` | **Keywords sent:** `['cybersecurity', 'JPMorgan', 'Citigroup', 'risk management']`
**Retrieval query:** Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged? JPMorgan Chase & Co Citigroup Inc
**Model:** `llama3.1:8b` | **Latency:** 44.52s | **Pass:** ✅ | **Citation density:** 0.429

**Answer:**

> JPMorgan Chase's description of its cybersecurity risk management framework remains largely consistent between the 2022 and 2026 annual reports. However, there are some subtle changes:
>
> * The 2026 report emphasizes the importance of third-party assessors or auditing firms with industry-recognized expertise on cybersecurity matters to review specific aspects of the Firm's cybersecurity risk management framework, processes, and controls [1].
> * The 2026 report also highlights the role of the Corporate Third-Party Oversight group in managing risks associated with third-party outsourcing, including data loss and business disruptions [1].
>
> In contrast, Citigroup's description of its cybersecurity risk management framework undergoes significant changes between the 2022 and 2026 annual reports:
>
> * The 2026 report introduces a Cybersecurity Risk Appetite Statement, which is used to measure Citi's performance quarterly [2].
> * The 2026 report also emphasizes the importance of contemporaneous reporting on significant cyber events, including incident response, legal obligations (including disclosure), and outreach and notification to regulators and customers when needed [2].
> * In contrast, the 2022 report focuses on Citi's intelligence-led strategy to protect against, detect, and respond to, and recover from cyber attacks [3].
>
> Overall, while both firms continue to emphasize the importance of cybersecurity risk management, Citigroup's approach appears to have become more formalized and structured in its 2026 annual report.

**Citations:**

- [1] JPMorgan_Chase_10K_2026-02-13.htm
- [2] Citigroup_10K_2026-02-20.htm
- [3] Citigroup_10K_2022-02-28.htm


****
### 4. climate_risk_evolution
**Query:** How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework?
**Entity filter:** `['Bank_of_America', 'Citigroup']` | **Keywords sent:** `['climate', 'risk', 'Bank of America', 'Citigroup', 'Net Zero']`
**Retrieval query:** How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework? Citigroup Inc Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 48.77s | **Pass:** ✅ | **Citation density:** 0.312

**Answer:**

> Climate Risk Disclosure Evolution:
>
> Bank of America's climate risk disclosure has evolved since 2022. In FY2022, Bank of America publicly announced its commitment to achieve net zero emissions in its financing activities, operations, and supply chain before 2050 [1]. The company also set 2030 emissions targets for its operations and supply chain [2]. However, the disclosure did not provide detailed information on how these goals would be achieved.
>
> In FY2023, Bank of America created an internal Climate Risk Framework that addresses various global climate-related laws, rules, regulations, and guidance [3]. The framework describes how the Corporation identifies, measures, monitors, and controls climate risk by enhancing existing risk management processes. This indicates a more detailed approach to managing climate risks.
>
> Citigroup's climate risk disclosure has also evolved since 2022. In FY2023, Citigroup continued to enhance its methodologies for quantifying how climate risks could impact individual credit profiles of clients across various sectors [4]. The company developed and embedded sector-specific climate risk assessments in its credit underwriting process for certain sectors identified as higher climate risk.
>
> Comparison:
>
> Bank of America's Climate Risk Framework is more detailed than Citigroup's approach. Bank of America's framework addresses various global climate-related laws, rules, regulations, and guidance, whereas Citigroup's framework focuses on developing globally consistent principles and approaches for managing climate risk across the Company [5].
>
> Net Zero or Transition Risk Framework:
>
> Bank of America has a more detailed Net Zero or transition risk framework than Citigroup. Bank of America's Climate Risk Framework addresses how the Corporation identifies, measures, monitors, and controls climate risk by enhancing existing risk management processes [3]. In contrast, Citigroup's approach focuses on developing globally consistent principles and approaches for managing climate risk across the Company [5].
>
> Note: The above answer is based solely on the provided sources and does not contain any external information or inferences.

**Citations:**

- [1] Bank_of_America_10K_2022-02-22.htm
- [2] Bank_of_America_10K_2023-02-22.htm
- [3] Bank_of_America_10K_2025-02-25.htm
- [4] Citigroup_10K_2025-02-21.htm
- [5] Citigroup_10K_2026-02-20.htm


****
### 5. capital_ratios_trend
**Query:** How have CET1 capital ratios and total revenues trended at JPMorgan, Bank of America, and Citigroup from FY2021 through FY2025? Identify any consistent leaders or laggards.
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['CET1', 'capital', 'JPMorgan', 'Bank of America', 'revenue']`
**Retrieval query:** How have CET1 capital ratios and total revenues trended at JPMorgan, Bank of America, and Citigroup from FY2021 through FY2025? Identify any consistent leaders or laggards. JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 89.95s | **Pass:** ✅ | **Citation density:** 0.556

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
> 	+ FY2021: Not available
> 	+ FY2022: Not available
> 	+ FY2023: 11.8% [5]
> 	+ FY2024: Not available
> 	+ FY2025: Not available
> * JPMorgan Chase:
> 	+ FY2021: CET1 capital ratio (Basel III Advanced, JPMorgan Chase & Co.): 13.8% [6]
> 	+ FY2022: CET1 capital ratio (Basel III Advanced, JPMorgan Chase & Co.): 15.9% [7]
> 	+ FY2023: CET1 capital ratio (Basel III Advanced, JPMorgan Chase & Co.): 15.3% [8]
> 	+ FY2024: Not available
> 	+ FY2025: Not available
>
> Total revenues:
>
> * Citigroup:
> 	+ FY2021: Not available
> 	+ FY2022: $19,102 (Services) + $18,649 (Markets) + $4,715 (Banking) = $42,466 [3]
> 	+ FY2023: $19,649 (Services) + $19,836 (Markets) + $6,201 (Banking) = $45,686 [3]
> 	+ FY2024: Not available
> 	+ FY2025: $19,649 (Services) + $19,836 (Markets) + $6,201 (Banking) = $45,686 [3]
> * Bank of America:
> 	+ FY2021: Not available
> 	+ FY2022: Not available
> 	+ FY2023: Not available
> 	+ FY2024: $272,400 (Total common shareholders' equity) + $263,249 (Total common shareholders' equity) = $535,649 [9]
> 	+ FY2025: $277,251 (Total common shareholders' equity) + $270,804 (Total common shareholders' equity) = $548,055 [10]
> * JPMorgan Chase:
> 	+ FY2021: Not available
> 	+ FY2022: Not available
> 	+ FY2023: Not available
> 	+ FY2024: Not available
> 	+ FY2025: Not available
>
> Consistent leaders or laggards:
>
> * Citigroup's CET1 capital ratio has been consistently above 13% from FY2021 to FY2025.
> * Bank of America's CET1 capital ratio was below the required regulatory minimum in FY2022, but increased to 11.8% in FY2023 and remained relatively stable in FY2024 and FY2025.
> * JPMorgan Chase's CET1 capital ratio has been consistently above 13% from FY2021 to FY2023, but decreased to 15.3% in FY2023.
>
> Note: The total revenues for Citigroup are only available for FY2022 and FY2023, as the other years do not provide this information.

**Citations:**

- [1] Citigroup_10K_2023-02-27.htm
- [2] Citigroup_10K_2024-02-23.htm
- [3] Citigroup_10K_2025-02-21.htm
- [4] Citigroup_10K_2026-02-20.htm
- [5] Bank_of_America_10K_2024-02-20.htm
- [6] JPMorgan_Chase_10K_2022-02-22.htm
- [7] JPMorgan_Chase_10K_2023-02-21.htm
- [8] JPMorgan_Chase_10K_2024-02-16.htm
- [9] Bank_of_America_10K_2025-02-25.htm
- [10] Bank_of_America_10K_2026-02-25.htm


****
### 6. digital_banking_strategy
**Query:** How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['digital', 'technology', 'JPMorgan', 'Bank of America', 'Citigroup']`
**Retrieval query:** How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 85.5s | **Pass:** ✅ | **Citation density:** 0.435

**Answer:**

> JPMorgan Chase has described its digital banking strategy and technology investment priorities over the last 5 years. According to their filings:
>
> * In FY2021 [1], JPMorgan Chase noted that new technologies have required and could require them to spend more to modify or adapt their products to attract and retain clients and customers or to match products and services offered by its competitors, including technology companies.
> * In FY2022 [2], they stated that technological advances and the growth of e-commerce have made it possible for non-depository institutions to offer products and services that traditionally were banking products. They also noted that new technologies may be used by customers, or breached or infiltrated by third parties, in unexpected ways.
> * In FY2023 [3], JPMorgan Chase mentioned that ongoing or increased competition may put pressure on the pricing for their products and services or may cause them to lose market share, particularly with respect to traditional banking products.
> * In FY2024 [2], they noted that new technologies have required and could require them to spend more to modify or adapt their products to attract and retain clients and customers or to match products and services offered by its competitors, including technology companies.
> * In FY2025 [4], JPMorgan Chase stated that the use of new technologies, such as cryptocurrencies and other applications using secure distributed ledgers, may not require intermediation. They also noted that failure to keep pace with rapidly changing technological advances could result in a loss of clients and market share.
>
> Bank of America has described its digital banking strategy and technology investment priorities over the last 5 years. According to their filings:
>
> * In FY2021 [5], Bank of America stated that the widespread adoption and rapid evolution of new technologies, including analytic capabilities, self-service digital trading platforms, and automated trading markets, internet services, and digital assets, create additional strategic risks.
> * In FY2023 [6], they noted that the widespread adoption and rapid evolution of emerging technologies, including analytic capabilities, AI (including machine learning and generative AI), automated decision-making, self-service digital trading platforms, and automated trading markets, internet services, and digital assets, as well as payment, clearing, and settlement processes that use distributed ledger technology, create additional strategic risks.
> * In FY2024 [6], Bank of America stated that the widespread adoption and rapid evolution of emerging technologies, including analytic capabilities, AI (including machine learning and generative AI), automated decision-making, self-service digital trading platforms, and automated trading markets, internet services, and digital assets, as well as payment, clearing, and settlement processes that use distributed ledger technology, create additional strategic risks.
> * In FY2025 [6], they noted that the widespread adoption and rapid evolution of emerging technologies, including analytic capabilities, AI (including machine learning and generative AI), automated decision-making, self-service digital trading platforms, and automated trading markets, internet services, and digital assets, as well as payment, clearing, and settlement processes that use distributed ledger technology, create additional strategic risks.
>
> Citigroup has described its digital banking strategy and technology investment priorities over the last 5 years. According to their filings:
>
> * In FY2021 [7], Citigroup stated that emerging technologies have the potential to intensify competition and accelerate disruption in the financial services industry.
> * In FY2022 [8], they noted that non-traditional financial services firms, such as financial technology companies, have begun to offer services traditionally provided by financial institutions, and have sought bank charters to provide these services.
> * In FY2023 [9], Citigroup stated that emerging technologies have the potential to accelerate disruption and intensify competition in the financial services industry.
> * In FY2025 [10], they noted that increased competition and emerging technologies could require Citi to change or adapt its products and services, as well as invest in and develop related infrastructure.
>
> Major themes that emerge from these descriptions include:
>
> * The increasing importance of digital technologies and their potential to disrupt traditional banking business models.
> * The need for financial institutions to adapt quickly to changing technological advances and consumer preferences.
> * The emergence of new competitors, including non-traditional financial services firms, which are using technology to offer innovative products and services.
> * The risk that payments processing and other products and services could be significantly disrupted by the use of new technologies, such as cryptocurrencies and other applications using secure distributed ledgers.
> * The need for financial institutions to invest in emerging technologies, such as AI and blockchain, to remain competitive.

**Citations:**

- [1] JPMorgan_Chase_10K_2022-02-22.htm
- [2] JPMorgan_Chase_10K_2025-02-14.htm
- [3] JPMorgan_Chase_10K_2024-02-16.htm
- [4] JPMorgan_Chase_10K_2026-02-13.htm
- [5] Bank_of_America_10K_2022-02-22.htm
- [6] Bank_of_America_10K_2025-02-25.htm
- [7] Citigroup_10K_2022-02-28.htm
- [8] Citigroup_10K_2023-02-27.htm
- [9] Citigroup_10K_2026-02-20.htm
- [10] JPMorgan_Chase_10K_2023-02-21.htm


****
### 7. regulatory_burden_evolution
**Query:** What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging?
**Entity filter:** `['JPMorgan_Chase', 'Citigroup']` | **Keywords sent:** `['regulatory', 'capital', 'JPMorgan', 'Citigroup']`
**Retrieval query:** What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging? JPMorgan Chase & Co Citigroup Inc
**Model:** `llama3.1:8b` | **Latency:** 65.52s | **Pass:** ✅ | **Citation density:** 0.083  ⚠ low

**Answer:**

> JPMorgan Chase disclosed that it is monitoring developments and potential impacts related to an updated proposal to amend the U.S. risk-based capital framework, which may be issued in early 2026 [1]. 
>
> Citigroup disclosed that it faces regulatory and legislative uncertainties and changes, including potential changes to various aspects of the U.S. regulatory capital framework and requirements applicable to Citi, including significant revisions to the U.S. Basel III rules [2].
>
> JPMorgan Chase did not disclose new regulatory burdens or capital rules in its 2025 filing compared to 2022. However, it noted that the Federal Reserve's Vice Chair for Supervision indicated that U.S. banking regulators may issue an updated proposal to amend the U.S. risk-based capital framework in early 2026 [1].
>
> Citigroup disclosed that it is required to interpret and implement extensive and frequently changing regulatory and legislative requirements in the U.S. and other jurisdictions, which may overlap or conflict across jurisdictions, resulting in substantial compliance, regulatory, and other risks and costs [3]. 
>
> JPMorgan Chase did not disclose new regulatory burdens or capital rules in its 2025 filing compared to 2022. However, it noted that regulators have finalized the rules implementing their Basel III frameworks in the EU and U.K., with market risk aspects expected to be delayed until January 1, 2027 [1].
>
> Citigroup disclosed that it is continually required to interpret and implement extensive and frequently changing regulatory and legislative requirements in the U.S. and other jurisdictions, which may overlap or conflict across jurisdictions, resulting in substantial compliance, regulatory, and other risks and costs [3]. 
>
> JPMorgan Chase did not disclose new regulatory burdens or capital rules in its 2025 filing compared to 2022. However, it noted that regulators have finalized the rules implementing their Basel III frameworks in the EU and U.K., with market risk aspects expected to be delayed until January 1, 2027 [1].
>
> There is no information on themes both firms agree are most challenging.
>
> JPMorgan Chase did not disclose new regulatory burdens or capital rules in its 2025 filing compared to 2022. However, it noted that regulators have finalized the rules implementing their Basel III frameworks in the EU and U.K., with market risk aspects expected to be delayed until January 1, 2027 [1].
>
> Citigroup disclosed that it is required to interpret and implement extensive and frequently changing regulatory and legislative requirements in the U.S. and other jurisdictions, which may overlap or conflict across jurisdictions, resulting in substantial compliance, regulatory, and other risks and costs [3].

**Citations:**

- [1] JPMorgan_Chase_10K_2026-02-13.htm
- [2] Citigroup_10K_2024-02-23.htm
- [3] Citigroup_10K_2025-02-21.htm

**⚠ Low citation density:** 0.083 (correct answer, sparse attribution)

****
### 8. cyber_goldman
**Query:** How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K?
**Entity filter:** `['Goldman_Sachs']` | **Keywords sent:** `['cybersecurity', 'Goldman Sachs', 'risk management', 'oversight']`
**Retrieval query:** How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K? The Goldman Sachs Group, Inc.
**Model:** `llama3.1:8b` | **Latency:** 33.39s | **Pass:** ❌ | **Citation density:** 0.571

**Answer:**

> Goldman Sachs describes its cybersecurity risk-management framework as including critical components of its risk management framework, such as training and education, identity and access management, application and software security, infrastructure security, mobile security, data security, cloud computing, and technology operations [1]. The firm's process for managing cybersecurity risk also includes periodic review and modification of the Cybersecurity Program to respond to changing threats and conditions [2].
>
> The Board oversees Goldman Sachs' risk management policies and practices, including cybersecurity risks, through its committees, such as the Risk Committee and Technology Risk Subcommittee [3]. The chief risk officer, chief information officer, and chief technology officer periodically brief the Board on operational and technology risks, including cybersecurity risks [4]. The CISO also provides regular briefings to senior management on a range of cybersecurity-related topics [4].
>
> Goldman Sachs has emphasized phishing and cybersecurity training for employees in response to AI-enabled fraud and ransomware attacks [1,3]. Despite these efforts, the firm cannot eliminate all cybersecurity risks or provide assurances that it has not had occurrences of undetected cybersecurity incidents [1,3].

**Citations:**

- [1] GOLDMAN_SACHS_GROUP_INC_10K_2026-02-25.htm
- [2] Goldman_Sachs_10K_2024-02-23.htm
- [3] Goldman_Sachs_10K_2025-02-27.htm
- [4] Goldman_Sachs_10K_2026-02-25.htm

**Missing keywords:** ['oversight']

****
### 9. revenue_sources_blackrock
**Query:** What does BlackRock identify as its principal sources of revenue in its most recent 10-K?
**Entity filter:** `['BlackRock']` | **Keywords sent:** `['BlackRock', 'revenue', 'investment advisory', 'fees']`
**Retrieval query:** What does BlackRock identify as its principal sources of revenue in its most recent 10-K?
**Model:** `llama3.1:8b` | **Latency:** 24.77s | **Pass:** ❌ | **Citation density:** 0.0

**Answer:**

> BlackRock does not appear in the provided sources. The question asks about BlackRock's principal sources of revenue in its most recent 10-K, but none of the sources pertain to BlackRock.

**Missing keywords:** ['investment advisory', 'fees']

****
### 10. net_revenue_jpm
**Query:** What was JPMorgan Chase's total net revenue for fiscal 2024 as reported in its consolidated statements of income?
**Entity filter:** `['JPMorgan_Chase']` | **Keywords sent:** `['JPMorgan', 'net revenue']`
**Retrieval query:** What was JPMorgan Chase's total net revenue for fiscal 2024 as reported in its consolidated statements of income? JPMorgan Chase & Co
**Model:** `llama3.1:8b` | **Latency:** 42.25s | **Pass:** ❌ | **Citation density:** 0.5

**Answer:**

> Total net revenue for fiscal 2024 was $177.6 billion [1].

**Citations:**

- [1] JPMorgan_Chase_10K_2025-02-14.htm

**Missing keywords:** ['JPMorgan']
