# Demo Corpus

> A curated collection of architecture and strategy documents spanning  
> 20+ years of work in financial services technology — from 2003 to 2021.

This corpus ships with AIStudio as a ready-to-query demonstration dataset.
It lets you experience the system immediately after install, without needing
to supply your own documents first.

It also serves as a substantive test of retrieval quality — these are real,
dense documents on complex topics, not toy data.

---

## What's Here

### IT Strategy & Architecture
Long-form strategy documents covering IT target state design, CTO planning,
and the "Air Traffic Controller" model for making things happen in large
technology organizations. Originally produced for a major wealth management
firm (2010).

- `01 - WMA IT Target State Strategy and Architecture - 2010.pdf` (30pp)
- `02 - WMA CTO Activity Plan.pdf` (18pp)
- `03 - WMA IT Strategy and Architecture - Making Things Happen - The Air Traffic Controller Model.pdf` (15pp)
- `WMA - IT Target State Post Trade ES-20100922.ppt`

### Architecture Methodology
Foundational thinking on enterprise architecture — how to use architecture
concepts to design organizations, how Quality Function Deployment (QFD)
applies to technology architecture, and how to structure an IT organization
around architectural principles.

- `Architecture Concepts and How To Use Them To Design an Organizations.pdf` (48pp)
- `Architecture and QFD.pdf` (9pp)
- `BOEI - Architecture and QFD - 2003.pdf` (9pp)
- `Architecting the IT Organization.pdf` (32pp)

### AI & Modern Technology
A reference architecture for enterprise AI systems, a technology
modernization and cloud migration framework, and a data strategy document.
These reflect the evolution from traditional IT architecture toward
AI-enabled systems.

- `AI-Reference-Architecture.pptx`
- `Barbero - 2020 - Technology Modernization and Cloud Migration - 2020-02-11.pdf` (17pp) *(sanitized)*
- `Data Strategy - 2021-01-08a.pdf` (15pp)

### DevOps & Organizational Design
A DevOps and IT operations review covering organizational roadmap design
for a mid-size financial services firm (2018).

- `CMK DevOps and IT Operations Review and Org Design - Org Roadmap - 2018-02-27a.pptx`

### GTIS Three Year Strategy
A full three-year technology strategy document with speaker notes, covering
infrastructure modernization, platform strategy, and organizational
transformation at scale.

- `GTIS STRATEGY - MAIN - Three Year Strategy - Final (with speaker notes).ppt`

### Financial Services Journal Series
Four volumes of an edited journal covering technology strategy and
architecture in financial services — each 36-61 pages. Topics span
strategy and architecture concepts, digitization, IT infrastructure,
and risk/compliance and security. Edited by Manuel Barbero (2005-2006).

- `FS Journal, Edited by M-1. Barbero - Strategy and Architecture Concepts and Techniques - 2006.pdf` (61pp)
- `FS Journal, Edited by M. Barbero - Digitization.pdf` (36pp)
- `FS Journal, Edited by M. Barbero - IT Infrastructure.pdf` (52pp)
- `FS Journal, Edited by M. Barbero - RiskCompliance and Security - 2005.pdf` (60pp)

---

## Suggested Demo Questions

These questions are designed to showcase both retrieval quality and the
depth of the corpus. They work well for demonstrating AIStudio to
technical reviewers or potential users.

The complete machine-readable question set lives in `benchmarks/demo_questions.yaml`
(12 questions across 4 topics, all validated against the corpus). Run `ais_bench`
to execute them as a benchmark.

**Mac Air OBE-validated questions** (strongest answers, both llama3.1:8b and mistral:7b):
1. "Explain the concept of plateau and its use in the context of planning"
2. "Why should you not spend too much time on intermediary plateaus?"
3. "How should a CTO prioritize a three-year technology strategy?"
4. "What are the key principles for modernizing legacy applications?"

See `docs/QA_TESTING_LESSONS_LEARNED.md` for the full clean install validation report.

**Strategy & Leadership**
- What is the Air Traffic Controller model and how does it apply to IT strategy?
- How should a CTO prioritize a three-year technology strategy?
- What are the key principles of IT target state architecture?

**Architecture Methodology**
- What is QFD and how does it apply to technology architecture?
- How do you design an IT organization around architecture principles?
- What are the core concepts of enterprise architecture?

**Modern Technology**
- What does a reference architecture for enterprise AI look like?
- What are the key considerations for cloud migration and technology modernization?
- What is the role of data strategy in digital transformation?
- How does DevOps change IT operations and organizational design?

**Financial Services**
- What are the key risk and compliance considerations for financial services IT?
- How has digitization changed financial services technology?
- What are the infrastructure considerations specific to financial services?

---

## Corpus Statistics

| Metric | Value |
|---|---|
| Total documents | 17 |
| Total pages (PDF/PPT) | ~530pp |
| Date range | 2003 — 2021 |
| Formats | PDF, PPTX, PPT |
| Domain | Financial services technology architecture |

---

## Ingesting the Demo Corpus

From the repo root with your virtual environment active:

```bash
PYTHONPATH=src python -m local_llm_bot.app.ingest \
  --corpus demo \
  --root data/demo
```

This indexes all documents in `data/demo/` into a corpus named `demo`.
Select it from the corpus dropdown in the UI and start querying.

Re-run this command any time new documents are added to `data/demo/`.
