# AIStudio — Benchmark Findings
*Generated: 2026-03-16 17:58*

## Configuration
- **Corpus:** `demo`
- **Top K:** 5
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 12
- **Passed:** 12/12 (100%)
- **Avg latency:** 6.0s

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
| 1 | What is QFD and how does it apply to technology architecture? | 7.78s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Tests retrieval of dedicated QFD documents (Architecture and QFD.pdf, BOEI - Architecture and QFD - 2003.pdf). Flagship demo question.
 |
| 2 | How do you design an IT organization around architectural principles? | 6.27s | ✅ | Architecture Concepts and How To Use The | Retrieves from Architecting the IT Organization and FS Journal. |
| 3 | How do architecture concepts help design organizations? | 4.76s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws on the universal architecture toolset concept — one of the core intellectual contributions of the corpus.
 |
| 4 | How should a CTO prioritize a three-year technology strategy? | 5.75s | ✅ | FS Journal, Edited by M. Barbero - IT In | Consistently returns 5 citations across all models. Draws from FS Journal Strategy volume and Barbero 2020 modernization paper.
 |
| 5 | What does a good technology target state look like? | 5.17s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong single-source answer from FS Journal Strategy volume. |
| 6 | How do you organize a large-scale IT transformation program? | 6.17s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws from GTIS Strategy document and FS Journal. |
| 7 | What is the relationship between business strategy and technology strategy? | 4.81s | ✅ | Barbero - 2020 - Technology Modernizatio | Core intellectual thread running through entire corpus — business strategy drives technology strategy, not the reverse.
 |
| 8 | What are the key considerations for cloud migration and technology modernization? | 6.83s | ✅ | Barbero - 2020 - Technology Modernizatio | Draws directly from Barbero 2020 Technology Modernization paper — original work with a principled-based approach framework. Replaces enterprise AI reference architecture question (weak retrieval).
 |
| 9 | What are the key principles for modernizing legacy applications? | 7.44s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong retrieval from Barbero 2020 Technology Modernization paper — original work, highly specific content.
 |
| 10 | What are the key risk and compliance considerations for financial services IT? | 6.05s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Retrieves from FS Journal Risk/Compliance/Security volume (2005). |
| 11 | How has digitization changed financial services technology? | 5.22s | ✅ | FS Journal, Edited by M. Barbero - Digit | Retrieves from FS Journal Digitization volume. Clean single-source answer with good citation compliance.
 |
| 12 | What is the role of architecture in managing technology risk in financial services? | 5.64s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Good synthesis question drawing on multiple FS Journal volumes. Strong closer for a demo sequence. |

## Detailed Results

### qfd_technology_architecture
**Query:** What is QFD and how does it apply to technology architecture?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.78s | **Pass:** ✅

**Answer:**
> Quality Function Deployment (QFD) is a methodology that can be applied to technology architecture to ensure that the design and implementation of technology solutions meet the needs and requirements of the business.

According to the provided sources, QFD is a tool that can be used in the development of an enterprise IT architecture [1]. It is based on the principles of quality development and is used to assess and select the best solutions to architectural or organizational problems. The QFD me...


### it_org_architectural_principles
**Query:** How do you design an IT organization around architectural principles?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.27s | **Pass:** ✅

**Answer:**
> Designing an IT organization around architectural principles involves several key steps and considerations. According to [1], defining an organizational architecture/model requires discipline and the definition of principles, standards, and implementation considerations. The first step in this process is to define the principles that will govern decisions and actions within the organization. These principles should be related to the use of outsourcing, for example, and influence the positioning ...


### architecture_concepts_organizations
**Query:** How do architecture concepts help design organizations?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.76s | **Pass:** ✅

**Answer:**
> Architecture concepts help design organizations in several ways. Firstly, they provide a framework for thinking about and organizing complex systems, which can be applied to both technology and organizational architecture. This framework includes concepts such as governance models, processes, and organizational constructs, which are essential for effective organizational design [1].

Secondly, architecture concepts can help identify and address critical success factors, such as leveraging the be...


### cto_three_year_strategy
**Query:** How should a CTO prioritize a three-year technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.75s | **Pass:** ✅

**Answer:**
> Based on the provided sources, a CTO should prioritize a three-year technology strategy by:

1. Deriving the high-level goal for technology from the business strategy or a well-defined transformative business initiative [5].
2. Tracing the technology goals back to the components of the business strategy [5].
3. Identifying and prioritizing the requirements, evaluating and short-listing vendors before selecting a best-fit tool [1].
4. Defining and including CIs (Configuration Items) that will pro...


### technology_target_state
**Query:** What does a good technology target state look like?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.17s | **Pass:** ✅

**Answer:**
> A good technology target state should be defined at a conceptual level, taking into account the high-level goal for technology that is derived from and traced back to the components of the business strategy [1]. This goal should focus on value delivered vis-à-vis costs, rather than just reducing costs [1].

In some cases, the technology necessary to implement the target state may not be ready yet, budgets may not be available, or key talents may not have been recruited yet, so the end state can ...


### large_scale_it_transformation
**Query:** How do you organize a large-scale IT transformation program?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.17s | **Pass:** ✅

**Answer:**
> To organize a large-scale IT transformation program, consider the following steps:

1. **Adopt a high level of formality and linearity in execution**: For large, enterprisewide projects, it is essential to adopt a high level of formality and linearity in execution, especially when employees are widely dispersed [1].
2. **Envision your first day in leading an IT transformational change**: On your first day, focus on organization transformation, whether it is a wholesale multiyear project or the r...


### business_technology_strategy
**Query:** What is the relationship between business strategy and technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.81s | **Pass:** ✅

**Answer:**
> According to the sources, the relationship between business strategy and technology strategy is that the technology strategy should be derived from and aligned with the business strategy. [1] states that the high-level goal for technology should be "derived and traced back to the components of the business strategy" (or a well-defined, transformative business initiative). [2] also emphasizes the importance of aligning IT strategy with business objectives, and that a good IT strategy is one that ...


### cloud_migration_modernization
**Query:** What are the key considerations for cloud migration and technology modernization?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.83s | **Pass:** ✅

**Answer:**
> To answer your question, the key considerations for cloud migration and technology modernization are:

1. **Assessing application readiness**: Evaluate each application in the portfolio using objective data (from code scans) and qualitative data (from surveys) to segment and prioritize applications into categories such as Refactor, Revise, Rehost, Replace, and Retire [2].
2. **Identifying cloud blockers and boosters**: Use scanning tools to identify specific cloud migration blockers and boosters...


### modernizing_legacy_applications
**Query:** What are the key principles for modernizing legacy applications?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.44s | **Pass:** ✅

**Answer:**
> The key principles for modernizing legacy applications are outlined in the provided sources. According to the sources, the key principles are:

1. **PRINCIPLE I - Identify, Understand and Prioritize**: This principle involves identifying the legacy application that requires modernization, understanding its current state, and prioritizing the modernization efforts based on business value and technical feasibility [1].
2. **PRINCIPLE II - Renovation**: This principle involves analyzing the legacy ...


### risk_compliance_financial_services
**Query:** What are the key risk and compliance considerations for financial services IT?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.05s | **Pass:** ✅

**Answer:**
> The key risk and compliance considerations for financial services IT, based on the provided source [1], are:

1. Convergence of risk, compliance, and security management: The source emphasizes that risk, compliance, and security management are converging, and financial institutions should consider this convergence when managing their IT infrastructure.
2. Regulatory compliance: The source highlights the importance of regulatory compliance, citing the Sarbanes-Oxley Act and Basel II as examples o...


### digitization_financial_services
**Query:** How has digitization changed financial services technology?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.22s | **Pass:** ✅

**Answer:**
> Digitization has significantly changed financial services technology by bringing together various technologies in a suite, or digitization stack, that captures and manifests the way an institution operates today [1]. This integration of technologies has enabled financial institutions to meet the demands of digitization, including the protection of digitized content, creating and maintaining digital identities, and improving security [1].

The digitization of financial services technology has als...


### architecture_technology_risk
**Query:** What is the role of architecture in managing technology risk in financial services?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.64s | **Pass:** ✅

**Answer:**
> Based on the provided sources, the role of architecture in managing technology risk in financial services is crucial. It enables near real-time monitoring of the firm's exposure in several risk domains, such as market risk and client risk, by leveraging advanced application integration architecture [1]. This allows financial services firms to better manage complexity and maintain the integrity of the IT environment [2].

Furthermore, enterprise IT architecture plays a vital role in managing tech...


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