# AIStudio — Benchmark Findings
*Generated: 2026-03-19 22:55*

## Configuration
- **Corpus:** `demo`
- **Top K:** 5
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 12
- **Passed:** 12/12 (100%)
- **Avg latency:** 4.8s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `demo` (see corpus stats in UI)
- Note: SEC 10-K corpus = 143 filings, 105,964 chunks — ChromaDB crashed at 32,285; Qdrant stable at 105,964

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | What is QFD and how does it apply to technology architecture? | 6.74s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Tests retrieval of dedicated QFD documents (Architecture and QFD.pdf, BOEI - Architecture and QFD - 2003.pdf). Flagship demo question.
 |
| 2 | How do you design an IT organization around architectural principles? | 5.37s | ✅ | Architecture Concepts and How To Use The | Retrieves from Architecting the IT Organization and FS Journal. |
| 3 | How do architecture concepts help design organizations? | 4.74s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws on the universal architecture toolset concept — one of the core intellectual contributions of the corpus.
 |
| 4 | How should a CTO prioritize a three-year technology strategy? | 4.51s | ✅ | FS Journal, Edited by M. Barbero - IT In | Consistently returns 5 citations across all models. Draws from FS Journal Strategy volume and Barbero 2020 modernization paper.
 |
| 5 | What does a good technology target state look like? | 4.66s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong single-source answer from FS Journal Strategy volume. |
| 6 | How do you organize a large-scale IT transformation program? | 5.35s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws from GTIS Strategy document and FS Journal. |
| 7 | What is the relationship between business strategy and technology strategy? | 3.38s | ✅ | Barbero - 2020 - Technology Modernizatio | Core intellectual thread running through entire corpus — business strategy drives technology strategy, not the reverse.
 |
| 8 | What are the key considerations for cloud migration and technology modernization? | 4.92s | ✅ | Barbero - 2020 - Technology Modernizatio | Draws directly from Barbero 2020 Technology Modernization paper — original work with a principled-based approach framework. Replaces enterprise AI reference architecture question (weak retrieval).
 |
| 9 | What are the key principles for modernizing legacy applications? | 3.99s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong retrieval from Barbero 2020 Technology Modernization paper — original work, highly specific content.
 |
| 10 | What are the key risk and compliance considerations for financial services IT? | 5.4s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Retrieves from FS Journal Risk/Compliance/Security volume (2005). |
| 11 | How has digitization changed financial services technology? | 5.03s | ✅ | FS Journal, Edited by M. Barbero - Digit | Retrieves from FS Journal Digitization volume. Clean single-source answer with good citation compliance.
 |
| 12 | What is the role of architecture in managing technology risk in financial services? | 3.99s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Good synthesis question drawing on multiple FS Journal volumes. Strong closer for a demo sequence. |

## Detailed Results

### qfd_technology_architecture
**Query:** What is QFD and how does it apply to technology architecture?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.74s | **Pass:** ✅

**Answer:**

> Quality Function Deployment (QFD) is a tool that can be used in the development of an enterprise IT architecture. According to [1], QFD is a technique such as quality function deployment (QFD).
>
> In the context of technology architecture, QFD helps to identify and prioritize solutions based on their alignment with business goals and objectives. This involves assessing several solutions and selecting one that best meets the needs of the organization.
>
> The systematic definition of principles and standards using techniques such as QFD is essential in developing an enterprise IT architecture. [1] states that "the development of an enterprise IT architecture is based on... the systematic definition of a coherent set of principlesand standardspresiding over the whole definition of the new architecture."
>
> In terms of how QFD applies to technology architecture, it helps to bridge the gap between business and technology strategies by defining the organizational architecture, which includes processes and enabling technologies required to execute the business vision. [2] notes that "designing an IT organization... should be the product of a systematic analysis that defines the bridge between the business vision, organizational constructs, processes and enabling technologies required to execute the vision."

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.10
- [2] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.4


### it_org_architectural_principles
**Query:** How do you design an IT organization around architectural principles?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.37s | **Pass:** ✅

**Answer:**

> Designing an IT organization around architectural principles requires defining principles, standards, and implementation considerations that collectively define an architecture [1]. The definition of these concepts is essential for making decisions and taking actions in the organization [1]. Principles related to outsourcing influence the positioning of the IT organization along the factory/service-oriented continuum [1].
>
> The process involves identifying key areas such as governance model, processes, and organizational constructs that need to be established [3]. A good starting point is to use a combination of principles and standards from IT architecture, such as those presented in the universal architecture toolset, and adapt them for organizational design [2][3].
>
> Some suggested approaches include using a pattern-driven approach to solve complex problems, such as Tollgate analysis, which involves formal presentation of results obtained so far before moving on to the next step [3]. The Define phase is also an essential step in organizational architecture, where key decisions are made and actions taken [1].
>
> Architects can contribute actively to the debate on how to structure the IT organization by applying their knowledge and expertise in technology and organizational design [2][3]. Non-architects can benefit from a high-level primer on how to design an architecture, whether technology or organizational, and understand how architects think and work [2].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.30
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.4
- [3] Architecting the IT Organization.pdf p.1


### architecture_concepts_organizations
**Query:** How do architecture concepts help design organizations?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.74s | **Pass:** ✅

**Answer:**

> The use of architecture concepts helps design organizations in several ways. Firstly, architects can leverage what they have learned about analyzing and resolving problems in complex systems to help non-architects design organizational structures ([1]). This is because the tools and techniques used in technology architecture are also applicable to organizational design ([1]).
>
> Moreover, analyzing the end-to-end "IT value chain" is crucial in designing the IT organization with an emphasis on defining processes rather than functions ([1]). Additionally, applying architectural frameworks requires a proper governance model, processes, and organizational constructs to be in place, which is critical for leveraging the benefits of using architectural frameworks ([2]).
>
> The article also highlights that architects think and work similarly regardless of whether they are designing technology or organizational architecture ([1][2]). Furthermore, it emphasizes the importance of technique in supporting inspiration, suggesting that a combination of good judgment, experience, and intuition is necessary for effective design ([2]).
>
> Therefore, by applying architectural concepts and tools to organizational design, architects can contribute actively to the debate on how to structure the IT organization, making their efforts more likely to be received favorably by impacted employees ([1][2]).

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.4
- [2] Architecting the IT Organization.pdf p.1


### cto_three_year_strategy
**Query:** How should a CTO prioritize a three-year technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.51s | **Pass:** ✅

**Answer:**

> A CTO should prioritize a three-year technology strategy by defining an initial straw man vision for the future linked to those goals and objectives, and embracing a broad understanding of current issues [2]. This involves prioritizing initiatives that represent actions that will realize the vision over time.
>
> To develop this vision, it's essential to define IT services and related infrastructure components required to provision and sustaining the CMDB [1]. The CTO should also consider the business strategy and trace technology goals back to its components [5].
>
> Furthermore, to ensure effective implementation, the CTO should employ an iterative process to assess the maturity of the CMDB and enhance it in alignment with organizational requirements [1]. This involves a broad understanding of current issues and prioritizing initiatives that deliver value vis-a-vis costs.
>
> Finally, the CTO should consider using House-Of-Quality (HoQ) to formally trace technology goals to business objectives [5], which will help ensure that the technology strategy is aligned with the overall business strategy.

**Citations:**

- [1] FS Journal, Edited by M. Barbero - IT Infrastructure.pdf p.20
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.16
- [5] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3


### technology_target_state
**Query:** What does a good technology target state look like?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.66s | **Pass:** ✅

**Answer:**

> A good technology target state looks like a well-defined, conceptual level vision that is derived from and traced back to the components of the business strategy or a well-defined transformative business initiative [1]. It should be realistic, achievable, and aligned with the organization's overall goals.
>
> To define such a state, it is recommended to use "transformation plateaus" - stepping stones that allow reaching the desired end state in actionable increments. These plateaus are essential for reducing technology and implementation risks [2].
>
> Additionally, a good technology target state should consider various aspects of the technology and its impact on the organization, including costs, value delivered, opportunity costs, and potential security issues associated with digitization initiatives [5]. It is also crucial to involve stakeholders in the process and use clear terminology to define and explain the approach and set expectations [3,4].
>
> A good example of how to express a technology target state is through multiple views that describe the current state, end state, and road map to that end state. These views can include user interface, application logic, data layer, and underlying infrastructure [3,4].

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3
- [2] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.36
- [3] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.25
- [4] Architecting the IT Organization.pdf p.7
- [5] FS Journal, Edited by M. Barbero - Digitization.pdf p.4


### large_scale_it_transformation
**Query:** How do you organize a large-scale IT transformation program?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.35s | **Pass:** ✅

**Answer:**

> According to the sources, organizing a large-scale IT transformation program involves an iterative approach with a high level of formality and linearity in execution [1][2]. The process includes:
>
> 1. Envisioning a future vision and priorities through a comprehensive but realistic data-gathering activity thread and a series of global workshops [1].
> 2. Establishing momentum by dealing with massive complexity, which can be achieved through an approach of iterative cycles with feedback loops at each stage [3][4].
> 3. Setting up project work streams to design and build the desired data structures and database as part of a larger infrastructure transformation [3].
>
> For large-scale IT transformations, it is essential to adopt a high level of formality and linearity in execution, especially when dealing with complex systems like Distributed Systems & Storage (DSS) [4]. The DSS transformation program activities need to be synchronized with application development priorities to achieve the end state [4].
>
> Regarding Agile methodologies, they use low ceremony and iterative processes for software development, which can be applied to IT organizational design and transformational change [1][2].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.23
- [2] Architecting the IT Organization.pdf p.5
- [3] FS Journal, Edited by M. Barbero - IT Infrastructure.pdf p.22
- [4] GTIS STRATEGY - MAIN - Three Year Strategy - Final (with speaker notes).pptx


### business_technology_strategy
**Query:** What is the relationship between business strategy and technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.38s | **Pass:** ✅

**Answer:**

> According to source [2], an enterprise IT strategy is considered successful when it produces and maintains underlying technology frameworks that bring its strategy to life. This implies a direct relationship between business strategy and technology strategy.
>
> Source [1] mentions that technology goals should be derived from and traced back to the components of the business strategy, indicating that business strategy has a foundational role in determining technology strategy.
>
> Source [3] provides an example of how GTIS's business strategy is driven by both Group IT and business objectives, illustrating the close connection between business and technology strategies.

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.1
- [3] GTIS STRATEGY - MAIN - Three Year Strategy - Final (with speaker notes).pptx


### cloud_migration_modernization
**Query:** What are the key considerations for cloud migration and technology modernization?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.92s | **Pass:** ✅

**Answer:**

> The key considerations for cloud migration and technology modernization include:
>
> 1. Assessing each application in the portfolio by both objective data (from a code scan) and qualitative data (from surveys) to segment and prioritize applications more intelligently into categories such as Refactor, Revise, Rehost, Replace, and Retire [2].
> 2. Identifying specific cloud migration Blockers and Boosters within the source code of an application that is slated for migration to the cloud.
> 3. Gathering relevant data through surveys, asking the right questions to cut through the analysis, including:
> 	* Business Impact: Does the application serve internal or external users? Could failure of this application lead to loss of revenue?
> 	* Cloud Ready: Is the application multi-tenant? Estimate ease of migration
> 	* What is the average skill level on cloud technologies of the development team?
> 	* Identify potential redundancies or consolidation opportunities across the portfolio [34].
> 4. Leveraging tools to perform an initial analysis of the portfolio, set up metrics, and assessing best candidates based on these questions.
> 5. Using a principle-based approach that supports a portfolio-wide yet iterative road to success.
>
> References:
> [1], [2]

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.10


### modernizing_legacy_applications
**Query:** What are the key principles for modernizing legacy applications?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.99s | **Pass:** ✅

**Answer:**

> Here are the key principles for modernizing legacy applications:
>
> PRINCIPLE I - Understand Legacy Applications [1]:
> The first principle is to understand how the legacy application works, including its data model and cross-application dependencies. This involves harvesting what data model the original designer(s) used to represent the world and understanding how business rules are embedded in the code.
>
> PRINCIPLE II - Identify Structure and Refactor Application Functionalities [2][1]:
> The second principle is to identify structure not dynamic behavior, which can be done through automated static pattern analysis and documentation. This helps to refactor application functionalities and restructure cross-application dependencies.
>
> PRINCIPLE III - Experiment, Learn and Loop [1]:
> The third principle is to solve complex problems iteratively, which involves experimenting, learning, and looping to leverage lessons learned across projects.

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.6
- [2] FS Journal, Edited by M. Barbero - RiskCompliance and Security - 2005.pdf p.20


### risk_compliance_financial_services
**Query:** What are the key risk and compliance considerations for financial services IT?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.4s | **Pass:** ✅

**Answer:**

> Key risk and compliance considerations for financial services IT include:
>
> * Convergence of risk, compliance, and security (RCS) management, which requires leveraging the same kind of data and monitoring the same processes across these domains [1].
> * Managing RCS involves dealing with financial aspects and operational requirements created by regulations and market forces [1].
> * Financial services institutions should consider a portfolio approach to dealing with risk, compliance, and security issues, along with expanding regulatory requirements [1].
> * Convergence involves different stages of life cycles for various domains, including market risk, anti-money laundering (AML), and capital adequacy and financial reporting [1].
>
> The article suggests that the key priorities in understanding the risk life cycle are:
>
> * Recognizing the risk and compliance management continuum, which includes purely financial risks and compliance requirements, as well as operational requirements created by regulations and market forces [1].
> * Understanding that all risk and compliance management require life cycles and can be prioritized in terms of current levels of concern [1].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] FS Journal, Edited by M. Barbero - RiskCompliance and Security - 2005.pdf p.6


### digitization_financial_services
**Query:** How has digitization changed financial services technology?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.03s | **Pass:** ✅

**Answer:**

> Digitization has changed financial services technology by bringing together many technologies in a suite or "stack" that captures and manifests the way an institution operates today [1]. This digitization stack enables financial institutions to meet security demands and concerns, including protection of digitized content, through a well-thought-out information security strategy and end-to-end framework.
>
> In particular, digitization has transformed financial institutions along the entire value chain of internal and external operations, freeing up financial, human, and information resources [1]. It involves actively taking steps to implement an end-to-end solution to support the full value chain, for better controls, standardization, consistency, and measurement of business processes.
>
> The actual underlying disciplines required to make digitization real, such as business process management, content and document management, digital imaging, and workflow and collaboration software, have themselves been around for a while [1]. However, it is only recently that they have reached the level of performance or cost to make them ubiquitous or integrated in financial institutions.
>
> Digitization has also created new opportunities for institutions to distribute tasks to optimal locations using repeatable, measurable, low-cost processes [1]. This enables end-to-end, straight-through processing and facilitates access to data, both structured and unstructured, as well as controls over processes and interactions.

**Citations:**

- [1] FS Journal, Edited by M. Barbero - Digitization.pdf p.34


### architecture_technology_risk
**Query:** What is the role of architecture in managing technology risk in financial services?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.99s | **Pass:** ✅

**Answer:**

> The role of architecture in managing technology risk in financial services is described in [2] as follows:
>
> Architects have learned a lot during these years struggling to promote their discipline. First among high-level lessons learned are:
> 1) enterprise architecture is just too important to ignore.
>
> Additionally, the article states that architects have been struggling to justify their role and the return on investment (ROI) of enterprise IT architecture initiatives has been—at best—difficult to justify to business stakeholders.
>
> The importance of long-term, strategic planning after years of quarter-to-quarter focus on cost takeout is also emphasized in [2].
>
> *[truncated — use --full for complete answer]*

**Citations:**

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