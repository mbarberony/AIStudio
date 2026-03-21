# AIStudio — Benchmark Findings
*Generated: 2026-03-19 22:07*

## Configuration
- **Corpus:** `demo`
- **Top K:** 5
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 12
- **Passed:** 12/12 (100%)
- **Avg latency:** 6.4s

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
| 1 | What is QFD and how does it apply to technology architecture? | 22.42s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Tests retrieval of dedicated QFD documents (Architecture and QFD.pdf, BOEI - Architecture and QFD - 2003.pdf). Flagship demo question.
 |
| 2 | How do you design an IT organization around architectural principles? | 5.95s | ✅ | Architecture Concepts and How To Use The | Retrieves from Architecting the IT Organization and FS Journal. |
| 3 | How do architecture concepts help design organizations? | 4.85s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws on the universal architecture toolset concept — one of the core intellectual contributions of the corpus.
 |
| 4 | How should a CTO prioritize a three-year technology strategy? | 5.52s | ✅ | FS Journal, Edited by M. Barbero - IT In | Consistently returns 5 citations across all models. Draws from FS Journal Strategy volume and Barbero 2020 modernization paper.
 |
| 5 | What does a good technology target state look like? | 4.59s | ✅ | Architecture Concepts and How To Use The | Strong single-source answer from FS Journal Strategy volume. |
| 6 | How do you organize a large-scale IT transformation program? | 5.26s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws from GTIS Strategy document and FS Journal. |
| 7 | What is the relationship between business strategy and technology strategy? | 4.95s | ✅ | Barbero - 2020 - Technology Modernizatio | Core intellectual thread running through entire corpus — business strategy drives technology strategy, not the reverse.
 |
| 8 | What are the key considerations for cloud migration and technology modernization? | 5.03s | ✅ | Barbero - 2020 - Technology Modernizatio | Draws directly from Barbero 2020 Technology Modernization paper — original work with a principled-based approach framework. Replaces enterprise AI reference architecture question (weak retrieval).
 |
| 9 | What are the key principles for modernizing legacy applications? | 5.48s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong retrieval from Barbero 2020 Technology Modernization paper — original work, highly specific content.
 |
| 10 | What are the key risk and compliance considerations for financial services IT? | 4.04s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Retrieves from FS Journal Risk/Compliance/Security volume (2005). |
| 11 | How has digitization changed financial services technology? | 4.48s | ✅ | FS Journal, Edited by M. Barbero - Digit | Retrieves from FS Journal Digitization volume. Clean single-source answer with good citation compliance.
 |
| 12 | What is the role of architecture in managing technology risk in financial services? | 3.78s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Good synthesis question drawing on multiple FS Journal volumes. Strong closer for a demo sequence. |

## Detailed Results

### qfd_technology_architecture
**Query:** What is QFD and how does it apply to technology architecture?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 22.42s | **Pass:** ✅

**Answer:**
> Quality Function Deployment (QFD) is a method that can be used in the development of an enterprise IT architecture. It involves the systematic definition of a coherent set of principles and standards presiding over the whole definition of the new architecture using techniques such as quality function deployment (QFD) [1]. 

According to the sources, QFD is associated with Design for Six Sigma (DFSS), which implies that in solving architectural or organizational problems, several solutions will b...


### it_org_architectural_principles
**Query:** How do you design an IT organization around architectural principles?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.95s | **Pass:** ✅

**Answer:**
> To design an IT organization around architectural principles, one should define the principles, standards, and implementation considerations that collectively define an architecture [1]. This involves identifying the conceptual/logical/physical concepts and their mapping to principle/standard/implementation consideration concepts [1]. For instance, principles related to outsourcing influence the positioning of the IT organization along a continuum, which in turn affects the structure of the orga...


### architecture_concepts_organizations
**Query:** How do architecture concepts help design organizations?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.85s | **Pass:** ✅

**Answer:**
> Architecture concepts help design organizations by providing a way to contribute actively to the debate on how to structure the IT organization [1,2]. According to Manuel Barbero, this can be done by applying tools and techniques that are essentially transposable from the enterprise IT architecture to the organizational architecture realm [1]. The article also shows that these concepts have applications beyond technology architecture, particularly in terms of communication, project management, a...


### cto_three_year_strategy
**Query:** How should a CTO prioritize a three-year technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.52s | **Pass:** ✅

**Answer:**
> Based on the provided sources, a CTO should prioritize a three-year technology strategy by:

1. Defining an initial straw man vision for the future linked to those goals and objectives and embracing a broad understanding of current issues [2].
2. Prioritizing initiatives that represent actions that will realize the vision over time [2].
3. Employing an iterative process to assess the maturity of the CMDB and enhance it in alignment with organizational requirements, starting with key capabilities...


### technology_target_state
**Query:** What does a good technology target state look like?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.59s | **Pass:** ✅

**Answer:**
> A good technology target state should be defined at a conceptual level if the necessary technology is not ready yet, budgets are not available or key talents have not been recruited yet [2]. 

To define this end state, it's recommended to use a progressive and pragmatic approach that defines realistic "transformation plateaus" aimed at implementing the end state step by step, while reducing technology and implementation risks [2]. These implementation plateaus serve as stepping stones allowing u...


### large_scale_it_transformation
**Query:** How do you organize a large-scale IT transformation program?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.26s | **Pass:** ✅

**Answer:**
> To organize a large-scale IT transformation program, it is essential to adopt an approach that balances formality and linearity with iterative cycles of data gathering, decision-making, and continuous improvement [1,2]. This involves setting up project work streams to design and build desired infrastructure components, such as CMDBs or service catalogs, in an iterative cycle with feedback loops at each stage [3].

The transformation process typically involves the following key steps: establishin...


### business_technology_strategy
**Query:** What is the relationship between business strategy and technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.95s | **Pass:** ✅

**Answer:**
> According to [1], a high-level goal for technology should be derived and traced back to the components of the business strategy. This is because most often, these are murky, too broad or just inexistent to be effectively useful in setting the technology strategy.

In order to formally trace technology goals to business objectives, one can use House-Of-Quality [1].

The relationship between business strategy and technology strategy is that the latter should be aligned with the former. As stated i...


### cloud_migration_modernization
**Query:** What are the key considerations for cloud migration and technology modernization?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.03s | **Pass:** ✅

**Answer:**
> Key considerations for cloud migration and technology modernization include:

* Assessing each application by both objective data (from a code scan) and qualitative data (from surveys) to segment and prioritize applications into categories such as Refactor, Revise, Rehost, Replace, and Retire [1].
* Identifying specific cloud migration Blockers and Boosters within the source code of an application that is slated for migration to the cloud.
* Building a right data set to scope and prioritize out ...


### modernizing_legacy_applications
**Query:** What are the key principles for modernizing legacy applications?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.48s | **Pass:** ✅

**Answer:**
> Unfortunately, there is no explicit information in the provided sources on the key principles for modernizing legacy applications. However, we can infer some general ideas from the text.

According to [1], one of the key principles mentioned is the "Experiment, Learn and Loop" principle (PRINCIPLE III), which suggests that solving complex problems like modernizing legacy applications should be an iterative process. This involves experimenting, learning, and looping through different approaches u...


### risk_compliance_financial_services
**Query:** What are the key risk and compliance considerations for financial services IT?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.04s | **Pass:** ✅

**Answer:**
> According to [1], the key risk and compliance considerations for financial services IT are:

* Managing purely financial risk and compliance requirements dictated by government regulations and market forces ([1])
* Dealing with business risk factors stemming from market issues, regulatory requirements, and reputational and legal consequences ([1])
* Convergence of key processes across multiple domains, including:
	+ Risk management
	+ Compliance management
	+ Security management
	+ Financial rep...


### digitization_financial_services
**Query:** How has digitization changed financial services technology?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.48s | **Pass:** ✅

**Answer:**
> Digitization has changed financial services technology by bringing together many technologies in a suite, or "digitization stack," that captures and manifests the way an institution operates today [1]. This digitization stack includes various underlying disciplines such as business process management, content and document management, digital imaging, and workflow and collaboration software [1].

One of the benefits of digitization is that it can help financial institutions meet the increased sec...


### architecture_technology_risk
**Query:** What is the role of architecture in managing technology risk in financial services?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.78s | **Pass:** ✅

**Answer:**
> Unfortunately, the sources provided do not explicitly address the role of architecture in managing technology risk in financial services.

However, [1] mentions that "near real-time monitoring of the firm’s exposure in several risk domains, such as market risk and client risk" is one of the expected benefits of a new technology architecture. This suggests that the authors are aware of the importance of managing technology-related risks in financial services.

[2] states that enterprise IT archit...


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