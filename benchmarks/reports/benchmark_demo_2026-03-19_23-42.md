# AIStudio — Benchmark Findings
*Generated: 2026-03-19 23:43*

## Configuration
- **Corpus:** `demo`
- **Top K:** 5
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 12
- **Passed:** 12/12 (100%)
- **Avg latency:** 4.6s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `demo` (see corpus stats in UI)
- Note: SEC 10-K corpus = 143 filings, 105,964 chunks — ChromaDB crashed at 32,285; Qdrant stable at 105,964

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | What is QFD and how does it apply to technology architecture? | 3.23s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Tests retrieval of dedicated QFD documents (Architecture and QFD.pdf, BOEI - Architecture and QFD - 2003.pdf). Flagship demo question.
 |
| 2 | How do you design an IT organization around architectural principles? | 5.05s | ✅ | Architecture Concepts and How To Use The | Retrieves from Architecting the IT Organization and FS Journal. |
| 3 | How do architecture concepts help design organizations? | 4.43s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws on the universal architecture toolset concept — one of the core intellectual contributions of the corpus.
 |
| 4 | How should a CTO prioritize a three-year technology strategy? | 4.52s | ✅ | FS Journal, Edited by M. Barbero - IT In | Consistently returns 5 citations across all models. Draws from FS Journal Strategy volume and Barbero 2020 modernization paper.
 |
| 5 | What does a good technology target state look like? | 5.25s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong single-source answer from FS Journal Strategy volume. |
| 6 | How do you organize a large-scale IT transformation program? | 4.88s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws from GTIS Strategy document and FS Journal. |
| 7 | What is the relationship between business strategy and technology strategy? | 5.0s | ✅ | Barbero - 2020 - Technology Modernizatio | Core intellectual thread running through entire corpus — business strategy drives technology strategy, not the reverse.
 |
| 8 | What are the key considerations for cloud migration and technology modernization? | 5.4s | ✅ | Barbero - 2020 - Technology Modernizatio | Draws directly from Barbero 2020 Technology Modernization paper — original work with a principled-based approach framework. Replaces enterprise AI reference architecture question (weak retrieval).
 |
| 9 | What are the key principles for modernizing legacy applications? | 4.68s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong retrieval from Barbero 2020 Technology Modernization paper — original work, highly specific content.
 |
| 10 | What are the key risk and compliance considerations for financial services IT? | 4.31s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Retrieves from FS Journal Risk/Compliance/Security volume (2005). |
| 11 | How has digitization changed financial services technology? | 5.45s | ✅ | FS Journal, Edited by M. Barbero - Digit | Retrieves from FS Journal Digitization volume. Clean single-source answer with good citation compliance.
 |
| 12 | What is the role of architecture in managing technology risk in financial services? | 3.59s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Good synthesis question drawing on multiple FS Journal volumes. Strong closer for a demo sequence. |

## Detailed Results

### qfd_technology_architecture
**Query:** What is QFD and how does it apply to technology architecture?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.23s | **Pass:** ✅

**Answer:**

> Quality Function Deployment (QFD) is a tool used in the development of technology architecture. According to [1], QFD is a technique used in solving architectural or organizational problems, where several solutions are assessed and one is selected for implementation.
>
> In the context of technology architecture, QFD can be applied by leveraging a number of well-defined tools and frameworks, including "techniques such as quality function deployment (QFD)" ([1]).

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.10


### it_org_architectural_principles
**Query:** How do you design an IT organization around architectural principles?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.05s | **Pass:** ✅

**Answer:**

> To design an IT organization around architectural principles, one must define the principles, standards, and implementation considerations that collectively define an architecture [1]. This requires a discipline similar to that of designing complex systems. Principles govern decisions made and actions taken, and organizational principles preside over the definition of the conceptual view of the organization [1].
>
> The development and acceptance of these principles influence the positioning of the IT organization along various continuums, such as the factory/service-oriented continuum presented in section 3 [1]. This point of view is not exhaustive and omits important issues like securing funding to implement organizational changes.
>
> According to Benedicte Lambert and Victoria Baldwin, one critical success factor in leveraging architectural frameworks is ensuring that proper governance models, processes, and organizational constructs are in place [2].
>
> The IT organization should be designed and operated with a high-level primer on how to design "architecture," whether technology or organizational architecture, and how architects think and work [3]. This article aims to debunk the notion that technology architects are the only ones who can contribute actively to the debate on how to structure the IT organization.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.30
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.4
- [3] Architecting the IT Organization.pdf p.1


### architecture_concepts_organizations
**Query:** How do architecture concepts help design organizations?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.43s | **Pass:** ✅

**Answer:**

> Architecture concepts can help design organizations in several ways:
>
> According to [1], architects have learned about analyzing and resolving problems that arise in dealing with complex systems, and these tools and techniques can be applied to organizational design.
>
> Additionally, [2] states that leveraging architectural frameworks requires proper governance models, processes, and organizational constructs to be in place. This suggests that architecture concepts can help design organizations by ensuring the right structures are established for success.
>
> Furthermore, [1] mentions that architects think and work using a universal architecture toolset, which can be applied to both technology and organizational architecture. This implies that architecture concepts can provide a common language and approach for designing organizations.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.4
- [2] Architecting the IT Organization.pdf p.1


### cto_three_year_strategy
**Query:** How should a CTO prioritize a three-year technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.52s | **Pass:** ✅

**Answer:**

> To develop a three-year technology strategy, a CTO should prioritize business objectives and ensure that technology goals are aligned with them. As stated in [5], ideally, the high-level goal for technology should be derived from the components of the business strategy.
>
> When establishing a technology vision, it's essential to consider current issues and express this vision using a standard visual notation, including scenario-based functions as described in [2]. This will provide a foundation for business cases.
>
> Furthermore, employing an iterative process to assess the maturity of the CMDB and enhance it in alignment with organizational requirements is crucial, as noted in [1].
>
> Additionally, in prioritizing architecture requirements, it's essential to consider factors such as control costs, increasing time to market, enabling customers, improving quality of service, and enabling business users to have a single view of firm X, as described in [3] and [4].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] FS Journal, Edited by M. Barbero - IT Infrastructure.pdf p.20
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.16
- [3] BOEI - Architecture and QFD -   2003.pdf p.5
- [4] Architecture and QFD.pdf p.5
- [5] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3


### technology_target_state
**Query:** What does a good technology target state look like?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.25s | **Pass:** ✅

**Answer:**

> A good technology target state is defined by several key characteristics, including:
>
> 1. High-level goals derived from and traced back to the components of the business strategy (or a well-defined, transformative business initiative) [1].
> 2. A clear understanding of the current state and the desired end state, which can be expressed as a series of views that describe the current state, the end state, and the road map to the end state [3][4].
> 3. The use of implementation plateaus, or stepping stones, that allow for an actionable plan to reach the end state in increments [2].
> 4. A multi-perspective approach, considering various domains such as user interface, application logic, data layer, and underlying computing infrastructure [3][4].
>
> Additionally, it is recommended to:
>
> * Not assume technologists understand specific concepts, but instead define and use terminology with team members and stakeholders to ensure everyone understands their preferences and the approach [3][4].
> * Develop a description of the situation before, during, and after the technology implementation in various domains [3][4].
> * Express the overall architecture as a series of views that help various audiences understand what the architecture is [3].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3
- [2] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.36
- [3] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.25
- [4] Architecting the IT Organization.pdf p.7
- [5] FS Journal, Edited by M. Barbero - Digitization.pdf p.4


### large_scale_it_transformation
**Query:** How do you organize a large-scale IT transformation program?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.88s | **Pass:** ✅

**Answer:**

> To organize a large-scale IT transformation program, follow these steps:
>
> 1. Establish a comprehensive but realistic data-gathering activity thread to gain insight into the infrastructure from an economic and management perspective [3].
> 2. Conduct a series of global workshops to drive agreement on a future vision, priorities, and implementation road map [2].
> 3. Identify areas of highest return in terms of benefit to end users and risk to management, and focus team members selectively on these areas [1][2].
> 4. Use agile methodologies with low ceremony and high formality and linearity in execution for large-scale projects [1].
> 5. Set up project work streams to design and build the desired data structures and database as part of a larger infrastructure transformation [3].
> 6. Establish an iterative cycle with a feedback loop at each stage of the decision cycle, allowing for continuous improvement and customization [3].
> 7. Synchronize DSS transformation program activities with application development priorities and lifecycle [4].
>
> Note: The answer is based on the provided sources, which seem to be duplicates of the same text. If there are any discrepancies or unclear information, please let me know.

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.23
- [2] Architecting the IT Organization.pdf p.5
- [3] FS Journal, Edited by M. Barbero - IT Infrastructure.pdf p.22
- [4] GTIS STRATEGY - MAIN - Three Year Strategy - Final (with speaker notes).pptx


### business_technology_strategy
**Query:** What is the relationship between business strategy and technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.0s | **Pass:** ✅

**Answer:**

> The relationship between business strategy and technology strategy is that the high-level goal for technology should be derived and traced back to the components of the business strategy [1]. Ideally, these goals are well-defined and provide a clear direction for setting the technology strategy. However, in practice, many organizations struggle with developing effective IT strategies due to the complexity of aligning technology goals with business objectives [2].
>
> One way to formally trace technology goals to business objectives is to use the House-Of-Quality method [1]. This approach involves defining and structuring relationships between concepts such as business strategy, IT strategy, and architecture.
>
> In essence, a technology strategy that is well-aligned with business goals should be able to produce incremental business value, sustain funding, and be driven by practical solutions to real problems [2]. The existence of an enterprise IT architecture can serve as evidence that the technology strategy is aligned with business objectives [2].
>
> The GTIS Three Year Strategy and Plan document provides a real-world example of how a business strategy drives both Group IT and business objectives [3]. In this case, the technology infrastructure transformation is aimed at moving beyond industry parity to become a competitive advantage for the business.

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.1
- [3] GTIS STRATEGY - MAIN - Three Year Strategy - Final (with speaker notes).pptx


### cloud_migration_modernization
**Query:** What are the key considerations for cloud migration and technology modernization?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.4s | **Pass:** ✅

**Answer:**

> According to the source [1], key considerations for cloud migration and technology modernization include:
>
> * Assessing each application by both objective data (from a code scan) and qualitative data (from surveys) to segment and prioritize applications into categories such as Refactor, Revise, Rehost, Replace, and Retire [1].
> * Identifying specific cloud migration Blockers and Boosters within the source code of an application that is slated for migration to the cloud [1].
> * Determining the current user authentication mechanism to identify security implications before migration [1].
> * Estimating ease of migration based on whether the application is multi-tenant [1].
> * Considering the average skill level on cloud technologies of the development team and estimating the timeline for migration [1].
>
> Additionally, the source mentions that a set of questions can help cut through the analysis, including:
>
> * Business Impact: Does the application serve internal or external users? Could failure of this application lead to loss of revenue?
> * Cloud Ready: Is the application multi-tenant? Estimate ease of migration What is the average skill level on cloud technologies of the development team?
> * Application Properties: What is the type of application?
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.10


### modernizing_legacy_applications
**Query:** What are the key principles for modernizing legacy applications?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.68s | **Pass:** ✅

**Answer:**

> Based on the provided sources [1] and [2], the key principles for modernizing legacy applications include:
>
> * Identifying application architecture issues and ensuring they do not become problematic in a distributed or hybrid cloud environment [1].
> * Understanding how business rules are embedded in the code and systematically harvesting what data model the original designer(s) used to represent the world [1].
> * Recognizing cross-application dependencies and re-organizing them through automated static pattern analysis and documentation [1].
>
> Additionally, source [2] mentions that building regulator confidence is key, but it does not provide further details on the principles for modernizing legacy applications.
>
> The SEI "Horseshoe" model diagram mentioned in source [1] provides a framework for renovating software by identifying two fundamental phases: Analysis and Synthesis. However, this seems to be more of an approach rather than a principle for modernization.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.6
- [2] FS Journal, Edited by M. Barbero - RiskCompliance and Security - 2005.pdf p.20


### risk_compliance_financial_services
**Query:** What are the key risk and compliance considerations for financial services IT?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.31s | **Pass:** ✅

**Answer:**

> The key risk and compliance considerations for financial services IT are:
>
> 1. Basel II Accord and anti-money laundering (AML) legislation ([1])
> 2. Regulatory requirements such as Sarbanes-Oxley Act ([1])
> 3. Convergence of risk, finance, and compliance management across the continuum, including:
> 	* Financial aspects with operational and compliance-oriented risks
> 	* Market risk, AML, and other mature areas of risk and compliance management
> 4. Data used across risk, finance, and compliance has life cycles and can be prioritized in terms of current level of concern ([1])
> 5. The importance of a holistic compliance framework to facilitate taking the right actions at the right time in response to compliance-related FUD (fear, uncertainty, and doubt) ([1])
>
> Note: These key risk and compliance considerations are based on the provided source [1].

**Citations:**

- [1] FS Journal, Edited by M. Barbero - RiskCompliance and Security - 2005.pdf p.6


### digitization_financial_services
**Query:** How has digitization changed financial services technology?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.45s | **Pass:** ✅

**Answer:**

> Digitization has changed financial services technology by bringing together many technologies in a suite that captures the way the institution operates today [1]. This digitization stack provides an integrated view and architecture, focusing on domains such as security and enterprise information integration [1].
>
> According to Richard Walker and Paul Dunay, digitization is about actively taking steps to implement an end-to-end solution to support the full value chain for better controls, standardization, consistency, and measurement of business processes [1]. Digitization also enables financial institutions to transform their internal and external operations, freeing up financial, human, and information resources [1].
>
> The actual underlying disciplines required to make digitization real have been around for a while but have only recently reached the level of performance or cost to be ubiquitous or integrated in financial institutions [1].
>
> Digitization has various applications across different domains in the financial industry, including portal-based claim processing in insurance, straight-through processing in capital markets, and integrated commercial loan underwriting in banking [1]. The renewed digitization push is driven by a confluence of developments, including a flurry of acquisitions and mergers, government mandates such as the Gramm-Leach-Bliley Act and Check 21, and the need for greater access to data and controls over processes [1].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] FS Journal, Edited by M. Barbero - Digitization.pdf p.34


### architecture_technology_risk
**Query:** What is the role of architecture in managing technology risk in financial services?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.59s | **Pass:** ✅

**Answer:**

> The role of architecture in managing technology risk in financial services is crucial in enabling near real-time monitoring of the firm's exposure in several risk domains, such as market risk and client risk [1]. This is achieved through advanced application integration architecture that leverages data from various sources.
>
> According to research, architects have learned a lot during their years of struggling to promote their discipline, particularly in managing complexity and maintaining the integrity of the IT environment [2]. One key lesson learned is that enterprise architecture is just too important to be left unattended or disconnected from the business.

**Citations:**

- [1] FS Journal, Edited by M. Barbero - RiskCompliance and Security - 2005.pdf p.36
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.6


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