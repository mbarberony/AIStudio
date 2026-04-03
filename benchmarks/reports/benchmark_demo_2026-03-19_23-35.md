# AIStudio — Benchmark Findings
*Generated: 2026-03-19 23:36*

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
| 1 | What is QFD and how does it apply to technology architecture? | 4.05s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Tests retrieval of dedicated QFD documents (Architecture and QFD.pdf, BOEI - Architecture and QFD - 2003.pdf). Flagship demo question.
 |
| 2 | How do you design an IT organization around architectural principles? | 3.74s | ✅ | Architecture Concepts and How To Use The | Retrieves from Architecting the IT Organization and FS Journal. |
| 3 | How do architecture concepts help design organizations? | 3.44s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws on the universal architecture toolset concept — one of the core intellectual contributions of the corpus.
 |
| 4 | How should a CTO prioritize a three-year technology strategy? | 4.66s | ✅ | FS Journal, Edited by M. Barbero - IT In | Consistently returns 5 citations across all models. Draws from FS Journal Strategy volume and Barbero 2020 modernization paper.
 |
| 5 | What does a good technology target state look like? | 4.38s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong single-source answer from FS Journal Strategy volume. |
| 6 | How do you organize a large-scale IT transformation program? | 4.43s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws from GTIS Strategy document and FS Journal. |
| 7 | What is the relationship between business strategy and technology strategy? | 5.5s | ✅ | Barbero - 2020 - Technology Modernizatio | Core intellectual thread running through entire corpus — business strategy drives technology strategy, not the reverse.
 |
| 8 | What are the key considerations for cloud migration and technology modernization? | 6.03s | ✅ | Barbero - 2020 - Technology Modernizatio | Draws directly from Barbero 2020 Technology Modernization paper — original work with a principled-based approach framework. Replaces enterprise AI reference architecture question (weak retrieval).
 |
| 9 | What are the key principles for modernizing legacy applications? | 5.13s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong retrieval from Barbero 2020 Technology Modernization paper — original work, highly specific content.
 |
| 10 | What are the key risk and compliance considerations for financial services IT? | 4.81s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Retrieves from FS Journal Risk/Compliance/Security volume (2005). |
| 11 | How has digitization changed financial services technology? | 5.58s | ✅ | FS Journal, Edited by M. Barbero - Digit | Retrieves from FS Journal Digitization volume. Clean single-source answer with good citation compliance.
 |
| 12 | What is the role of architecture in managing technology risk in financial services? | 6.05s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Good synthesis question drawing on multiple FS Journal volumes. Strong closer for a demo sequence. |

## Detailed Results

### qfd_technology_architecture
**Query:** What is QFD and how does it apply to technology architecture?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.05s | **Pass:** ✅

**Answer:**

> Quality Function Deployment (QFD) is a method that can be used in the development of an enterprise IT architecture. According to [1], QFD is one of the techniques that can be used in the systematic definition of a coherent set of principles and standards for the new architecture.
>
> QFD involves assessing several solutions to a problem, and selecting and implementing one. This approach is similar to Design for Six Sigma (DFSS), which also implies the selection of one solution from multiple options [1].
>
> In the context of technology architecture, QFD can be applied at various levels of specificity. The Conceptual Level provides the highest level of abstraction, defining the overall vision and fundamental principles for future IT decisions. It must be closely aligned with the business vision [2].

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.10
- [2] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.4


### it_org_architectural_principles
**Query:** How do you design an IT organization around architectural principles?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.74s | **Pass:** ✅

**Answer:**

> To design an IT organization around architectural principles, one should follow these steps:
>
> First, define the organizational architecture/model by establishing principles, standards, and implementation considerations that collectively define an architecture [1]. This process requires discipline, similar to the architecture of complex systems. Principles govern decisions made and actions taken, influencing the conceptual view of the organization.
>
> Next, identify key concepts related to the use of outsourcing, which influence the positioning of the IT organization along the factory/service-oriented continuum [1].
>
> Furthermore, leverage architectural frameworks by ensuring that the proper governance model, processes, and organizational constructs are in place. This is critical for leveraging the benefits of using architectural frameworks [3].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.30
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.4
- [3] Architecting the IT Organization.pdf p.1


### architecture_concepts_organizations
**Query:** How do architecture concepts help design organizations?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.44s | **Pass:** ✅

**Answer:**

> Architecture concepts help design organizations by providing a way to structure the IT organization, define governance models, processes, and organizational constructs [1]. These concepts can be applied to organizational architecture and design, particularly in terms of communication, project management, and knowledge management [2]. In addition, analyzing the end-to-end "IT value chain" is essential for designing the IT organization with an emphasis on defining process rather than functions [2]. The proper application of these concepts can benefit both architects and non-architects by providing a high-level primer on how to design architectures, whether technology or organizational architecture [1,2].

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.4
- [2] Architecting the IT Organization.pdf p.1


### cto_three_year_strategy
**Query:** How should a CTO prioritize a three-year technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.66s | **Pass:** ✅

**Answer:**

> Based on the provided sources, a CTO should prioritize a three-year technology strategy by following these steps:
>
> 1. Define an initial straw man vision for the future linked to those goals and objectives ([2]). This involves prioritizing initiatives that represent actions that will realize the vision over time.
> 2. Employ an iterative process to assess the maturity of the CMDB and enhance it in alignment with specific organizational requirements ([1]).
> 3. Correlate technology products (databases, operating systems, and application servers) to QFD input sets to refine selections of designs, features, and technology products ([4]).
> 4. Prioritize and select each architecture platform's components to be rolled out in sequence to ensure a smooth transition between the current and future states ([3]).
> 5. Define high-level goals for technology by tracing them back to the components of the business strategy or well-defined transformative business initiatives ([5]).
>
> Additionally, the CTO should consider using House-Of-Quality methods to formally trace technology goals to business objectives if they exist ([5]).

**Citations:**

- [1] FS Journal, Edited by M. Barbero - IT Infrastructure.pdf p.20
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.16
- [3] BOEI - Architecture and QFD -   2003.pdf p.5
- [4] Architecture and QFD.pdf p.5
- [5] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3


### technology_target_state
**Query:** What does a good technology target state look like?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.38s | **Pass:** ✅

**Answer:**

> A good technology target state should be defined at the conceptual level, especially if the necessary technology is not ready yet or budgets are not available [2]. To achieve a high-level goal for technology, it should be derived and traced back to the components of the business strategy [1].
>
> To define such a target state, a progressive and pragmatic approach can be used, defining realistic "transformation plateaus" (B1, B2, B3, etc.) aimed at implementing the end state step by step, while reducing technology and implementation risks [2].
>
> Additionally, the overall architecture can be expressed as a series of views that help various audiences understand what the architecture is. These views are necessary to describe the current situation, the desired end state, and the road map to get there [3][4].
>
> It's also essential to consider issues related to the combined "physical layer process x computing infrastructure" in the context of the ERP implementation [3][4].

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3
- [2] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.36
- [3] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.25
- [4] Architecting the IT Organization.pdf p.7


### large_scale_it_transformation
**Query:** How do you organize a large-scale IT transformation program?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.43s | **Pass:** ✅

**Answer:**

> To organize a large-scale IT transformation program, consider adopting an iterative approach with high formality and linearity in execution ([1]). This involves establishing a comprehensive but realistic data-gathering activity thread, followed by global workshops to drive agreement on a future vision, priorities, and implementation road map ([2]). In addition, implement master data management (MDM) practices to gain insight into the infrastructure from an economic and management perspective ([3]).
>
> When setting priorities for IT transformation, view the decision-making process as an iterative cycle with a feedback loop at each stage of the decision cycle, allowing for continuous improvement and customization ([1]). This approach can help translate business strategy into action using IT architecture as a common language ([2]).
>
> To change the engagement model with application development, consider moving from requesting specific infrastructure stacks to requesting infrastructure solutions based on capacity and functional requirements. This change should be integrated with the normal application development lifecycle to ensure minimal overall resource impact ([4]).

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.23
- [2] Architecting the IT Organization.pdf p.5
- [3] FS Journal, Edited by M. Barbero - IT Infrastructure.pdf p.22
- [4] GTIS STRATEGY - MAIN - Three Year Strategy - Final (with speaker notes).pptx


### business_technology_strategy
**Query:** What is the relationship between business strategy and technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.5s | **Pass:** ✅

**Answer:**

> The relationship between business strategy and technology strategy is as follows:
>
> Ideally, the high-level goal for technology should be derived and traced back to the components of the business strategy [1]. In fact, creating an enterprise IT architecture is a strategic planning effort that can transform the way an organization operates, particularly how the IT function and its business-side clients interact and work together [2].
>
> The ability to produce and maintain underlying technology frameworks—principles, standards and implementation blueprints—that bring this strategy to life is proof that an IT organization has a strategy [2].
>
> In addition, developing IT strategies that are assets but also well-aligned with business goals and objectives—and achievable in that they deliver incremental business value—is considered the most right process that can help translate an enterprise strategy into an actionable plan for its IT function [2].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.1
- [3] GTIS STRATEGY - MAIN - Three Year Strategy - Final (with speaker notes).pptx


### cloud_migration_modernization
**Query:** What are the key considerations for cloud migration and technology modernization?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.03s | **Pass:** ✅

**Answer:**

> The key considerations for cloud migration and technology modernization include:
>
> 1. Assessing each application in the portfolio by both objective data (from a code scan) and qualitative data (from surveys) to segment and prioritize applications more intelligently into categories such as Refactor, Revise, Rehost, Replace, and Retire [2].
> 2. Identifying specific cloud migration Blockers and Boosters within the source code of an application that is slated for migration to the cloud.
> 3. Gathering relevant data through surveys, asking the right questions, and resisting boiling the ocean.
> 4. Using a simple set of questions to help cut through analysis, including:
> 	* Business Impact: Does the application serve internal or external users? Could failure of this application lead to loss of revenue?
> 	* Cloud Ready: Is the application multi-tenant? Estimate ease of migration
> 	* What is the average skill level on cloud technologies of the development team?
> 5. Identifying potential redundancies or consolidation opportunities across the portfolio.
> 6. Performing an initial analysis of the portfolio using tools that can help set up metrics and assess best candidates [35].
> 7. Developing a roadmap to the cloud for large application portfolios using both objective cloud readiness measurements and qualitative business context considerations [36].
>
> References:
> [1] /Users/manuelbarbero/Developer/AIStudio/data/corpora/demo/uploads/Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf
> [2] (not explicitly mentioned in the text, but implied as a reference)

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.10


### modernizing_legacy_applications
**Query:** What are the key principles for modernizing legacy applications?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.13s | **Pass:** ✅

**Answer:**

> Unfortunately, the provided sources do not explicitly state the key principles for modernizing legacy applications. However, I can extract some information related to this topic from both sources.
>
> From [1], it seems that there is a lack of clear guidance on this topic. It mentions the SEI "Horseshoe" model diagram (which is referenced but not provided), which suggests that renovation of software consists of two fundamental phases: Analysis and Synthesis.
>
> From [2], I found some relevant information, although it does not directly address modernizing legacy applications. However, it discusses the importance of connecting business support systems to provide a mechanism for supplementing linkage data and enforcing policies through BPM (Business Process Management).
>
> To answer the question based on the provided sources:
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.6
- [2] FS Journal, Edited by M. Barbero - RiskCompliance and Security - 2005.pdf p.20


### risk_compliance_financial_services
**Query:** What are the key risk and compliance considerations for financial services IT?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.81s | **Pass:** ✅

**Answer:**

> The key risk and compliance considerations for financial services IT include:
>
> * Managing the convergence of risk, compliance, and security management across multiple domains [1].
> * Addressing the staggered approach to dealing with different stages of the risk life cycle [1].
> * Implementing point solutions in mature areas such as market risk and anti-money laundering (AML) [1].
> * Understanding that all risk and compliance management require life cycles and can be prioritized based on current levels of concern [1].
> * Focusing on stronger and more useful linkages between the risk, compliance, and security domains by leveraging shared data and processes [1].
> * Recognizing the impact of government regulations and market forces on financial services companies [1].
>
> The article also highlights the importance of a holistic approach to risk and compliance management, including:
>
> * Building a workflow infrastructure that exposes audit events [1].
> * Integrating systems, processes, and tools for effective risk and compliance management [1].
> * Creating a framework that facilitates taking the right actions at the right time in response to compliance-related FUD (fear, uncertainty, and doubt) [1].

**Citations:**

- [1] FS Journal, Edited by M. Barbero - RiskCompliance and Security - 2005.pdf p.6


### digitization_financial_services
**Query:** How has digitization changed financial services technology?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.58s | **Pass:** ✅

**Answer:**

> Digitization in financial services technology has led to the integration of various disciplines such as business process management, content and document management, digital imaging, and workflow and collaboration software [1]. This integration enables institutions to achieve end-to-end solutions that support the full value chain, resulting in better controls, standardization, consistency, and measurement of business processes [1].
>
> The digitization of financial services has also led to increased security demands due to potential vulnerabilities in digitized information [1]. A well-thought-out information security strategy, coupled with an end-to-end information security framework, can address most security concerns for the digitized organization [1].
>
> Moreover, digitization has transformed financial institutions along the entire value chain of internal and external operations, freeing up financial, human, and information resources [1]. This transformation is driven by a renewed flurry of acquisitions and mergers, government mandates such as Know Your Customer and Check 21, and the need for greater access to data and controls over processes and interactions [1].
>
> In terms of specific technologies, digitization in financial services has led to the adoption of portal-based claim processing in insurance, straight-through processing in capital markets, and integrated commercial loan underwriting in banking [1]. These technologies have been around for a while but are now being implemented in a more integrated way due to advances in performance or cost [1].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] FS Journal, Edited by M. Barbero - Digitization.pdf p.34


### architecture_technology_risk
**Query:** What is the role of architecture in managing technology risk in financial services?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.05s | **Pass:** ✅

**Answer:**

> According to [1], managing technology risk in financial services is not explicitly mentioned as a role of architecture. However, it mentions that "IT investments have a number of common characteristics" and that enterprise IT architecture can help manage complexity and maintain the integrity of the IT environment.
>
> On the other hand, [2] mentions that there is a renewed interest among financial services firms in looking at long-term, strategic planning after years of quarter-to-quarter focus on cost takeout. It also states that architects have learned to promote their discipline during these years and that enterprise architecture is just too important to be managed by IT alone.
>
> The text [2] does not provide direct information about the role of architecture in managing technology risk in financial services, but it mentions that there are 10 specific leading practices to tackle the enterprise architecture definition challenge.
>
> However, we can infer from [2] that enterprise architecture is crucial for long-term, strategic planning and maintaining the integrity of the IT environment.
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