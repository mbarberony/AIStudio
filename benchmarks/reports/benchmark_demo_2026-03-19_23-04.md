# AIStudio — Benchmark Findings
*Generated: 2026-03-19 23:05*

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
| 1 | What is QFD and how does it apply to technology architecture? | 5.46s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Tests retrieval of dedicated QFD documents (Architecture and QFD.pdf, BOEI - Architecture and QFD - 2003.pdf). Flagship demo question.
 |
| 2 | How do you design an IT organization around architectural principles? | 6.07s | ✅ | Architecture Concepts and How To Use The | Retrieves from Architecting the IT Organization and FS Journal. |
| 3 | How do architecture concepts help design organizations? | 3.54s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws on the universal architecture toolset concept — one of the core intellectual contributions of the corpus.
 |
| 4 | How should a CTO prioritize a three-year technology strategy? | 4.86s | ✅ | FS Journal, Edited by M. Barbero - IT In | Consistently returns 5 citations across all models. Draws from FS Journal Strategy volume and Barbero 2020 modernization paper.
 |
| 5 | What does a good technology target state look like? | 4.68s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong single-source answer from FS Journal Strategy volume. |
| 6 | How do you organize a large-scale IT transformation program? | 4.91s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws from GTIS Strategy document and FS Journal. |
| 7 | What is the relationship between business strategy and technology strategy? | 4.83s | ✅ | Barbero - 2020 - Technology Modernizatio | Core intellectual thread running through entire corpus — business strategy drives technology strategy, not the reverse.
 |
| 8 | What are the key considerations for cloud migration and technology modernization? | 4.96s | ✅ | Barbero - 2020 - Technology Modernizatio | Draws directly from Barbero 2020 Technology Modernization paper — original work with a principled-based approach framework. Replaces enterprise AI reference architecture question (weak retrieval).
 |
| 9 | What are the key principles for modernizing legacy applications? | 4.19s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong retrieval from Barbero 2020 Technology Modernization paper — original work, highly specific content.
 |
| 10 | What are the key risk and compliance considerations for financial services IT? | 3.58s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Retrieves from FS Journal Risk/Compliance/Security volume (2005). |
| 11 | How has digitization changed financial services technology? | 4.71s | ✅ | FS Journal, Edited by M. Barbero - Digit | Retrieves from FS Journal Digitization volume. Clean single-source answer with good citation compliance.
 |
| 12 | What is the role of architecture in managing technology risk in financial services? | 3.81s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Good synthesis question drawing on multiple FS Journal volumes. Strong closer for a demo sequence. |

## Detailed Results

### qfd_technology_architecture
**Query:** What is QFD and how does it apply to technology architecture?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.46s | **Pass:** ✅

**Answer:**

> Quality Function Deployment (QFD) is a method used in the development of an enterprise IT architecture [1]. It involves the systematic definition of a coherent set of principles and standards presiding over the whole definition of the new architecture using techniques such as quality function deployment (QFD) [1].
>
> In the context of technology architecture, QFD can be applied to develop a target architecture that includes actionable models and engineering blueprints [2]. This allows for different approaches to be differentiated and provides a set of product-independent architectures for IT components not fully specified.
>
> There is no further information in the provided sources on how QFD specifically applies to technology architecture.

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.10
- [2] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.4


### it_org_architectural_principles
**Query:** How do you design an IT organization around architectural principles?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.07s | **Pass:** ✅

**Answer:**

> To design an IT organization around architectural principles, one should define the organizational architecture/model by applying the discipline associated with the architecture of complex systems ([1]). This involves defining principles, standards, and implementation considerations that collectively define an architecture. The definition of these elements should be informed by a one-to-one mapping between conceptual/logical/physical concepts and principle/standard/implementation consideration concepts ([1]).
>
> In particular, organizational principles preside over the definition of the conceptual view of the organization, influencing decisions made and actions taken ([1]). For example, principles related to outsourcing influence the positioning of the IT organization along the factory/service-oriented continuum ([1]).
>
> Good judgment, experience, and intuition play a role in architecting an organization, but no less so than in architecting a technology solution ([2], [3]). In both cases, good technique is essential in supporting inspiration. By sharing "universal architecture toolset," one can help debunk the notion that technology architects are high priests of an inscrutable religion and that organizational design is exclusive to non-architects ([1]).
>
> To address IT governance issues, approaches such as tollgate analysis can be applied ([3]). Tollgate analysis recommends formal presentation of results obtained so far in each step before proceeding to the next one. The Define phase is probably the most important step in an organizational architecture ([3]), and it should involve defining principles that govern decisions made and actions taken.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.30
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.4
- [3] Architecting the IT Organization.pdf p.1


### architecture_concepts_organizations
**Query:** How do architecture concepts help design organizations?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.54s | **Pass:** ✅

**Answer:**

> Architecture concepts help design organizations by providing a framework for understanding how to structure the IT organization and making sure that the proper governance model, processes, and organizational constructs are in place [1][2]. This is essential for leveraging the benefits of using architectural frameworks, which can be applied to both technology architecture and organizational architecture [1]. The concepts presented in this article can be used by architects and non-architects alike, providing a high-level primer on how to design an "architecture," whether technology or organizational [1][2]. Additionally, analyzing the end-to-end "IT value chain" is crucial for designing the IT organization with an emphasis on defining process rather than functions [1].

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.4
- [2] Architecting the IT Organization.pdf p.1


### cto_three_year_strategy
**Query:** How should a CTO prioritize a three-year technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.86s | **Pass:** ✅

**Answer:**

> Based on the provided sources, a CTO should prioritize a three-year technology strategy by tracing back the high-level goal for technology to the components of the business strategy [5]. This involves formally linking technology goals to business objectives using a method such as House-of-Quality [5].
>
> To develop a comprehensive strategy, the CTO should also consider the following steps:
>
> 1. Define an initial straw man vision for the future linked to those goals and objectives [2].
> 2. Prioritize initiatives that represent actions that will realize the vision over time [2].
> 3. Employ an iterative process to assess the maturity of the technology infrastructure and enhance it in alignment with organizational requirements [1].
> 4. Use Quality Function Deployment (QFD) to correlate technology products with architecture principles and prioritize architecture rollout phases [3][4].
>
> Additionally, the CTO should consider the following non-functional architecture requirements, as listed in Table 1:
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
**Latency:** 4.68s | **Pass:** ✅

**Answer:**

> A good technology target state should be defined at the conceptual level if the necessary technology is not ready yet, budgets are not available, or key talents have not been recruited yet [2].
>
> To achieve precision in defining a technology target state, it is recommended to use House-Of-Quality to formally trace technology goals to business objectives (if they exist) [1].
>
> A progressive and pragmatic approach can be used to define realistic "transformation plateaus" aimed at implementing the end state step by step, while reducing technology and implementation risks [2]. This involves defining various implementation plateaus as stepping stones allowing us to reach the desired end state in actionable increments.
>
> The overall architecture can be expressed as a series of views that help various audiences and stakeholders understand what the architecture is. It's essential to note that each of these views is necessary, but only once they have been recognized [3, 4].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3
- [2] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.36
- [3] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.25
- [4] Architecting the IT Organization.pdf p.7


### large_scale_it_transformation
**Query:** How do you organize a large-scale IT transformation program?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.91s | **Pass:** ✅

**Answer:**

> To organize a large-scale IT transformation program, follow these steps:
>
> 1. Envision your first day in leading an IT transformational change focusing on organization [1].
> 2. Adopt a high level of formality and linearity in execution for large, enterprisewide projects [1].
> 3. Use Agile methodologies that employ low ceremony and iterative processes for software development [1].
> 4. Establish a comprehensive but realistic data-gathering activity thread to drive agreement on a future vision, priorities, and implementation road map [2].
> 5. Set up project work streams to design and build the desired data structures and database as part of a larger infrastructure transformation [3].
> 6. View decision-making as an iterative cycle with a feedback loop at each stage of the decision cycle, allowing for continuous improvement and customization [3].
> 7. Integrate compute transformation opportunities with the normal application development lifecycle to ensure minimal overall resource impact [4].
> 8. Change the engagement model with application development from requesting specific infrastructure stacks to requesting infrastructure solutions based on capacity and functional requirements [4].
>
> Note that these steps are based on the provided sources, which may not provide a comprehensive guide for organizing large-scale IT transformation programs.

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.23
- [2] Architecting the IT Organization.pdf p.5
- [3] FS Journal, Edited by M. Barbero - IT Infrastructure.pdf p.22
- [4] GTIS STRATEGY - MAIN - Three Year Strategy - Final (with speaker notes).pptx


### business_technology_strategy
**Query:** What is the relationship between business strategy and technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.83s | **Pass:** ✅

**Answer:**

> The relationship between business strategy and technology strategy is that the high-level goal for technology should be derived and traced back to the components of the business strategy [1]. However, this is often murky or inexistent, making it challenging to set the technology strategy effectively [1].
>
> One way to formally trace technology goals to business objectives is to use House-Of-Quality [1]. Additionally, creating an enterprise IT architecture is a strategic planning effort that can transform the way an organization operates, particularly how the IT function and its business-side clients interact and work together [2].
>
> In financial services organizations, developing a common enterprisewide IT strategy and architecture is indeed a challenge due to their multi-enterprise nature [2]. However, it is possible to define enterprise IT architecture as the sum of the architectures that bring the business strategy to life [2].
>
> The GTIS Three Year Strategy presentation provides an example of how business and technology objectives are aligned [3]. The goal of transforming the ITI legacy infrastructure into a world-leading technology asset is driven by both Group IT and business objectives, demonstrating the importance of aligning technology strategy with business strategy.

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.1
- [3] GTIS STRATEGY - MAIN - Three Year Strategy - Final (with speaker notes).pptx


### cloud_migration_modernization
**Query:** What are the key considerations for cloud migration and technology modernization?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.96s | **Pass:** ✅

**Answer:**

> To address the question of key considerations for cloud migration and technology modernization, I'll rely on the provided source [1].
>
> According to [1], the key considerations include:
>
> 1. Assessing each application in the portfolio by both objective data (from a code scan) and qualitative data (from surveys) to segment and prioritize applications into categories such as Refactor, Revise, Rehost, Replace, and Retire.
> 2. Identifying specific cloud migration Blockers and Boosters within the source code of an application that is slated for migration to the cloud.
> 3. Building the right data set to scope and prioritize out the modernization effort.
>
> Additionally, [1] mentions a list of questions that can help cut through the analysis, including:
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.10


### modernizing_legacy_applications
**Query:** What are the key principles for modernizing legacy applications?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.19s | **Pass:** ✅

**Answer:**

> According to [1], the key principles for modernizing legacy applications include:
>
> * PRINCIPLE I - Understand the "As Is" State (Analysis phase): recovering and checking the code's structure/architecture for conformance with known or desired best practices/principles.
> * PRINCIPLE II - Refactor for a Desired Future State (Synthesis phase): applying better principles to modify the architecture at the conceptual level, which then translates into implementation at the logical and code levels.
>
> Additionally, [1] mentions that modernizing legacy applications involves identifying potential application architecture issues, such as remote call in loops, and ensuring they do not become problematic in a distributed or hybrid cloud environment.
>
> [2] does not provide information on key principles for modernizing legacy applications. However, it discusses the importance of digitization projects and the need to connect business support systems to provide a holistic framework for regulating compliance.

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.6
- [2] FS Journal, Edited by M. Barbero - RiskCompliance and Security - 2005.pdf p.20


### risk_compliance_financial_services
**Query:** What are the key risk and compliance considerations for financial services IT?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.58s | **Pass:** ✅

**Answer:**

> The key risk and compliance considerations for financial services IT are:
>
> * Convergence between risk management and compliance management issues ( [1] )
> * Increasing business risk factors stemming from market forces ( [1] )
> * Expanding regulatory requirements, including Basel II and anti-money laundering legislation (AML) ( [1] )
> * The need to manage risk, finance, and compliance domains in a holistic manner ( [1] )
> * Prioritizing risk and compliance management based on the current level of concern ( [1] )
>
> Note: These considerations are not an exhaustive list but rather a summary of the key points mentioned in the provided source.

**Citations:**

- [1] FS Journal, Edited by M. Barbero - RiskCompliance and Security - 2005.pdf p.6


### digitization_financial_services
**Query:** How has digitization changed financial services technology?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.71s | **Pass:** ✅

**Answer:**

> Digitization has changed financial services technology by bringing together many technologies in a suite or "stack" that captures and manifests the way an institution operates today [1]. This digitization stack allows institutions to meet various demands resulting from digitization, such as protection of digitized content [1].
>
> Specifically, digitization can help financial institutions:
>
> * Create and maintain digital documents
> * Implement end-to-end solutions for better controls, standardization, consistency, and measurement of business processes
> * Use technologies such as business process management, content and document management, digital imaging, and workflow and collaboration software to support these disciplines
>
> Digitization also enables the creation of a true digital enterprise capable of end-to-end, straight-through processing [1]. This is driven by three critical drivers: technological advancements, government mandates, and market demands.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] FS Journal, Edited by M. Barbero - Digitization.pdf p.34


### architecture_technology_risk
**Query:** What is the role of architecture in managing technology risk in financial services?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.81s | **Pass:** ✅

**Answer:**

> According to [1], financial services firms have struggled with managing technology risk due to the complexity and lack of integrity in their IT environment.
>
> The role of architecture in managing technology risk in financial services is not explicitly stated in either source. However, [2] mentions that enterprise IT architecture projects often become disconnected from the business and fail to manage the complexity and maintain the integrity of the IT environment.
>
> But this change might also mark the renewed emphasis among financial services firms in looking again at long-term, strategic planning after years of quarter-to-quarter focus on cost takeout [2].
>
> It is worth noting that neither source provides information about the specific role of architecture in managing technology risk.

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