# AIStudio — Benchmark Findings
*Generated: 2026-03-19 23:19*

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
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `demo` (see corpus stats in UI)
- Note: SEC 10-K corpus = 143 filings, 105,964 chunks — ChromaDB crashed at 32,285; Qdrant stable at 105,964

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | What is QFD and how does it apply to technology architecture? | 7.16s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Tests retrieval of dedicated QFD documents (Architecture and QFD.pdf, BOEI - Architecture and QFD - 2003.pdf). Flagship demo question.
 |
| 2 | How do you design an IT organization around architectural principles? | 5.47s | ✅ | Architecture Concepts and How To Use The | Retrieves from Architecting the IT Organization and FS Journal. |
| 3 | How do architecture concepts help design organizations? | 5.59s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws on the universal architecture toolset concept — one of the core intellectual contributions of the corpus.
 |
| 4 | How should a CTO prioritize a three-year technology strategy? | 4.44s | ✅ | FS Journal, Edited by M. Barbero - IT In | Consistently returns 5 citations across all models. Draws from FS Journal Strategy volume and Barbero 2020 modernization paper.
 |
| 5 | What does a good technology target state look like? | 3.08s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong single-source answer from FS Journal Strategy volume. |
| 6 | How do you organize a large-scale IT transformation program? | 5.14s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws from GTIS Strategy document and FS Journal. |
| 7 | What is the relationship between business strategy and technology strategy? | 4.33s | ✅ | Barbero - 2020 - Technology Modernizatio | Core intellectual thread running through entire corpus — business strategy drives technology strategy, not the reverse.
 |
| 8 | What are the key considerations for cloud migration and technology modernization? | 4.97s | ✅ | Barbero - 2020 - Technology Modernizatio | Draws directly from Barbero 2020 Technology Modernization paper — original work with a principled-based approach framework. Replaces enterprise AI reference architecture question (weak retrieval).
 |
| 9 | What are the key principles for modernizing legacy applications? | 4.56s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong retrieval from Barbero 2020 Technology Modernization paper — original work, highly specific content.
 |
| 10 | What are the key risk and compliance considerations for financial services IT? | 3.86s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Retrieves from FS Journal Risk/Compliance/Security volume (2005). |
| 11 | How has digitization changed financial services technology? | 5.32s | ✅ | FS Journal, Edited by M. Barbero - Digit | Retrieves from FS Journal Digitization volume. Clean single-source answer with good citation compliance.
 |
| 12 | What is the role of architecture in managing technology risk in financial services? | 5.38s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Good synthesis question drawing on multiple FS Journal volumes. Strong closer for a demo sequence. |

## Detailed Results

### qfd_technology_architecture
**Query:** What is QFD and how does it apply to technology architecture?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.16s | **Pass:** ✅

**Answer:**

> Quality Function Deployment (QFD) is a tool that can be used in the development of an enterprise IT architecture. It is mentioned as one of the techniques used to develop an enterprise IT architecture, along with others such as "use case," "value chain," and "voice of the customer analysis" [1]. QFD involves assessing several solutions to a problem and selecting one to implement.
>
> QFD has applications beyond technology architecture, including organizational change management. According to [2], when attempting to mold an organization around existing people and skill sets, employees impacted by the change may resist implementation if they are not informed about the decision-making process and how it was fair. QFD can be used in this context to ensure that the needs of all stakeholders are considered.
>
> A systematic analysis using QFD can define the bridge between business vision, organizational constructs, processes, and enabling technologies required to execute the vision [2]. This involves defining the conceptual, logical, and physical levels of specificity in architecture, which include the overall vision, actionable models and engineering blueprints, and product-independent architectures for IT components, respectively [3].
>
> In terms of technology architecture, QFD can be used to fill the "plateaus" or provide a more detailed approach to developing an enterprise IT architecture using techniques such as quality function deployment (QFD) [1].

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.10
- [2] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.4
- [3] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.1


### it_org_architectural_principles
**Query:** How do you design an IT organization around architectural principles?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.47s | **Pass:** ✅

**Answer:**

> To design an IT organization around architectural principles, one should follow a structured approach that involves defining principles, standards, and implementation considerations. This requires the discipline of architecture, which is also essential for designing complex systems.
>
> According to [1], organizational principles preside over the definition of the conceptual view of the organization, just like IT principles preside over the definition of IT conceptual architectures. For example, principles related to outsourcing influence the positioning of the IT organization along the factory/service-oriented continuum.
>
> Similarly, [3] states that architecting an organization is no less an art than architecting a technology solution, and good judgment, experience, and intuition have a role to play in both cases. However, technique also plays a crucial role in supporting inspiration. By sharing universal architecture toolsets, one can help debunk the notions that technology architects are high priests of an inscrutable religion.
>
> [2] proposes using architectural frameworks to leverage benefits, but notes that proper governance models, processes, and organizational constructs must be in place for this to happen.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.30
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.4
- [3] Architecting the IT Organization.pdf p.1


### architecture_concepts_organizations
**Query:** How do architecture concepts help design organizations?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.59s | **Pass:** ✅

**Answer:**

> Architecture concepts can help design organizations by applying tools and techniques that architects use to analyze and resolve problems in complex systems [1]. These concepts are transferable from technology architecture to organizational architecture, allowing designers to create a high-level primer on how to design "architecture," whether technology or organizational architecture, and understand how architects think and work [1][2].
>
> For non-architects, this can serve as a primer on how to design an organization, including understanding the proper governance model, processes, and organizational constructs that should be in place [1][2]. For architects, these concepts provide a way to contribute actively to the debate on how to structure the IT organization [1][2].
>
> Specifically, analyzing the end-to-end "IT value chain" is crucial in designing the IT organization with an emphasis on defining process rather than functions [1]. Additionally, using a universal architecture toolset can help debunk the notion that organizational design is exclusively a matter of insightful improvisation and leverage what architects have learned about analyzing and resolving problems in complex systems [2].
>
> The 10 critical performance factors mentioned include:
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.4
- [2] Architecting the IT Organization.pdf p.1


### cto_three_year_strategy
**Query:** How should a CTO prioritize a three-year technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.44s | **Pass:** ✅

**Answer:**

> To prioritize a three-year technology strategy, a CTO should:
>
> 1. Start by defining an initial straw man vision for the future linked to those goals and objectives [2].
> 2. Employ a broad understanding of current issues, expressing this vision using a standard visual notation and including a scenario-based functional view that serves as the foundation for business cases [2].
> 3. Define IT services and related infrastructure components required to provision these services [1].
> 4. Prioritize initiatives by correlating technology products to the Quality Function Deployment (QFD) input set, ensuring control costs, increasing time to market, enabling customers, improving quality of service, and planning architecture releases are prioritized [3][4].
> 5. Trace back high-level technology goals to the components of the business strategy or a well-defined transformative business initiative [5].
>
> The CTO should also ensure that technology goals are aligned with business objectives, possibly using House-Of-Quality methodology for formal tracing [5].

**Citations:**

- [1] FS Journal, Edited by M. Barbero - IT Infrastructure.pdf p.20
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.16
- [3] BOEI - Architecture and QFD -   2003.pdf p.5
- [4] Architecture and QFD.pdf p.5
- [5] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3


### technology_target_state
**Query:** What does a good technology target state look like?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.08s | **Pass:** ✅

**Answer:**

> A good technology target state should be defined at the conceptual level when necessary information is lacking, as [1] and [2] suggest.
>
> To formally trace technology goals to business objectives (if they exist), one can use the House-Of-Quality approach [1].
>
> An actionable plan to reach the end state from the current state can be developed by defining various implementation plateaus, which are stepping stones allowing us to reach the desired end state in actionable increments [2].

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3
- [2] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.36


### large_scale_it_transformation
**Query:** How do you organize a large-scale IT transformation program?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.14s | **Pass:** ✅

**Answer:**

> To organize a large-scale IT transformation program, I would recommend following these steps:
>
> 1. **Establish a comprehensive data-gathering activity thread** and series of global workshops to drive agreement on a future vision, priorities, and implementation road map [1][2].
> 2. **Adopt an iterative approach**, using low ceremony and high formality in execution, as Agile methodologies have emerged as effective for large, enterprisewide projects [1][3].
> 3. **Set up project work streams** to design and build the desired data structures and database as part of a larger infrastructure transformation [3].
> 4. **Synchronize DSS transformation program activities** with application development priorities, particularly new builds and extensive application rationalization underway [4].
>
> Additionally, I would recommend:
>
> * Viewing decision-making as an iterative cycle with a feedback loop at each stage to allow for continuous improvement and customization.
> * Implementing master data management (MDM) practices to gain insight into the infrastructure from an economic and management perspective [3][4].
> * Changing the engagement model with application development from requesting specific infrastructure stacks to requesting infrastructure solutions based on capacity and functional requirements.
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
**Latency:** 4.33s | **Pass:** ✅

**Answer:**

> The relationship between business strategy and technology strategy is as follows:
>
> According to [1], the high-level goal for technology should be derived and traced back to the components of the business strategy (or a well-defined, transformative business initiative). However, this is often not clearly defined or too broad to effectively set the technology strategy.
>
> [2] states that an IT organization has a strategy when it can produce and maintain underlying technology frameworks - principles, standards, and implementation blueprints - that bring its strategy to life. This implies that technology strategy should align with business objectives and goals.
>
> [3] provides a real-world example of how business strategy is driven by both Group IT and business objectives, and how the two are aligned through an integrated timeline and critical assumptions.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.1
- [3] GTIS STRATEGY - MAIN - Three Year Strategy - Final (with speaker notes).pptx


### cloud_migration_modernization
**Query:** What are the key considerations for cloud migration and technology modernization?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.97s | **Pass:** ✅

**Answer:**

> The key considerations for cloud migration and technology modernization are:
>
> * Assessing each application in the portfolio by both objective data (from a code scan) and qualitative data (from surveys) to segment and prioritize applications into categories such as Refactor, Revise, Rehost, Replace, and Retire [1].
> * Identifying specific cloud migration Blockers and Boosters within the source code of an application that is slated for migration to the cloud [1].
> * Asking relevant questions to gather data, including:
> 	+ Business Impact: Does the application serve internal or external users? Could failure of this application lead to loss of revenue?
> 	+ Cloud Ready: Is the application multi-tenant? Estimate ease of migration. What is the average skill level on cloud technologies of the development team?
> 	+ Application Properties: What is the type of application?
> * Using tools to perform an initial analysis of the portfolio, set up metrics, and assess best candidates [35].
> * Considering objective cloud readiness measurements and qualitative business context considerations when developing a roadmap to the cloud for large application portfolios [1].
>
> Note that these key considerations are based on the provided source [1], which is the only available source.

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.10


### modernizing_legacy_applications
**Query:** What are the key principles for modernizing legacy applications?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.56s | **Pass:** ✅

**Answer:**

> Unfortunately, neither source directly answers the question "What are the key principles for modernizing legacy applications?"
>
> However, [1] mentions three key principles in the context of technology modernization:
>
> PRINCIPLE I - Understand - That solving complex problems (such as organizing the rewrite of a portfolio of legacy apps) requires understanding the code's structure and architecture. 
> PRINCIPLE II - Prioritize - That organizations should prioritize replacing components with obsolete technologies, such as the STRUTS framework.
> PRINCIPLE III - Experiment, Learn and Loop - That modernizing legacy applications is an iterative process that involves harvesting and leveraging lessons learned across projects.
>
> As for [2], it discusses the digitization of compliance value chains, but does not directly address the question of key principles for modernizing legacy applications.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.6
- [2] FS Journal, Edited by M. Barbero - RiskCompliance and Security - 2005.pdf p.20


### risk_compliance_financial_services
**Query:** What are the key risk and compliance considerations for financial services IT?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.86s | **Pass:** ✅

**Answer:**

> The key risk and compliance considerations for financial services IT can be understood by examining the "risk continuum" [1]. This continuum depicts several risk and compliance domains, from purely financial to purely operational issues.
>
> The risk continuum includes:
>
> * Market risks associated with the Basel II Accord
> * Anti-money laundering (AML) legislation
> * Capital adequacy and financial risk management
> * Operational requirements created by regulations and market forces
>
> These domains are at different stages of their life cycle, so financial services companies can address them with a staggered approach [1].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] FS Journal, Edited by M. Barbero - RiskCompliance and Security - 2005.pdf p.6


### digitization_financial_services
**Query:** How has digitization changed financial services technology?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.32s | **Pass:** ✅

**Answer:**

> Digitization has changed financial services technology by bringing together many technologies in a suite, or digitization stack, that captures and manifests the way an institution operates today [1]. This includes various disciplines such as business process management, content and document management, digital imaging, and workflow and collaboration software. Digitization is about actively taking steps to implement an end-to-end solution to support the full value chain, for better controls, standardization, consistency, and measurement of business processes [1].
>
> In terms of specific changes, digitization has led to:
>
> * The use of integrated commercial loan underwriting in banking [1]
> * Portal-based claim processing in insurance [1]
> * Straight-through processing in capital markets [1]
>
> Digitization also calls for an integrated vision and architectures with due focus on domains such as security and enterprise information integration as well as the necessary computing and communications infrastructures [1].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] FS Journal, Edited by M. Barbero - Digitization.pdf p.34


### architecture_technology_risk
**Query:** What is the role of architecture in managing technology risk in financial services?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.38s | **Pass:** ✅

**Answer:**

> The role of architecture in managing technology risk in financial services is multifaceted and can be understood through various perspectives.
>
> Firstly, [1] highlights that managing complexity and maintaining integrity of the IT environment are key reasons why financial services firms are acknowledging the importance of enterprise IT architecture today. This renewed emphasis on long-term planning after years of cost-takeout focus is crucial in tackling technology risk.
>
> Secondly, [2] emphasizes that enterprise architecture projects often struggle to promote their discipline due to various factors such as the siloed nature of the organization and technology, making it difficult to assess risk accurately at a portfolio or customer level. However, the article also suggests that applying an architecture-driven approach can be effective in managing technology risk.
>
> Lastly, [2] lists 10 specific leading practices for implementing enterprise IT architecture initiatives, including convergence of equities and fixed income functions, data mining across businesses, and the use of architecture to justify ROI from a financial perspective. These practices aim to address the challenges associated with traditional enterprise IT architecture efforts being perceived as large, difficult, and expensive.
>
> *[truncated — use --full for complete answer]*

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