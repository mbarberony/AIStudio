# Demo Corpus

*Version: 1.2.0 | Updated: 2026-06-15*

> A curated collection of architecture and strategy documents spanning  
> 20+ years of work in financial services technology — from 2003 to 2026.

This corpus ships with AIStudio as a ready-to-query demonstration dataset.
It lets you experience the system immediately after install, without needing
to supply your own documents first.

It also serves as a substantive test of retrieval quality — these are real,
dense documents on complex topics, not toy data.

---

## What's Here

Nine original documents spanning 2003–2026 — architecture methodology, financial-services
technology strategy, and the evolution toward AI-enabled systems.

### Architecture Methodology
Foundational thinking on enterprise architecture and how Quality Function Deployment (QFD)
applies to technology architecture.

- `Erder | Pureur - 2003 - Architecture and QFD.pdf` (454 KB)
- `Barbero - 2006 - Architecture Concepts and How To Use Them To Design an Organization.pdf` (1.1 MB)

### Financial Services Journal Series
Volumes of an edited journal on technology strategy and architecture in financial services —
strategy/architecture concepts, digitization, IT infrastructure, and risk/compliance/security.
Edited by Manuel Barbero (2005–2006).

- `Barbero et al. - 2006 - FS Journal - Strategy and Architecture Concepts and Techniques.pdf` (2.7 MB)
- `Barbero et al. - 2005 - FS Journal - Digitization.pdf` (1.8 MB)
- `Barbero et al. - 2005 - FS Journal - IT Infrastructure.pdf` (1.1 MB)
- `Barbero et al. - 2005 - FS Journal - Risk Compliance and Security.pdf` (872 KB)

### Modern Technology, Data & AI
The evolution from traditional IT architecture toward cloud, data, and AI-enabled systems.

- `Barbero - 2020 - Technology Modernization and Cloud Migration.pdf` (1.4 MB)
- `Barbero | Hunt - 2021 - Data Strategy.pdf` (2.3 MB)
- `Barbero - 2026 - Agentic AI in Financial Services.pdf` (97 KB)

---

## Suggested Demo Questions

These are the questions AIStudio's demo benchmark runs against the corpus — all 14 are
validated to retrieve and answer cleanly from the nine documents. Run `ais_bench` to
execute them; the machine-readable set lives in `benchmarks/demo/demo_questions.yaml`.

**Architecture Methodology**
- What is QFD and how does it apply to technology architecture?
- How do you design an IT organization around architectural principles?
- How do architecture concepts help design organizations?

**IT Strategy & Leadership**
- How should a CTO prioritize a three-year technology strategy?
- What does a good technology target state look like?
- How do you organize a large-scale IT transformation program?
- What is the relationship between business strategy and technology strategy?

**Modern Technology**
- What are the key considerations for cloud migration and technology modernization?
- What are the key principles for modernizing legacy applications?

**Financial Services**
- How do Sarbanes-Oxley and Basel II requirements shape IT governance and security architecture in financial services firms?
- How has digitization changed financial services technology?
- What is the role of architecture in managing technology risk in financial services?

**Agentic AI**
- What are the key opportunities and limitations of agentic AI in financial services?
- How should organizations embed AI into their knowledge productivity ecosystem?

## Corpus Statistics

| Metric | Value |
|---|---|
| Total documents | 9 |
| Date range | 2003 — 2026 |
| Formats | PDF |
| Domain | Financial services technology architecture |

---

## Ingesting the Demo Corpus

You don't need to. The demo corpus ships pre-ingested and indexes itself on the first `ais_start` — select **demo** from the corpus dropdown and start querying. (To rebuild it from scratch, delete it in the UI and re-add the files via **Upload**.)
