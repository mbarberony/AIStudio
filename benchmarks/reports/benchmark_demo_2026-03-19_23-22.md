# AIStudio — Benchmark Findings
*Generated: 2026-03-19 23:23*

## Configuration
- **Corpus:** `demo`
- **Top K:** 5
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 12
- **Passed:** 12/12 (100%)
- **Avg latency:** 5.0s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `demo` (see corpus stats in UI)
- Note: SEC 10-K corpus = 143 filings, 105,964 chunks — ChromaDB crashed at 32,285; Qdrant stable at 105,964

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | What is QFD and how does it apply to technology architecture? | 4.87s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Tests retrieval of dedicated QFD documents (Architecture and QFD.pdf, BOEI - Architecture and QFD - 2003.pdf). Flagship demo question.
 |
| 2 | How do you design an IT organization around architectural principles? | 5.18s | ✅ | Architecture Concepts and How To Use The | Retrieves from Architecting the IT Organization and FS Journal. |
| 3 | How do architecture concepts help design organizations? | 4.74s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws on the universal architecture toolset concept — one of the core intellectual contributions of the corpus.
 |
| 4 | How should a CTO prioritize a three-year technology strategy? | 4.6s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Consistently returns 5 citations across all models. Draws from FS Journal Strategy volume and Barbero 2020 modernization paper.
 |
| 5 | What does a good technology target state look like? | 4.26s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong single-source answer from FS Journal Strategy volume. |
| 6 | How do you organize a large-scale IT transformation program? | 7.86s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws from GTIS Strategy document and FS Journal. |
| 7 | What is the relationship between business strategy and technology strategy? | 3.98s | ✅ | Barbero - 2020 - Technology Modernizatio | Core intellectual thread running through entire corpus — business strategy drives technology strategy, not the reverse.
 |
| 8 | What are the key considerations for cloud migration and technology modernization? | 5.38s | ✅ | Barbero - 2020 - Technology Modernizatio | Draws directly from Barbero 2020 Technology Modernization paper — original work with a principled-based approach framework. Replaces enterprise AI reference architecture question (weak retrieval).
 |
| 9 | What are the key principles for modernizing legacy applications? | 5.09s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong retrieval from Barbero 2020 Technology Modernization paper — original work, highly specific content.
 |
| 10 | What are the key risk and compliance considerations for financial services IT? | 4.13s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Retrieves from FS Journal Risk/Compliance/Security volume (2005). |
| 11 | How has digitization changed financial services technology? | 5.11s | ✅ | FS Journal, Edited by M. Barbero - Digit | Retrieves from FS Journal Digitization volume. Clean single-source answer with good citation compliance.
 |
| 12 | What is the role of architecture in managing technology risk in financial services? | 4.73s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Good synthesis question drawing on multiple FS Journal volumes. Strong closer for a demo sequence. |

## Detailed Results

### qfd_technology_architecture
**Query:** What is QFD and how does it apply to technology architecture?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.87s | **Pass:** ✅

**Answer:**

> Quality Function Deployment (QFD) is a tool that can be used in the development of an enterprise IT architecture, according to [1]. It involves assessing multiple solutions and selecting one to implement. QFD is often used in conjunction with other tools such as Six Sigma philosophy, Voice of the Customer analysis, and object-oriented paradigm.
>
> In the context of technology architecture, QFD fills the section on "plateaus" or buzzwords, highlighting what really matters in making an architecture definition work [1]. The systematic definition of a coherent set of principles and standards is essential for successful IT architecture development [1].
>
> QFD has applications beyond technology architecture, as illustrated by its use in non-technology areas [7]. It implies that several solutions will be assessed and one selected for implementation.
>
> It's worth noting that the provided sources do not explicitly define QFD or explain its application to technology architecture in detail. However, based on the context, it appears that QFD is a tool used in IT architecture development that involves assessing multiple solutions and selecting one to implement.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.10


### it_org_architectural_principles
**Query:** How do you design an IT organization around architectural principles?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.18s | **Pass:** ✅

**Answer:**

> To design an IT organization around architectural principles, we need to define the principles, standards, and implementation considerations that collectively define an architecture [1]. This requires a one-to-one mapping between conceptual/logical/physical concepts and principle/standard/implementation consideration concepts, where principles govern decisions made and actions taken [1].
>
> One approach is to use organizational patterns, such as tollgate analysis, which recommends formal presentation of results obtained so far before going to the next step [3]. The Define phase is probably the most important step in an organizational architecture, where we define the principles that will guide our decision-making [3].
>
> According to Benedicte Lambert and Victoria Baldwin, a critical success factor in leveraging the benefits of using architectural frameworks is to make sure that the proper governance model, processes, and organizational constructs are in place [2]. This involves using tried-and-true approaches, or patterns, to solving complex problems.
>
> In terms of technique, architecting an organization is no less an art than architecting a technology solution, requiring good judgment, experience, and intuition [1, 3]. By sharing our "universal architecture toolset," we can help debunk the notions that technology architects are the high priests of an inscrutable religion and that organizational design is exclusively artistic [1].
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

> Architecture concepts can help design organizations by providing a framework for analyzing and resolving problems that arise in dealing with any kind of complex system [1]. These tools and techniques can be applied to organizational design, which involves defining process rather than functions [1][2]. Furthermore, architects' skills in analyzing the end-to-end "IT value chain" are essential in designing the IT organization [2].
>
> Additionally, good judgment, experience, and intuition play a role in architecting an organization, but technique is also crucial in supporting inspiration [2]. The proper governance model, processes, and organizational constructs must be in place to leverage the benefits of using architectural frameworks [1][2].
>
> Moreover, the concept of "universal architecture toolset" can help non-architects design an architecture by providing a high-level primer on how to design technology or organizational architecture [1][2]. For architects, this article can provide a way to contribute actively to the debate on how to structure the IT organization and offer insights into seminal ideas regarding IT organization [1][2].
>
> Lastly, a short time frame is essential for effective organizational redesign, which focuses on defining process rather than functions [2].

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.4
- [2] Architecting the IT Organization.pdf p.1


### cto_three_year_strategy
**Query:** How should a CTO prioritize a three-year technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.6s | **Pass:** ✅

**Answer:**

> Based on the provided sources, a CTO should prioritize a three-year technology strategy by first defining an initial straw man vision for the future linked to business and organizational objectives ([2]). This vision should be expressed using standard visual notation and include scenario-based views that serve as the foundation for business cases ([2]).
>
> The next step is to develop an overall plan as to how the corporate and business objectives are supported and enabled by technology, including an assessment of whether the right technology, program plans, road maps, and processes are being used ([2]). This plan should be developed in alignment with the realities of implementing prioritized initiatives ([2]).
>
> Additionally, it is recommended to use a structured approach such as House-Of-Quality to formally trace technology goals to business objectives (if they exist) ([5]).
>
> As for specific priorities within the three-year strategy, it is not explicitly stated in the provided sources. However, based on general principles of IT strategy development, cost control and reducing costs might be a consideration ([3][4]).

**Citations:**

- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.16
- [3] BOEI - Architecture and QFD -   2003.pdf p.5
- [4] Architecture and QFD.pdf p.5
- [5] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3


### technology_target_state
**Query:** What does a good technology target state look like?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.26s | **Pass:** ✅

**Answer:**

> A good technology target state should be traceable back to the components of the business strategy, but this is often murky or inexistent [1]. Therefore, one way to formally define and reach a desired end state is by using House-Of-Quality [11].
>
> In some cases, it may be necessary to keep the end state defined at the conceptual level due to lack of information or unavailability of technology, budgets, or key talents [2].
>
> To achieve precision in defining an end state, one should consider a progressive and pragmatic approach that defines realistic "transformation plateaus" aimed at implementing the end state step by step, while reducing technology and implementation risks [3].
>
> The overall architecture can be expressed as a series of views that help various audiences understand what the architecture is. Each of these views is necessary, but once they have been recognized, you can assume that everyone understands their components and is on the same page [4].

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3
- [2] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.36
- [3] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.25
- [4] Architecting the IT Organization.pdf p.7


### large_scale_it_transformation
**Query:** How do you organize a large-scale IT transformation program?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.86s | **Pass:** ✅

**Answer:**

> To organize a large-scale IT transformation program, it's essential to adopt an approach that balances formality and linearity with the need for agility and flexibility. One effective method is to implement an iterative cycle with continuous feedback and improvement at each stage.
>
> As described in [1], large projects often require a high level of risk management and traceability of results, particularly when dealing with government-mandated standards such as DOD-STD-2167A and MIL-STD-498. In these cases, a formal and linear approach is necessary to ensure compliance and success.
>
> However, for large-scale IT transformation programs, an iterative approach can be more effective. Agile methodologies, which have emerged in the past decade, use low ceremony and high levels of formality and linearity in execution [1]. These methodologies emphasize continuous improvement and customization as each initiative progresses.
>
> In addition to adopting an agile methodology, it's also essential to establish a comprehensive but realistic data-gathering activity thread to drive agreement on a future vision, priorities, and implementation road map [2].
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
**Latency:** 3.98s | **Pass:** ✅

**Answer:**

> The relationship between business strategy and technology strategy is as follows:
>
> Ideally, the high-level goal for technology should be derived and traced back to the components of the business strategy [1]. This means that a well-defined business strategy should inform and drive the development of a technology strategy.
>
> In fact, developing IT strategies that are assets but as a process—that is, well aligned with business goals and objectives—and achievable in that they deliver incremental business value to sustain funding and are driven by practical solutions to real problems [2].
>
> The GTIS Three Year Strategy and Plan document also highlights the importance of aligning technology strategy with business objectives. According to this document, the GTIS business strategy is driven by both the Group IT and business objectives [3].

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.1
- [3] GTIS STRATEGY - MAIN - Three Year Strategy - Final (with speaker notes).pptx


### cloud_migration_modernization
**Query:** What are the key considerations for cloud migration and technology modernization?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.38s | **Pass:** ✅

**Answer:**

> Key considerations for cloud migration and technology modernization include:
>
> * Assessing each application in the portfolio by both objective data (from a code scan) and qualitative data (from surveys), enabling segmentation and prioritization into categories such as Refactor, Revise, Rehost, Replace, and Retire [1].
> * Identifying specific cloud migration Blockers and Boosters within the source code of an application slated for migration to the cloud [1].
> * Gathering relevant data through surveys, asking the right questions, and focusing on a simple set of questions that help cut through analysis, including:
> 	+ Business Impact: Does the application serve internal or external users? Could failure of this application lead to loss of revenue?
> 	+ Cloud Ready: Is the application multi-tenant? Estimate ease of migration
> 	+ What is the average skill level on cloud technologies of the development team?
> 	+ What is the current user authentication mechanism? Identify security implications before migration [1].
> * Performing an initial analysis of the portfolio using tools that leverage these questions and answer them to identify quick wins [35][36].
> * Developing a roadmap to the cloud for large application portfolios using both objective cloud readiness measurements and qualitative business context considerations [1].
>
> Note: The source numbers in brackets refer to the provided document, which is cited as [1].

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.10


### modernizing_legacy_applications
**Query:** What are the key principles for modernizing legacy applications?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.09s | **Pass:** ✅

**Answer:**

> Unfortunately, the provided sources do not explicitly state the key principles for modernizing legacy applications. However, based on [1], we can identify some principles mentioned in the context of software legacy modernization:
>
> * PRINCIPLE I - Focus on the Highest Value to the Business (not explicitly stated)
> * PRINCIPLE II - Use an "Architecture-Driven" approach to code development
> * PRINCIPLE III - Experiment, Learn and Loop
>
> Additionally, [2] mentions that systems must be modified to link information and enforce policies in a workflow framework, but it does not provide specific principles for modernizing legacy applications.
>
> From the text in [1], we can extract some key points related to software legacy modernization:
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.6
- [2] FS Journal, Edited by M. Barbero - RiskCompliance and Security - 2005.pdf p.20


### risk_compliance_financial_services
**Query:** What are the key risk and compliance considerations for financial services IT?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.13s | **Pass:** ✅

**Answer:**

> Key risk and compliance considerations for financial services IT include:
>
> * Convergence of risk management and compliance management across multiple domains [1]
> * Managing purely financial risk and compliance requirements dictated by government regulations, along with operational requirements created both by regulations and market forces [1]
> * A holistic approach to dealing with risk, compliance, and security issues, considering the convergence of key processes and data sharing [1]
> * Regulatory compliance initiatives such as Sarbanes-Oxley Act and Basel II [1]
> * Managing RCS (risk, compliance, and security) by leveraging the same kind of data and monitoring the same processes across the three domains [1]
>
> Financial services companies are recommended to consider a portfolio approach to addressing risk, compliance, and security issues, with a focus on convergence of key processes and data sharing.

**Citations:**

- [1] FS Journal, Edited by M. Barbero - RiskCompliance and Security - 2005.pdf p.6


### digitization_financial_services
**Query:** How has digitization changed financial services technology?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.11s | **Pass:** ✅

**Answer:**

> Digitization has changed financial services technology by bringing together many technologies in a suite or "stack" that captures and manifests the way the institution operates today [1]. This digitization stack can help financial institutions meet security concerns, including protection of digitized content, creating and maintaining digital records, and addressing vulnerabilities of digitized information [1].
>
> Digitization is also characterized by integrated vision and architectures with due focus on domains such as security and enterprise information integration, as well as the necessary computing and communications infrastructures [1]. This shift towards digitization is driven by various factors, including a renewed flurry of acquisitions and mergers, government mandates (such as Know Your Customer, the Sarbanes-Oxley Act, Basel II, and the Gramm-Leach-Bliley Act), and the need for end-to-end processing and straight-through processing [1].
>
> Furthermore, digitization can transform financial institutions along the entire value chain of internal and external operations, freeing up financial, human, and information resources [1]. It enables integrated commercial loan underwriting in banking, portal-based claim processing in insurance, and straight-through processing in capital markets [1].
>
> Overall, digitization has a profound impact on financial services technology, requiring institutions to take an integrated view of their processes and technologies to achieve real value from these tools.

**Citations:**

- [1] FS Journal, Edited by M. Barbero - Digitization.pdf p.34


### architecture_technology_risk
**Query:** What is the role of architecture in managing technology risk in financial services?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.73s | **Pass:** ✅

**Answer:**

> The role of architecture in managing technology risk in financial services is crucial for enabling near real-time monitoring of exposure in several risk domains, such as market risk and client risk [1]. This can be achieved through advanced application integration architecture.
>
> In addition, enterprise IT architecture helps manage complexity and maintain the integrity of the IT environment, which is essential for financial services firms to survive [2].
>
> Financial services firms have struggled with promoting the systematic use of architecture within their IT function due to various challenges, including justifying the return on investment (ROI) from enterprise IT architecture initiatives [1][2]. To overcome these challenges, architects can apply leading practices such as convergence of equities and fixed income functions, data mining across businesses, and consolidating or retiring cash-trading systems [1].
>
> Moreover, financial services firms have begun to acknowledge the importance of enterprise IT architecture in managing complexity and maintaining the integrity of the IT environment, marking a renewed emphasis on long-term strategic planning after years of quarter-to-quarter focus on cost takeout [2].

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