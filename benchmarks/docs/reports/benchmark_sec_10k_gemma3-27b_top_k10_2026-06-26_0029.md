# AIStudio — Benchmark Findings
*Generated: 2026-06-26 00:38*

## Configuration
- **Corpus:** `sec_10k`
- **Scope:** none (full corpus)
- **Base Top K:** 10 (effective K may be higher for multi-entity queries)
- **Temperature:** 0.3
- **Alpha:** 0.5
- **Min Score:** 0.5
- **Model:** gemma3:27b
- **API:** http://localhost:8000
- **Questions:** `benchmarks/sec_10k/sec_10k_questions.yaml` · sha `bc38f105`

## Summary
- **Questions:** 10
- **Passed (binary):** 10/10 (100%)
- **Rating (AIStudio_878):** 🟢 10 GREEN · 🟡 0 AMBER · 🔴 0 RED
- **Avg latency:** 50.9s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `sec_10k` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings? | 46.69s | 🟢 | JPMorgan_Chase_10K_2024-02-16.htm, JPMor | Emergence-of-AI-risk-language framing; answerable with current corpus. |
| 2 | How do JPMorgan, Bank of America, and Citigroup describe oversight of AI-related risk — through dedicated AI committees, or folded into their existing risk-governance structures? | 43.12s | 🟢 | JPMorgan_Chase_10K_2024-02-16.htm, JPMor | Reframed (BIC) — drops the dedicated-AI-committee presupposition; the correct answer ('AI risk is folded into existing risk governance') scores clean and contains 'AI'. The presupposing original lives in the June_2026 set. |
| 3 | Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged? | 56.68s | 🟢 | JPMorgan_Chase_10K_2024-02-16.htm, JPMor | Explicit 2022-vs-2026 temporal contrast across two firms. |
| 4 | How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework? | 43.48s | 🟢 | Bank_of_America_10K_2023-02-22.htm, Bank | Two-firm climate evolution since 2022. |
| 5 | How do JPMorgan, Bank of America, and Citigroup describe their approach to managing capital strength and their CET1 capital position in their most recent 10-K filings? | 56.98s | 🟢 | JPMorgan_Chase_10K_2023-02-21.htm, JPMor | Reframed (BIC) — qualitative capital-management / CET1-position comparison, prose-only. The hard multi-year CET1+revenue TABLE trend is preserved in the June_2026 set as the work-in-progress table exhibit (Annex 5). |
| 6 | How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge? | 57.85s | 🟢 | Bank_of_America_10K_2022-02-22.htm, Bank | Three-firm digital strategy over a relative 5-year window. |
| 7 | What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging? | 81.75s | 🟢 | JPMorgan_Chase_10K_2023-02-21.htm, JPMor | 'compliance' keyword removed 2026-05-30 (AIStudio_850) as a false negative. |
| 8 | How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K? | 40.48s | 🟢 | Goldman_Sachs_10K_2026-02-25.htm, Goldma | L1 baseline. 2026-06-02 audit GREEN — Goldman-only, substantive. Token verified on Beast. |
| 9 | What are the principal categories of revenue BlackRock identifies in its most recent 10-K, and how does it describe each? | 37.58s | 🟢 | BlackRock,_Inc._10K_2026-02-25.htm, Blac | Reframed (BIC) — qualitative 'describe the sources' (base & performance fees, securities lending, technology services). Avoids inviting a precise sub-line figure; the original audited GREEN on sources but the model volunteered a wrong technology-services number. |
| 10 | What was JPMorgan Chase's total net revenue for fiscal year 2024, as reported in its FY2024 consolidated statements of income? Report the single FY2024 figure. | 44.58s | 🟢 | JPMorgan_Chase_10K_2025-02-14.htm, JPMor | Pinned (BIC) — single FY2024 figure (~$177.6B), the income-statement total the system retrieves correctly; the wording discourages the multi-year pull that produced the contradictory FY2025 figure in the June_2026 run. The single-cell table lookup is the one quantitative shape handled cleanly. |

## Detailed Results

****
### 1. ai_disclosure_evolution
**Query:** When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America']` | **Keywords sent:** `['AI', 'risk', 'JPMorgan', 'Bank of America']`
**Retrieval query:** When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings? JPMorgan Chase & Co Bank of America Corporation
**Model:** `gemma3:27b` | **Latency:** 46.69s | **Pass:** ✅ | **Citation density:** 0.571

**Answer:**

> JPMorgan Chase began disclosing AI as a specific risk factor in its 10-K filings with the FY2023 filing [1]. In that filing, JPMorgan Chase noted that models using machine learning, artificial intelligence or quantum computing may not be effective in all cases to identify, observe and mitigate risk [1].  In the most recent 2025 Form 10-K filing [2], JPMorgan Chase details risks related to AI system failures, inappropriate use, lack of transparency, inaccurate output, increased cyber threats, competitive disadvantage, and workforce miscalibration [2].
>
> Bank of America first disclosed AI as a specific risk factor in its 10-K filings with the FY2024 filing [3]. The filing highlights that the proliferation of emerging technologies, including AI, increases cybersecurity risks and exposure [3]. In the most recent 2026 Form 10-K filing [4], Bank of America details risks related to data risk, unpredictable system interactions, inadequate controls, AI failure, unintended consequences, operational, legal, regulatory, and reputational harm stemming from expanded use of AI [4]. The filing also notes potential impacts on third parties, clients, and the financial services industry infrastructure due to increased AI adoption [4].

**Citations:**

- [1] JPMorgan_Chase_10K_2024-02-16.htm
- [2] JPMorgan_Chase_10K_2026-02-13.htm
- [3] Bank_of_America_10K_2024-02-20.htm
- [4] Bank_of_America_10K_2026-02-25.htm


****
### 2. ai_governance_committees_comparison
**Query:** How do JPMorgan, Bank of America, and Citigroup describe oversight of AI-related risk — through dedicated AI committees, or folded into their existing risk-governance structures?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['AI', 'risk', 'governance', 'oversight']`
**Retrieval query:** How do JPMorgan, Bank of America, and Citigroup describe oversight of AI-related risk — through dedicated AI committees, or folded into their existing risk-governance structures? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `gemma3:27b` | **Latency:** 43.12s | **Pass:** ✅ | **Citation density:** 1.429

**Answer:**

> JPMorgan Chase utilizes a risk governance and oversight structure with standing committees and management-level committees to oversee risk, including escalation channels to senior management, the Financial Risk Committee (FRC), and the Board of Directors [1,2]. Line of Business and Corporate Function Control Committees review operational risks and control environments within their areas [3,4]. Bank of America employs a similar approach with a Risk Framework overseen by the Board and its committees, delegating authority to management-level committees [5]. They utilize a three lines of defense model and escalate issues to executive management, board committees, or the Board itself [6]. Citigroup integrates AI risk into existing risk governance; however, they note that ineffective deployment practices could result in control gaps [7,8,9]. Bank of America notes increased AI adoption by third parties and clients, which may interact with their systems and create additional operational, legal, and regulatory risks [10]. As of the filings available, none of the firms explicitly state establishing *dedicated* AI committees separate from existing structures; rather, they incorporate AI risk oversight into established frameworks.

**Citations:**

- [1] JPMorgan_Chase_10K_2024-02-16.htm
- [2] JPMorgan_Chase_10K_2026-02-13.htm
- [3] JPMorgan_Chase_10K_2022-02-22.htm
- [4] JPMorgan_Chase_10K_2023-02-21.htm
- [5] Bank_of_America_10K_2024-02-20.htm
- [6] Bank_of_America_10K_2025-02-25.htm
- [7] Citigroup_10K_2026-02-20.htm
- [8] Citigroup_10K_2025-02-21.htm
- [9] Citigroup_10K_2024-02-23.htm
- [10] Bank_of_America_10K_2026-02-25.htm


****
### 3. cyber_disclosure_2022_vs_2026
**Query:** Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged?
**Entity filter:** `['JPMorgan_Chase', 'Citigroup']` | **Keywords sent:** `['cybersecurity', 'JPMorgan', 'Citigroup', 'risk management']`
**Retrieval query:** Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged? JPMorgan Chase & Co Citigroup Inc
**Model:** `gemma3:27b` | **Latency:** 56.68s | **Pass:** ✅ | **Citation density:** 0.353

**Answer:**

> ## JPMorgan Chase & Citigroup Cybersecurity Risk Management: A Comparison (2022 vs. 2026)
>
> **JPMorgan Chase**
>
> In 2024 [1], JPMorgan Chase’s cybersecurity framework centers on integrating risk management into its operational risk framework, with escalation of key issues and development of mitigation plans [1]. The Global Cybersecurity and Technology Controls organization is overseen by the CIO, CISO, and CTOC, receiving updates from these leaders regarding security matters [1]. Independent Risk Management (IRM) independently assesses and challenges cybersecurity practices [1]. This structure remained consistent in 2025 [2], with continued emphasis on identifying, escalating, and mitigating risks through established governance forums like the Cybersecurity and Technology Controls Operating Committee (CTOC) [2]. The firm also actively partners with government agencies and industry peers to enhance defenses [1,2].
>
> **Citigroup**
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] JPMorgan_Chase_10K_2024-02-16.htm
- [2] JPMorgan_Chase_10K_2026-02-13.htm
- [3] Citigroup_10K_2022-02-28.htm
- [4] Citigroup_10K_2023-02-27.htm
- [5] Citigroup_10K_2026-02-20.htm
- [6] Citigroup_10K_2025-02-21.htm


****
### 4. climate_risk_evolution
**Query:** How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework?
**Entity filter:** `['Bank_of_America', 'Citigroup']` | **Keywords sent:** `['climate', 'risk', 'Bank of America', 'Citigroup', 'Net Zero']`
**Retrieval query:** How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework? Citigroup Inc Bank of America Corporation
**Model:** `gemma3:27b` | **Latency:** 43.48s | **Pass:** ✅ | **Citation density:** 0.545

**Answer:**

> Since 2022, both Bank of America and Citigroup have been enhancing their climate risk disclosures and frameworks. In 2022, Bank of America announced targets to reduce emissions by 2030 associated with its financing activities related to auto manufacturing, energy, and power generation [1]. They also disclosed financed emissions for these sectors and planned further disclosure in 2023 [1]. In 2023, Bank of America created an internal Climate Risk Framework addressing how the corporation identifies, measures, monitors, and controls climate risk [2]. In 2024, they continued to refine this framework, aligning it with global laws, rules, regulations, and guidance [3].
>
> Citigroup has also been enhancing its methodologies for quantifying climate risks impacting client credit profiles and embedding sector-specific assessments into underwriting processes [4,5]. They have developed a Climate Risk Management Framework (Climate RMF) providing governance, roles, responsibilities, and principles to support the identification, measurement, monitoring, controlling, and reporting of climate risks [6,5].
>
> Citigroup has the most detailed Net Zero or transition risk framework. As of 2024, Citi’s Climate RMF provides information on governance, roles, responsibilities, and principles for managing climate risks across the company [5]. Additionally, Citigroup details how climate risk acts as a driver of other categories of risk such as credit, strategic, reputational, and operational risk [6,5]. While Bank of America has developed its Climate Risk Framework, the sources do not detail the same level of comprehensive integration with broader risk categories as described by Citigroup.

**Citations:**

- [1] Bank_of_America_10K_2023-02-22.htm
- [2] Bank_of_America_10K_2024-02-20.htm
- [3] Bank_of_America_10K_2025-02-25.htm
- [4] Citigroup_10K_2024-02-23.htm
- [5] Citigroup_10K_2025-02-21.htm
- [6] Citigroup_10K_2026-02-20.htm


****
### 5. capital_ratios_trend
**Query:** How do JPMorgan, Bank of America, and Citigroup describe their approach to managing capital strength and their CET1 capital position in their most recent 10-K filings?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['CET1', 'capital', 'JPMorgan', 'Bank of America', 'Citigroup']`
**Retrieval query:** How do JPMorgan, Bank of America, and Citigroup describe their approach to managing capital strength and their CET1 capital position in their most recent 10-K filings? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `gemma3:27b` | **Latency:** 56.98s | **Pass:** ✅ | **Citation density:** 0.476

**Answer:**

> **JPMorgan Chase:** JPMorgan Chase manages its capital position by establishing internal minimum capital requirements, maintaining a strong governance framework, and regularly monitoring its capital position [1,2]. The firm allocates capital to each Line of Business (LOB) considering peer capital levels, regulatory requirements, and stress testing simulations [3]. As of 2025, the firm’s current equity allocation methodology incorporates Basel III Standardized RWA and the GSIB surcharge [3]. JPMorgan Chase aims to maintain “well-capitalized” status for itself and its subsidiaries under applicable regulatory standards [2].
>
> **Bank of America:** Bank of America manages its capital position to ensure it is adequate to support business activities, aligns with risk appetite, and satisfies regulatory requirements [4,5]. The Corporation uses proprietary models to measure capital needs for various risks and allocates capital based on each business's unique risk profile [4,5]. As of December 31, 2023, Bank of America’s CET1 capital ratio under the Standardized approach was 11.8%, exceeding its minimum requirement of 9.5% (increasing to 10.0% effective January 1, 2024) [4]. The firm also maintains a minimum supplementary leverage ratio (SLR) of 3.0% plus a 2.0% buffer [4].
>
> **Citigroup:** Citigroup’s capital management framework is designed to maintain sufficient capital consistent with each entity's risk profile and regulatory standards [6,7,8,9]. Citi assesses its capital adequacy against internal quantitative goals in expected and stressed environments [6]. As of December 31, 2024, Citibank was “well capitalized” maintaining CET1 Capital, Tier 1 Capital, Total Capital and Leverage ratios of at least 6.5%, 8.0%, 10.0% and 5.0%, respectively to meet regulatory requirements [10,9]. The firm is subject to annual assessment by the FRB through CCAR and DFAST programs to ensure effective capital planning processes [7].

**Citations:**

- [1] JPMorgan_Chase_10K_2023-02-21.htm
- [2] JPMorgan_Chase_10K_2022-02-22.htm
- [3] JPMorgan_Chase_10K_2026-02-13.htm
- [4] Bank_of_America_10K_2024-02-20.htm
- [5] Bank_of_America_10K_2026-02-25.htm
- [6] Citigroup_10K_2023-02-27.htm
- [7] Citigroup_10K_2024-02-23.htm
- [8] Citigroup_10K_2022-02-28.htm
- [9] Citigroup_10K_2026-02-20.htm
- [10] Citigroup_10K_2025-02-21.htm


****
### 6. digital_banking_strategy
**Query:** How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['digital', 'technology', 'JPMorgan', 'Bank of America', 'Citigroup']`
**Retrieval query:** How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `gemma3:27b` | **Latency:** 57.85s | **Pass:** ✅ | **Citation density:** 0.923

**Answer:**

> Over the last five years, JPMorgan Chase, Bank of America, and Citigroup have all highlighted the increasing importance of digital banking and technology investment in their strategies. A major theme across these firms is the need to adapt to rapidly evolving industry standards and consumer preferences [1,2,3].
>
> **JPMorgan Chase** consistently emphasizes the impact of technological advances and e-commerce enabling non-depository institutions to offer traditional banking products [4,5,6]. They note the risk of disruption to payments processing from technologies like cryptocurrencies and the need for ongoing investment to match competitors’ offerings [7,4,5].  Generative AI is a key area requiring attention to avoid losing market share [7].
>
> **Bank of America** stresses the increased reliance on digital banking accelerated by the pandemic [1] and the importance of adapting strategies, products, and technology accordingly [2,3,8]. They specifically mention investments in analytic capabilities, self-service digital platforms, AI, machine learning, and automation [2,3,8].  The firm also acknowledges the potential for financial disintermediation due to new technologies and competitors [8].
>
> **Citigroup** recognizes competition from both traditional banks and non-traditional firms like fintech companies and digital asset businesses [9,10,11,12]. They highlight the need to embrace emerging technologies such as blockchain, digital assets, and AI to remain competitive [9,12] while acknowledging potential regulatory hurdles and compliance risks related to these new areas [9,10].  Citi also notes that increased competition may require investment in infrastructure to attract and retain customers [12].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Bank_of_America_10K_2022-02-22.htm
- [2] Bank_of_America_10K_2024-02-20.htm
- [3] Bank_of_America_10K_2025-02-25.htm
- [4] JPMorgan_Chase_10K_2025-02-14.htm
- [5] JPMorgan_Chase_10K_2024-02-16.htm
- [6] JPMorgan_Chase_10K_2023-02-21.htm
- [7] JPMorgan_Chase_10K_2026-02-13.htm
- [8] Bank_of_America_10K_2026-02-25.htm
- [9] Citigroup_10K_2025-02-21.htm
- [10] Citigroup_10K_2022-02-28.htm
- [11] Citigroup_10K_2023-02-27.htm
- [12] Citigroup_10K_2026-02-20.htm


****
### 7. regulatory_burden_evolution
**Query:** What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging?
**Entity filter:** `['JPMorgan_Chase', 'Citigroup']` | **Keywords sent:** `['regulatory', 'capital', 'JPMorgan', 'Citigroup']`
**Retrieval query:** What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging? JPMorgan Chase & Co Citigroup Inc
**Model:** `gemma3:27b` | **Latency:** 81.75s | **Pass:** ✅ | **Citation density:** 0.231

**Answer:**

> ## JPMorgan Chase & Citigroup: New Regulatory Burdens & Capital Rules (2025/2026 vs. 2022)
>
> **JPMorgan Chase:**
>
> *   **2022 Disclosures**: In FY2022, JPMorgan Chase was subject to regulatory capital requirements including leverage- and risk-based capital requirements, a GSIB surcharge, Stress Capital Buffer (SCB), and countercyclical buffer [1]. The firm targeted a Basel III Standardized CET1 capital ratio of 13.0%, increasing to 13.5% in Q1 2024 with consideration for an increase in the GSIB surcharge [1]. A CECL capital benefit of $2.9 billion was being phased out beginning January 1, 2022 [2].
> *   **2025 Disclosures**: In FY2025, JPMorgan Chase noted the phasing out of the $2.9 billion CECL capital benefit by January 1, 2025, with $720 million remaining as of December 31, 2024 [3]. The firm also reported that other CECL transition provisions impacting Tier 2 capital, adjusted average assets, total leverage exposure and RWA were phased out as of January 1, 2025 [3]. Additionally, the Federal Reserve indicated a potential update to the U.S. risk-based capital framework in early 2026, replacing the July 2023 proposal [3,4].
> *   **2026 Disclosures**: In FY2026, JPMorgan Chase continues to monitor developments and potential impacts of the updated proposal to amend the U.S. risk-based capital framework [3].
>
> **Citigroup:**
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] JPMorgan_Chase_10K_2023-02-21.htm
- [2] JPMorgan_Chase_10K_2022-02-22.htm
- [3] JPMorgan_Chase_10K_2026-02-13.htm
- [4] JPMorgan_Chase_10K_2025-02-14.htm
- [5] Citigroup_10K_2023-02-27.htm
- [6] Citigroup_10K_2022-02-28.htm
- [7] Citigroup_10K_2024-02-23.htm
- [8] Citigroup_10K_2025-02-21.htm
- [9] Citigroup_10K_2026-02-20.htm


****
### 8. cyber_goldman
**Query:** How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K?
**Entity filter:** `['Goldman_Sachs']` | **Keywords sent:** `['cybersecurity', 'Goldman Sachs', 'risk management', 'oversight']`
**Retrieval query:** How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K? The Goldman Sachs Group, Inc.
**Model:** `gemma3:27b` | **Latency:** 40.48s | **Pass:** ✅ | **Citation density:** 0.429

**Answer:**

> Goldman Sachs’ cybersecurity risk management framework includes a dedicated Operational Risk team reporting to the chief risk officer, providing oversight of the Cybersecurity Program independent of Technology Risk [1,2,3]. This program is designed to identify, assess, document, and mitigate threats, with periodic reviews and modifications to respond to changing conditions [2,3]. The process incorporates training and education, identity and access management, application/software security, infrastructure security, mobile security, and data security measures [1,2,3].
>
> Board-level oversight is conducted directly by the Board and through its committees, including the Risk Committee and Technology Risk Subcommittee [1,2,3]. The chief risk officer, chief information officer, and chief technology officer periodically brief the Board on operational and technology risks, including cybersecurity [1,2,3]. Regular briefings are also provided by the CISO regarding the Cybersecurity Program’s status, emerging threats, mitigation strategies, and regulatory engagements; directors maintain ongoing dialogue with the CISO, CIO, and CTO [1,2,3]. The CISO is responsible for managing and implementing the program and reports directly to the chief information officer, overseeing the Technology Risk team which assesses and manages material cybersecurity risks [1,2,3].

**Citations:**

- [1] Goldman_Sachs_10K_2026-02-25.htm
- [2] Goldman_Sachs_10K_2025-02-27.htm
- [3] Goldman_Sachs_10K_2024-02-23.htm


****
### 9. revenue_sources_blackrock
**Query:** What are the principal categories of revenue BlackRock identifies in its most recent 10-K, and how does it describe each?
**Entity filter:** `['BlackRock']` | **Keywords sent:** `['BlackRock', 'revenue', 'investment advisory', 'fees']`
**Retrieval query:** What are the principal categories of revenue BlackRock identifies in its most recent 10-K, and how does it describe each? BlackRock, Inc.
**Model:** `gemma3:27b` | **Latency:** 37.58s | **Pass:** ✅ | **Citation density:** 0.286

**Answer:**

> BlackRock identifies the following principal categories of revenue in its FY2025 10-K [1]:
>
> *   **Investment Advisory, Administration Fees and Securities Lending Revenue:** These fees are based on percentages of assets under management (AUM) and recognized as services are performed over time [1]. Changes in AUM due to market fluctuations or net inflows/outflows affect these fees [1].
> *   **Technology services and subscription revenue**: This includes investment management technology systems, risk management services, wealth management and digital distribution tools and subscriptions, all on a fee basis. Fees are primarily recorded as services are performed over time and determined using the value of positions on the Aladdin platform or on a fixed-rate basis [1]. Revenue from software licenses is recognized when access rights are granted [1].
> *   **Distribution Fees:** These fees relate to distributing investment products and providing shareholder support services, and are passed through to third-party distributors [1]. 
> *   **Advisory and other revenue**: This includes fees earned for advisory services determined using fixed-rate fees recognized over time as related services are completed, and commissions from transition management services recorded on a trade-date basis [2].

**Citations:**

- [1] BlackRock,_Inc._10K_2026-02-25.htm
- [2] BlackRock,_Inc._10K_2025-02-25.htm


****
### 10. net_revenue_jpm
**Query:** What was JPMorgan Chase's total net revenue for fiscal year 2024, as reported in its FY2024 consolidated statements of income? Report the single FY2024 figure.
**Entity filter:** `['JPMorgan_Chase']` | **Keywords sent:** `['JPMorgan', 'net revenue', '2024']`
**Retrieval query:** What was JPMorgan Chase's total net revenue for fiscal year 2024, as reported in its FY2024 consolidated statements of income? Report the single FY2024 figure. JPMorgan Chase & Co
**Model:** `gemma3:27b` | **Latency:** 44.58s | **Pass:** ✅ | **Citation density:** 0.667

**Answer:**

> JPMorgan Chase’s total net revenue for fiscal year 2024 was $177.6 billion [1]. This figure is also reported as $177,556 in another section of the same document [2].

**Citations:**

- [1] JPMorgan_Chase_10K_2025-02-14.htm
- [2] JPMorgan_Chase_10K_2026-02-13.htm

