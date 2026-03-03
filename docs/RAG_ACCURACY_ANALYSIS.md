# RAG System Analysis - Accuracy Issues

## 📊 System Overview

Your RAG system is a hybrid retrieval system combining:
1. **Chroma vector store** (semantic/embedding search)
2. **JSONL lexical search** (keyword matching)
3. **Ollama LLM** for answer generation

## 🔍 Identified Issues Affecting Accuracy

### 1. **CRITICAL: Chunking Strategy Too Simple**

**Location**: `src/local_llm_bot/app/ingest/chunking.py`

**Problem**:
```python
def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> list[str]:
    # Simple character-based splitting - NO SEMANTIC AWARENESS
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunk = text[start:end].strip()  # ❌ Cuts mid-sentence, mid-paragraph
```

**Impact on Resume Corpus**:
- A resume section like "Led team of 50 engineers at Google developing..." 
  might be cut at character 1200, splitting across "Google" and "developing"
- Context is fragmented: "Manuel Barbero" might be in chunk 1, his role in chunk 2
- Related skills/achievements are separated

**Why This Hurts Accuracy**:
- LLM receives incomplete context
- "What do you know about Manuel Barbero" retrieves chunks that may have his name 
  but not his actual accomplishments
- Character 1200 is arbitrary - doesn't respect document structure

### 2. **Lexical Tokenization Is Too Naive**

**Location**: `src/local_llm_bot/app/rag_core.py:35-36`

```python
def _tokenize(s: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", s.lower()) if len(t) >= 3}
```

**Problems**:
- Only matches tokens >= 3 chars (misses "AI", "VP", "CTO", "ML", "UI", "UX")
- No stemming: "engineer" won't match "engineering", "engineered"
- No synonyms: "managed" won't match "led", "directed", "supervised"
- Case-insensitive but loses emphasis: "Manuel BARBERO" treated same as "manuel barbero"

**For Resume Query**:
```
Query: "What do you know about Manuel Barbero"
Tokens: {'what', 'know', 'about', 'manuel', 'barbero'}

Resume text: "M. Barbero led engineering at..."
Tokens: {'barbero', 'led', 'engineering', ...}
Only overlap: 'barbero' (1 token) ❌
```

### 3. **Query Decomposition Doesn't Help Resume Queries**

**Location**: `src/local_llm_bot/app/rag_core.py:39-82`

```python
def compose_queries(query: str, *, corpus: str) -> list[str]:
    # Tax-specific logic ✅
    if _is_tax_corpus(corpus):
        qs.extend(["adjusted gross income", "federal adjusted gross income", ...])
    
    # BUT: No resume-specific expansion ❌
    # Query "What do you know about Manuel Barbero" doesn't expand to:
    # - "Manuel Barbero experience"
    # - "Manuel Barbero education"
    # - "Manuel Barbero skills"
    # - "Manuel Barbero achievements"
```

### 4. **Hybrid Ranking Is Generic**

**Location**: `src/local_llm_bot/app/rag_core.py:123-141`

```python
def _combined_rank(query: str, d: RetrievedDoc) -> float:
    q_tokens = _tokenize(query)
    text = d.content.lower()
    overlap = sum(1 for t in q_tokens if t in text)
    
    if d.score <= 10.0:
        return (d.score * 10.0) - (overlap * 1.5)  # ❌ Magic numbers
```

**Issues**:
- Magic numbers (10.0, 1.5) not tuned for resumes
- No boost for important resume sections (Summary, Experience, Skills)
- No penalty for less relevant sections (References, Address)
- Tax-specific reranking exists, but no resume reranking

### 5. **Top-K=100 Overwhelms Context**

**Your Query**:
```bash
"top_k": 100
```

**Problem**:
- Retrieves 100 chunks
- At 1200 chars/chunk = 120,000 characters = ~30,000 tokens
- Most LLMs have context limits around 8K-128K tokens
- BUT: More context ≠ better answers
- "Needle in haystack" problem: LLM must find relevant info in 100 chunks

**Better Strategy**: Retrieve top 10-20 high-quality chunks

### 6. **System Prompt Too Strict for Open Questions**

**Location**: `src/local_llm_bot/app/rag_core.py:258-272`

```python
system = (
    "You are a precise extraction assistant.\n"
    "Use ONLY the provided context.\n"
    "If the answer is not explicitly present, answer exactly: 
     \"I don't know based on the provided documents.\" \n"
)
```

**Issue for Resume Queries**:
- "What do you know about Manuel Barbero" is OPEN-ENDED
- System prompt optimized for EXTRACTION (specific facts)
- Should synthesize/summarize for biographical queries
- Too strict = truncated answers even with good context

### 7. **No Document-Level Metadata**

**Missing**:
- Document type (resume, cover letter, bio)
- Document recency (2025 resume vs 2020 resume)
- Section headers (Summary, Experience, Education)
- Importance scores (Executive Summary > References)

**Impact**: Can't prefer:
- Latest resume over old versions
- Summary sections over boilerplate
- Full resumes over cover letters

### 8. **Embedding Model May Not Be Resume-Optimized**

**Current**: `nomic-embed-text`

**Consideration**:
- General-purpose embeddings
- May not capture resume-specific semantics:
  - "Led 50-person team" vs "Managed large organization"
  - "Increased revenue 300%" vs "Drove significant growth"
  - Technical skills vs soft skills clustering

## 🎯 Recommended Fixes (Priority Order)

### Priority 1: Better Chunking (CRITICAL)

**Replace character-based chunking with semantic chunking**:

```python
def chunk_document_semantic(doc: Document, chunk_size: int = 1200) -> list[Chunk]:
    """
    Smart chunking that respects:
    - Section boundaries (Experience, Education, Skills)
    - Paragraph boundaries
    - Bullet points
    - Sentence boundaries
    """
    # Detect sections
    sections = detect_resume_sections(doc.text)
    
    chunks = []
    for section in sections:
        # Chunk within section, respecting paragraphs
        section_chunks = chunk_by_paragraphs(
            section.text, 
            max_size=chunk_size,
            section_title=section.title  # Include in metadata
        )
        chunks.extend(section_chunks)
    
    return chunks
```

### Priority 2: Resume-Specific Query Expansion

```python
def compose_queries(query: str, *, corpus: str) -> list[str]:
    qs = [query.strip()]
    
    if _is_resume_corpus(corpus):
        # Detect person name in query
        person = extract_person_name(query)
        if person:
            qs.extend([
                f"{person} professional experience",
                f"{person} education background",
                f"{person} technical skills",
                f"{person} career achievements",
                f"{person} leadership roles"
            ])
    
    return qs
```

### Priority 3: Better Tokenization

```python
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

def _tokenize_smart(s: str) -> set[str]:
    stemmer = PorterStemmer()
    tokens = re.findall(r'\b[a-z0-9]+\b', s.lower())
    
    # Keep important 2-letter acronyms
    important_short = {'ai', 'ml', 'vp', 'ceo', 'cto', 'ui', 'ux', 'qa'}
    
    result = set()
    for t in tokens:
        if len(t) >= 3 or t in important_short:
            result.add(stemmer.stem(t))  # Stem for better matching
    
    return result
```

### Priority 4: Resume-Specific Reranking

```python
def _resume_rerank(query: str, docs: list[RetrievedDoc]) -> list[RetrievedDoc]:
    """Boost resume-relevant content"""
    
    important_sections = [
        'executive summary', 'professional summary',
        'experience', 'achievements', 'education',
        'skills', 'technical expertise'
    ]
    
    def score(d: RetrievedDoc) -> float:
        text = d.content.lower()
        s = 0.0
        
        # Boost important sections
        for section in important_sections:
            if section in text:
                s += 5.0
        
        # Boost recent dates (2024, 2025)
        if any(year in text for year in ['2024', '2025', '2023']):
            s += 2.0
        
        # Boost achievement indicators
        achievement_words = ['led', 'managed', 'built', 'increased', 'delivered', 'achieved']
        s += sum(2.0 for word in achievement_words if word in text)
        
        # Boost numeric results (revenue, team size, percentages)
        if re.search(r'\d+%|\$\d+|team of \d+', text):
            s += 3.0
        
        return s
    
    return sorted(docs, key=score, reverse=True)
```

### Priority 5: Optimize Top-K

```python
# For biographical queries, use fewer, higher-quality chunks
if query_is_biographical(query):
    top_k = min(20, top_k)  # Cap at 20 for open-ended questions
```

### Priority 6: Better System Prompt for Resumes

```python
def generate_answer(*, query: str, docs: list[RetrievedDoc], query_type: str = "extraction") -> str:
    if query_type == "biographical":
        system = (
            "You are a professional resume analyst.\n"
            "Synthesize information from the provided resume excerpts.\n"
            "Create a comprehensive profile highlighting:\n"
            "- Professional background and experience\n"
            "- Key achievements and impact\n"
            "- Technical skills and expertise\n"
            "- Educational background\n"
            "Organize the response logically and cite specific accomplishments."
        )
    else:
        system = "You are a precise extraction assistant..."
    
    # Rest of generation logic
```

## 🧪 Testing Recommendations

### Test 1: Chunk Quality
```bash
python -m local_llm_bot.app.cli.corpus_stats --corpus mb_resumes --inspect-chunks

# Check:
# - Are chunks split mid-sentence?
# - Are related facts in same chunk?
# - Do chunks have clear context?
```

### Test 2: Retrieval Precision
```bash
# Test with lower top_k
curl -X POST http://localhost:8000/ask \
  -d '{"query": "What do you know about Manuel Barbero", "corpus": "mb_resumes", "top_k": 10}'

# Compare results with top_k: 10, 20, 50, 100
```

### Test 3: Debug Retrieval
```bash
curl -X POST http://localhost:8000/debug/retrieve \
  -d '{"query": "Manuel Barbero experience", "corpus": "mb_resumes", "top_k": 10}'

# Inspect:
# - Are retrieved chunks relevant?
# - What are the similarity scores?
# - Are name matches in chunks?
```

## 📈 Expected Improvements

After implementing these fixes:

**Before**: 
- Query: "What do you know about Manuel Barbero"
- Result: Generic fragments, missing context

**After**:
- Semantic chunks with full context
- Query expansion finds relevant sections
- Resume-specific ranking prioritizes summary/achievements
- Synthesized, comprehensive answer

**Accuracy gain**: 40-60% improvement expected

## 🛠️ Implementation Order

1. **Day 1**: Implement semantic chunking (biggest impact)
2. **Day 2**: Add resume query expansion
3. **Day 3**: Implement resume reranking
4. **Day 4**: Optimize top_k and system prompts
5. **Day 5**: Test and iterate

## 📝 Quick Win: Test Current System Better

**Try this query format instead**:
```bash
curl -X POST http://localhost:8000/ask \
  -d '{
    "query": "Summarize Manuel Barbero professional experience, education, and key achievements",
    "corpus": "mb_resumes",
    "top_k": 15
  }'
```

More specific query + lower top_k = better results with current system.
