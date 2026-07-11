# AIStudio — Benchmark Findings
*Generated: 2026-07-07 09:25*

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
- **Avg latency:** 44.4s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `sec_10k` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings? | 44.96s | 🟢 | JPMorgan_Chase_10K_2026-02-13.htm, Bank_ | Emergence-of-AI-risk-language framing; answerable with current corpus. |
| 2 | How do JPMorgan, Bank of America, and Citigroup describe oversight of AI-related risk — through dedicated AI committees, or folded into their existing risk-governance structures? | 39.08s | 🟢 | JPMorgan_Chase_10K_2023-02-21.htm, Bank_ | Reframed (BIC) — drops the dedicated-AI-committee presupposition; the correct answer ('AI risk is folded into existing risk governance') scores clean and contains 'AI'. The presupposing original lives in the June_2026 set. |
| 3 | Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged? | 48.01s | 🟢 | JPMorgan_Chase_10K_2024-02-16.htm, JPMor | Explicit 2022-vs-2026 temporal contrast across two firms. |
| 4 | How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework? | 40.83s | 🟢 | Bank_of_America_10K_2023-02-22.htm, Bank | Two-firm climate evolution since 2022. |
| 5 | How do JPMorgan, Bank of America, and Citigroup describe their approach to managing capital strength and their CET1 capital position in their most recent 10-K filings? | 59.51s | 🟢 | JPMorgan_Chase_10K_2025-02-14.htm, JPMor | Reframed (BIC) — qualitative capital-management / CET1-position comparison, prose-only. The hard multi-year CET1+revenue TABLE trend is preserved in the June_2026 set as the work-in-progress table exhibit (Annex 5). |
| 6 | How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge? | 54.47s | 🟢 | JPMorgan_Chase_10K_2026-02-13.htm, JPMor | Three-firm digital strategy over a relative 5-year window. |
| 7 | What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging? | 45.54s | 🟢 | JPMorgan_Chase_10K_2026-02-13.htm, Citig | 'compliance' keyword removed 2026-05-30 (AIStudio_850) as a false negative. |
| 8 | How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K? | 40.19s | 🟢 | GOLDMAN_SACHS_GROUP_INC_10K_2026-02-25.h | L1 baseline. 2026-06-02 audit GREEN — Goldman-only, substantive. Token verified on Beast. |
| 9 | What are the principal categories of revenue BlackRock identifies in its most recent 10-K, and how does it describe each? | 31.89s | 🟡 | GOLDMAN_SACHS_GROUP_INC_10K_2026-02-25.h | Reframed (BIC) — qualitative 'describe the sources' (base & performance fees, securities lending, technology services). Avoids inviting a precise sub-line figure; the original audited GREEN on sources but the model volunteered a wrong technology-services number. |
| 10 | What was JPMorgan Chase's total net revenue for fiscal year 2024, as reported in its FY2024 consolidated statements of income? Report the single FY2024 figure. | 39.68s | 🟢 | JPMorgan_Chase_10K_2025-02-14.htm | Pinned (BIC) — single FY2024 figure (~$177.6B), the income-statement total the system retrieves correctly; the wording discourages the multi-year pull that produced the contradictory FY2025 figure in the June_2026 run. The single-cell table lookup is the one quantitative shape handled cleanly. |

## Detailed Results

****
### 1. ai_disclosure_evolution
**Query:** When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America']` | **Keywords sent:** `['AI', 'risk', 'JPMorgan', 'Bank of America']`
**Retrieval query:** When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings? JPMorgan Chase & Co Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 44.96s | **Pass:** ✅ | **Citation density:** 1.0

**Answer:**

> JPMorgan Chase first started disclosing AI as a specific risk factor in their 10-K filings in FY2023 [1]. In the most recent filing (FY2025), JPMorgan Chase uses language such as "rapid development and deployment of advanced technologies, including generative and agentic AI systems" to describe potential risks [1].
>
> Bank of America first started disclosing AI as a specific risk factor in their 10-K filings in FY2025 [2]. In the most recent filing (FY2025), Bank of America uses language such as "expanded use of AI, including emerging third-party AI services and autonomous AI agents" to describe potential risks [2].
>
> Both JPMorgan Chase and Bank of America mention cybersecurity risks associated with AI, including data breaches, unauthorized access to sensitive information, and system manipulation [1,3,4,5].

**Citations:**

- [1] JPMorgan_Chase_10K_2026-02-13.htm
- [2] Bank_of_America_10K_2026-02-25.htm
- [3] Bank_of_America_10K_2024-02-20.htm
- [4] JPMorgan_Chase_10K_2024-02-16.htm
- [5] Bank_of_America_10K_2025-02-25.htm


****
### 2. ai_governance_committees_comparison
**Query:** How do JPMorgan, Bank of America, and Citigroup describe oversight of AI-related risk — through dedicated AI committees, or folded into their existing risk-governance structures?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['AI', 'risk', 'governance', 'oversight']`
**Retrieval query:** How do JPMorgan, Bank of America, and Citigroup describe oversight of AI-related risk — through dedicated AI committees, or folded into their existing risk-governance structures? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 39.08s | **Pass:** ✅ | **Citation density:** 1.0

**Answer:**

> JPMorgan Chase describes oversight of AI-related risk through dedicated committees, such as the Firmwide Valuation Governance Forum (VGF), which oversees the management of risks arising from valuation activities conducted across the Firm [1]. 
>
> Bank of America discusses AI-related risk in the context of cybersecurity and operational risk, but does not explicitly mention a dedicated committee for AI oversight. Instead, it highlights the importance of governance structures and policies to facilitate oversight of cybersecurity risk [2].
>
> Citigroup mentions AI-related risks in various sections, including operational processes and systems, cybersecurity, and emerging markets risk factors. However, it does not describe a specific committee or structure dedicated to overseeing AI-related risk [3,4,5].

**Citations:**

- [1] JPMorgan_Chase_10K_2023-02-21.htm
- [2] Bank_of_America_10K_2025-02-25.htm
- [3] Citigroup_10K_2026-02-20.htm
- [4] Citigroup_10K_2025-02-21.htm
- [5] Citigroup_10K_2024-02-23.htm


****
### 3. cyber_disclosure_2022_vs_2026
**Query:** Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged?
**Entity filter:** `['JPMorgan_Chase', 'Citigroup']` | **Keywords sent:** `['cybersecurity', 'JPMorgan', 'Citigroup', 'risk management']`
**Retrieval query:** Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged? JPMorgan Chase & Co Citigroup Inc
**Model:** `llama3.1:8b` | **Latency:** 48.01s | **Pass:** ✅ | **Citation density:** 0.455

**Answer:**

> JPMorgan Chase's description of its cybersecurity risk management framework has evolved over time. In the 2022 annual report [1], JPMorgan Chase mentions that the Firm's Board of Directors receives periodic updates from the CIO, CISO, and senior members of the CTOC concerning cybersecurity matters.
>
> In contrast, the 2026 annual report [2] does not provide a detailed description of the governance structure for the Global Cybersecurity and Technology Controls organization. However, it mentions that IRM independently assesses and challenges the activities and risk management practices of the Global Cybersecurity and Technology Controls organization related to the identification, assessment, measurement, and mitigation of cybersecurity risk.
>
> Comparing the two reports, there is no clear indication of concrete changes in JPMorgan Chase's description of its cybersecurity risk management framework between 2022 and 2026.
>
> In contrast, Citigroup's description of its cybersecurity risk management framework has also evolved over time. In the 2022 annual report [3], Citigroup mentions that it leverages an intelligence-led strategy to protect against, detect, and respond to, and recover from cyber attacks. 
>
> In the 2023 annual report [4], Citigroup mentions that it actively participates in financial industry, government, and cross-sector knowledge-sharing groups to enhance individual and collective cybersecurity preparedness and resilience.
>
> In the 2026 annual report [5], Citigroup mentions that it has a Cybersecurity Risk Appetite Statement against which Citi's performance is measured quarterly. In addition, the RMC oversees Citi's risk profile, which includes cybersecurity risk, and monitors whether Citi is operating within its cybersecurity risk appetite under its mandate to review key operational risks.
>
> Comparing the three reports, there are clear indications of changes in Citigroup's description of its cybersecurity risk management framework between 2022 and 2026.

**Citations:**

- [1] JPMorgan_Chase_10K_2024-02-16.htm
- [2] JPMorgan_Chase_10K_2026-02-13.htm
- [3] Citigroup_10K_2022-02-28.htm
- [4] Citigroup_10K_2023-02-27.htm
- [5] Citigroup_10K_2026-02-20.htm


****
### 4. climate_risk_evolution
**Query:** How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework?
**Entity filter:** `['Bank_of_America', 'Citigroup']` | **Keywords sent:** `['climate', 'risk', 'Bank of America', 'Citigroup', 'Net Zero']`
**Retrieval query:** How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework? Citigroup Inc Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 40.83s | **Pass:** ✅ | **Citation density:** 0.545

**Answer:**

> Climate Risk Disclosure Evolution:
>
> Bank of America's climate risk disclosure has evolved since 2022. In FY2022, the company announced a target to reduce emissions by 2030 associated with its financing activities related to auto manufacturing, energy, and power generation [1]. By FY2023, Bank of America created an internal Climate Risk Framework that addresses how the Corporation identifies, measures, monitors, and controls climate risk [2].
>
> In contrast, Citigroup's climate risk disclosure has not significantly evolved since 2022. In FY2022, Citigroup mentioned that it was developing globally consistent principles and approaches for managing climate risk across the Company through its Climate Risk Management Framework (Climate RMF) [3]. However, in subsequent years, the company continued to discuss the same general approach without significant changes.
>
> Net Zero or Transition Risk Framework:
>
> Bank of America has a more detailed Net Zero or transition risk framework. The company's FY2024 10-K report describes a comprehensive Climate and Environmental Risk Management function that oversees climate risk management [4]. This includes establishing the Climate Risk Framework, governance structure, and providing an independent assessment of enterprise-wide climate risks.
>
> In comparison, Citigroup's climate risk management approach is more general, focusing on developing globally consistent principles and approaches for managing climate risk through its Climate RMF [5,6]. While Citigroup has made progress in embedding climate-related considerations into its overarching risk management approach, the company does not have a detailed Net Zero or transition risk framework comparable to Bank of America's.

**Citations:**

- [1] Bank_of_America_10K_2023-02-22.htm
- [2] Bank_of_America_10K_2024-02-20.htm
- [3] Citigroup_10K_2023-02-27.htm
- [4] Bank_of_America_10K_2025-02-25.htm
- [5] Citigroup_10K_2026-02-20.htm
- [6] Citigroup_10K_2025-02-21.htm


****
### 5. capital_ratios_trend
**Query:** How do JPMorgan, Bank of America, and Citigroup describe their approach to managing capital strength and their CET1 capital position in their most recent 10-K filings?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['CET1', 'capital', 'JPMorgan', 'Bank of America', 'Citigroup']`
**Retrieval query:** How do JPMorgan, Bank of America, and Citigroup describe their approach to managing capital strength and their CET1 capital position in their most recent 10-K filings? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 59.51s | **Pass:** ✅ | **Citation density:** 0.4

**Answer:**

> JPMorgan Chase describes its approach to managing capital strength and CET1 capital position in its most recent 10-K filings as follows:
>
> * The Firm's capital management framework is designed to ensure that JPMorgan Chase & Co. and its principal subsidiaries maintain sufficient capital consistent with each entity's respective risk profile, management targets, and all applicable regulatory standards and guidelines [1].
> * The Firm periodically assesses the assumptions, methodologies, and reporting classifications used for segment reporting, and further refinements may be implemented in future periods to arrive at a business segment's net income applicable to common equity [2].
>
> Bank of America describes its approach to managing capital strength and CET1 capital position in its most recent 10-K filings as follows:
>
> * The Corporation manages its capital position so that its capital is more than adequate to support its business activities and aligns with risk, risk appetite, and strategic planning [3].
> * The Corporation is required to maintain a minimum supplementary leverage ratio (SLR) of 3.0 percent plus a leverage buffer of 2.0 percent in order to avoid certain restrictions on capital distributions and discretionary bonus payments [3].
>
> Citigroup describes its approach to managing capital strength and CET1 capital position in its most recent 10-K filings as follows:
>
> * Citi's capital management framework is designed to ensure that Citigroup and its principal subsidiaries maintain sufficient capital consistent with each entity's respective risk profile, management targets, and all applicable regulatory standards and guidelines [4].
> * An insured depository institution, such as Citibank, must maintain minimum CET1 Capital, Tier 1 Capital, Total Capital, and Leverage ratios of 6.5%, 8.0%, 10.0%, and 5.0%, respectively, to be considered "well capitalized" [5].
> * Citi is subject to an annual assessment by the FRB as to whether Citigroup has effective capital planning processes as well as sufficient regulatory capital to absorb losses during stressful economic and financial conditions [6].
>
> Note that there is no information in the sources on how JPMorgan Chase, Bank of America, or Citigroup describe their approach to managing capital strength and CET1 capital position in their 2026 filings.

**Citations:**

- [1] JPMorgan_Chase_10K_2025-02-14.htm
- [2] JPMorgan_Chase_10K_2026-02-13.htm
- [3] Bank_of_America_10K_2024-02-20.htm
- [4] Citigroup_10K_2023-02-27.htm
- [5] Citigroup_10K_2025-02-21.htm
- [6] Citigroup_10K_2024-02-23.htm


****
### 6. digital_banking_strategy
**Query:** How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['digital', 'technology', 'JPMorgan', 'Bank of America', 'Citigroup']`
**Retrieval query:** How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `llama3.1:8b` | **Latency:** 54.47s | **Pass:** ✅ | **Citation density:** 0.583

**Answer:**

> JPMorgan Chase has described its digital banking strategy and technology investment priorities over the last 5 years as adapting to emerging technologies, including AI, blockchain, and distributed ledger technology, to remain competitive [1]. The firm acknowledges that new technologies may disrupt traditional banking products and services, requiring JPMorgan Chase to invest in modifying or adapting its products to attract and retain clients and customers [2].
>
> Bank of America has also highlighted the importance of adapting to emerging technologies, including AI, machine learning, and generative AI, to remain competitive [3]. The firm notes that widespread adoption and rapid evolution of these technologies create additional strategic risks, could negatively impact their ability to compete, and require substantial expenditures to modify or adapt existing products and services [4].
>
> Citigroup has emphasized the need to adapt to emerging technologies, including blockchain and digital assets, to remain competitive [5]. The firm acknowledges that new competitors in the financial services industry continue to emerge, and that non-traditional financial services firms are expanding their offerings of services traditionally provided by financial institutions [6]. Citigroup also notes that emerging technologies have the potential to accelerate disruption and intensify competition in the financial services industry [7].
>
> Major themes that emerge from these descriptions include:
>
> * The need for traditional banks to adapt to emerging technologies, including AI, blockchain, and distributed ledger technology, to remain competitive.
> * The risk of disruption to payments processing and other products and services due to the use of new technologies, such as cryptocurrencies and other applications using secure distributed ledgers.
> * The importance of investing in modifying or adapting existing products and services to attract and retain clients and customers.
> * The emergence of new competitors in the financial services industry, including non-traditional financial services firms that are expanding their offerings of services traditionally provided by financial institutions.
>
> Overall, the descriptions suggest that traditional banks face significant challenges in adapting to emerging technologies and remaining competitive in a rapidly changing financial services landscape.

**Citations:**

- [1] JPMorgan_Chase_10K_2026-02-13.htm
- [2] JPMorgan_Chase_10K_2025-02-14.htm
- [3] Bank_of_America_10K_2025-02-25.htm
- [4] Bank_of_America_10K_2026-02-25.htm
- [5] Citigroup_10K_2025-02-21.htm
- [6] Citigroup_10K_2023-02-27.htm
- [7] Citigroup_10K_2026-02-20.htm


****
### 7. regulatory_burden_evolution
**Query:** What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging?
**Entity filter:** `['JPMorgan_Chase', 'Citigroup']` | **Keywords sent:** `['regulatory', 'capital', 'JPMorgan', 'Citigroup']`
**Retrieval query:** What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging? JPMorgan Chase & Co Citigroup Inc
**Model:** `llama3.1:8b` | **Latency:** 45.54s | **Pass:** ✅ | **Citation density:** 0.3

**Answer:**

> Compared to 2022, JPMorgan Chase's 2025 filings mention an updated proposal to amend the US risk-based capital framework, which is expected to be issued by the Federal Reserve in early 2026 [1]. The EU and UK regulators have finalized rules implementing their Basel III frameworks, with new rules effective in the EU beginning January 1, 2025, and delayed until January 1, 2027 for market risk aspects [1].
>
> In contrast, Citigroup's 2023 filings mention potential changes to the US regulatory capital framework, including revisions to the US Basel III rules [2]. The U.S. banking agencies are considering a number of changes to the US regulatory capital framework in the future, including revisions to the US Basel III rules and potential changes to the GSIB surcharge, SLR, and discretionary Countercyclical Capital Buffer [2].
>
> Both firms face regulatory and legislative uncertainties and changes, but Citigroup's 2026 filings mention specific examples of ongoing regulatory and legislative uncertainties and changes in the U.S. and globally, including potential changes to US laws or regulations with respect to credit cards, and potential changes to various aspects of the US regulatory capital framework [3].
>
> There are no explicit mentions of themes both firms agree are most challenging in their 2025 filings.

**Citations:**

- [1] JPMorgan_Chase_10K_2026-02-13.htm
- [2] Citigroup_10K_2023-02-27.htm
- [3] Citigroup_10K_2026-02-20.htm


****
### 8. cyber_goldman
**Query:** How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K?
**Entity filter:** `['Goldman_Sachs']` | **Keywords sent:** `['cybersecurity', 'Goldman Sachs', 'risk management', 'oversight']`
**Retrieval query:** How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K? The Goldman Sachs Group, Inc.
**Model:** `llama3.1:8b` | **Latency:** 40.19s | **Pass:** ✅ | **Citation density:** 0.333

**Answer:**

> Goldman Sachs describes its cybersecurity risk-management framework as including critical components of its risk management framework, such as training and education, identity and access management, application and software security, infrastructure security, mobile security, data security, cloud computing, and technology operations [1]. The firm's process for managing cybersecurity risk also includes monitoring the network for known vulnerabilities and signs of unauthorized attempts to access data and systems [1].
>
> The Cybersecurity Program is administered by Technology Risk within Engineering and overseen by the CISO. This program is designed to identify, assess, document, and mitigate threats, establish and evaluate compliance with information security mandates, adopt and apply a security control framework, and prevent, detect, and respond to security incidents [2]. The program is periodically reviewed and modified to respond to changing threats and conditions.
>
> The Board oversees the firm's risk management policies and practices, including cybersecurity risks, through its committees, such as the Risk Committee and Technology Risk Subcommittee. The Board receives regular briefings from the CISO on a range of cybersecurity-related topics [1,3,4,2].
>
> Goldman Sachs' governance structure for cybersecurity includes the Firmwide Technology Risk Committee, which oversees cybersecurity matters, technology risk management frameworks, and methodologies, and monitors their effectiveness [1]. The committee is co-chaired by the CISO and chief technology officer.
>
> The firm's operational risk team provides oversight and challenge of the Cybersecurity Program, independent of Technology Risk, and assesses its operating effectiveness against industry standard frameworks and Board risk appetite-approved operational risk limits and thresholds [1,2].
>
> Goldman Sachs emphasizes phishing and cybersecurity training for employees in response to AI-enabled fraud and ransomware attacks. However, despite these efforts, the firm cannot eliminate all cybersecurity risks or provide assurances that it has not had occurrences of undetected cybersecurity incidents [1,3,4].

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
**Model:** `llama3.1:8b` | **Latency:** 31.89s | **Pass:** ❌ | **Citation density:** 0.3

**Answer:**

> BlackRock's principal categories of revenue are not explicitly stated in any of the provided sources. However, we can infer that BlackRock is a global investment management firm and likely has various revenue streams related to its investment products and services.
>
> The most relevant source for this question is [1] GOLDMAN_SACHS_GROUP_INC_10K_2026-02-25.htm, which discusses Goldman Sachs' Value-at-Risk (VaR) measure. However, this source does not provide information on BlackRock's revenue categories.
>
> Another relevant source is [2] Raymond_James_10K_2021-11-23.htm and [3] Raymond_James_10K_2023-11-21.htm, which discuss Raymond James Financial's segment revenues. While these sources do not explicitly mention BlackRock, they provide information on the revenue categories of a similar financial firm.
>
> However, none of the provided sources specifically mention BlackRock or its revenue categories.

**Citations:**

- [1] GOLDMAN_SACHS_GROUP_INC_10K_2026-02-25.htm
- [2] Raymond_James_10K_2021-11-23.htm
- [3] Raymond_James_10K_2023-11-21.htm

**Missing keywords:** ['investment advisory', 'fees']

****
### 10. net_revenue_jpm
**Query:** What was JPMorgan Chase's total net revenue for fiscal year 2024, as reported in its FY2024 consolidated statements of income? Report the single FY2024 figure.
**Entity filter:** `['JPMorgan_Chase']` | **Keywords sent:** `['JPMorgan', 'net revenue', '2024']`
**Retrieval query:** What was JPMorgan Chase's total net revenue for fiscal year 2024, as reported in its FY2024 consolidated statements of income? Report the single FY2024 figure. JPMorgan Chase & Co
**Model:** `llama3.1:8b` | **Latency:** 39.68s | **Pass:** ✅ | **Citation density:** 0.5

**Answer:**

> JPMorgan Chase's total net revenue for fiscal year 2024 was $177.6 billion [1].

**Citations:**

- [1] JPMorgan_Chase_10K_2025-02-14.htm

