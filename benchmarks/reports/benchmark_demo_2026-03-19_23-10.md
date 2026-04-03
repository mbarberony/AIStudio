# AIStudio — Benchmark Findings
*Generated: 2026-03-19 23:11*

## Configuration
- **Corpus:** `demo`
- **Top K:** 5
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 12
- **Passed:** 11/12 (92%)
- **Avg latency:** 4.7s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `demo` (see corpus stats in UI)
- Note: SEC 10-K corpus = 143 filings, 105,964 chunks — ChromaDB crashed at 32,285; Qdrant stable at 105,964

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | What is QFD and how does it apply to technology architecture? | 6.79s | ❌ | FS Journal, Edited by M-1. Barbero - Str | Tests retrieval of dedicated QFD documents (Architecture and QFD.pdf, BOEI - Architecture and QFD - 2003.pdf). Flagship demo question.
 |
| 2 | How do you design an IT organization around architectural principles? | 4.74s | ✅ | Architecture Concepts and How To Use The | Retrieves from Architecting the IT Organization and FS Journal. |
| 3 | How do architecture concepts help design organizations? | 3.8s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws on the universal architecture toolset concept — one of the core intellectual contributions of the corpus.
 |
| 4 | How should a CTO prioritize a three-year technology strategy? | 5.16s | ✅ | FS Journal, Edited by M. Barbero - IT In | Consistently returns 5 citations across all models. Draws from FS Journal Strategy volume and Barbero 2020 modernization paper.
 |
| 5 | What does a good technology target state look like? | 4.08s | ✅ | Architecture Concepts and How To Use The | Strong single-source answer from FS Journal Strategy volume. |
| 6 | How do you organize a large-scale IT transformation program? | 5.44s | ✅ | FS Journal, Edited by M-1. Barbero - Str | Draws from GTIS Strategy document and FS Journal. |
| 7 | What is the relationship between business strategy and technology strategy? | 3.45s | ✅ | Barbero - 2020 - Technology Modernizatio | Core intellectual thread running through entire corpus — business strategy drives technology strategy, not the reverse.
 |
| 8 | What are the key considerations for cloud migration and technology modernization? | 4.73s | ✅ | Barbero - 2020 - Technology Modernizatio | Draws directly from Barbero 2020 Technology Modernization paper — original work with a principled-based approach framework. Replaces enterprise AI reference architecture question (weak retrieval).
 |
| 9 | What are the key principles for modernizing legacy applications? | 5.42s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong retrieval from Barbero 2020 Technology Modernization paper — original work, highly specific content.
 |
| 10 | What are the key risk and compliance considerations for financial services IT? | 3.58s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Retrieves from FS Journal Risk/Compliance/Security volume (2005). |
| 11 | How has digitization changed financial services technology? | 4.6s | ✅ | FS Journal, Edited by M. Barbero - Digit | Retrieves from FS Journal Digitization volume. Clean single-source answer with good citation compliance.
 |
| 12 | What is the role of architecture in managing technology risk in financial services? | 5.09s | ✅ | FS Journal, Edited by M. Barbero - RiskC | Good synthesis question drawing on multiple FS Journal volumes. Strong closer for a demo sequence. |

## Detailed Results

### qfd_technology_architecture
**Query:** What is QFD and how does it apply to technology architecture?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.79s | **Pass:** ❌

**Answer:**

> QFD stands for Quality Function Deployment, which is a tool that can be used in the development of an enterprise IT architecture. According to [1], QFD implies that several solutions will be assessed and one will be selected and implemented. This tool is part of the Six Sigma philosophy, which emphasizes a systematic approach to problem-solving.
>
> QFD is not directly related to technology architecture, but rather it is a tool that can be used in both contexts, such as in software development or organizational design [1]. The article also mentions that QFD fills the previous section with "a few too many buzzwords" [1], implying that it is a concrete approach to problem-solving.
>
> According to [2], designing an IT organization should be the product of a systematic analysis that defines the bridge between the business vision, organizational constructs, processes and enabling technologies required to execute the vision. However, this article does not mention QFD as one of the tools or concepts used in architecture definition.
>
> In [3], there is no mention of QFD. The article discusses various buzzwords related to technology modernization and cloud migration, but it does not provide a definition or discussion of QFD.

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.10
- [2] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.4
- [3] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.1

**⚠ Model said 'no information' — possible retrieval miss**

### it_org_architectural_principles
**Query:** How do you design an IT organization around architectural principles?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.74s | **Pass:** ✅

**Answer:**

> To design an IT organization around architectural principles, one should define the principles, standards, and implementation considerations that collectively define an architecture [1]. This involves identifying organizational principles that govern decisions made and actions taken, such as those related to outsourcing, which influence the positioning of the IT organization along a factory/service-oriented continuum [1].
>
> Additionally, it is essential to ensure that the proper governance model, processes, and organizational constructs are in place to leverage the benefits of using architectural frameworks [3]. This includes developing an architecture toolset that can be shared with both architects and non-architects to help design an IT organization and its architecture.
>
> Furthermore, a pattern-driven approach can be beneficial for solving complex problems in IT organization design. According to Benedicte Lambert and Victoria Baldwin, a pattern is a tried-and-true approach to solving a particular problem [2]. By applying these patterns and approaches, one can create an effective IT organization architecture that aligns with business goals.
>
> The Define phase is probably the most important step in an organizational architecture, as it sets the foundation for the entire design process [3]. This involves defining the principles, standards, and implementation considerations that will guide the development of the IT organization's architecture.

**Citations:**

- [1] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.30
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.4
- [3] Architecting the IT Organization.pdf p.1


### architecture_concepts_organizations
**Query:** How do architecture concepts help design organizations?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.8s | **Pass:** ✅

**Answer:**

> Architecture concepts help design organizations by providing a way to contribute actively to the debate on how to structure the IT organization, as well as helping non-architects understand how to design "architecture," whether technology or organizational architecture [1]. The proper governance model, processes and organizational constructs are essential in leveraging the benefits of using architectural frameworks [1]. The article also suggests that architects can leverage what they have learned about analyzing and resolving problems in complex systems to contribute to organizational design [2].
>
> In particular, the article highlights the importance of time, as an effective organizational redesign helps focus the process and forces [1], and recommends going from one step to another subject to the formal presentation of results obtained so far [2]. The Define phase is also considered crucial in an organizational architecture [2].

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.4
- [2] Architecting the IT Organization.pdf p.1


### cto_three_year_strategy
**Query:** How should a CTO prioritize a three-year technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.16s | **Pass:** ✅

**Answer:**

> To prioritize a three-year technology strategy, a CTO should first define an initial straw man vision for the future linked to those goals and objectives, as stated in [2]. This involves prioritizing initiatives that will realize the vision over time, using a scenario-based functional view as the foundation for business cases.
>
> Next, the CTO should evaluate the current state of the organization and refine the vision through an iterative process, including ongoing refinement of the vision and a refined understanding of the current state analysis phase. This is in line with [1], which suggests employing an iterative process to assess the maturity of the CMDB and enhance it in alignment with specific organizational requirements.
>
> Additionally, the CTO should consider using QFD (Quality Function Deployment) to select technology products that correlate to architecture principles and refine both selections of designs, features, and technology products. This is mentioned in [3] and [4], which state that correlating technology products to QFD input sets can further refine both selections.
>
> Finally, the CTO should formally trace technology goals to business objectives using a methodology such as House-Of-Quality (HOQ) to ensure alignment with organizational strategy. As stated in [5], this can help identify specific, measurable technology goals that support overall business objectives.

**Citations:**

- [1] FS Journal, Edited by M. Barbero - IT Infrastructure.pdf p.20
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.16
- [3] BOEI - Architecture and QFD -   2003.pdf p.5
- [4] Architecture and QFD.pdf p.5
- [5] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3


### technology_target_state
**Query:** What does a good technology target state look like?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.08s | **Pass:** ✅

**Answer:**

> A good technology target state looks like a series of implementation plateaus that help reach the desired end state in actionable increments [2,3]. It's expressed as a series of views that describe the current state, the end state, and the road map to that end state [4,5]. Each view is necessary, but not sufficient on its own [4].
>
> The transformation process involves developing an actionable plan to reach the end state from the current state, which can be achieved by defining various implementation plateaus [2]. This approach helps reduce technology and implementation risks [2].
>
> It's also recommended to use a progressive and pragmatic approach that defines realistic "transformation plateaus" aimed at implementing transitional states step by step [2]. The transformation process should consider issues related to the combined "physical layer x process x computing infrastructure" views of the ERP project [3,4].

**Citations:**

- [2] Architecture Concepts and How To Use Them To Design an Organizations.pdf p.36
- [3] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.25
- [4] Architecting the IT Organization.pdf p.7
- [5] FS Journal, Edited by M. Barbero - Digitization.pdf p.4


### large_scale_it_transformation
**Query:** How do you organize a large-scale IT transformation program?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.44s | **Pass:** ✅

**Answer:**

> To organize a large-scale IT transformation program, one should follow an approach that involves multiple stages and activities, as described in [1] and [2]. The first step is to establish a comprehensive data-gathering activity thread and a series of global workshops to drive agreement on a future vision, priorities, and implementation road map ([1]). This process should be iterative, with a feedback loop at each stage, allowing for continuous improvement and customization as the initiative progresses.
>
> The approach also involves adopting a high level of formality and linearity in execution, particularly for large, enterprisewide projects ([1] and [2]). Additionally, it is essential to involve stakeholders, such as employees and technology processing flows, in the decision-making process to ensure that their needs are addressed ([3]).
>
> The transformation program should also include activities related to master data management (MDM), which involves setting up a "master data management" or MDM initiative to gain insight into the infrastructure from an economic and management perspective ([3] and [4]). This can be achieved by establishing a CMDB or service catalog and migrating this structure into a production environment.
>
> In terms of changing the engagement model with application development, it is recommended to integrate compute transformation opportunities with the normal application development lifecycle, ensuring minimal overall resource impact ([4]). The demand for distributed compute needs to be rationalized for most efficient use of available capacity.

**Citations:**

- [1] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.23
- [2] Architecting the IT Organization.pdf p.5
- [3] FS Journal, Edited by M. Barbero - IT Infrastructure.pdf p.22
- [4] GTIS STRATEGY - MAIN - Three Year Strategy - Final (with speaker notes).pptx


### business_technology_strategy
**Query:** What is the relationship between business strategy and technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.45s | **Pass:** ✅

**Answer:**

> The relationship between business strategy and technology strategy is as follows:
>
> According to [1], an IT organization should have its goals derived from and traced back to the components of the business strategy. However, this is often murky or inexistent.
>
> [2] states that a level of difficulty arises in developing a common enterprisewide IT strategy and architecture due to financial services organizations being multi-enterprise organizations consisting of related but distinct lines of business.
>
> Furthermore, [1] mentions using House-Of-Quality to formally trace technology goals to business objectives, if they exist.

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.3
- [2] FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf p.1


### cloud_migration_modernization
**Query:** What are the key considerations for cloud migration and technology modernization?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.73s | **Pass:** ✅

**Answer:**

> According to the source [1], key considerations for cloud migration and technology modernization include:
>
> * Assessing each application by both objective data (from a code scan) and qualitative data (from surveys)
> * Segmenting and prioritizing applications into categories such as Refactor, Revise, Rehost, Replace, and Retire
> * Identifying specific cloud migration Blockers and Boosters within the source code of an application
> * Building a right dataset to scope and prioritize out the modernization effort
> * Relying on surveys: gathering relevant data is about asking the right questions
>
> Additionally, the following categories of questions can help cut through the analysis:
>
> * Business Impact:
> 	+ Does the application serve internal or external users?
> 	+ Could failure of this application lead to loss of revenue? Identify financial impact if there was an outage
> * Cloud Ready:
> 	+ Is the application multi-tenant? Estimate ease of migration
> 	+ What is the average skill level on cloud technologies of the development team?
> 	+ Estimate timeline for migration
> 	+ What is the current user authentication mechanism? Identify security implications before migration

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.10


### modernizing_legacy_applications
**Query:** What are the key principles for modernizing legacy applications?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.42s | **Pass:** ✅

**Answer:**

> According to [1], the key principles for modernizing legacy applications include:
>
> 1. **PRINCIPLE I - Identify Opportunities for Business Change** - This principle involves identifying opportunities for business change that can be driven by modernization of legacy apps.
> 2. **PRINCIPLE II - Governance and Standards** - This principle emphasizes the importance of governance and standards in modernizing legacy applications, including the use of a "horseshoe" model diagram [1].
> 3. **PRINCIPLE III - Experiment, Learn and Loop** - This principle advocates for an iterative process when solving complex problems, such as modernizing legacy apps.
> 4. **Data Analysis** - This involves understanding how business rules are embedded in the code and harvesting what data model the original designer(s) used to represent the world [1].
> 5. **Cross-Application Dependencies** - This requires identifying and re-organizing cross-application dependencies through automated static pattern analysis and documentation [1].
>
> Additionally, according to [2], a holistic compliance framework is necessary for digitization projects, which includes:
>
> * Connecting to business support applications
> * Modifying systems to link information and enforce policies
> * Implementing BPM (Business Process Management) to supplement linkage data and provide a mechanism to escalate issues in a traceable manner.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf p.6
- [2] FS Journal, Edited by M. Barbero - RiskCompliance and Security - 2005.pdf p.20


### risk_compliance_financial_services
**Query:** What are the key risk and compliance considerations for financial services IT?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.58s | **Pass:** ✅

**Answer:**

> The key risk and compliance considerations for financial services IT include:
>
> * Managing purely financial risk and compliance requirements dictated by government regulations and market forces ([1])
> * Addressing operational requirements created both by regulations and market forces, including reputational and legal consequences ([1])
> * Understanding the convergence of risk, finance, and compliance management, which have similar data used across these domains ([1])
> * Recognizing that all risk and compliance management require life cycles and can be prioritized in terms of current level of concern ([1])
>
> Note: The source [1] is a comprehensive document on Risk Compliance and Security in Financial Services.

**Citations:**

- [1] FS Journal, Edited by M. Barbero - RiskCompliance and Security - 2005.pdf p.6


### digitization_financial_services
**Query:** How has digitization changed financial services technology?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.6s | **Pass:** ✅

**Answer:**

> Digitization has changed financial services technology by bringing together many technologies in a suite or "stack" that captures and manifests the way an institution operates today [1]. This digitization stack provides a critical link between the customer and the back office, as well as among disparate technologies [1]. It enables institutions to implement end-to-end solutions for better controls, standardization, consistency, and measurement of business processes [1].
>
> Digitization has also transformed financial institutions along the entire value chain of internal and external operations, freeing up financial, human, and information resources [1]. This is achieved by actively taking steps to implement an end-to-end solution that supports the full value chain [1].
>
> Furthermore, digitization requires integrated vision and architectures with due focus on domains such as security and enterprise information integration, as well as the necessary computing and communications infrastructures [1].
>
> The underlying disciplines required for digitization, such as business process management, content and document management, digital imaging, and workflow and collaboration software, have been around for a while but are now being integrated in a way that financial institutions envision today [1].

**Citations:**

- [1] FS Journal, Edited by M. Barbero - Digitization.pdf p.34


### architecture_technology_risk
**Query:** What is the role of architecture in managing technology risk in financial services?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.09s | **Pass:** ✅

**Answer:**

> According to [1], financial services firms have struggled with managing technology risk due to the complexity and lack of integrity in their IT environment. This is because traditional enterprise IT architecture efforts are perceived as large, difficult, and expensive, making it challenging to justify the return on investment (ROI) from a financial perspective.
>
> However, [2] suggests that there is a renewed interest in promoting the systematic use of architecture within IT functions in general and defining enterprise IT architecture in particular. This is driven by the need to manage complexity and maintain integrity in the IT environment. The article also highlights key lessons learned, including:
>
> 1) Enterprise architecture is just too important to be left to chance (i.e., it requires a strategic approach);
> 2) There are high-level benefits from adopting enterprise architecture that can be justified financially;
> 3) Justifying an enterprise architecture initiative from a financial perspective might be close to impossible.
>
> Furthermore, [2] notes that architects have learned to promote their discipline by highlighting the importance of long-term, strategic planning and the need for a renewed emphasis among financial services firms in looking at long-term, strategic planning after years of quarter-to-quarter focus on cost takeout.

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