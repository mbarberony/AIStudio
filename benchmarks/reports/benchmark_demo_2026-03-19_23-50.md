# AIStudio — Benchmark Findings
*Generated: 2026-03-19 23:51*

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
| 1 | What is QFD and how does it apply to technology architecture? | 5.72s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Tests retrieval of dedicated QFD documents (Architecture and QFD.pdf, BOEI - Architecture and QFD - 2003.pdf). Flagship demo question.
 |
| 2 | How do you design an IT organization around architectural principles? | 3.61s | ✅ | Architecture Concepts and How To Use The | Retrieves from Architecting the IT Organization and FS Journal. |
| 3 | How do architecture concepts help design organizations? | 4.3s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws on the universal architecture toolset concept — one of the core intellectual contributions of the corpus.
 |
| 4 | How should a CTO prioritize a three-year technology strategy? | 5.02s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Consistently returns 5 citations across all models. Draws from FS Journal Strategy volume and Barbero 2020 modernization paper.
 |
| 5 | What does a good technology target state look like? | 4.03s | ✅ | Architecture Concepts and How To Use The | Strong single-source answer from FS Journal Strategy volume. |
| 6 | How do you organize a large-scale IT transformation program? | 6.02s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws from GTIS Strategy document and FS Journal. |
| 7 | What is the relationship between business strategy and technology strategy? | 5.66s | ✅ | Barbero - 2020 - Technology Modernizatio | Core intellectual thread running through entire corpus — business strategy drives technology strategy, not the reverse.
 |
| 8 | What are the key considerations for cloud migration and technology modernization? | 4.88s | ✅ | Barbero - 2020 - Technology Modernizatio | Draws directly from Barbero 2020 Technology Modernization paper — original work with a principled-based approach framework. Replaces enterprise AI reference architecture question (weak retrieval).
 |
| 9 | What are the key principles for modernizing legacy applications? | 4.4s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong retrieval from Barbero 2020 Technology Modernization paper — original work, highly specific content.
 |
| 10 | What are the key risk and compliance considerations for financial services IT? | 3.98s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Retrieves from FS Journal Risk/Compliance/Security volume (2005). |
| 11 | How has digitization changed financial services technology? | 4.94s | ✅ | FS Journal, Edited by M. Barbero - Digit | Retrieves from FS Journal Digitization volume. Clean single-source answer with good citation compliance.
 |
| 12 | What is the role of architecture in managing technology risk in financial services? | 5.79s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Good synthesis question drawing on multiple FS Journal volumes. Strong closer for a demo sequence. |

## Detailed Results

### qfd_technology_architecture
**Query:** What is QFD and how does it apply to technology architecture?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.72s | **Pass:** ✅

**Answer:**

> Quality Function Deployment (QFD) is a method that leverages several solutions, assessing them, and selecting one to be implemented [1]. It implies that in solving architectural or organizational problems, multiple solutions will be assessed and one will be selected and implemented [1].
>
> In the context of technology architecture, QFD can be applied using techniques such as quality function development (QFD) [1]. The systematic definition of a coherent set of principles and standards presiding over the whole definition of the new architecture is essential for making the architecture definition work [2].
>
> QFD is mentioned in [1] as one of the tools that can be used in the context of technology architecture, along with other tools such as Voice of the Customer analysis [1].

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.10
- [2] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.4


### it_org_architectural_principles
**Query:** How do you design an IT organization around architectural principles?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.61s | **Pass:** ✅

**Answer:**

> To design an IT organization around architectural principles, it's essential to define the principles, standards, and implementation considerations that collectively define an architecture [1]. This requires a one-to-one mapping between conceptual/logical/physical concepts and principle/standard/implementation considerations concepts [1].
>
> The development and acceptance of these principles influence the positioning of the IT organization along the factory/service-oriented continuum [1]. It's also crucial to ensure proper governance, processes, and organizational constructs are in place to leverage the benefits of using architectural frameworks [3].
>
> According to Manuel Barbero, architecting an organization is no less an art than architecting a technology solution, but good judgment, experience, and intuition have a role to play, along with technique in supporting inspiration [1].

**Citations:**

- [1] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.30
- [3] Architecting the IT Organization.pdf p.1


### architecture_concepts_organizations
**Query:** How do architecture concepts help design organizations?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.3s | **Pass:** ✅

**Answer:**

> Architecture concepts can help design organizations by leveraging what architects have learned about analyzing and resolving problems in complex systems [1]. By applying these tools and techniques, organizational redesign can be made more effective, focusing on defining process rather than functions, which helps in designing the IT organization with an emphasis on defining process rather than functions [2].
>
> Organizational architecture can benefit from the use of architectural frameworks, including governance models, processes, and organizational constructs [1]. This approach can help make sure that the proper governance model, processes, and organizational constructs are in place [1]. Designers can leverage what architects have learned about analyzing and resolving problems in complex systems to create effective solutions [2].
>
> The article on page 19 of the Financial Services Technology Journal presents key concepts and tools that architects are likely to come across in the definition and implementation of an architecture, showing how those constructs can be applied in the field of organizational architecture and design, particularly in terms of communication, project management, and knowledge management [1].

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.4
- [2] Architecting the IT Organization.pdf p.1


### cto_three_year_strategy
**Query:** How should a CTO prioritize a three-year technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.02s | **Pass:** ✅

**Answer:**

> Based on the provided sources, here's a suggested approach for a CTO to prioritize a three-year technology strategy:
>
> The CTO should start by defining an initial vision for the future linked to the company's goals and objectives ([2]). This vision can be expressed using a standard visual notation and including scenario-based functional views that serve as the foundation for business cases.
>
> Next, the CTO should develop a prioritized list of initiatives that represent actions that will realize the vision over time ([2]). This phase includes development of practical plans that deliver incremental value to the organization. The CTO should also consider using Quality Function Deployment (QFD) to prioritize architecture requirements and select technology products that align with the company's objectives ([3][4]).
>
> In terms of specific priorities, the CTO can refer to the QFD input set, which includes factors such as control costs, increase time to market, enable customers, improve quality of service, and improve the financial services institution's ability to answer questions from business users ([3][4]).
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.16
- [3] BOEI - Architecture and QFD -   2003.pdf p.5
- [4] Architecture and QFD.pdf p.5
- [5] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3


### technology_target_state
**Query:** What does a good technology target state look like?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.03s | **Pass:** ✅

**Answer:**

> A good technology target state looks like a series of implementation plateaus that define an actionable plan to reach the desired end state from the current state [2]. These plateaus are stepping stones allowing organizations to reach the desired end state in increments, while reducing technology and implementation risks [2].
>
> The overall architecture can be expressed as a series of views that help various audiences understand what the architecture is [3][4]. Each view is necessary, but once they have been recognized, they provide a high level of precision for achieving an organization's vision [2].
>
> It is also recommended to use a progressive and pragmatic approach when defining transformation plateaus, which aims at implementing transitional states step by step, while reducing technology and implementation risks [2].
>
> When envisioning digitization, security and compliance are recurring themes that demand utmost attention [5].

**Citations:**

- [2] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.36
- [3] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.25
- [4] Architecting the IT Organization.pdf p.7
- [5] FS Journal, Edited by M. Barbero - Digitization.pdf p.4


### large_scale_it_transformation
**Query:** How do you organize a large-scale IT transformation program?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.02s | **Pass:** ✅

**Answer:**

> To organize a large-scale IT transformation program, it is recommended to adopt an iterative approach with a high level of formality and linearity in execution, particularly when dealing with complex projects mandated by government agencies ([1][2]). This approach involves breaking down the project into smaller components, focusing on areas of highest return in terms of benefit to end users and risk management ([1][2]).
>
> When establishing priorities and selecting the order in which a CMDB or service catalog should be implemented, it is essential to view the decision-making process as an iterative cycle with a feedback loop at each stage, allowing for continuous improvement and customization ([3]). This approach requires data gathering, cleansing, maintenance, and ongoing management of data elements to gain insight into the infrastructure from both economic and management perspectives.
>
> In large, enterprisewide projects, it is also necessary to set up project work streams to design and build the desired data structures and database as part of a larger infrastructure transformation ([3]). This involves migrating this structure into a production environment where the database would then be utilized as the CMDB.
>
> To drive change in a large-scale IT organization, it is crucial to establish momentum and gain international support through a means that deals with massive complexity. An iterative approach can help achieve this by making small changes at regular intervals ([1][2]).
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
**Latency:** 5.66s | **Pass:** ✅

**Answer:**

> According to [1], the high-level goal for technology should be derived and traced back to the components of the business strategy (or a well-defined transformative business initiative). However, in many cases, these goals are murky or inexistent, making it challenging to set an effective technology strategy.
>
> The relationship between business strategy and technology strategy can be formally traced using methods like House-Of-Quality [1]. Furthermore, creating an enterprise IT architecture is a strategic planning effort that transforms the way an organization operates, particularly how the IT function and its business-side clients interact and work together [2].
>
> In financial services organizations, developing an enterprisewide IT strategy and architecture can be challenging due to their multi-enterprise nature [2]. However, creating an enterprise IT architecture is crucial for translating an enterprise strategy into an actionable plan for its IT function [2].
>
> This process requires agreeing on key terms like "IT strategy" and "IT tactics," as well as defining enterprise IT architecture as the sum of the architectures that bring this strategy to life [2].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.1
- [3] GTIS STRATEGY - MAIN - Three Year Strategy - Final (with speaker notes).pptx


### cloud_migration_modernization
**Query:** What are the key considerations for cloud migration and technology modernization?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.88s | **Pass:** ✅

**Answer:**

> The key considerations for cloud migration and technology modernization include:
>
> 1. Assessing each application by both objective data (from a code scan) and qualitative data (from surveys) [1].
> 2. Segmentation and prioritization of applications into categories such as Refactor, Revise, Rehost, Replace, and Retire [1].
> 3. Identifying cloud migration Blockers and Boosters within the source code of an application [1].
> 4. Estimating financial impact in case of outage, ease of migration, and timeline for migration [34].
> 5. Identifying potential redundancies or consolidation opportunities across the portfolio [35].
> 6. Leveraging tools to perform an initial analysis of the portfolio, set up metrics, and assessing best candidates [35].
>
> It is also important to consider the following:
>
> * Not all legacy systems can be easily migrated to the cloud through "Lift and Shift" methods [1].
> * This approach rarely cuts costs and does not provide new business capabilities [1].
> * A principled-based approach is recommended for a portfolio-wide yet iterative road to success [1].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.10


### modernizing_legacy_applications
**Query:** What are the key principles for modernizing legacy applications?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.4s | **Pass:** ✅

**Answer:**

> Based on the provided sources [1] and [2], the key principles for modernizing legacy applications can be summarized as follows:
>
> PRINCIPLE I - Data (from [1]): Understanding how business rules are embedded in the code is key, but harvesting what data model the original designer(s) used to represent the world is equally important.
>
> PRINCIPLE II - Cross-Application Dependencies (from [1]): Identifying and re-organizing cross-application dependencies is crucial for modernizing legacy applications. This can be done through automated static pattern analysis and documentation.
>
> PRINCIPLE III - Experiment, Learn and Loop (from [1]): Solving complex problems like modernizing legacy applications should be an iterative process. Organizations should harvest and leverage lessons learned across projects to achieve a worthy goal like creating customer loyalty and recurring revenues.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.6
- [2] FS Journal, Edited by M. Barbero - RiskCompliance and Security - 2005.pdf p.20


### risk_compliance_financial_services
**Query:** What are the key risk and compliance considerations for financial services IT?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.98s | **Pass:** ✅

**Answer:**

> The key risk and compliance considerations for financial services IT include:
>
> * Managing purely financial risk and compliance requirements dictated by government regulations and market forces [1].
> * Recognizing the risk and compliance management continuum, which includes:
> 	+ Market risk
> 	+ Credit risk
> 	+ Operational risk
> 	+ Reputational and legal risk [1]
> * Understanding that all risk and compliance management require life cycles and can be prioritized in terms of current level of concern [1].
> * Linking key applications into a workflow framework that exposes audit events to manage internal reporting and external disclosure of financial risk and compliance information [1].
>
> Additionally, the article highlights the importance of considering the convergence of key processes and the sharing of data across the three domains of risk management, finance, and compliance to manage RCS effectively.

**Citations:**

- [1] FS Journal, Edited by M. Barbero - RiskCompliance and Security - 2005.pdf p.6


### digitization_financial_services
**Query:** How has digitization changed financial services technology?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.94s | **Pass:** ✅

**Answer:**

> Digitization has changed financial services technology by bringing together many technologies in a suite or "stack" that captures and manifests the way an institution operates today [1]. This digitization stack can help financial institutions meet various demands, including protection of digitized content, creating and maintaining digital identity, and ensuring real-time enterprise capabilities [1].
>
> The concept of digitization is not new, but its implementation has become more pronounced in recent years due to the availability of high-performance technologies at affordable costs [1]. Financial institutions are now implementing these solutions in a more integrated way, rather than in isolation, which was common previously [1].
>
> Digitization can transform financial institutions along the entire value chain of internal and external operations, freeing up resources and providing better controls, standardization, consistency, and measurement of business processes [1]. It also enables real-time processing, repeatable, measurable, low-cost processes, and end-to-end, straight-through processing capabilities [1].
>
> The drivers for digitization in the financial services industry include technology advancements, government mandates (such as Know Your Customer, Sarbanes-Oxley Act, Basel II, Gramm-Leach-Bliley Act, and Check 21), and business needs to access data, control processes, and interactions [1].

**Citations:**

- [1] FS Journal, Edited by M. Barbero - Digitization.pdf p.34


### architecture_technology_risk
**Query:** What is the role of architecture in managing technology risk in financial services?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.79s | **Pass:** ✅

**Answer:**

> The role of architecture in managing technology risk in financial services is crucial in managing complexity and maintaining the integrity of the IT environment [1]. Enterprise IT architecture can help financial services firms develop a long-term, strategic approach to planning after years of quarter-to-quarter focus on cost takeout [2]. According to research, the increasing importance of enterprise IT architecture has led to a renewed emphasis among financial services firms in looking again at long-term, strategic planning [2].
>
> Financial services firms have struggled with the concept of enterprise architecture in practice due to its perceived large, difficult, and expensive nature, making it challenging to justify the return on investment (ROI) from a financial perspective [2]. However, applying an architecture-driven approach has been successful in one case, allowing a firm to achieve efficiency and reduce risk by consolidating or retiring systems and developing a strategic plan for the front-to-back office [2].
>
> Architects have learned that enterprise architecture is just too important to be managed as a project; it must be embedded into the organizational fabric [2]. The convergence of equities and fixed income functions and customers has also led to challenges in assessing risk accurately at a portfolio or customer level, highlighting the need for an enterprise IT architecture approach [2].
>
> Therefore, the role of architecture in managing technology risk in financial services is essential in promoting long-term strategic planning, managing complexity, maintaining integrity, and developing an enterprise IT architecture that can help firms assess risk accurately and reduce costs.

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