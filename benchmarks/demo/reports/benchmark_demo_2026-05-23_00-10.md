# AIStudio — Benchmark Findings
*Generated: 2026-05-23 00:12*

## Configuration
- **Corpus:** `demo`
- **Top K:** 10
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 14
- **Passed:** 14/14 (100%)
- **Avg latency:** 8.6s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `demo` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | What is QFD and how does it apply to technology architecture? | 12.22s | ✅ | Erder | Pureur - 2003 - Architecture and | Tests retrieval of dedicated QFD document (Erder|Pureur 2003). Flagship demo question.
 |
| 2 | How do you design an IT organization around architectural principles? | 8.08s | ✅ | Barbero - 2006 - Architecture Concepts a | Retrieves from Barbero 2006 Architecture Concepts and FS Journal. |
| 3 | How do architecture concepts help design organizations? | 6.9s | ✅ | Barbero et al. - 2006 - FS Journal - Str | Draws on the universal architecture toolset concept — one of the core intellectual contributions of the corpus.
 |
| 4 | How should a CTO prioritize a three-year technology strategy? | 8.46s | ✅ | Barbero et al. - 2005 - FS Journal - IT  | Consistently returns multiple citations. Draws from FS Journal Strategy volume and Barbero 2020 modernization paper.
 |
| 5 | What does a good technology target state look like? | 7.84s | ✅ | Barbero - 2006 - Architecture Concepts a | Strong single-source answer from FS Journal Strategy volume. |
| 6 | How do you organize a large-scale IT transformation program? | 8.69s | ✅ | Barbero - 2006 - Architecture Concepts a | Primary source is Barbero - 2020 - Technology Modernization and Cloud Migration.pdf — covers large-scale transformation program organization, Refactor/Rehost/Replace framework, and cloud transformation execution.
 |
| 7 | What is the relationship between business strategy and technology strategy? | 9.76s | ✅ | Barbero - 2020 - Technology Modernizatio | Core intellectual thread running through entire corpus — business strategy drives technology strategy, not the reverse.
 |
| 8 | What are the key considerations for cloud migration and technology modernization? | 9.39s | ✅ | Barbero - 2020 - Technology Modernizatio | Draws directly from Barbero 2020 Technology Modernization paper — original work with a principled-based approach framework.
 |
| 9 | What are the key principles for modernizing legacy applications? | 9.58s | ✅ | Barbero - 2020 - Technology Modernizatio | Strong retrieval from Barbero 2020 Technology Modernization paper — original work, highly specific content.
 |
| 10 | How do Sarbanes-Oxley and Basel II requirements shape IT governance and security architecture in financial services firms? | 7.33s | ✅ | Barbero et al. - 2005 - FS Journal - Ris | Specific regulatory terms force retrieval from FS Journal Risk/Compliance/Security volume (2005). Sarbanes-Oxley and Basel II are named in the corpus metadata search guidance — this question cannot be answered from general knowledge alone.
 |
| 11 | How has digitization changed financial services technology? | 7.87s | ✅ | Barbero et al. - 2005 - FS Journal - Dig | Retrieves from FS Journal Digitization volume. Clean single-source answer with good citation compliance.
 |
| 12 | What is the role of architecture in managing technology risk in financial services? | 7.77s | ✅ | Barbero et al. - 2005 - FS Journal - Ris | Good synthesis question drawing on multiple FS Journal volumes. Strong closer for a demo sequence.
 |
| 13 | What are the key opportunities and limitations of agentic AI in financial services? | 8.18s | ✅ | Barbero - 2026 - Agentic AI in Financial | Tests retrieval from Barbero 2026 Agentic AI paper. Covers Verifier Law, limitations, and strategic implications.
 |
| 14 | How should organizations embed AI into their knowledge productivity ecosystem? | 7.93s | ✅ | Barbero - 2026 - Agentic AI in Financial | Tests Section C content from Barbero 2026 — vision for AI integration as foundational element of knowledge work reinvention. |

## Detailed Results

****
### 1. qfd_technology_architecture
**Query:** What is QFD and how does it apply to technology architecture?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 12.22s | **Pass:** ✅

**Answer:**

> Quality Function Deployment (QFD) is a methodology used to translate customer requirements into design specifications and prioritize product or service features. It applies the concept of "house of quality" to identify key drivers of product or service performance [1].
>
> In the context of technology architecture, QFD helps to correlate business requirements with key technical drivers, enabling architects to create a rigorous approach to system design [1]. This involves using techniques such as Design Space to prioritize and organize requirements against business priorities.
>
> QFD is also related to other methodologies, including Six Sigma, which emphasizes the importance of technique in supporting innovation. The Six Sigma toolset includes quality function deployment (QFD) as one of its key concepts [2].
>
> In terms of levels of specificity, QFD can be applied at different stages of architecture development, from conceptual to physical [3]. This helps to ensure that business and technical requirements are aligned throughout the architecture process.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Erder | Pureur - 2003 - Architecture and QFD.pdf p.4
- [2] Barbero - 2006 - Architecture Concepts and How To Use Them To Design an Organization.pdf p.45
- [3] Barbero - 2020 - Technology Modernization and Cloud Migration.pdf p.16


****
### 2. it_org_architectural_principles
**Query:** How do you design an IT organization around architectural principles?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 8.08s | **Pass:** ✅

**Answer:**

> Designing an IT organization around architectural principles involves a systematic analysis of the bridge between business vision, organizational constructs, processes, and enabling technologies required to execute the vision. The organizational architecture is the foundation upon which decisions are made, processes are developed, and supporting technology is implemented [1].
>
> To design an IT organization, one should define the principles, standards, and implementation considerations that collectively define an architecture. This requires a discipline associated with complex systems architecture, where principles govern decisions made and actions taken [1]. For example, principles related to outsourcing influence the positioning of the IT organization along the factory/service-oriented continuum.
>
> The 10 concepts presented in the sources are essentially transposable from the IT architecture realm to the organizational architecture realm. These concepts include:
>
> * Tollgate analysis
> * Sound Define phase (DFS)
> * Analyzing the end-to-end "IT value chain"
> * Designing the IT architecture function
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero - 2006 - Architecture Concepts and How To Use Them To Design an Organization.pdf p.4
- [2] Barbero et al. - 2006 - FS Journal - Strategy and Architecture Concepts and Techniques.pdf p.4


****
### 3. architecture_concepts_organizations
**Query:** How do architecture concepts help design organizations?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.9s | **Pass:** ✅

**Answer:**

> Architecture concepts help design organizations by leveraging what architects have learned about analyzing and resolving problems in complex systems. These tools and techniques can be applied to organizational design, allowing for the creation of a "universal architecture toolset" that benefits both architects and non-architects.
>
> The 10 critical performance factors mentioned in the sources are essentially transposable from the IT architecture realm to the organization architecture realm [1]. This means that the concepts presented can be applied almost directly to organizational design, demonstrating their universality. By applying these concepts, organizations can improve their processes, communication, project management, and knowledge management.
>
> The article notes that architecting an organization is no less of an art than architecting a technology solution, requiring good judgment, experience, and intuition [1]. However, technique plays a crucial role in supporting inspiration, and sharing the "universal architecture toolset" can help debunk myths about the expertise required for organizational design.
>
> In particular, Six Sigma philosophy and its tools can be applied to organizational architecture projects when dealing with complex issues that cut across organizational boundaries [2]. By considering the Six Sigma toolset, organizations can improve their processes and management, using statistical analysis and data-oriented techniques to drive decision-making.

**Citations:**

- [1] Barbero et al. - 2006 - FS Journal - Strategy and Architecture Concepts and Techniques.pdf p.4
- [2] Barbero - 2006 - Architecture Concepts and How To Use Them To Design an Organization.pdf p.30


****
### 4. cto_three_year_strategy
**Query:** How should a CTO prioritize a three-year technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 8.46s | **Pass:** ✅

**Answer:**

> To prioritize a three-year technology strategy, a CTO should follow these steps:
>
> 1. **Define IT services and related infrastructure components**: Identify the key capabilities and scope of the CMDB implementation to define and include CIs (Configuration Items) that provide business value in the short term (0-4 months) [1].
> 2. **Employ an iterative process**: Assess the maturity of the CMDB and enhance it in alignment with organizational requirements, using a phased approach to evaluate and prioritize initiatives.
> 3. **Use scenarios or use cases as a foundation for expression of business value**: Define an initial straw man vision for the future linked to goals and objectives, and embrace a broad understanding of current issues [2].
> 4. **Prioritize initiatives based on ROI analysis**: Estimate the return on investment (ROI) for each initiative and prioritize those with the highest potential return [3].
> 5. **Establish clear goals and objectives**: Derive high-level technology goals from business strategy components or well-defined transformative business initiatives, and ensure these are effectively useful in setting the technology strategy [4].
>
> To create a successful three-year technology strategy, it's essential to:
>
> * Clearly define IT services and related infrastructure components
> * Employ an iterative process for CMDB implementation
> * Prioritize initiatives based on ROI analysis
> * Establish clear goals and objectives
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero et al. - 2005 - FS Journal - IT Infrastructure.pdf p.20
- [2] Barbero et al. - 2006 - FS Journal - Strategy and Architecture Concepts and Techniques.pdf p.16
- [3] Erder | Pureur - 2003 - Architecture and QFD.pdf p.5
- [4] Barbero - 2020 - Technology Modernization and Cloud Migration.pdf p.3


****
### 5. technology_target_state
**Query:** What does a good technology target state look like?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.84s | **Pass:** ✅

**Answer:**

> A good technology target state is defined by a progressive and pragmatic approach that uses transformation plateaus to reach the desired end state in actionable increments [1]. This involves breaking down the complex goal into smaller, manageable steps that reduce technology and implementation risks.
>
> Transformation plateaus are stepping stones that allow organizations to move from their current state (A) to their desired end state (C) [1]. They are defined as a series of realistic "transformation plateaus" (B1, B2, B3, etc.) aimed at implementing the end state step by step.
>
> To define a good technology target state, it is essential to establish clear goals and objectives that align with business strategy. These goals should be articulated in a way that the business can value and relate to [2]. A worthwhile goal should be tangible, measurable, achievable, relevant, and time-bound (SMART).
>
> The architecture function plays a crucial role in ensuring that "the right technology decisions are made" by establishing technology governance, setting standards, visualizing target state architecture and roadmaps, and ensuring that the right remedial actions are taken when implementation of these plans are not going as planned [2].

**Citations:**

- [1] Barbero - 2006 - Architecture Concepts and How To Use Them To Design an Organization.pdf p.35
- [2] Barbero - 2020 - Technology Modernization and Cloud Migration.pdf p.4


****
### 6. large_scale_it_transformation
**Query:** How do you organize a large-scale IT transformation program?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 8.69s | **Pass:** ✅

**Answer:**

> To organize a large-scale IT transformation program, follow this approach:
>
> 1. **Understand the business vision and requirements** [1]: The first step in leading an IT transformational change is to envision your first day in leading that change, focusing on organization.
> 2. **Gather data and conduct stakeholder analysis** [2]: Identify key stakeholders and their needs, gather data on current processes and systems, and cleanse this data for effective decision-making.
> 3. **Establish a guiding coalition and leadership team** [3]: A strong, respected leadership team is required to drive the transformation program forward. This team should include technologists who understand the business vision and requirements.
> 4. **Develop a comprehensive road map** [4]: Create a high-level overview of the transformation process, including key steps, timelines, and resource allocation.
> 5. **Identify key processes and prioritize them** [2]: Conduct risk analysis to identify critical processes that require immediate attention and develop plans for their implementation.
> 6. **Implement an agile-iterative approach or waterfall method** [1]: Depending on the organization's size, complexity, and cultural characteristics, choose either an agile-iterative approach or a high-ceremony, waterfall method.
> 7. **Continuously monitor progress and adjust** [3]: Regularly review program status, address emerging issues, and make adjustments to ensure successful completion of the transformation.
>
> By following these steps, you can effectively organize a large-scale IT transformation program.

**Citations:**

- [1] Barbero - 2006 - Architecture Concepts and How To Use Them To Design an Organization.pdf p.8
- [2] Barbero et al. - 2005 - FS Journal - IT Infrastructure.pdf p.22
- [3] Barbero et al. - 2005 - FS Journal - Risk Compliance and Security.pdf p.21
- [4] Barbero et al. - 2006 - FS Journal - Strategy and Architecture Concepts and Techniques.pdf p.23


****
### 7. business_technology_strategy
**Query:** What is the relationship between business strategy and technology strategy?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 9.76s | **Pass:** ✅

**Answer:**

> The relationship between business strategy and technology strategy is that the high-level goal for technology should be derived and traced back to the components of the business strategy [1]. This involves articulating goals in a way that the business can value and relate to, such as creating customer loyalty and recurring revenues through a seamless user experience [1]. Achieving these business objectives requires solving issues at lower levels, which might require achieving goals through a combination of technological solutions.
>
> Defining an IT strategy is not a matter of choice for financial services companies, but rather a critical component of their success, as technology is tightly linked to business success [2]. In fact, the manifestation of an IT organization's strategy is its ability to produce and maintain underlying technology frameworks that bring this strategy to life [2].
>
> Creating an enterprise IT architecture is a strategic planning effort that can transform how an organization operates, particularly how the IT function and its business-side clients interact and work together [2]. This involves defining enterprise IT architecture as the sum of the architectures of systems or organizations, which expresses and establishes consensus about a vision of the future aligned to those goals and objectives.
>
> A good approach to developing IT strategic planning is to use a systematic method that can lead to the definition of an enterprise IT architecture. This involves understanding what strategy is, as it requires agreed-on definitions, particularly between technologists and their management [2].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration.pdf p.3
- [2] Barbero et al. - 2006 - FS Journal - Strategy and Architecture Concepts and Techniques.pdf p.14


****
### 8. cloud_migration_modernization
**Query:** What are the key considerations for cloud migration and technology modernization?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 9.39s | **Pass:** ✅

**Answer:**

> The key considerations for cloud migration and technology modernization are:
>
> 1. **Portfolio Analysis**: Assessing the application portfolio to identify potential impacts on customers, financial implications, and ease of migration [1]. This involves categorizing applications into Refactor, Revise, Rehost, Replace, or Retire based on objective data (code scan) and qualitative data (surveys).
> 2. **Cloud Readiness**: Evaluating the current user authentication mechanism, estimating the ease of migration, and identifying security implications before migration [1]. This involves using tools to perform an initial analysis of the portfolio and setting up metrics for assessing best candidates.
> 3. **Data Governance**: Sourcing legacy data as is and not rethinking it in the context of a better, rationalized cross-application enterprise data architecture and governance model [2].
> 4. **Principled-Based Approach**: Adopting a principled-based approach to modernization, which supports a portfolio-wide yet iterative road to success [1]. This involves emphasizing identification of business logic and data structure information, optimizing the portfolio by refactoring applications in modules that can be shared across applications, and implementing cross-application orchestration.
> 5. **Avoidance of Lift and Shift**: Avoiding the simplistic approach of "Lift and Shift," which does not provide new business capabilities and creates new transition costs [2].

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration.pdf p.10
- [2] Barbero - 2026 - Agentic AI in Financial Services.pdf p.4


****
### 9. modernizing_legacy_applications
**Query:** What are the key principles for modernizing legacy applications?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 9.58s | **Pass:** ✅

**Answer:**

> The key principles for modernizing legacy applications are outlined in the provided sources. According to [1], the approach should be systematic, incremental, and iterative, as stated in PRINCIPLE III - Experiment, Learn and Loop. This principle emphasizes the importance of harvesting and leveraging lessons learned across projects.
>
> To modernize legacy applications, it is essential to identify potential issues before moving them to the cloud. As mentioned in [1], this includes re-performing unit tests to profile bottlenecks and using automated code analysis technology to spot engineering anti-patterns across multi-tier architecture.
>
> Another crucial aspect is understanding cross-application dependencies, as highlighted in [1]. This involves identifying structure, not dynamic behavior, through automated static pattern analysis and documentation. By doing so, it becomes possible to refactor application functionalities and restructure the data model, leading to a more efficient and integrated system.
>
> In addition, the traditional SEI model from 1999 is insufficient for modernizing legacy applications, as stated in [1]. The approach needs an update to show how enterprises can visualize the overall topology of the application structure at various levels. This includes identifying data models, understanding business rules embedded in the code, and rethinking the enterprise data model.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero - 2020 - Technology Modernization and Cloud Migration.pdf p.6


****
### 10. risk_compliance_financial_services
**Query:** How do Sarbanes-Oxley and Basel II requirements shape IT governance and security architecture in financial services firms?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.33s | **Pass:** ✅

**Answer:**

> Sarbanes-Oxley and Basel II requirements shape IT governance and security architecture in financial services firms by imposing stringent security measures to protect all information assets, not just customer information [1]. These regulations demand that financial institutions protect their digital information from cyber threats, data breaches, and identity theft. To comply with these regulations, financial institutions must implement robust security systems that can detect and prevent unauthorized access to confidential information.
>
> According to the sources, Sarbanes-Oxley and Basel II require financial institutions to:
>
> * Protect all information assets, including customer information [1]
> * Implement stringent security measures to prevent data breaches and cyber threats [2]
> * Ensure the integrity and availability of key financial information [2]
> * Implement a holistic approach to manage IT governance and security architecture [3]
>
> The sources also indicate that financial institutions can reduce the risk of their information by:
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero et al. - 2005 - FS Journal - Risk Compliance and Security.pdf p.17
- [2] Barbero et al. - 2005 - FS Journal - Digitization.pdf p.19
- [3] Barbero et al. - 2006 - FS Journal - Strategy and Architecture Concepts and Techniques.pdf p.7


****
### 11. digitization_financial_services
**Query:** How has digitization changed financial services technology?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.87s | **Pass:** ✅

**Answer:**

> Digitization in financial services has brought together many technologies in a suite or "digitization stack" that captures and manifests the way an institution operates today. This digitization stack includes business process automation, management technologies, and new technologies such as portal-based claim processing, straight-through processing, and integrated commercial loan underwriting.
>
> The digitization of financial services technology has transformed the industry by freeing up financial, human, and information resources along the entire value chain of internal and external operations. It has also enabled the creation of a seamless process that speeds up transactions and significantly improves the efficiency of personnel involved in various processes [1].
>
> In retail banking, digitization is helping break down intra-institution barriers that have impeded cross-selling at the most ambitious level and the opening of new accounts at the most mundane level. By connecting disparate systems with business process automation and management technologies, new accounts can be funded from existing brokerage and asset management data accounts [2].
>
> The security domains in an organization employing digitization tools would include protection of digitized content, authentication, and integrity to ensure that data remains unchanged or matches exactly what was sent [3]. Digitization also calls for integrated vision and architectures with due focus on domains such as security and enterprise information integration.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero et al. - 2005 - FS Journal - Digitization.pdf p.3


****
### 12. architecture_technology_risk
**Query:** What is the role of architecture in managing technology risk in financial services?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.77s | **Pass:** ✅

**Answer:**

> The role of architecture in managing technology risk in financial services is to define and implement an enterprise IT architecture that integrates business and technology strategies. This involves developing a "convergence" approach that combines different technologies and systems, such as application integration architecture, data mining, and infrastructure IT architecture, to manage risk and compliance [1].
>
> Financial services firms have historically struggled with implementing enterprise IT architectures due to the complexity and uncertainty of reaching the future architectural state, but this is no longer seen as an insurmountable challenge. Instead, there is a renewed interest in promoting the systematic use of architecture within their IT function in general and defining enterprise IT architecture in particular [1].
>
> The development of an enterprise IT architecture that integrates business and technology strategies requires a "prescriptive" view of the architecture, which defines the actions required to realize the architecture over time. This involves creating a transitional architecture or "transitional roadmap" that outlines the steps needed to achieve the future state [2].
>
> Effective implementation of the architecture is critical to managing technology risk in financial services. A study by BearingPoint found that 10 specific leading practices, including data mining and infrastructure IT architecture, can be applied to develop an enterprise IT architecture that integrates business and technology strategies [2].

**Citations:**

- [1] Barbero et al. - 2005 - FS Journal - Risk Compliance and Security.pdf p.36
- [2] Barbero et al. - 2006 - FS Journal - Strategy and Architecture Concepts and Techniques.pdf p.6


****
### 13. agentic_ai_financial_services
**Query:** What are the key opportunities and limitations of agentic AI in financial services?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 8.18s | **Pass:** ✅

**Answer:**

> The key opportunities of agentic AI in financial services include:
>
> Agentic AI promises to expand AI's cognitive capabilities from memorization and classification to generation and strategizing, enabling automation of entire workflows [1]. This evolution combines perception, reasoning, planning, and autonomous task execution to achieve high-level goals. Agentic AI can orchestrate complex workflows autonomously across modalities: numbers, text, images, and sound [1].
>
> Agentic AI has the potential to uplift sectors, displace labor, and trigger regulatory or societal shifts that could reshape investment landscapes [1]. However, its current limitations — reliance on rule-based workflows, linear reasoning, insufficient data quality, and change management hurdles — restrict its ability to perform autonomous, complex decision-making fully [1].
>
> The key limitations of agentic AI in financial services include:
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero - 2026 - Agentic AI in Financial Services.pdf p.1
- [2] Barbero et al. - 2005 - FS Journal - IT Infrastructure.pdf p.30


****
### 14. ai_knowledge_productivity
**Query:** How should organizations embed AI into their knowledge productivity ecosystem?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.93s | **Pass:** ✅

**Answer:**

> To embed AI into their knowledge productivity ecosystem, organizations should follow these guidelines:
>
> 1. **Human-AI Collaboration**: Automation should augment human expertise, not replace it. Knowledge workers can co-create and manage knowledge with AI agents [1].
> 2. **Stakeholder-Centered Design**: Solutions should be developed with input from content owners, technology teams, and end-users to ensure relevance and usability [1].
> 3. **Modularity and Reuse**: Build standardized components that can be leveraged across multiple domains and use cases [1].
> 4. **Security and Governance**: AI should be embedded within secure, monitored environments with robust access control and policy management serving the entire ecosystem [1].
> 5. **Integration and Interoperability**: Open APIs and facades abstract complexity, enabling seamless integration with existing systems and workflows [1].
>
> Additionally, organizations should consider:
>
> * Developing a conceptual vision of their organization by articulating key principles [2]
> * Focusing on building areas of expertise in various technology domains staffed by highly competent technologists [2]
> * Using the value chain representation technique to map out the various processes of the IT organization and define what each component does and how it interacts with other components [3]
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] Barbero - 2026 - Agentic AI in Financial Services.pdf p.4
- [2] Barbero et al. - 2006 - FS Journal - Strategy and Architecture Concepts and Techniques.pdf p.39
- [3] Barbero - 2006 - Architecture Concepts and How To Use Them To Design an Organization.pdf p.23

