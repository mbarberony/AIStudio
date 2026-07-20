# AIStudio — Benchmark Findings
*Generated: 2026-06-26 22:35*

## Configuration
- **Corpus:** `esef_banks`
- **Scope:** none (full corpus)
- **Base Top K:** 10 (effective K may be higher for multi-entity queries)
- **Temperature:** 0.3
- **Alpha:** 0.5
- **Min Score:** 0.5
- **Model:** gemma3:27b
- **API:** http://localhost:8000
- **Questions:** `benchmarks/esef_banks/esef_banks_questions.yaml` · sha `d1083aec`

## Summary
- **Questions:** 12
- **Passed (binary):** 8/12 (67%)
- **Rating (AIStudio_878):** 🟢 6 GREEN · 🟡 6 AMBER · 🔴 0 RED
- **Avg latency:** 62.4s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `esef_banks` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | How does ING Group describe its CET1 capital ratio and regulatory capital position in its most recent annual report? | 50.0s | 🟡 | ING_Groep_N.V._ESEF_2025.xhtml ⚠low-density | L1 baseline. ING files in English. Entity tag in corpus = 'ING Groep N.V.'. |
| 2 | What is Barclays' Tier 1 capital ratio and what are the components of their capital stack? | 37.23s | 🟢 | Barclays_Bank_PLC_ESEF_2025.xhtml | Annex 1 holdco/sub case. Entity in corpus = 'Barclays Bank PLC' (sub). Tests alias resolution. |
| 3 | What is HSBC's leverage ratio and how does it compare to the regulatory minimum requirement? | 40.68s | 🟡 | HSBC_Holdings_plc_ESEF_2025.xhtml | L1 table-located fact. Tests table extraction on a clean EN filer. |
| 4 | How do ING Group, HSBC, and Barclays compare in terms of their CET1 capital ratios and capital management approaches? | 77.92s | 🟢 | ING_Groep_N.V._ESEF_2025.xhtml, HSBC_Hol | Cross-firm EN comparison. Tests entity isolation across 3 firms. |
| 5 | What is Nordea's leverage ratio and how does management describe its approach to leverage risk management? | 69.46s | 🟢 | Nordeakoncernen_ESEF_2025.xhtml | Benchmarking Journey leverage_nordea. Entity tag = 'Nordeakoncernen' — alias resolution test. |
| 6 | How does KBC Group describe its net interest income sensitivity and interest rate risk management? | 109.1s | 🟡 | KBC_Groep_NV_ESEF_2025.xhtml ⚠low-density | Tutorial Annex 3 canonical NII example. Entity tag = 'KBC Groep NV'. |
| 7 | How does BBVA describe its approach to climate-related risks and its net zero transition strategy? | 67.37s | 🟡 | Banco_Bilbao_Vizcaya_Argentaria,_S.A._ES ⚠low-density | BBVA FY2024 (latest available). EN filer despite Spanish jurisdiction. GLEIF mis-merge risk class. |
| 8 | How does Standard Chartered describe its climate risk framework and net zero commitments? | 46.2s | 🟢 | StandardChartered_Bank_ESEF_2025.xhtml | Annex 1 holdco/sub class. Entity in corpus = 'StandardChartered Bank' (whitespace missing). |
| 9 | What are ING Group's key technology investments and digital transformation priorities? | 50.18s | 🟢 | ING_Groep_N.V._ESEF_2025.xhtml | Digital Banking |
| 10 | How does Nordea describe its digital banking strategy and IT modernization program? | 79.72s | 🟡 | Nordeakoncernen_ESEF_2025.xhtml | Localized entity name 'Nordeakoncernen' — alias resolution test. |
| 11 | How does Barclays describe its capital structure and the relationship between the holding company and its banking subsidiaries? | 58.85s | 🟢 | Barclays_Bank_PLC_ESEF_2025.xhtml | Annex 1 DEMO_10 holdco/sub teaching case. Entity = 'Barclays Bank PLC' in corpus. PROVEN PASS. |
| 12 | How does Erste Group describe its overall risk profile and key risk management priorities? | 62.62s | 🟡 | Erste_Group_BankAG_ESEF_2025.xhtml | Annex 1 whitespace-collapse case. Entity = 'Erste Group BankAG' in corpus. 0 citations in prior run — F-030. |

## Detailed Results

****
### 1. cet1_ing_group
**Query:** How does ING Group describe its CET1 capital ratio and regulatory capital position in its most recent annual report?
**Entity filter:** `['ING_Groep_N.V.']` | **Keywords sent:** `['CET1', 'capital', 'ING', 'ratio', 'regulatory']`
**Retrieval query:** How does ING Group describe its CET1 capital ratio and regulatory capital position in its most recent annual report? ING Groep N.V.
**Model:** `gemma3:27b` | **Latency:** 50.0s | **Pass:** ✅ | **Citation density:** 0.067  ⚠ low

**Answer:**

> ING Group’s CET1 ratio was 13.1% as of December 31, 2025, decreasing from 13.6% at the end of 2024 [1]. The firm's fully loaded CET1 requirement stood at 11.09% at the end of 4Q2025 (versus 10.88% in 4Q2024) [1]. ING’s CET1 target is approximately 13%, which is above the prevailing maximum distributable amount (MDA) level of 11.03% at December 31, 2025, creating a management buffer of about 195 basis points [1]. The minimum Pillar 1 capital requirements applicable to ING Group are a CET1 ratio of 4.5%, a Tier 1 ratio of 6.0%, and a Total capital ratio of 8.0% of risk-weighted assets [1].  The overall SREP CET1 requirement for the group was 11.03% at December 31, 2025 [1]. ING applies the following definitions: CET1 capital consists of shareholders’ equity after regulatory adjustments and is calculated as CET1 capital divided by risk-weighted assets (RWAs) [1].

**Citations:**

- [1] ING_Groep_N.V._ESEF_2025.xhtml

**⚠ Low citation density:** 0.067 (correct answer, sparse attribution)

****
### 2. tier1_capital_barclays
**Query:** What is Barclays' Tier 1 capital ratio and what are the components of their capital stack?
**Entity filter:** `['Barclays_Bank_PLC']` | **Keywords sent:** `['Tier 1', 'capital', 'ratio', 'Barclays', 'CET1']`
**Retrieval query:** What is Barclays' Tier 1 capital ratio and what are the components of their capital stack? Barclays Bank PLC
**Model:** `gemma3:27b` | **Latency:** 37.23s | **Pass:** ✅ | **Citation density:** 0.143

**Answer:**

> Barclays Bank PLC’s solo-consolidated CET1 ratio was 12.7% as of December 31, 2025 [1]. The Tier 1 capital ratio was 16.1%, and the total regulatory capital ratio was 19.0% in 2025 [1].
>
> As of 2025, Barclays Bank PLC’s CET1 capital totaled £28,177 million, while its Tier 1 capital reached £35,848 million, and total regulatory capital amounted to £42,129 million [1]. Total risk weighted assets (RWAs) were £222,247 million in 2025 [1].

**Citations:**

- [1] Barclays_Bank_PLC_ESEF_2025.xhtml


****
### 3. leverage_ratio_hsbc
**Query:** What is HSBC's leverage ratio and how does it compare to the regulatory minimum requirement?
**Entity filter:** `['HSBC_Holdings_plc']` | **Keywords sent:** `['leverage', 'ratio', 'HSBC', 'regulatory', 'minimum']`
**Retrieval query:** What is HSBC's leverage ratio and how does it compare to the regulatory minimum requirement? HSBC Holdings plc
**Model:** `gemma3:27b` | **Latency:** 40.68s | **Pass:** ❌ | **Citation density:** 0.111

**Answer:**

> HSBC’s leverage ratio was 5.3% at December 31, 2025, decreasing from 5.6% at December 31, 2024 [1]. The UK minimum leverage ratio requirement was 3.25%, with an additional buffer of 0.9% – comprising a 0.7% additional leverage ratio buffer and a 0.2% countercyclical leverage ratio buffer as of December 31, 2025 [1]. HSBC exceeded these leverage requirements throughout 2025 [1].

**Citations:**

- [1] HSBC_Holdings_plc_ESEF_2025.xhtml

**Missing keywords:** ['regulatory']

****
### 4. cet1_cross_firm_en
**Query:** How do ING Group, HSBC, and Barclays compare in terms of their CET1 capital ratios and capital management approaches?
**Entity filter:** `['ING_Groep_N.V.', 'HSBC_Holdings_plc', 'Barclays_Bank_PLC']` | **Keywords sent:** `['CET1', 'capital', 'ING', 'HSBC', 'Barclays']`
**Retrieval query:** How do ING Group, HSBC, and Barclays compare in terms of their CET1 capital ratios and capital management approaches? ING Groep N.V. Barclays Bank PLC HSBC Holdings plc
**Model:** `gemma3:27b` | **Latency:** 77.92s | **Pass:** ✅ | **Citation density:** 0.125

**Answer:**

> ING Group’s fully loaded CET1 requirement was 11.09% at the end of 4Q2025, higher than the prevailing CET1 ratio requirement [1]. The overall SREP CET1 requirement for ING Group increased to 11.03% at December 31, 2025, comprised of a 4.5% Pillar 1 requirement, a 0.93% Pillar 2 requirement, a 2.5% capital conservation buffer, a 0.93% countercyclical buffer, 0.16% Sectoral Systemic Risk buffer, and a 2.0% Other Systemically Important Institutions (O-SII) buffer [1]. ING intends to maintain its CET1 capital ratio within a medium-term target range of 14%-14.5% [2].
>
> Barclays Bank PLC’s solo-consolidated CET1 ratio was 12.7% as of December 31, 2025, exceeding the minimum regulatory requirement of 10.4% [3]. The firm is subject to a binding Pillar 1 minimum capital requirement to satisfy a CET1 ratio of 4.5%, a Tier 1 capital ratio of 6.0%, and a total capital ratio of 8.0% of risk-weighted assets [3]. Barclays also has additional capital requirements including Pillar 2A, capital buffers (CCB & CCyB), O-SII buffer, and G-SII buffer [3].
>
> HSBC Holdings plc aimed to maintain its CET1 capital ratio within a medium-term target range of 14%-14.5% [2]. The privatization of Hang Seng Bank had a net CET1 capital impact of 110bps in January 2026, but HSBC expects to restore its CET1 ratio within the target range through organic capital generation and by not initiating further buybacks until this is achieved [2].  HSBC’s capital management approach is underpinned by a global capital risk policy, complemented by frameworks for recovery and resolution planning and stress testing [2].

**Citations:**

- [1] ING_Groep_N.V._ESEF_2025.xhtml
- [2] HSBC_Holdings_plc_ESEF_2025.xhtml
- [3] Barclays_Bank_PLC_ESEF_2025.xhtml


****
### 5. nordea_leverage_ratio
**Query:** What is Nordea's leverage ratio and how does management describe its approach to leverage risk management?
**Entity filter:** `['Nordeakoncernen']` | **Keywords sent:** `['leverage', 'ratio', 'Nordea', 'risk']`
**Retrieval query:** What is Nordea's leverage ratio and how does management describe its approach to leverage risk management? Nordeakoncernen
**Model:** `gemma3:27b` | **Latency:** 69.46s | **Pass:** ✅ | **Citation density:** 0.333

**Answer:**

> The available sources do not directly address this question. While the document extensively discusses risk management frameworks and various types of risks Nordea is exposed to (including credit, market, operational, and liquidity risk) [1], it does not explicitly state Nordea’s leverage ratio. Additionally, while the document details Nordea's approach to risk management—emphasizing a three-lines-of-defense model, integration into business strategies, and clear frameworks with policies and instructions [1]—it doesn’t specifically describe its approach to *leverage* risk management beyond general risk governance principles.

**Citations:**

- [1] Nordeakoncernen_ESEF_2025.xhtml


****
### 6. kbc_nii_sensitivity
**Query:** How does KBC Group describe its net interest income sensitivity and interest rate risk management?
**Entity filter:** `['KBC_Groep_NV']` | **Keywords sent:** `['KBC', 'interest', 'income', 'sensitivity', 'risk']`
**Retrieval query:** How does KBC Group describe its net interest income sensitivity and interest rate risk management? KBC Groep NV
**Model:** `gemma3:27b` | **Latency:** 109.1s | **Pass:** ❌ | **Citation density:** 0.071  ⚠ low

**Answer:**

> KBC Group identifies, measures, and monitors ESG-related credit risks as part of its Credit Risk Management Framework (CRMF) [1]. They use the Environmental Risk Impact Map (ERIM) to map the impact of climate and environmental risk factors on the credit risk profile [1]. Thematic analyses, known as White Papers, are also conducted regularly [1]. A sector heatmap is used in the credit acceptance and assessment process as a screening tool for risks within the corporate and SME portfolios [1]. ESG assessments are performed at counterparty level for significant credit files in high E&S-risk sectors [1].
>
> KBC develops specific measurement techniques to estimate the impact of ESG risks on its credit portfolio, including examining climate scenarios from the Network for Greening the Financial System (NGFS) to estimate sectoral climate impact on Probability of Default (PD) [1]. KBC aims to limit the negative impacts of its activities on the environment and society while promoting a positive impact through responsible lending practices outlined in a group-wide sustainability policy [1]. This commitment is reflected in credit risk standards and policies applied throughout the entire credit process [1].
>
> KBC’s hedging portfolio covers interest rate and inflation risks using interest rate swaps, with a return portfolio aiming for additional yield [1]. The average discount rate used was 3.39% in 2025 and 3.10% in 2024, with an expected salary increase of 2.45% in 2025 and 2.47% in 2024 [1].

**Citations:**

- [1] KBC_Groep_NV_ESEF_2025.xhtml

**Missing keywords:** ['income', 'sensitivity']
**⚠ Low citation density:** 0.071 (correct answer, sparse attribution)

****
### 7. climate_risk_bbva
**Query:** How does BBVA describe its approach to climate-related risks and its net zero transition strategy?
**Entity filter:** `['Banco_Bilbao_Vizcaya_Argentaria']` | **Keywords sent:** `['climate', 'risk', 'BBVA', 'emissions', 'transition']`
**Retrieval query:** How does BBVA describe its approach to climate-related risks and its net zero transition strategy? Banco Bilbao Vizcaya Argentaria, S.A.
**Model:** `gemma3:27b` | **Latency:** 67.37s | **Pass:** ✅ | **Citation density:** 0.091  ⚠ low

**Answer:**

> BBVA recognizes its important role in mitigating climate change due to its responsibility as a purpose-driven organization, aspiration to manage related risks, and opportunity to finance the transition [1]. The firm follows the recommendations of the Task Force on Climate-related Financial Disclosures (TCFD) and has developed a Transition Plan aligned with TCFD and the Glasgow Financial Alliance for Net Zero (GFANZ) [1].
>
> BBVA’s strategy focuses on two main objectives: promoting new business through sustainability – aiming to channel €300 billion into sustainable finance – and achieving net zero emissions by 2050. It is incorporating sustainability-related opportunities and risks into its strategy, business, processes, and risk management, expanding its sustainable product portfolio and considering climate transition risk in operations. BBVA assesses the impact of different climate scenarios—both transition and physical risks—on its strategy and business through exercises updated at least twice a year.
>
> BBVA conducts a climate assessment to determine its vulnerability to transition and physical risk, progressing towards a quantitative approach with defined metrics for assessing risk levels. It also assesses the materiality of climate-related risks using a double materiality analysis considering internal and external inputs such as Risk Assessment exercises [1]. The firm prioritizes sectors with more emissions-intensive production processes—like Oil & Gas, Power generation, Auto, Steel, Cement, Coal, Aviation, Shipping, Aluminum and Real estate—for decarbonization efforts through sectoral transition plans. BBVA is also working to reduce its own carbon footprint by measuring and managing energy consumption.
>
> BBVA integrates climate risk into its risk planning, internal reports, admission processes, and annual customer reviews, including evaluating compliance with its Environmental and Social Framework and assessing customer transition plans. It monitors customers’ progress toward improvements in ESG profiles and assesses the resilience of its strategy to different climate scenarios.

**Citations:**

- [1] Banco_Bilbao_Vizcaya_Argentaria,_S.A._ESEF_2024.xhtml

**⚠ Low citation density:** 0.091 (correct answer, sparse attribution)

****
### 8. climate_standard_chartered
**Query:** How does Standard Chartered describe its climate risk framework and net zero commitments?
**Entity filter:** `['StandardChartered_Bank']` | **Keywords sent:** `['climate', 'Standard Chartered', 'risk', 'net zero', 'transition']`
**Retrieval query:** How does Standard Chartered describe its climate risk framework and net zero commitments?
**Model:** `gemma3:27b` | **Latency:** 46.2s | **Pass:** ✅ | **Citation density:** 0.2

**Answer:**

> Standard Chartered embeds Climate Risk considerations across relevant Principal Risk Types and performs client-level Climate Risk assessments with adequate mitigants [1]. The PLC Group committed to be net zero in its own operations (Scope 1 and 2 emissions) by the end of 2025, intending to maintain this going forward [1]. They also use scenario analysis to evaluate how various Transition Risk scenarios impact Loan Impairment intensities and set net zero targets covering their 12 highest emitting sectors [1]. Standard Chartered has explained how it reflects the impact of climate change in its financial statements, aligning with its commitment to achieve net zero emissions by 2050 [1]. They assess potential impacts of climate change on the Group’s business and any consequential material impact on its financial statements [1].

**Citations:**

- [1] StandardChartered_Bank_ESEF_2025.xhtml


****
### 9. digital_ing
**Query:** What are ING Group's key technology investments and digital transformation priorities?
**Entity filter:** `['ING_Groep_N.V.']` | **Keywords sent:** `['technology', 'digital', 'ING', 'transformation']`
**Retrieval query:** What are ING Group's key technology investments and digital transformation priorities? ING Groep N.V.
**Model:** `gemma3:27b` | **Latency:** 50.18s | **Pass:** ✅ | **Citation density:** 0.143

**Answer:**

> ING Group’s key technology investments and digital transformation priorities center around four key enablers: providing seamless digital services, using scalable technology and operations, staying safe and secure, and unlocking their people’s full potential [1]. The ING Tech strategy has three goals under the leadership of the chief technology officer: increase productivity, excel in customer experience, and be a top employer for engineering talent [1].
>
> Specific priorities include operational excellence (enhancing reliability, reinforcing cybersecurity, investing in workforce), digital product governance (advancing capabilities for control & alignment), engineering (driving an engineering way of working including AI-enabled coding), transformation (expanding the scalable technology platform), and data/AI development [1]. They are focused on delivering scalable technology and operations that enable seamless, fully digital services with high standards of safety and security [1].
>
> ING aims to provide a seamless, mobile-first digital experience with personalized products supported by advanced technology and data insights; 87% of customers chose mobile as their primary channel in 2025 [1]. They are also focused on AI implications and allocating more time considering the strategic implications of AI [1]. Furthermore, they prioritize enhancing digital engagement for younger customers and offering personalized solutions for affluent clients [1].

**Citations:**

- [1] ING_Groep_N.V._ESEF_2025.xhtml


****
### 10. digital_nordea
**Query:** How does Nordea describe its digital banking strategy and IT modernization program?
**Entity filter:** `['Nordeakoncernen']` | **Keywords sent:** `['digital', 'banking', 'Nordea', 'technology']`
**Retrieval query:** How does Nordea describe its digital banking strategy and IT modernization program? Nordeakoncernen
**Model:** `gemma3:27b` | **Latency:** 79.72s | **Pass:** ❌ | **Citation density:** 0.167

**Answer:**

> Nordea is internationally recognized for its digital services and commitment to positive customer experiences [1]. The firm ranks among the top three banks globally in digitalization and is considered the best in Europe, with its bank app being named the best for private customers in the Nordics by the App Store [1]. Since 2019, Nordea has made structural changes to strengthen profitability and capital growth, resulting in a strong total return on equity compared to other banks [1]. Nordea’s strength lies in its Nordic business model and diversified credit portfolio, which have contributed to its position as one of Europe's leading financial groups [1].
>
> Nordea is also focused on enhancing its cyber defense with new tools and features, improving security routines for new business needs such as reliable mobile banking apps, and providing proactive support to customers to detect and prevent fraud [1]. The firm aims to offer inclusive, intuitive services that support customers in improving their financial well-being, expanding digital offerings, and assisting those who may not be able or willing to use digital bank services [1].

**Citations:**

- [1] Nordeakoncernen_ESEF_2025.xhtml

**Missing keywords:** ['technology']

****
### 11. barclays_holdco_sub
**Query:** How does Barclays describe its capital structure and the relationship between the holding company and its banking subsidiaries?
**Entity filter:** `['Barclays_Bank_PLC']` | **Keywords sent:** `['Barclays', 'capital', 'structure', 'holding', 'subsidiary']`
**Retrieval query:** How does Barclays describe its capital structure and the relationship between the holding company and its banking subsidiaries? Barclays Bank PLC
**Model:** `gemma3:27b` | **Latency:** 58.85s | **Pass:** ✅ | **Citation density:** 0.125

**Answer:**

> Barclays PLC holds 100% of the issued ordinary shares of Barclays Bank PLC [1]. The largest group in which the results of Barclays Bank PLC are consolidated is headed by Barclays PLC, located at 1 Churchill Place London E14 5HP [1].
>
> Barclays PLC, Barclays Bank PLC, BUSHL and BUSL have financial holding company (FHC) status under the Bank Holding Company Act of 1956, allowing them to engage in activities like underwriting and dealing in securities [1]. BUSL is the ultimate US holding company that holds substantially all of the Barclays Bank Group’s US subsidiaries, including Barclays Capital Inc. and Barclays Bank Delaware [1].
>
> The principal subsidiary companies of Barclays Bank Group had combined assets and liabilities of £582 billion (2024: £515 billion) and £559 billion (2024: £490 billion) respectively as of December 31, 2025 [1]. Regulatory requirements restrict the ability of these subsidiaries to remit dividends to Barclays Bank PLC except in specific circumstances like legal capital reduction or liquidation [1].
>
> Control over entities, including structured entities, is generally determined by ownership of voting capital; however, judgement is required when voting rights do not determine control, particularly with structured entities where activities are directed via contractual arrangements [1].

**Citations:**

- [1] Barclays_Bank_PLC_ESEF_2025.xhtml


****
### 12. erste_whitespace_collapse
**Query:** How does Erste Group describe its overall risk profile and key risk management priorities?
**Entity filter:** `['Erste_Group_BankAG']` | **Keywords sent:** `['Erste', 'risk', 'profile', 'management', 'framework']`
**Retrieval query:** How does Erste Group describe its overall risk profile and key risk management priorities? Erste Group BankAG
**Model:** `gemma3:27b` | **Latency:** 62.62s | **Pass:** ❌ | **Citation density:** 0.125

**Answer:**

> Erste Group’s overall risk profile is monitored through a Risk Dashboard, which illustrates the group and local units' risk potential against their limits [1]. The Group Risk Report/Risk Dashboard is regularly presented to the Board of Directors and Supervisory Board (including its Risk Committee) to support oversight and monitoring of the group’s and local subsidiaries’ risk profiles [1].
>
> The firm’s Risk Appetite Statement (RAS) for 2025-2029 was approved by the Board of Directors and the Supervisory Board's Risk Committee in late 2024, and presented to the Supervisory Board for information [1]. ESG risks are integrated into both the risk appetite and strategy, as well as being part of the Risk Materiality Assessment (RMA) — a process used to identify and assess potential impacts of these risks on the group’s risk profile [1].
>
> Key risk management priorities include monitoring credit risks based on parameters set by Credit Risk Management, with operational decisions made locally and at the Group level by Group Credit Risk Management [1]. The firm also prioritizes market risk activities through limits consistent with the overall RWA limit, translated into VaR and SVaR limits assigned to individual trading units [1]. Additionally, Erste Group focuses on non-financial risks, using internal loss data and Key Risk Indicators (KRI) to measure changes in risk levels, with a regular process for identifying new risk types and increasing risks [1]. Cyber Risk Management is also a key function reporting directly to the Group CRO [1].

**Citations:**

- [1] Erste_Group_BankAG_ESEF_2025.xhtml

**Missing keywords:** ['framework']
