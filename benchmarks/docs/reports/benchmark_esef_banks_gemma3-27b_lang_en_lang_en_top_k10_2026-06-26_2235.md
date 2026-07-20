# AIStudio — Benchmark Findings
*Generated: 2026-06-26 22:43*

## Configuration
- **Corpus:** `esef_banks`
- **Scope:** lang_en — 5 firm(s): ING Groep N.V., Barclays Bank PLC, HSBC Holdings plc, StandardChartered Bank, Banco Bilbao Vizcaya Argentaria, S.A.
- **Base Top K:** 10 (effective K may be higher for multi-entity queries)
- **Temperature:** 0.3
- **Alpha:** 0.5
- **Min Score:** 0.5
- **Model:** gemma3:27b
- **API:** http://localhost:8000
- **Questions:** `lang_en`

## Summary
- **Questions:** 8
- **Passed (binary):** 6/8 (75%)
- **Rating (AIStudio_878):** 🟢 6 GREEN · 🟡 2 AMBER · 🔴 0 RED
- **Avg latency:** 62.7s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `esef_banks` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | How does ING Group describe its CET1 capital ratio and regulatory capital position in its most recent annual report? | 62.13s | 🟡 | ING_Groep_N.V._ESEF_2025.xhtml ⚠low-density | L1 baseline. ING files in English. Entity tag in corpus = 'ING Groep N.V.'. |
| 2 | What is Barclays' Tier 1 capital ratio and what are the components of their capital stack? | 46.59s | 🟢 | Barclays_Bank_PLC_ESEF_2025.xhtml | Annex 1 holdco/sub case. Entity in corpus = 'Barclays Bank PLC' (sub). Tests alias resolution. |
| 3 | What is HSBC's leverage ratio and how does it compare to the regulatory minimum requirement? | 49.97s | 🟡 | HSBC_Holdings_plc_ESEF_2025.xhtml | L1 table-located fact. Tests table extraction on a clean EN filer. |
| 4 | How do ING Group, HSBC, and Barclays compare in terms of their CET1 capital ratios and capital management approaches? | 74.24s | 🟢 | ING_Groep_N.V._ESEF_2025.xhtml, HSBC_Hol | Cross-firm EN comparison. Tests entity isolation across 3 firms. |
| 5 | How does BBVA describe its approach to climate-related risks and its net zero transition strategy? | 59.13s | 🟢 | Banco_Bilbao_Vizcaya_Argentaria,_S.A._ES | BBVA FY2024 (latest available). EN filer despite Spanish jurisdiction. GLEIF mis-merge risk class. |
| 6 | How does Standard Chartered describe its climate risk framework and net zero commitments? | 49.78s | 🟢 | StandardChartered_Bank_ESEF_2025.xhtml | Annex 1 holdco/sub class. Entity in corpus = 'StandardChartered Bank' (whitespace missing). |
| 7 | What are ING Group's key technology investments and digital transformation priorities? | 53.05s | 🟢 | ING_Groep_N.V._ESEF_2025.xhtml | Digital Banking |
| 8 | How does Barclays describe its capital structure and the relationship between the holding company and its banking subsidiaries? | 107.04s | 🟢 | Barclays_Bank_PLC_ESEF_2025.xhtml | Annex 1 DEMO_10 holdco/sub teaching case. Entity = 'Barclays Bank PLC' in corpus. PROVEN PASS. |

## Detailed Results

****
### 1. cet1_ing_group
**Query:** How does ING Group describe its CET1 capital ratio and regulatory capital position in its most recent annual report?
**Entity filter:** `['ING_Groep_N.V.']` | **Keywords sent:** `['CET1', 'capital', 'ING', 'ratio', 'regulatory']`
**Retrieval query:** How does ING Group describe its CET1 capital ratio and regulatory capital position in its most recent annual report? ING Groep N.V.
**Model:** `gemma3:27b` | **Latency:** 62.13s | **Pass:** ❌ | **Citation density:** 0.071  ⚠ low

**Answer:**

> ING Group's CET1 ratio was 13.1% as of December 31, 2025, decreasing from 13.6% at the end of 2024 [1]. The firm’s fully loaded CET1 requirement stood at 11.09% at the end of 4Q2025 (compared to 10.88% in 4Q2024) and is higher than the prevailing CET1 ratio requirement [1]. ING's CET1 target level is approximately 13%, which is well above the maximum distributable amount (MDA) level of 11.03% at December 31, 2025, creating a management buffer of about 195 basis points [1]. The overall SREP CET1 requirement for ING Group increased during 2025 to 11.03% due to an increase in the countercyclical buffer requirement [1]. Minimum Pillar 1 capital requirements applicable to ING Group are a CET1 ratio of 4.5%, a Tier 1 ratio of 6.0%, and a Total capital ratio of 8.0% of risk-weighted assets [1].

**Citations:**

- [1] ING_Groep_N.V._ESEF_2025.xhtml

**Missing keywords:** ['regulatory']
**⚠ Low citation density:** 0.071 (correct answer, sparse attribution)

****
### 2. tier1_capital_barclays
**Query:** What is Barclays' Tier 1 capital ratio and what are the components of their capital stack?
**Entity filter:** `['Barclays_Bank_PLC']` | **Keywords sent:** `['Tier 1', 'capital', 'ratio', 'Barclays', 'CET1']`
**Retrieval query:** What is Barclays' Tier 1 capital ratio and what are the components of their capital stack? Barclays Bank PLC
**Model:** `gemma3:27b` | **Latency:** 46.59s | **Pass:** ✅ | **Citation density:** 0.143

**Answer:**

> Barclays Bank PLC’s solo-consolidated CET1 ratio was 12.7% as of December 31, 2025 [1]. The Tier 1 capital ratio was 16.1% and total regulatory capital was 19.0% in 2025 [1].
>
> As of 2025, Barclays Bank PLC’s CET1 capital totaled £28,177 million, while its Tier 1 capital reached £35,848 million and total regulatory capital amounted to £42,129 million [1]. Total risk weighted assets were £222,247 million in 2025 [1].

**Citations:**

- [1] Barclays_Bank_PLC_ESEF_2025.xhtml


****
### 3. leverage_ratio_hsbc
**Query:** What is HSBC's leverage ratio and how does it compare to the regulatory minimum requirement?
**Entity filter:** `['HSBC_Holdings_plc']` | **Keywords sent:** `['leverage', 'ratio', 'HSBC', 'regulatory', 'minimum']`
**Retrieval query:** What is HSBC's leverage ratio and how does it compare to the regulatory minimum requirement? HSBC Holdings plc
**Model:** `gemma3:27b` | **Latency:** 49.97s | **Pass:** ❌ | **Citation density:** 0.111

**Answer:**

> HSBC's leverage ratio was 5.3% at December 31, 2025, decreasing from 5.6% at December 31, 2024 [1]. The UK minimum leverage ratio requirement was 3.25%, with an additional buffer of 0.9% – comprising a 0.7% additional leverage ratio buffer and a 0.2% countercyclical leverage ratio buffer [1]. HSBC exceeded these leverage requirements throughout 2025 [1].

**Citations:**

- [1] HSBC_Holdings_plc_ESEF_2025.xhtml

**Missing keywords:** ['regulatory']

****
### 4. cet1_cross_firm_en
**Query:** How do ING Group, HSBC, and Barclays compare in terms of their CET1 capital ratios and capital management approaches?
**Entity filter:** `['ING_Groep_N.V.', 'HSBC_Holdings_plc', 'Barclays_Bank_PLC']` | **Keywords sent:** `['CET1', 'capital', 'ING', 'HSBC', 'Barclays']`
**Retrieval query:** How do ING Group, HSBC, and Barclays compare in terms of their CET1 capital ratios and capital management approaches? ING Groep N.V. Barclays Bank PLC HSBC Holdings plc
**Model:** `gemma3:27b` | **Latency:** 74.24s | **Pass:** ✅ | **Citation density:** 0.12

**Answer:**

> ING Group’s fully loaded CET1 requirement was 11.09% at the end of 4Q2025, up from 10.88% in 4Q2024 [1]. The overall SREP CET1 requirement for ING Group increased to 11.03% at December 31, 2025, comprised of a 4.5% Pillar 1 requirement, a 0.93% Pillar 2 requirement, a 2.5% capital conservation buffer, a 0.93% countercyclical buffer, 0.16% Sectoral Systemic Risk buffer, and a 2.0% Other Systemically Important Institutions (O-SII) buffer [1]. ING intends to maintain its CET1 capital ratio within a medium-term target range of 14%-14.5% [2].
>
> Barclays Bank PLC’s solo-consolidated CET1 ratio was 12.7% as of December 31, 2025, exceeding the minimum regulatory requirement of 10.4% [3]. The firm is subject to a binding Pillar 1 minimum capital requirement to satisfy a CET1 ratio of 4.5%, a Tier 1 capital ratio of 6.0%, and a total capital ratio of 8.0% of risk-weighted assets [3]. Barclays also has additional capital requirements including Pillar 2A, capital buffers (CCB, CCyB, O-SII), and a G-SII buffer [3].
>
> HSBC’s target CET1 capital ratio is within the range of 14%-14.5% [2]. The privatization of Hang Seng Bank had a net CET1 capital impact of 110bps in January 2026, but HSBC expects to restore its CET1 capital ratio within this target range through organic capital generation and by not initiating further buy-backs until the ratio is back within or above the range [2].
>
> The available sources do not directly address a comparison of capital management *approaches* between these three firms beyond stating that each firm has internal processes to manage capital adequacy, regulatory requirements, and risk appetite.

**Citations:**

- [1] ING_Groep_N.V._ESEF_2025.xhtml
- [2] HSBC_Holdings_plc_ESEF_2025.xhtml
- [3] Barclays_Bank_PLC_ESEF_2025.xhtml


****
### 5. climate_risk_bbva
**Query:** How does BBVA describe its approach to climate-related risks and its net zero transition strategy?
**Entity filter:** `['Banco_Bilbao_Vizcaya_Argentaria']` | **Keywords sent:** `['climate', 'risk', 'BBVA', 'emissions', 'transition']`
**Retrieval query:** How does BBVA describe its approach to climate-related risks and its net zero transition strategy? Banco Bilbao Vizcaya Argentaria, S.A.
**Model:** `gemma3:27b` | **Latency:** 59.13s | **Pass:** ✅ | **Citation density:** 0.1

**Answer:**

> BBVA recognizes its important role in mitigating climate change due to its responsibility as a purpose-driven organization, its aspiration to manage associated risks, and the business opportunity presented by supporting customers’ transitions [1]. The firm follows the recommendations of the Task Force on Climate-related Financial Disclosures (TCFD) and has developed a Transition Plan aligned with TCFD and the Glasgow Financial Alliance for Net Zero (GFANZ) [1].
>
> BBVA's strategy centers around two main objectives: promoting new business through sustainability – aiming to channel €300 billion into sustainable finance – and achieving net zero emissions by 2050. It is progressively incorporating sustainability-related opportunities and risks into its strategy, business, processes, and risk management, expanding its sustainable product portfolio and considering climate transition risk in its operations.
>
> BBVA assesses the impact of different climate scenarios (both transition and physical risks) on its strategy and business through a forward-looking exercise updated at least twice a year. Since 2020, it has conducted climate assessments to determine its vulnerability to these risks, progressing toward a quantitative approach with defined metrics.  It also assesses potential impacts of extreme climate events on its portfolio and how climate-related factors might influence its main risk categories.
>
> BBVA's decarbonization strategy includes sectoral transition plans prioritizing emissions-intensive sectors like Oil & Gas, Power generation, Auto, Steel, Cement, Coal, Aviation, Shipping, Aluminum and Real estate. It is also working to reduce its own carbon footprint by measuring and managing energy consumption, integrating climate risk into its risk planning and capital assessment exercises.  BBVA monitors customers’ progress on sustainability and expects improvements in the short and medium term.

**Citations:**

- [1] Banco_Bilbao_Vizcaya_Argentaria,_S.A._ESEF_2024.xhtml


****
### 6. climate_standard_chartered
**Query:** How does Standard Chartered describe its climate risk framework and net zero commitments?
**Entity filter:** `['StandardChartered_Bank']` | **Keywords sent:** `['climate', 'Standard Chartered', 'risk', 'net zero', 'transition']`
**Retrieval query:** How does Standard Chartered describe its climate risk framework and net zero commitments?
**Model:** `gemma3:27b` | **Latency:** 49.78s | **Pass:** ✅ | **Citation density:** 0.143

**Answer:**

> Standard Chartered embeds Climate Risk considerations across relevant Principal Risk Types and performs client-level Climate Risk assessments, setting adequate mitigants or controls where relevant [1]. The PLC Group has committed to be net zero in its own operations (Scope 1 and 2 emissions) by the end of 2025 and intends to maintain this going forward [1]. They also embed values through Position Statements and a list of prohibited activities, maintaining ESG and Reputational Risk standards to identify, assess, and manage risks when providing services to clients [1].
>
> Standard Chartered considers transition risk with reference to client transition pathways, covering 12 highest emitting sectors, and uses net zero targets alongside climate risk questionnaires to assess clients for transition risks [1]. They use scenario analysis to evaluate how Transition Risk scenarios impact Loan Impairment intensities [1].  Exposure to Climate Risk is monitored in conjunction with other Principal Risk Types, embedding qualitative and quantitative climate considerations into Credit Underwriting Principles for portfolios like Oil & Gas, Mining, Shipping, Commercial real estate, and Project Finance [1]. Starting October 2025, they introduced a Client-level Physical Risk Grading Framework to identify and monitor key risk hotspots in the CIB portfolio regarding exposure to extreme weather events, alongside existing Transition Risk Grading [1].

**Citations:**

- [1] StandardChartered_Bank_ESEF_2025.xhtml


****
### 7. digital_ing
**Query:** What are ING Group's key technology investments and digital transformation priorities?
**Entity filter:** `['ING_Groep_N.V.']` | **Keywords sent:** `['technology', 'digital', 'ING', 'transformation']`
**Retrieval query:** What are ING Group's key technology investments and digital transformation priorities? ING Groep N.V.
**Model:** `gemma3:27b` | **Latency:** 53.05s | **Pass:** ✅ | **Citation density:** 0.143

**Answer:**

> ING Group’s key technology investments and digital transformation priorities center around four key enablers: providing seamless digital services, using scalable technology and operations, staying safe and secure, and unlocking their people’s full potential [1]. The ING Tech strategy has three goals under the leadership of the chief technology officer: increase productivity, excel in customer experience, and be a top employer for engineering talent [1].
>
> Specific priorities include operational excellence – enhancing reliability, reinforcing cybersecurity, and investing in the workforce [1]; digital product governance – advancing digital product capabilities for control, transparency, and strategic alignment [1]; engineering – driving an engineering way of working and innovation including AI-enabled coding [1]; transformation – continuing development and expansion of their scalable technology platform [1]; and data and AI development – accelerating responsible and effective use of data [1].
>
> ING aims to deliver scalable technology and operations that enable seamless, fully digital services with enhanced customer experience and high standards of safety and security [1]. They are focused on providing a seamless, mobile-first digital experience, engaging customers across daily banking activities with personalized products supported by advanced technology and data insights [1]. In 2025, 87% of customers chose mobile as their primary channel [1]. Furthermore, they prioritize making banking frictionless and relevant through ‘always-on’ channels and data-enabled personalization [1].

**Citations:**

- [1] ING_Groep_N.V._ESEF_2025.xhtml


****
### 8. barclays_holdco_sub
**Query:** How does Barclays describe its capital structure and the relationship between the holding company and its banking subsidiaries?
**Entity filter:** `['Barclays_Bank_PLC']` | **Keywords sent:** `['Barclays', 'capital', 'structure', 'holding', 'subsidiary']`
**Retrieval query:** How does Barclays describe its capital structure and the relationship between the holding company and its banking subsidiaries? Barclays Bank PLC
**Model:** `gemma3:27b` | **Latency:** 107.04s | **Pass:** ✅ | **Citation density:** 0.111

**Answer:**

> Barclays PLC holds 100% of the issued ordinary shares of Barclays Bank PLC [1]. The largest group in which the results of Barclays Bank PLC are consolidated is headed by Barclays PLC, located at 1 Churchill Place London E14 5HP [1].
>
> Barclays PLC, Barclays Bank PLC, BUSHL and BUSL have financial holding company (FHC) status under the Bank Holding Company Act of 1956, allowing them to engage in various financial activities through subsidiaries [1]. BUSL is the ultimate US holding company that holds substantially all of the Barclays Bank Group’s US subsidiaries, including Barclays Capital Inc. and Barclays Bank Delaware [1].
>
> The Barclays Bank Group’s principal subsidiary companies had combined assets and liabilities (before intercompany eliminations) of £582 billion in 2025 and £515 billion in 2024 [1]. Regulatory requirements restrict subsidiaries' ability to remit dividends to Barclays Bank PLC except during legal capital reduction or liquidation [1].
>
> Control over entities, particularly structured entities, is determined by assessing power over activities, not just voting rights [1]. The Barclays Bank Group consolidates structured entities where it has control and exposure to returns [1].

**Citations:**

- [1] Barclays_Bank_PLC_ESEF_2025.xhtml

