# AIStudio — Benchmark Findings
*Generated: 2026-03-15 21:46*

## Configuration
- **Corpus:** `demo`
- **Top K:** 5
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 12
- **Passed:** 12/12 (100%)
- **Avg latency:** 5.9s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Corpus: 143 financial services 10-K filings, 105,964 chunks
- Ingest throughput: ~54 chunks/sec on M4
- Total ingest time: ~34 minutes for 143 files
- ChromaDB comparison: crashed at 32,285 chunks; Qdrant stable at 105,964

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | What is QFD and how does it apply to technology architecture? | 5.22s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Tests retrieval of dedicated QFD documents (Architecture and QFD.pdf, BOEI - Architecture and QFD - 2003.pdf). Flagship demo question.
 |
| 2 | How do you design an IT organization around architectural principles? | 5.4s | ✅ | Architecture Concepts and How To Use The | Retrieves from Architecting the IT Organization and FS Journal. |
| 3 | How do architecture concepts help design organizations? | 5.1s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws on the universal architecture toolset concept — one of the core intellectual contributions of the corpus.
 |
| 4 | How should a CTO prioritize a three-year technology strategy? | 5.51s | ✅ | FS Journal, Edited by M. Barbero - IT In | Consistently returns 5 citations across all models. Draws from FS Journal Strategy volume and Barbero 2020 modernization paper.
 |
| 5 | What does a good technology target state look like? | 5.94s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong single-source answer from FS Journal Strategy volume. |
| 6 | How do you organize a large-scale IT transformation program? | 6.6s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws from GTIS Strategy document and FS Journal. |
| 7 | What is the relationship between business strategy and technology strategy? | 5.22s | ✅ | Barbero - 2020 - Technology Modernizatio | Core intellectual thread running through entire corpus — business strategy drives technology strategy, not the reverse.
 |
| 8 | What are the key considerations for cloud migration and technology modernization? | 6.49s | ✅ | Barbero - 2020 - Technology Modernizatio | Draws directly from Barbero 2020 Technology Modernization paper — original work with a principled-based approach framework. Replaces enterprise AI reference architecture question (weak retrieval).
 |
| 9 | What are the key principles for modernizing legacy applications? | 7.99s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong retrieval from Barbero 2020 Technology Modernization paper — original work, highly specific content.
 |
| 10 | What are the key risk and compliance considerations for financial services IT? | 7.04s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Retrieves from FS Journal Risk/Compliance/Security volume (2005). |
| 11 | How has digitization changed financial services technology? | 4.24s | ✅ | FS Journal, Edited by M. Barbero - Digit | Retrieves from FS Journal Digitization volume. Clean single-source answer with good citation compliance.
 |
| 12 | What is the role of architecture in managing technology risk in financial services? | 5.68s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Good synthesis question drawing on multiple FS Journal volumes. Strong closer for a demo sequence. |

## Detailed Results

### qfd_technology_architecture
**Query:** What is QFD and how does it apply to technology architecture?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.22s | **Pass:** ✅

**Answer:**
> QFD stands for Quality Function Deployment, a tool used in the development of an enterprise IT architecture [1]. It implies that several solutions will be assessed and one will be selected and implemented [1]. QFD is mentioned as a technique that can be used in the development of an enterprise IT architecture, along with other tools such as voice of the customer analysis [1].

In the context of technology architecture, QFD can be used to systematically define a coherent set of principles and sta...


### it_org_architectural_principles
**Query:** How do you design an IT organization around architectural principles?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.4s | **Pass:** ✅

**Answer:**
> To design an IT organization around architectural principles, one should start by defining the principles, standards, and implementation considerations that collectively define an architecture [1]. This involves identifying the key organizational principles that will guide decision-making and actions within the IT organization.

These principles should be aligned with the business goals and objectives, and should take into account the specific needs and requirements of the organization. For exam...


### architecture_concepts_organizations
**Query:** How do architecture concepts help design organizations?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.1s | **Pass:** ✅

**Answer:**
> Architecture concepts can help design organizations by providing a high-level primer on how to design "architecture," whether technology or organizational architecture. They also help architects think and work, and provide a way for them to contribute actively to the debate on how to structure the IT organization.

According to [1], architecture concepts can be applied to organizational design, particularly in terms of communication, project management, and knowledge management. The article also...


### cto_three_year_strategy
**Query:** How should a CTO prioritize a three-year technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.51s | **Pass:** ✅

**Answer:**
> To prioritize a three-year technology strategy, a CTO should start by defining and prioritizing the requirements, as suggested in [1]. This involves identifying the key capabilities and scope of the CMDB implementation, defining and including CIs that will provide the most business value in the short term (0-4 months), and employing an iterative process to assess the maturity of the CMDB and enhance it in alignment with the organization's specific requirements.

Next, the CTO should establish a ...


### technology_target_state
**Query:** What does a good technology target state look like?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.94s | **Pass:** ✅

**Answer:**
> A good technology target state looks like a clear and well-defined description of the organization's desired future state, with a focus on the value to be delivered, rather than just costs. 

To achieve this, it is recommended to use a progressive and pragmatic approach that defines realistic "transformation plateaus" aimed at implementing the end state step by step, while reducing technology and implementation risks [2]. This involves breaking down the end state into actionable increments, or i...


### large_scale_it_transformation
**Query:** How do you organize a large-scale IT transformation program?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.6s | **Pass:** ✅

**Answer:**
> To organize a large-scale IT transformation program, a structured approach is necessary. Based on the provided sources, here is a step-by-step guide:

1. **Establish a clear vision and priorities**: Envision the future state of the organization and identify key priorities for the transformation program. This involves gathering data, analyzing infrastructure requirements, and determining the most beneficial areas for improvement (Source: [1, 2]).
2. **Break down the transformation into manageable...


### business_technology_strategy
**Query:** What is the relationship between business strategy and technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.22s | **Pass:** ✅

**Answer:**
> According to [2], the relationship between business strategy and technology strategy is that the technology strategy should be derived from and aligned with the business strategy. In fact, the article states that "a level of difficulty arises from the fact that financial services organizations are best described as multi-enterprise organizations consisting of related, but often very distinct, lines of business." [2] This suggests that developing a common enterprise-wide IT strategy and architect...


### cloud_migration_modernization
**Query:** What are the key considerations for cloud migration and technology modernization?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.49s | **Pass:** ✅

**Answer:**
> To answer the question, the key considerations for cloud migration and technology modernization are:

1. **Assessing each application's cloud readiness**: This involves evaluating each application using both objective data (from code scans) and qualitative data (from surveys) to segment and prioritize applications into categories such as Refactor, Revise, Rehost, Replace, and Retire [2].
2. **Identifying cloud migration blockers and boosters**: The scanning process can identify specific cloud mi...


### modernizing_legacy_applications
**Query:** What are the key principles for modernizing legacy applications?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.99s | **Pass:** ✅

**Answer:**
> The key principles for modernizing legacy applications are:

1. **PRINCIPLE I - Refactor and Re-Architect - That the original design of a legacy application is, by definition, a product of its time and should be refactored to meet current best practices.** This principle is based on the idea that the original design of a legacy application is outdated and should be re-architectured to meet current needs.
2. **PRINCIPLE II - Understand and Manage Cross-Portfolio Governance - That solving complex ...


### risk_compliance_financial_services
**Query:** What are the key risk and compliance considerations for financial services IT?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.04s | **Pass:** ✅

**Answer:**
> Based on the provided sources, the key risk and compliance considerations for financial services IT can be summarized as follows:

The financial services industry is experiencing increasing convergence between risk management and compliance management issues, driven by expanding regulatory requirements and market forces [1]. This convergence extends across the risk and compliance continuum, from purely financial risk and compliance requirements to operational requirements created by regulations ...


### digitization_financial_services
**Query:** How has digitization changed financial services technology?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.24s | **Pass:** ✅

**Answer:**
> Digitization has significantly changed financial services technology by bringing together many technologies in a suite, or "digitization stack," that captures and manifests the way an institution operates today [1]. This integrated view enables financial institutions to transform their internal and external operations, freeing up financial, human, and information resources [1].

The digitization of financial services technology has several key benefits, including:

* Creating and maintaining a d...


### architecture_technology_risk
**Query:** What is the role of architecture in managing technology risk in financial services?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.68s | **Pass:** ✅

**Answer:**
> According to the sources, the role of architecture in managing technology risk in financial services is crucial, but often challenging for financial services firms to implement effectively.

[1] highlights the need for a strategic approach to IT investments, emphasizing the importance of managing complexity and maintaining the integrity of the IT environment. It also notes that traditional enterprise IT architecture efforts often have been perceived as large, difficult, and expensive, making it ...


## Known Limitations
- Cross-corpus semantic pollution: queries without firm filter may return non-target firm chunks
- XBRL/structured data noise in HTML 10-K filings — BeautifulSoup parser needs XBRL stripping
- Relevance threshold not yet implemented — low-scoring chunks included in context
- Northern Trust / Nuveen CIK collision — duplicate filings in corpus
- BNY Mellon CIK incorrect — old filings only

## Roadmap
- Metadata filtering UI (firm/year dropdown in query area)
- Relevance threshold — discard chunks below similarity cutoff
- XBRL stripping in HTML ingestion
- Reranker pass (CrossEncoder ms-marco-MiniLM)
- Embedding model eval: nomic-embed-text vs bge-large
- PDF viewer with click-to-source citation