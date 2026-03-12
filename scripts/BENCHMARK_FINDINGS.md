# AIStudio — Benchmark Findings
*Generated: 2026-03-12 14:38*

## Configuration
- **Corpus:** `sec_10k`
- **Top K:** 10
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 8
- **Passed:** 6/8 (75%)
- **Avg latency:** 6.5s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Corpus: 143 financial services 10-K filings, 105,964 chunks
- Ingest throughput: ~54 chunks/sec on M4
- Total ingest time: ~34 minutes for 143 files
- ChromaDB comparison: crashed at 32,285 chunks; Qdrant stable at 105,964

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | Goldman Sachs AI risk — firm filter | 7.17s | ✅ | Goldman_Sachs_10K_2026-02-25.htm | Should return Goldman-specific AI risk disclosure |
| 2 | JPMorgan cybersecurity risk — firm filter | 9.8s | ✅ | JPMorgan_Chase_10K_2026-02-13.htm | Should return JPMorgan cybersecurity section |
| 3 | Morgan Stanley model risk — firm filter | 5.85s | ✅ | Morgan_Stanley_10K_2026-02-19.htm | Should return model risk governance section |
| 4 | Goldman AI governance committee — firm filter | 4.25s | ❌ | — | Should mention Firmwide Artificial Intelligence Risk and Controls Committee |
| 5 | Cross-corpus AI governance — no filter | 6.2s | ✅ | AIG_10K_2022-02-17.htm, Goldman_Sachs_10 | No firm filter — tests cross-corpus retrieval quality |
| 6 | Bank of America climate risk — firm filter | 6.47s | ✅ | Bank_of_America_10K_2026-02-25.htm | Should return climate risk section |
| 7 | Goldman 2025 revenue — firm + year filter | 6.9s | ✅ | Goldman_Sachs_10K_2026-02-25.htm | Tests year filter combined with firm filter |
| 8 | Simple factual — latency baseline | 5.21s | ❌ | — | Simple query for latency baseline measurement |

## Detailed Results

### goldman_ai_risk
**Query:** What does Goldman Sachs say about the risks of artificial intelligence?
**Firm filter:** `Goldman Sachs` | **Year filter:** `none`
**Latency:** 7.17s | **Pass:** ✅

**Answer:**
> According to the provided sources, Goldman Sachs mentions the following risks associated with artificial intelligence (AI):

1. "New AI technologies may increase the frequency and severity of cybersecurity attacks." [1]
2. "Generative AI, if used to perpetrate fraud or launch cyber attacks, could result in losses, liquidity outflows or other adverse effects for us and our clients." [1]
3. The use of AI technologies may heighten the risk of fraud and misappropriation of funds, as well as facilita...


### jpmorgan_cybersecurity
**Query:** How does JPMorgan Chase describe their cybersecurity risk management?
**Firm filter:** `JPMorgan Chase` | **Year filter:** `none`
**Latency:** 9.8s | **Pass:** ✅

**Answer:**
> According to JPMorgan Chase's 2025 Form 10-K, the company describes their cybersecurity risk management as follows:

The Firm's Information Security Program is designed to prevent, detect and respond to cyber attacks in order to help safeguard the confidentiality, integrity and availability of the Firm's infrastructure, resources and information. The program includes managing the Firm's global cybersecurity operations centers, providing training, conducting cybersecurity event simulation exercis...


### morgan_stanley_model_risk
**Query:** What is Morgan Stanley's approach to model risk?
**Firm filter:** `Morgan Stanley` | **Year filter:** `none`
**Latency:** 5.85s | **Pass:** ✅

**Answer:**
> Morgan Stanley's approach to model risk is outlined in the Model Risk Management Department's ("MRM") responsibilities. According to the text, the MRM is a distinct department in Risk Management responsible for the oversight of model risk. The MRM establishes a model risk tolerance in line with the firm's risk appetite, based on an assessment of the materiality of the risk of financial loss or reputational damage due to errors in design, implementation, and/or inappropriate use of models.

The M...


### goldman_ai_committee
**Query:** Does Goldman Sachs have an AI governance committee and what does it do?
**Firm filter:** `Goldman Sachs` | **Year filter:** `none`
**Latency:** 4.25s | **Pass:** ❌

**Answer:**
> Goldman Sachs has a Firmwide Artificial Intelligence Risk and Controls Committee, which is responsible for overseeing risks associated with the use of AI. This committee reports to the Firmwide Technology Risk Committee, which oversees cybersecurity matters, as well as technology risk management frameworks and methodologies, and monitors their effectiveness.

So, to answer your question, yes, Goldman Sachs has an AI governance committee, and it is the Firmwide Artificial Intelligence Risk and Co...


### cross_corpus_ai_governance
**Query:** Which financial firms have dedicated AI governance committees?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.2s | **Pass:** ✅

**Answer:**
> Based on the provided sources, the following financial firms have dedicated AI governance committees:

 None, as none of the provided sources mention AI governance committees. However, the following firms have dedicated enterprise risk management or risk governance committees that oversee various types of risk, including financial and non-financial risks:

1. AIG: The Group Risk Committee (GRC) and the Enterprise Risk Management Committee (ERMC) are mentioned in sources [1], [2], [4], and [6]. 
...


### bofa_climate_risk
**Query:** How does Bank of America describe climate risk in their annual report?
**Firm filter:** `Bank of America` | **Year filter:** `none`
**Latency:** 6.47s | **Pass:** ✅

**Answer:**
> According to Bank of America's annual report, climate risk is described as a transverse risk that includes physical risk and transition risk. Physical risks related to severe weather events can increase credit risk, while transition risks related to transitioning to a low-carbon economy can amplify credit risks through the financial impacts of changes in policy, technology, or the market on counterparties [1].

The report also states that climate-related matters present short-, medium-, and long...


### goldman_2026_revenue
**Query:** What were Goldman Sachs total revenues in 2025?
**Firm filter:** `Goldman Sachs` | **Year filter:** `2026`
**Latency:** 6.9s | **Pass:** ✅

**Answer:**
> According to the provided sources, the total revenues of Goldman Sachs in 2025 were $58.28 billion, which is 9% higher than 2024. 

[1] does not directly mention the total revenues, but mentions that "Net revenues in the consolidated statements of earnings were $58.28 billion for 2025, 9% higher than 2024" in the section "Segment Assets and Operating Results — Consolidated Results of Operations — Net Revenues".

However, we can break down the total revenues into its components:

Net revenues in ...


### latency_test
**Query:** What is Goldman Sachs?
**Firm filter:** `Goldman Sachs` | **Year filter:** `none`
**Latency:** 5.21s | **Pass:** ❌

**Answer:**
> Goldman Sachs is a leading global financial institution that delivers a broad range of financial services to a large and diversified client base that includes corporations, financial institutions, governments, and individuals.

**Missing keywords:** ['bank']

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