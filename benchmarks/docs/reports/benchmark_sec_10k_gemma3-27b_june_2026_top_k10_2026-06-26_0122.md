# AIStudio — Benchmark Findings
*Generated: 2026-06-26 01:31*

## Configuration
- **Corpus:** `sec_10k`
- **Scope:** none (full corpus)
- **Base Top K:** 10 (effective K may be higher for multi-entity queries)
- **Temperature:** 0.3
- **Alpha:** 0.5
- **Min Score:** 0.5
- **Model:** gemma3:27b
- **API:** http://localhost:8000
- **Questions:** `June_2026`

## Summary
- **Questions:** 10
- **Passed (binary):** 10/10 (100%)
- **Rating (AIStudio_878):** 🟢 10 GREEN · 🟡 0 AMBER · 🔴 0 RED
- **Avg latency:** 49.7s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `sec_10k` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings? | 39.52s | 🟢 | JPMorgan_Chase_10K_2024-02-16.htm, JPMor | Emergence-of-AI-risk-language framing; answerable with current corpus. |
| 2 | Which of JPMorgan, Bank of America, or Citigroup have established dedicated AI governance committees, and how do their oversight structures differ? | 43.45s | 🟢 | JPMorgan_Chase_10K_2026-02-13.htm, JPMor | 3-firm comparison. 2026-06-02 audit AMBER — answers drift to general risk committees; missing 'AI' is a genuine drift signal, not a phrasing artifact. Keyword retained deliberately. |
| 3 | Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged? | 58.49s | 🟢 | JPMorgan_Chase_10K_2024-02-16.htm, JPMor | Explicit 2022-vs-2026 temporal contrast across two firms. |
| 4 | How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework? | 44.04s | 🟢 | Bank_of_America_10K_2023-02-22.htm, Bank | Two-firm climate evolution since 2022. |
| 5 | How have CET1 capital ratios and total revenues trended at JPMorgan, Bank of America, and Citigroup from FY2021 through FY2025? Identify any consistent leaders or laggards. | 78.68s | 🟢 | JPMorgan_Chase_10K_2022-02-22.htm, JPMor | The stacked case — 3 firms × FY2021-FY2025 × quantitative table. Heaviest question (~114s). |
| 6 | How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge? | 61.23s | 🟢 | Citigroup_10K_2025-02-21.htm, Bank_of_Am | Three-firm digital strategy over a relative 5-year window. |
| 7 | What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging? | 51.18s | 🟢 | JPMorgan_Chase_10K_2026-02-13.htm, JPMor | 'compliance' keyword removed 2026-05-30 (AIStudio_850) as a false negative. |
| 8 | How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K? | 39.08s | 🟢 | Goldman_Sachs_10K_2026-02-25.htm, Goldma | L1 baseline. 2026-06-02 audit GREEN — Goldman-only, substantive. Token verified on Beast. |
| 9 | What does BlackRock identify as its principal sources of revenue in its most recent 10-K? | 32.61s | 🟢 | BlackRock,_Inc._10K_2026-02-25.htm, Blac | L1 baseline. 2026-06-02 audit GREEN — BlackRock-only. Token verified on Beast. |
| 10 | What was JPMorgan Chase's total net revenue for fiscal 2024 as reported in its consolidated statements of income? | 48.61s | 🟢 | JPMorgan_Chase_10K_2025-02-14.htm, JPMor | L2 — the table-location ∂. 2026-06-02 audit AMBER→fixed — pulled $177.6B FY2024 from the income-statement table; keyword 'total revenue' → 'net revenue' (answer says "total net revenue"). derived=false (figure is stated, not computed — contrast L7). |

## Detailed Results

****
### 1. ai_disclosure_evolution
**Query:** When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America']` | **Keywords sent:** `['AI', 'risk', 'JPMorgan', 'Bank of America']`
**Retrieval query:** When did JPMorgan and Bank of America first start disclosing AI as a specific risk factor in their 10-K filings, and what language do they use in their most recent filings? JPMorgan Chase & Co Bank of America Corporation
**Model:** `gemma3:27b` | **Latency:** 39.52s | **Pass:** ✅ | **Citation density:** 0.667

**Answer:**

> JPMorgan Chase began disclosing AI as a specific risk factor in its 10-K filings with the FY2023 filing [1]. In that filing, JPMorgan Chase notes that models using machine learning, artificial intelligence or quantum computing “may not be effective in all cases to identify, observe and mitigate risk” [1].
>
> In its most recent 2025 10-K filing, JPMorgan Chase details several risks associated with advanced technologies like AI, including system failures, inappropriate use, lack of transparency, inaccurate output, increased cyber threats, competitive disadvantage, and potential workforce miscalibration [2].
>
> Bank of America first disclosed AI as a specific risk factor in its FY2025 10-K filing [3]. The bank states that expanded use of AI may result in “increased data risk, unpredictable system interactions, inadequate controls or safeguards, AI failure, or produce unintended operations or consequences” and highlights risks related to third-party AI services [3].  The most recent filing also notes the potential for inaccurate AI outputs, biases, intellectual property infringement, and increased cybersecurity risks [3,4].

**Citations:**

- [1] JPMorgan_Chase_10K_2024-02-16.htm
- [2] JPMorgan_Chase_10K_2026-02-13.htm
- [3] Bank_of_America_10K_2026-02-25.htm
- [4] Bank_of_America_10K_2025-02-25.htm


****
### 2. ai_governance_committees_comparison
**Query:** Which of JPMorgan, Bank of America, or Citigroup have established dedicated AI governance committees, and how do their oversight structures differ?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['AI', 'governance', 'committee', 'JPMorgan']`
**Retrieval query:** Which of JPMorgan, Bank of America, or Citigroup have established dedicated AI governance committees, and how do their oversight structures differ? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `gemma3:27b` | **Latency:** 43.45s | **Pass:** ✅ | **Citation density:** 0.6

**Answer:**

> JPMorgan Chase has established a Firmwide Risk Committee that escalates to the Board Risk Committee as appropriate [1]. The firm’s Operating Committee, consisting of the CEO, CRO, CFO, General Counsel, and LOB CEOs, is accountable to the Board [1]. JPMorgan Chase also utilizes Line of Business and Corporate Function Control Committees to oversee operational risk within their respective areas [2]. In FY2021, the JPMorgan Chase Bank, N.A. Board oversaw management through its own standing committees, including the Risk Committee and Audit Committee [3].
>
> Citigroup has established an Executive Management Governance Committee that reviews Citi’s approach to Generative AI and assesses significant technology investments [4]. Additionally, Citigroup formed a Transformation Oversight Committee focused on risk and control environment improvements [4].
>
> Bank of America utilizes a three lines of defense model with governance structures to oversee cybersecurity risk; the CTIO and CISO are responsible for managing and assessing this risk, supported by over 3,400 information security professionals [5]. Bank of America expects increased AI adoption by third parties, clients, and counterparties, which may result in additional operational, legal, and regulatory risks [6].

**Citations:**

- [1] JPMorgan_Chase_10K_2026-02-13.htm
- [2] JPMorgan_Chase_10K_2023-02-21.htm
- [3] JPMorgan_Chase_10K_2022-02-22.htm
- [4] Citigroup_10K_2026-02-20.htm
- [5] Bank_of_America_10K_2025-02-25.htm
- [6] Bank_of_America_10K_2026-02-25.htm


****
### 3. cyber_disclosure_2022_vs_2026
**Query:** Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged?
**Entity filter:** `['JPMorgan_Chase', 'Citigroup']` | **Keywords sent:** `['cybersecurity', 'JPMorgan', 'Citigroup', 'risk management']`
**Retrieval query:** Compare how JPMorgan and Citigroup describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes have emerged? JPMorgan Chase & Co Citigroup Inc
**Model:** `gemma3:27b` | **Latency:** 58.49s | **Pass:** ✅ | **Citation density:** 0.333

**Answer:**

> ## JPMorgan Chase & Citigroup Cybersecurity Risk Management: A Comparison (2022 vs. 2026)
>
> **JPMorgan Chase**
>
> In 2024 [1], JPMorgan Chase’s cybersecurity framework centers around a governance structure for the Global Cybersecurity and Technology Controls organization, designed to identify, escalate, and mitigate risks. This is integrated into their operational risk management framework with key issues escalated to management and mitigation plans developed [1]. Independent Risk Management (IRM) independently assesses these practices [1]. In 2025 [2], this structure remains consistent; the focus continues on integrating cybersecurity risk management within the broader operational risk framework, emphasizing escalation of risks and development of mitigation plans. IRM’s independent assessment role is also maintained [2]. A key governance forum, the Cybersecurity and Technology Controls Operating Committee (CTOC), oversees risk assessment and control implementation [3].
>
> **Citigroup**
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] JPMorgan_Chase_10K_2024-02-16.htm
- [2] JPMorgan_Chase_10K_2026-02-13.htm
- [3] JPMorgan_Chase_10K_2025-02-14.htm
- [4] Citigroup_10K_2022-02-28.htm
- [5] Citigroup_10K_2023-02-27.htm
- [6] Citigroup_10K_2026-02-20.htm
- [7] Citigroup_10K_2025-02-21.htm


****
### 4. climate_risk_evolution
**Query:** How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework?
**Entity filter:** `['Bank_of_America', 'Citigroup']` | **Keywords sent:** `['climate', 'risk', 'Bank of America', 'Citigroup', 'Net Zero']`
**Retrieval query:** How has climate risk disclosure evolved since 2022 at Bank of America and Citigroup? Which firm has the most detailed Net Zero or transition risk framework? Citigroup Inc Bank of America Corporation
**Model:** `gemma3:27b` | **Latency:** 44.04s | **Pass:** ✅ | **Citation density:** 0.6

**Answer:**

> Since 2022, both Bank of America and Citigroup have enhanced their climate risk disclosures and frameworks. In 2022, Bank of America announced targets to reduce emissions by 2030 associated with its financing activities related to auto manufacturing, energy, and power generation [1]. They also disclosed financed emissions for these sectors and planned further disclosure in 2023 [1]. In 2023, Bank of America created an internal Climate Risk Framework addressing how the corporation identifies, measures, monitors, and controls climate risk [2]. In 2024, they continued to refine this framework and governance structure [3].
>
> Citigroup has also focused on enhancing methodologies for quantifying climate risks impacting client credit profiles and embedding sector-specific assessments into underwriting processes [4,5]. They developed a Climate Risk Management Framework (Climate RMF) providing information on governance, roles, responsibilities, and principles for identifying, measuring, monitoring, controlling, and reporting climate risks [6,5].
>
> Citigroup has the most detailed Net Zero or transition risk framework. As of FY2024, Citi’s Climate RMF provides a comprehensive approach to managing climate risk across the company, detailing governance, roles, responsibilities, and principles for identifying, measuring, monitoring, controlling, and reporting risks [5]. While Bank of America has developed its own framework, the sources detail more specifics regarding Citigroup's integrated approach as of the latest filings.

**Citations:**

- [1] Bank_of_America_10K_2023-02-22.htm
- [2] Bank_of_America_10K_2024-02-20.htm
- [3] Bank_of_America_10K_2025-02-25.htm
- [4] Citigroup_10K_2024-02-23.htm
- [5] Citigroup_10K_2025-02-21.htm
- [6] Citigroup_10K_2026-02-20.htm


****
### 5. capital_ratios_trend
**Query:** How have CET1 capital ratios and total revenues trended at JPMorgan, Bank of America, and Citigroup from FY2021 through FY2025? Identify any consistent leaders or laggards.
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['CET1', 'capital', 'JPMorgan', 'Bank of America', 'revenue']`
**Retrieval query:** How have CET1 capital ratios and total revenues trended at JPMorgan, Bank of America, and Citigroup from FY2021 through FY2025? Identify any consistent leaders or laggards. JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `gemma3:27b` | **Latency:** 78.68s | **Pass:** ✅ | **Citation density:** 0.37

**Answer:**

> ## JPMorgan Chase CET1 Capital & Revenues (FY2021-2025)
>
> **CET1 Capital Ratios:** JPMorgan Chase’s CET1 capital ratio (Basel III Standardized, JPM Co.) was 15.7% in FY2021 [1], increasing to 16.8% in FY2022 [2], then decreasing slightly to 16.9% in FY2023 [2] and remaining at 16.9% in FY2024 [3]. As of FY2025, the ratio was 17.0% [3].
>
> **Total Revenues:** Total revenues for JPMorgan Chase are not directly provided in a consolidated format across all years within these sources. However, data is available for specific components.
>
> ## Bank of America CET1 Capital & Revenues (FY2021-2025)
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] JPMorgan_Chase_10K_2022-02-22.htm
- [2] JPMorgan_Chase_10K_2024-02-16.htm
- [3] JPMorgan_Chase_10K_2025-02-14.htm
- [4] Bank_of_America_10K_2024-02-20.htm
- [5] Bank_of_America_10K_2025-02-25.htm
- [6] Bank_of_America_10K_2026-02-25.htm
- [7] Citigroup_10K_2023-02-27.htm
- [8] Citigroup_10K_2024-02-23.htm
- [9] Citigroup_10K_2025-02-21.htm
- [10] Citigroup_10K_2026-02-20.htm


****
### 6. digital_banking_strategy
**Query:** How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge?
**Entity filter:** `['JPMorgan_Chase', 'Bank_of_America', 'Citigroup']` | **Keywords sent:** `['digital', 'technology', 'JPMorgan', 'Bank of America', 'Citigroup']`
**Retrieval query:** How have JPMorgan, Bank of America, and Citigroup described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge? JPMorgan Chase & Co Citigroup Inc Bank of America Corporation
**Model:** `gemma3:27b` | **Latency:** 61.23s | **Pass:** ✅ | **Citation density:** 1.0

**Answer:**

> Over the last five years, JPMorgan Chase, Bank of America, and Citigroup have all highlighted the increasing importance of digital banking and technology investment in their strategies. A major theme across all three firms is recognizing the competitive pressure from both traditional financial institutions *and* non-bank entities like fintech companies and those offering digital assets [1,2,3,4,5,6,7,8,9].
>
> **JPMorgan Chase** consistently emphasizes adapting to new technologies – including AI and blockchain – to avoid losing market share and maintain competitiveness [4,5,6]. They specifically mention electronic securities/cryptocurrency trading, lending, payments processing, and algorithmic investment advice as areas of focus [4,10,6]. JPMorgan Chase acknowledges the need for increased expenditure to modify products and match competitor offerings [5,10,6].
>
> **Bank of America** has focused on adapting business strategies, products, and services to rapidly evolving industry standards and consumer preferences, particularly since the pandemic-driven increase in digital banking reliance [2,3,11,12]. They highlight investment in analytic capabilities, self-service digital platforms, AI, machine learning, and digital assets like cryptocurrencies as key priorities [3,11,12]. Bank of America also recognizes that emerging technologies create strategic risks and may require substantial expenditures [12].
>
> **Citigroup** has similarly noted the growth of non-traditional financial services firms (fintech, digital asset companies) and the need to adapt to remain competitive [1,13,7,8]. They are paying attention to mobile platforms, AI, digital assets, instant payments, and blockchain technology [1,13,8]. Citigroup acknowledges that failure to embrace emerging technologies could result in a competitive disadvantage [1] and emphasizes the need for investment in related infrastructure [8].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Citigroup_10K_2025-02-21.htm
- [2] Bank_of_America_10K_2022-02-22.htm
- [3] Bank_of_America_10K_2024-02-20.htm
- [4] JPMorgan_Chase_10K_2026-02-13.htm
- [5] JPMorgan_Chase_10K_2025-02-14.htm
- [6] JPMorgan_Chase_10K_2024-02-16.htm
- [7] Citigroup_10K_2023-02-27.htm
- [8] Citigroup_10K_2026-02-20.htm
- [9] JPMorgan_Chase_10K_2023-02-21.htm
- [10] JPMorgan_Chase_10K_2022-02-22.htm
- [11] Bank_of_America_10K_2025-02-25.htm
- [12] Bank_of_America_10K_2026-02-25.htm
- [13] Citigroup_10K_2022-02-28.htm


****
### 7. regulatory_burden_evolution
**Query:** What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging?
**Entity filter:** `['JPMorgan_Chase', 'Citigroup']` | **Keywords sent:** `['regulatory', 'capital', 'JPMorgan', 'Citigroup']`
**Retrieval query:** What new regulatory burdens and capital rules have JPMorgan and Citigroup disclosed in their 2025 and 2026 filings compared to 2022? Are there themes both firms agree are most challenging? JPMorgan Chase & Co Citigroup Inc
**Model:** `gemma3:27b` | **Latency:** 51.18s | **Pass:** ✅ | **Citation density:** 0.35

**Answer:**

> JPMorgan Chase and Citigroup both disclosed new regulatory burdens and capital rule changes primarily related to Basel III implementation in their 2025 and 2026 filings compared to 2022 [1,2,3,4,5]. In the EU and U.K., these firms noted the finalization of rules implementing Basel III frameworks effective January 1, 2025 (with some aspects delayed) [1,2]. JPMorgan Chase also anticipates a revised proposal from U.S. banking regulators to amend the U.S. risk-based capital framework in early 2026 [1].
>
> Citigroup specifically noted increases to its required regulatory CET1 Capital ratio – from 10.5% to 11.5% in October 2022, and further to 12% by January 2023 due to increases in the Stress Capital Buffer (SCB) and GSIB surcharge [3]. JPMorgan Chase disclosed that a $2.9 billion CECL capital benefit was fully phased out as of January 1, 2025 [1], after being phased out at 25% per year beginning in 2022 [6].
>
> Both firms highlighted ongoing regulatory and legislative uncertainties and changes as significant challenges [7,4,5]. Specifically, both mentioned potential revisions to U.S. Basel III rules and the impact of supervisory stress tests on capital requirements [1,3,7,4,5]. Increased expectations from regulators following banking stresses in 2023 were also a common theme [7,4]. Both firms are subject to increased scrutiny regarding governance, infrastructure, data, and risk management practices [7,4].

**Citations:**

- [1] JPMorgan_Chase_10K_2026-02-13.htm
- [2] JPMorgan_Chase_10K_2025-02-14.htm
- [3] Citigroup_10K_2023-02-27.htm
- [4] Citigroup_10K_2024-02-23.htm
- [5] Citigroup_10K_2026-02-20.htm
- [6] JPMorgan_Chase_10K_2022-02-22.htm
- [7] Citigroup_10K_2025-02-21.htm


****
### 8. cyber_goldman
**Query:** How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K?
**Entity filter:** `['Goldman_Sachs']` | **Keywords sent:** `['cybersecurity', 'Goldman Sachs', 'risk management', 'oversight']`
**Retrieval query:** How does Goldman Sachs describe its cybersecurity risk-management framework and board-level oversight in its most recent 10-K? The Goldman Sachs Group, Inc.
**Model:** `gemma3:27b` | **Latency:** 39.08s | **Pass:** ✅ | **Citation density:** 0.429

**Answer:**

> Goldman Sachs’ cybersecurity risk management framework includes a dedicated Operational Risk team reporting to the chief risk officer, providing oversight of the Cybersecurity Program independent of Technology Risk [1,2,3]. The program is designed to identify, assess, document, and mitigate threats, establish compliance with security mandates, adopt a security control framework, and prevent/respond to incidents [2,3]. Key components of their process include training & education, identity & access management, application/software security, infrastructure security, mobile security, and data security [1,2,3].
>
> Board-level oversight is conducted directly by the Board and through its committees – specifically the Risk Committee and Technology Risk Subcommittee — which oversee risk management policies and practices, including cybersecurity matters [1,2,3]. The chief risk officer, chief information officer, and chief technology officer periodically brief the Board on operational and technology risks, including those related to cybersecurity [1,2,3]. Regular briefings are also provided by the CISO regarding program status, emerging threats, mitigation strategies, and regulatory engagements; individual directors maintain ongoing dialogue with the CISO, CIO, and CTO [1,2,3]. The CISO is responsible for managing and implementing the Cybersecurity Program, reporting directly to the chief information officer, and oversees the Technology Risk team which assesses and manages material cybersecurity risks [1,2,3].

**Citations:**

- [1] Goldman_Sachs_10K_2026-02-25.htm
- [2] Goldman_Sachs_10K_2025-02-27.htm
- [3] Goldman_Sachs_10K_2024-02-23.htm


****
### 9. revenue_sources_blackrock
**Query:** What does BlackRock identify as its principal sources of revenue in its most recent 10-K?
**Entity filter:** `['BlackRock']` | **Keywords sent:** `['BlackRock', 'revenue', 'investment advisory', 'fees']`
**Retrieval query:** What does BlackRock identify as its principal sources of revenue in its most recent 10-K? BlackRock, Inc.
**Model:** `gemma3:27b` | **Latency:** 32.61s | **Pass:** ✅ | **Citation density:** 0.4

**Answer:**

> BlackRock’s principal sources of revenue are investment advisory and administration fees, securities lending revenue, technology services and subscription revenue, and distribution fees [1][2]. Investment advisory and administration fees are based on percentages of assets under management (AUM) [1][2]. Technology services revenue comes from systems like Aladdin, risk management services, and digital tools offered to clients on a fee basis [1][2]. Distribution fees are earned through distributing investment products and providing shareholder support services [1][2].
>
> In fiscal year 2025, BlackRock’s total revenue was $24,216 [1].

**Citations:**

- [1] BlackRock,_Inc._10K_2026-02-25.htm
- [2] BlackRock,_Inc._10K_2025-02-25.htm


****
### 10. net_revenue_jpm
**Query:** What was JPMorgan Chase's total net revenue for fiscal 2024 as reported in its consolidated statements of income?
**Entity filter:** `['JPMorgan_Chase']` | **Keywords sent:** `['JPMorgan', 'net revenue']`
**Retrieval query:** What was JPMorgan Chase's total net revenue for fiscal 2024 as reported in its consolidated statements of income? JPMorgan Chase & Co
**Model:** `gemma3:27b` | **Latency:** 48.61s | **Pass:** ✅ | **Citation density:** 0.667

**Answer:**

> JPMorgan Chase's total net revenue for fiscal 2024 was $177.6 billion [1]. Additionally, the firm’s managed basis total net revenue for fiscal year 2024 was $185,581 [2].

**Citations:**

- [1] JPMorgan_Chase_10K_2025-02-14.htm
- [2] JPMorgan_Chase_10K_2026-02-13.htm

