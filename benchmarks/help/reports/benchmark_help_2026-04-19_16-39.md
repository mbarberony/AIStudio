# AIStudio — Benchmark Findings
*Generated: 2026-04-19 16:41*

## Configuration
- **Corpus:** `help`
- **Top K:** 5
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 8
- **Passed:** 2/8 (25%)
- **Avg latency:** 9.6s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `help` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | Goldman Sachs AI risk — firm filter | 14.86s | ✅ | HOWTO.pdf, QUICKSTART.pdf, README.pdf | Should return Goldman-specific AI risk disclosure |
| 2 | JPMorgan cybersecurity risk — firm filter | 5.1s | ❌ | — | Should return JPMorgan cybersecurity section |
| 3 | Morgan Stanley model risk — firm filter | 12.15s | ❌ | DEMO_CORPUS.pdf, README.pdf, HARNESS.pdf | Should return model risk governance section |
| 4 | Goldman AI governance committee — firm filter | 8.39s | ❌ | HOWTO.pdf | Should mention Firmwide Artificial Intelligence Risk and Controls Committee |
| 5 | Cross-corpus AI governance — no filter | 7.88s | ❌ | README.pdf | No firm filter — tests cross-corpus retrieval quality |
| 6 | Bank of America climate risk — firm filter | 11.83s | ✅ | DEMO_CORPUS.pdf, README.pdf, HOWTO.pdf,  | Should return climate risk section |
| 7 | Goldman 2025 revenue — firm + year filter | 5.43s | ❌ | QUICKSTART.pdf, QA_TESTING_LESSONS_LEARN | Tests year filter combined with firm filter |
| 8 | Simple factual — latency baseline | 11.55s | ❌ | QUICKSTART.pdf, README.pdf | Simple query for latency baseline measurement |

## Detailed Results

### goldman_ai_risk
**Query:** What does Goldman Sachs say about the risks of artificial intelligence?
**Firm filter:** `Goldman Sachs` | **Year filter:** `none`
**Latency:** 14.86s | **Pass:** ✅

**Answer:**

> There is no information provided by the sources about Goldman Sachs' views on the risks of artificial intelligence. The relevant sources are [1] and [2], but they do not mention Goldman Sachs or its opinions on AI risks.
>
> However, [3] provides a document titled "Agentic AI in Financial Services: Some Reflections" which explores the transition from descriptive to generative to agentic AI, and discusses the practical constraints on autonomous systems today. This text is related to the context of financial services and AI, but it does not explicitly mention Goldman Sachs or its views on AI risks.
>
> Therefore, I can only conclude that there is no information provided by the sources about Goldman Sachs' views on the risks of artificial intelligence.

**Citations:**

- [1] HOWTO.pdf p.1
- [2] QUICKSTART.pdf p.7
- [3] README.pdf p.2


### jpmorgan_cybersecurity
**Query:** How does JPMorgan Chase describe their cybersecurity risk management?
**Firm filter:** `JPMorgan Chase` | **Year filter:** `none`
**Latency:** 5.1s | **Pass:** ❌

**Answer:**

> The sources do not address how JPMorgan Chase describes their cybersecurity risk management.

**⚠ Model said 'no information' — possible retrieval miss**

### morgan_stanley_model_risk
**Query:** What is Morgan Stanley's approach to model risk?
**Firm filter:** `Morgan Stanley` | **Year filter:** `none`
**Latency:** 12.15s | **Pass:** ❌

**Answer:**

> The source [2] README.pdf and [3] HARNESS.pdf provide information about AIStudio's capabilities, but neither of them mentions Morgan Stanley's approach to model risk. The DEMO_CORPUS.pdf document also doesn't address this topic.
>
> However, the source [1] DEMO_CORPUS.pdf mentions a "Financial Services" section (Page 2 of 4), which includes a question about key risk and compliance considerations for financial services IT. But it does not provide information on Morgan Stanley's approach to model risk specifically.
>
> The RiskCompliance and Security - 2005.pdf source [3] is the most relevant one, as it deals with security and risk management in finance. However, upon reviewing its content, I did not find any specific mention of Morgan Stanley or their approach to model risk.
>
> Unfortunately, there is no information available about Morgan Stanley's approach to model risk from the provided sources.

**Citations:**

- [1] DEMO_CORPUS.pdf p.3
- [2] README.pdf p.3
- [3] HARNESS.pdf p.4

**⚠ Model said 'no information' — possible retrieval miss**

### goldman_ai_committee
**Query:** Does Goldman Sachs have an AI governance committee and what does it do?
**Firm filter:** `Goldman Sachs` | **Year filter:** `none`
**Latency:** 8.39s | **Pass:** ❌

**Answer:**

> There is no mention of an "AI governance committee" or any similar structure in the provided sources.
>
> However, [4] mentions a general topic related to AI and compliance: "Financial Services - What are the key risk and compliance considerations for financial services IT?" But it does not address the existence of a specific governance committee.

**Citations:**

- [4] HOWTO.pdf p.1

**Missing keywords:** ['Artificial Intelligence']

### cross_corpus_ai_governance
**Query:** Which financial firms have dedicated AI governance committees?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.88s | **Pass:** ❌

**Answer:**

> This question is not addressed in the provided sources. The sources do not address which financial firms have dedicated AI governance committees.
>
> However, [2] mentions that AIStudio ships with a curated set of 11 documents spanning 20 years of work in financial services technology, including strategy and architecture documents from a major wealth management firm (WMA) produced in 2010.

**Citations:**

- [2] README.pdf p.2

**⚠ Model said 'no information' — possible retrieval miss**

### bofa_climate_risk
**Query:** How does Bank of America describe climate risk in their annual report?
**Firm filter:** `Bank of America` | **Year filter:** `none`
**Latency:** 11.83s | **Pass:** ✅

**Answer:**

> The source document that describes Bank of America's annual report is not among the provided sources. The topic "Financial Services" is mentioned in [2] as a corpus, but it does not describe climate risk in Bank of America's annual report.
>
> However, I can suggest searching for information on "SEC 10-K corpus" in [1] or [2], since they mention corporate filings from financial services firms.
>
> After re-reading the provided documents again: 
> [3] and [4] do not contain any relevant information about Bank of America's annual report.
>
> [1] does not describe Bank of America's climate risk, but it mentions "SEC 10-K corpus" which has a description in [2].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] DEMO_CORPUS.pdf p.3
- [2] README.pdf p.3
- [3] HOWTO.pdf p.7
- [4] CODEBASE_GUIDE.pdf p.1


### goldman_2026_revenue
**Query:** What were Goldman Sachs total revenues in 2025?
**Firm filter:** `Goldman Sachs` | **Year filter:** `2026`
**Latency:** 5.43s | **Pass:** ❌

**Answer:**

> There is no information available about Goldman Sachs' total revenues in 2025 in any of the provided sources [1] through [4]. The sources do not address this question.

**Citations:**

- [1] QUICKSTART.pdf p.7
- [4] QA_TESTING_LESSONS_LEARNED.pdf p.1

**Missing keywords:** ['billion']
**⚠ Model said 'no information' — possible retrieval miss**

### latency_test
**Query:** What is Goldman Sachs?
**Firm filter:** `Goldman Sachs` | **Year filter:** `none`
**Latency:** 11.55s | **Pass:** ❌

**Answer:**

> Goldman Sachs is mentioned as one of the firms whose documents are included in the SEC 10-K corpus, which is a large corpus used to demonstrate how AIStudio can operate at scale. [3] Specifically, it states that this corpus explores 143 annual filings from 25 financial services firms, including Goldman Sachs, JPMorgan Chase, Morgan Stanley, and others. Additionally, when filtering or querying the corpus, one can type "Goldman Sachs" in the Firm filter field to restrict retrieval to documents only from that firm. [1]

**Citations:**

- [1] QUICKSTART.pdf p.7
- [3] README.pdf p.3

**Missing keywords:** ['bank']
