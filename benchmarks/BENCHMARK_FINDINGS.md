# AIStudio — Benchmark Findings
*Generated: 2026-03-19 22:40*

## Configuration
- **Corpus:** `demo`
- **Top K:** 5
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 12
- **Passed:** 12/12 (100%)
- **Avg latency:** 4.9s

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
| 1 | What is QFD and how does it apply to technology architecture? | 5.72s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Tests retrieval of dedicated QFD documents (Architecture and QFD.pdf, BOEI - Architecture and QFD - 2003.pdf). Flagship demo question.
 |
| 2 | How do you design an IT organization around architectural principles? | 4.97s | ✅ | Architecture Concepts and How To Use The | Retrieves from Architecting the IT Organization and FS Journal. |
| 3 | How do architecture concepts help design organizations? | 3.77s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws on the universal architecture toolset concept — one of the core intellectual contributions of the corpus.
 |
| 4 | How should a CTO prioritize a three-year technology strategy? | 6.61s | ✅ | FS Journal, Edited by M. Barbero - IT In | Consistently returns 5 citations across all models. Draws from FS Journal Strategy volume and Barbero 2020 modernization paper.
 |
| 5 | What does a good technology target state look like? | 4.59s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong single-source answer from FS Journal Strategy volume. |
| 6 | How do you organize a large-scale IT transformation program? | 6.1s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws from GTIS Strategy document and FS Journal. |
| 7 | What is the relationship between business strategy and technology strategy? | 3.62s | ✅ | Barbero - 2020 - Technology Modernizatio | Core intellectual thread running through entire corpus — business strategy drives technology strategy, not the reverse.
 |
| 8 | What are the key considerations for cloud migration and technology modernization? | 5.52s | ✅ | Barbero - 2020 - Technology Modernizatio | Draws directly from Barbero 2020 Technology Modernization paper — original work with a principled-based approach framework. Replaces enterprise AI reference architecture question (weak retrieval).
 |
| 9 | What are the key principles for modernizing legacy applications? | 4.4s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong retrieval from Barbero 2020 Technology Modernization paper — original work, highly specific content.
 |
| 10 | What are the key risk and compliance considerations for financial services IT? | 4.31s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Retrieves from FS Journal Risk/Compliance/Security volume (2005). |
| 11 | How has digitization changed financial services technology? | 3.48s | ✅ | FS Journal, Edited by M. Barbero - Digit | Retrieves from FS Journal Digitization volume. Clean single-source answer with good citation compliance.
 |
| 12 | What is the role of architecture in managing technology risk in financial services? | 5.17s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Good synthesis question drawing on multiple FS Journal volumes. Strong closer for a demo sequence. |

## Detailed Results

### qfd_technology_architecture
**Query:** What is QFD and how does it apply to technology architecture?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.72s | **Pass:** ✅

**Answer:**
> Quality Function Deployment (QFD) is a methodology that can be used in the development of technology architecture. It is a systematic approach to defining the bridge between business vision, organizational constructs, processes and enabling technologies required to execute the vision [1].

In the context of IT architecture, QFD involves assessing multiple solutions and selecting one to implement [1]. This process is often referred to as "Design for Six Sigma" (DFSS) or "Voice of the Customer ana...


### it_org_architectural_principles
**Query:** How do you design an IT organization around architectural principles?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.97s | **Pass:** ✅

**Answer:**
> To design an IT organization around architectural principles, it is essential to define the principles, standards, and implementation considerations that collectively define an architecture [1]. This involves a one-to-one mapping between the conceptual/logical/physical concepts and the principle/standard/implementation consideration concepts [1]. The definition of organizational architecture/model requires the discipline usually associated with the architecture of complex systems [1].

The first...


### architecture_concepts_organizations
**Query:** How do architecture concepts help design organizations?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.77s | **Pass:** ✅

**Answer:**
> Architecture concepts can help design organizations by providing a framework for analyzing and resolving problems that arise in dealing with any kind of complex system [1]. These tools and techniques can be applied to organizational design, helping architects contribute actively to the debate on how to structure the IT organization [1][2]. Additionally, understanding the end-to-end "IT value chain" is essential in designing the IT organization with an emphasis on defining process rather than fun...


### cto_three_year_strategy
**Query:** How should a CTO prioritize a three-year technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.61s | **Pass:** ✅

**Answer:**
> To prioritize a three-year technology strategy, I would recommend combining elements from sources [1] and [2].

First, define an initial vision for the future linked to specific business goals and objectives. This can be done by prioritizing gaps between the present state and the desired future state, as described in source [2]. A standard visual notation and scenario-based functional view can serve as a foundation for business cases.

Next, consider the requirements from source [1], which sugge...


### technology_target_state
**Query:** What does a good technology target state look like?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.59s | **Pass:** ✅

**Answer:**
> A good technology target state looks like a progressive and pragmatic approach that defines realistic "transformation plateaus" aimed at implementing the end state step by step, while reducing technology and implementation risks [2]. This can be achieved by defining various implementation plateaus as stepping stones to reach the desired end state in actionable increments [2].

It's essential to consider multiple views when describing the current state, the end state, and the road map to that end...


### large_scale_it_transformation
**Query:** How do you organize a large-scale IT transformation program?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.1s | **Pass:** ✅

**Answer:**
> To organize a large-scale IT transformation program, it is essential to adopt an approach that is both formal and linear in execution ([1]). This involves setting up project work streams to design and build the desired data structures and database as part of a larger infrastructure transformation ([3]).

The decision-making process should be viewed as an iterative cycle with a feedback loop at each stage, allowing for continuous improvement and customization ([3]). This is similar to setting up ...


### business_technology_strategy
**Query:** What is the relationship between business strategy and technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.62s | **Pass:** ✅

**Answer:**
> According to [1], the high-level goal for technology should be derived and traced back to the components of the business strategy. This suggests that there is a direct relationship between business strategy and technology strategy.

[2] also supports this idea by stating that an IT organization's ability to produce and maintain underlying technology frameworks that bring its strategy to life is evidence of its strategic planning capabilities.

In addition, [3] discusses how the GTIS business str...


### cloud_migration_modernization
**Query:** What are the key considerations for cloud migration and technology modernization?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.52s | **Pass:** ✅

**Answer:**
> The key considerations for cloud migration and technology modernization include:

1. Assessing each application in the portfolio by both objective data (from a code scan) and qualitative data (from surveys) to segment and prioritize applications into categories such as Refactor, Revise, Rehost, Replace, and Retire ([2]).
2. Identifying specific cloud migration Blockers and Boosters within the source code of an application that is slated for migration to the cloud, including good practices that m...


### modernizing_legacy_applications
**Query:** What are the key principles for modernizing legacy applications?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.4s | **Pass:** ✅

**Answer:**
> Unfortunately, I don't see any information in the provided sources about key principles for modernizing legacy applications. However, I can extract some relevant information that might be helpful.

From [1], it seems that there is a mention of the Software Engineering Institute's "Horseshoe" model diagram, which goes back to 1999. This model stipulates two fundamental phases: Analysis and Synthesis. In the Analysis phase, the code's structure/architecture is recovered and checked for conformance...


### risk_compliance_financial_services
**Query:** What are the key risk and compliance considerations for financial services IT?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.31s | **Pass:** ✅

**Answer:**
> Key risk and compliance considerations for financial services IT include:

* Managing purely financial risk and compliance requirements dictated by government regulations [1]
* Addressing operational requirements created both by regulations and market forces [1]
* Understanding the convergence of key processes and the sharing of data across risk, finance, and compliance domains [1]
* Recognizing that all risk and compliance management require life cycles and can be prioritized in terms of curren...


### digitization_financial_services
**Query:** How has digitization changed financial services technology?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.48s | **Pass:** ✅

**Answer:**
> Digitization has changed financial services technology by bringing together many technologies in a suite or "digitization stack" that captures and manifests the way an institution operates today [1]. This allows financial institutions to meet security concerns for digitized organizations, including protection of digitized content, creating and maintaining digital records, and end-to-end information security strategy [1].

Digitization has also enabled banks to move away from paper-based processe...


### architecture_technology_risk
**Query:** What is the role of architecture in managing technology risk in financial services?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.17s | **Pass:** ✅

**Answer:**
> According to [1], IT investments have several common characteristics, regardless of their actual purpose.

The role of architecture in managing technology risk in financial services is not explicitly stated. However, it can be inferred that the development of an enterprise IT architecture (as mentioned in [2]) is necessary for managing complexity and maintaining the integrity of the IT environment.

[1] mentions the importance of strategic planning in IT investments, but does not directly addres...


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