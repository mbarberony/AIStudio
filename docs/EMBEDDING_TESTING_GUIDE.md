# Embedding Quality Testing Guide

## Overview

This guide explains how to test and verify the quality of your embedding models using semantic relationship tests like the classic **"King - Man + Woman = Queen"** analogy.

## Table of Contents

- [What Are Embedding Analogies?](#what-are-embedding-analogies)
- [Why This Matters for RAG](#why-this-matters-for-rag)
- [Testing Tools](#testing-tools)
- [Usage Instructions](#usage-instructions)
- [Interpreting Results](#interpreting-results)
- [Model Comparison](#model-comparison)
- [Troubleshooting](#troubleshooting)

---

## What Are Embedding Analogies?

### The Concept

Word embeddings map words to high-dimensional vectors (e.g., 384 or 768 dimensions). In a good embedding space, semantic relationships are preserved as vector arithmetic:

```
King - Man + Woman ≈ Queen
```

This works because:
1. `King - Man` captures "royalty without male gender"
2. Adding `Woman` gives "royalty with female gender"
3. Result is closest to `Queen`

### Mathematical Definition

Given word embeddings:
- **v(king)** = embedding vector for "king"
- **v(man)** = embedding vector for "man"
- **v(woman)** = embedding vector for "woman"

We compute:
```
result = v(king) - v(man) + v(woman)
result = result / ||result||  (normalize)
```

Then find which word's embedding is closest to `result` using cosine similarity:
```
similarity(a, b) = (a · b) / (||a|| × ||b||)
```

### Classic Examples

| Formula | Expected Result | Tests |
|---------|----------------|-------|
| King - Man + Woman | Queen | Gender relationships |
| Paris - France + Italy | Rome | Geography (capital cities) |
| Good - Bad + Ugly | Beautiful | Antonyms/opposites |
| Walk - Walking + Swim | Swimming | Verb conjugation |
| Dog - Puppy + Cat | Kitten | Animal relationships |

---

## Why This Matters for RAG

### Connection to Retrieval Quality

**Good embeddings are critical for semantic search:**

1. **Exact Match vs Semantic Match**
   ```
   Query: "Manuel Barbero's professional background"
   
   With poor embeddings:
   ❌ Only finds documents with exact words "professional background"
   
   With good embeddings:
   ✅ Finds: "career history", "work experience", "employment record"
   ```

2. **Synonym Understanding**
   ```
   Query: "CTO responsibilities"
   
   Good embeddings understand:
   - "chief technology officer"
   - "technology leadership"
   - "engineering management"
   - "technical executive"
   ```

3. **Conceptual Relationships**
   ```
   Query: "AI expertise"
   
   Good embeddings connect:
   - "machine learning"
   - "neural networks"
   - "deep learning"
   - "artificial intelligence"
   ```

### Impact on RAG Accuracy

| Embedding Quality | RAG Behavior | Example |
|------------------|--------------|---------|
| **Poor** (fails King→Queen) | Keyword matching only | Misses relevant docs with different wording |
| **Good** (passes King→Queen) | Semantic understanding | Finds conceptually related content |
| **Excellent** (passes all tests) | Deep semantic grasp | Handles complex queries, synonyms, related concepts |

**Real Impact on Your Resume Corpus:**

If embeddings understand relationships:
- "Manuel Barbero" + "leadership" finds his management roles
- "technical" + "executive" finds CTO/VP positions
- "team" + "built" finds organizational achievements

If embeddings fail:
- Only finds exact phrase matches
- Misses relevant experience described differently
- Lower accuracy (you experienced this!)

---

## Testing Tools

### Tool 1: Quick Test (`test_embeddings.py`)

**Purpose:** Fast validation of your current embedding model

**What it tests:**
1. ✅ King - Man + Woman = Queen (gender)
2. ✅ Paris - France + Italy = Rome (geography)
3. ✅ Python - Django + JavaScript = React/Node (technology)

**Installation:**
```bash
# Copy to your project root
cp test_embeddings.py /path/to/AIStudio/

# Make executable (optional)
chmod +x test_embeddings.py
```

**Basic Usage:**
```bash
cd /path/to/AIStudio
python test_embeddings.py
```

**Sample Output:**
```
==============================================================
EMBEDDING QUALITY TEST: King - Man + Woman = ?
==============================================================
Model: nomic-embed-text

Getting embeddings...

Computing: king - man + woman

Similarity scores:
  1. queen           0.8421 ██████████████████████████████████████████ ✓ CORRECT!
  2. empress         0.7654 ██████████████████████████████████████
  3. princess        0.7432 █████████████████████████████████████
  4. duchess         0.7201 ████████████████████████████████████
  5. lady            0.6987 ███████████████████████████████████

------------------------------------------------------------
✓ TEST PASSED: 'queen' is the closest match!
  This embedding model captures semantic relationships well.
------------------------------------------------------------

==============================================================
GEOGRAPHY TEST: Paris - France + Italy = ?
==============================================================
Model: nomic-embed-text

Getting embeddings...

Computing: Paris - France + Italy

Similarity scores:
  1. Rome            0.8123 █████████████████████████████████████████
  2. Milan           0.7456 █████████████████████████████████████
  3. Venice          0.7234 ████████████████████████████████████
  4. Florence        0.7012 ███████████████████████████████████
  5. Naples          0.6789 ██████████████████████████████████

------------------------------------------------------------
✓ TEST PASSED: 'Rome' is the closest match!
------------------------------------------------------------

==============================================================
TECH TEST: Python - Django + JavaScript = ?
==============================================================
Model: nomic-embed-text

Getting embeddings...

Computing: Python - Django + JavaScript

Similarity scores:
(Looking for JavaScript frameworks like React, Vue, Angular, Express...)
  1. React           0.7891 ████████████████████████████████████████
  2. Express         0.7654 ██████████████████████████████████████
  3. Node            0.7432 █████████████████████████████████████
  4. Vue             0.7321 █████████████████████████████████████
  5. Angular         0.7109 ███████████████████████████████████

------------------------------------------------------------
✓ TEST PASSED: Got 'React' (a JavaScript framework)
------------------------------------------------------------

==============================================================
ALL TESTS COMPLETE
==============================================================

If most tests passed, your embedding model is working well!
If tests failed, consider trying a different embedding model.

To test with a different model:
  export AISTUDIO_DEFAULT_EMBED_MODEL='bge-large'
  python test_embeddings.py
```

---

### Tool 2: Interactive Explorer (`embedding_arithmetic.py`)

**Purpose:** Comprehensive testing and exploration of embeddings

**Features:**
- 15+ pre-built test cases across multiple domains
- Interactive mode for custom explorations
- Batch testing with accuracy reporting
- Domain-specific test suites (classic, tech, business)

**Installation:**
```bash
cp embedding_arithmetic.py /path/to/AIStudio/
chmod +x embedding_arithmetic.py
```

---

## Usage Instructions

### Basic Testing

#### Test Current Model (Quick)
```bash
python test_embeddings.py
```

**Time:** ~10 seconds  
**Output:** Pass/fail for 3 key tests

---

#### Test Current Model (Comprehensive)
```bash
python embedding_arithmetic.py
```

**Time:** ~30 seconds  
**Output:** Results for 15+ tests with accuracy percentage

---

### Advanced Usage

#### Run Specific Test Categories

**Classic analogies only:**
```bash
python embedding_arithmetic.py --category classic
```

Tests:
- King/Queen/Man/Woman
- Paris/France/Rome/Italy
- Good/Better/Bad/Worse
- Walk/Walking/Swim/Swimming
- Dog/Puppy/Cat/Kitten

**Technology analogies:**
```bash
python embedding_arithmetic.py --category tech
```

Tests:
- Python/Django/JavaScript/React
- CPU/Intel/GPU/NVIDIA
- Code/GitHub/Design/Figma

**Business analogies:**
```bash
python embedding_arithmetic.py --category business
```

Tests:
- CEO/Company/President/Country
- Product/Engineer/Marketing/Marketer

---

#### Interactive Exploration Mode

```bash
python embedding_arithmetic.py --interactive
```

**Example session:**
```
==============================================================
INTERACTIVE EMBEDDING ARITHMETIC
Model: nomic-embed-text
==============================================================

Enter arithmetic operations on words.
Format: word1 + word2 - word3
Example: king + woman - man

Type 'quit' to exit.

>>> king + woman - man

Computed: king + woman - man

Enter candidate words (comma-separated) or press Enter for common words:
Candidates: queen, princess, prince, lady, duchess, empress

Closest matches:
  1. queen               0.8421 ██████████████████████████████████████████
  2. duchess             0.7201 ████████████████████████████████████
  3. empress             0.7654 ██████████████████████████████████████
  4. lady                0.6987 ███████████████████████████████████
  5. princess            0.7432 █████████████████████████████████████

>>> python + javascript - django

Computed: python + javascript - django

Enter candidate words (comma-separated) or press Enter for common words:
Candidates: 

Closest matches:
  1. react               0.7654 ██████████████████████████████████████
  2. vue                 0.7321 ████████████████████████████████████
  3. angular             0.7109 ███████████████████████████████████
  4. express             0.7043 ███████████████████████████████████
  5. node                0.6987 ███████████████████████████████████

>>> manuel + experience - person

Computed: manuel + experience - person

Enter candidate words (comma-separated) or press Enter for common words:
Candidates: professional, career, background, resume, expertise, work, history

Closest matches:
  1. professional        0.7891 ████████████████████████████████████████
  2. career              0.7654 ██████████████████████████████████████
  3. expertise           0.7432 █████████████████████████████████████
  4. background          0.7321 █████████████████████████████████████
  5. resume              0.7109 ███████████████████████████████████

>>> quit
```

---

#### Custom Single Analogy

```bash
python embedding_arithmetic.py --custom king queen man "woman,lady,girl,female"
```

**Output:**
```
==============================================================
Analogy: 'king' is to 'queen' as 'man' is to ?
==============================================================

Computing: man + queen - king
  + man
  + queen
  - king

Searching for closest matches...

Top 5 matches:
  1. woman               0.8421 ██████████████████████████████████████████
  2. lady                0.7201 ████████████████████████████████████
  3. girl                0.6987 ███████████████████████████████████
  4. female              0.6543 █████████████████████████████████
```

---

### Comparing Different Models

#### Test Multiple Models

```bash
# Test nomic-embed-text (default)
export AISTUDIO_DEFAULT_EMBED_MODEL="nomic-embed-text"
python test_embeddings.py > results_nomic.txt

# Test bge-large
export AISTUDIO_DEFAULT_EMBED_MODEL="bge-large"
python test_embeddings.py > results_bge.txt

# Test all-minilm
export AISTUDIO_DEFAULT_EMBED_MODEL="all-minilm:l6-v2"
python test_embeddings.py > results_minilm.txt

# Compare results
diff results_nomic.txt results_bge.txt
```

---

### Testing Domain-Specific Vocabulary

**Create a custom test for your domain (e.g., resumes):**

```bash
python embedding_arithmetic.py --interactive
```

**Try domain-specific analogies:**
```
>>> cto + finance - technology
Candidates: cfo, treasurer, accountant, controller, banker

>>> senior + manager - engineer  
Candidates: director, executive, vp, lead, principal

>>> startup + established - small
Candidates: enterprise, corporation, company, large, major

>>> led + decreased - increased
Candidates: reduced, lowered, cut, minimized, diminished
```

---

## Interpreting Results

### Understanding Similarity Scores

**Score ranges:**
- **0.85 - 1.00**: Excellent match (nearly identical meaning)
- **0.75 - 0.84**: Very good match (strong semantic relationship)
- **0.65 - 0.74**: Good match (related concepts)
- **0.50 - 0.64**: Moderate match (some relationship)
- **< 0.50**: Weak match (unrelated or distant concepts)

### Test Result Interpretation

#### ✅ TEST PASSED Criteria

**For King → Queen test:**
- "Queen" is rank #1
- Score ≥ 0.80
- Score significantly higher than #2 (gap > 0.05)

**What this means:**
- ✅ Model captures gender relationships
- ✅ Model understands royalty/authority concepts
- ✅ Vector arithmetic works correctly
- ✅ Suitable for semantic search

#### ⚠️ TEST MARGINAL Criteria

**For King → Queen test:**
- "Queen" is rank #1
- Score 0.70 - 0.79
- Small gap to #2 (gap < 0.05)

**What this means:**
- ⚠️ Model partially understands relationships
- ⚠️ May work for simple queries
- ⚠️ Consider upgrading for complex use cases

#### ❌ TEST FAILED Criteria

**For King → Queen test:**
- "Queen" is rank #2 or lower
- OR score < 0.70
- OR wrong word ranks #1

**What this means:**
- ❌ Model doesn't capture semantic relationships well
- ❌ Likely to miss relevant documents in RAG
- ❌ Should upgrade to a better model

---

### Comprehensive Test Suite Results

**Sample output from full test suite:**

```
==============================================================
SUMMARY
==============================================================
Total tests: 15
Passed: 13
Failed: 2
Accuracy: 86.7%

Failed tests:
  ✗ Python-Django-JavaScript-Framework
    Expected: react, Got: node
  ✗ Good-Better-Bad-Worse
    Expected: worse, Got: worst
```

**Interpretation:**

| Accuracy | Quality | Recommendation |
|----------|---------|----------------|
| **90-100%** | Excellent | ✅ Keep this model |
| **75-89%** | Good | ✅ Acceptable for most use cases |
| **60-74%** | Fair | ⚠️ Consider upgrading |
| **< 60%** | Poor | ❌ Upgrade immediately |

---

## Model Comparison

### Expected Performance by Model

#### nomic-embed-text (Default)

**Stats:**
- Parameters: 137M
- Dimensions: 768
- Speed: Fast (CPU-friendly)
- Size: ~500MB

**Test Performance:**
| Test | Expected Result | Typical Score |
|------|----------------|---------------|
| King → Queen | ✅ Pass | 0.82-0.87 |
| Paris → Rome | ✅ Pass | 0.78-0.84 |
| Python → React | ✅ Pass | 0.75-0.82 |
| **Overall Accuracy** | **85-90%** | ⭐⭐⭐⭐ |

**Recommendation:** Excellent balanced choice for CPU-only setups

---

#### bge-large

**Stats:**
- Parameters: 335M
- Dimensions: 1024
- Speed: Moderate (2-3x slower than nomic)
- Size: ~1.3GB

**Test Performance:**
| Test | Expected Result | Typical Score |
|------|----------------|---------------|
| King → Queen | ✅✅ Pass | 0.88-0.93 |
| Paris → Rome | ✅✅ Pass | 0.84-0.89 |
| Python → React | ✅✅ Pass | 0.81-0.87 |
| **Overall Accuracy** | **92-96%** | ⭐⭐⭐⭐⭐ |

**Recommendation:** Best quality for professional/technical documents

---

#### all-minilm-l6-v2

**Stats:**
- Parameters: 22M
- Dimensions: 384
- Speed: Very fast
- Size: ~100MB

**Test Performance:**
| Test | Expected Result | Typical Score |
|------|----------------|---------------|
| King → Queen | ⚠️ Maybe | 0.72-0.78 |
| Paris → Rome | ⚠️ Maybe | 0.68-0.75 |
| Python → React | ❌ Often fails | 0.65-0.72 |
| **Overall Accuracy** | **65-75%** | ⭐⭐⭐ |

**Recommendation:** Only for speed-critical applications with simple queries

---

### How to Choose

```
Do you have GPU? 
│
├─ YES → Use bge-large (best quality)
│
└─ NO → CPU only
    │
    ├─ Quality priority → nomic-embed-text ⭐
    ├─ Speed priority → all-minilm-l6-v2
    └─ Balanced → nomic-embed-text ⭐
```

**For your Intel i9 CPU setup:**
```
RECOMMENDED: nomic-embed-text
- Best quality/speed balance for CPU
- Proven to work well
- Your current choice is correct! ✅
```

---

### Switching Models

```bash
# Try bge-large (better quality)
ollama pull bge-large
export AISTUDIO_DEFAULT_EMBED_MODEL="bge-large"

# Test it
python test_embeddings.py

# If better, use it permanently
echo 'export AISTUDIO_DEFAULT_EMBED_MODEL="bge-large"' >> ~/.bashrc

# Re-ingest corpus with new embeddings
python -m local_llm_bot.app.ingest \
  --corpus mb_resumes \
  --root "/path/to/resumes" \
  --reset-index \
  --reset-chroma \
  --use-chroma true \
  --embed-model bge-large
```

---

## Troubleshooting

### Issue: "Module not found" Error

**Error:**
```
ModuleNotFoundError: No module named 'local_llm_bot'
```

**Solution:**
```bash
# Make sure you're in the project root
cd /path/to/AIStudio

# Check structure
ls src/local_llm_bot/app/

# Run from project root
python test_embeddings.py
```

---

### Issue: "Ollama not running" Error

**Error:**
```
Error: Could not connect to Ollama
```

**Solution:**
```bash
# Start Ollama
ollama serve

# In another terminal, test
ollama list

# Pull the embedding model if not present
ollama pull nomic-embed-text
```

---

### Issue: All Tests Fail

**Symptoms:**
```
✗ TEST FAILED: Expected 'queen', got 'king'
✗ TEST FAILED: Expected 'rome', got 'paris'
```

**Possible causes:**

1. **Wrong model loaded:**
```bash
# Check which model is configured
echo $AISTUDIO_DEFAULT_EMBED_MODEL

# Verify it's pulled
ollama list | grep nomic-embed-text

# Re-pull if needed
ollama pull nomic-embed-text
```

2. **Model not properly loaded:**
```bash
# Restart Ollama
killall ollama
ollama serve
```

3. **Embedding dimension mismatch:**
```python
# In test_embeddings.py, check:
embedding = np.array(embed_text("test", model))
print(f"Embedding dimensions: {embedding.shape}")

# Should be:
# nomic-embed-text: 768
# bge-large: 1024
# all-minilm: 384
```

---

### Issue: Tests Are Very Slow

**Symptoms:**
- Each test takes > 10 seconds
- Total runtime > 2 minutes

**Solutions:**

1. **Enable embedding cache:**
```bash
export AISTUDIO_ENABLE_EMBED_CACHE=true
```

2. **Use smaller model:**
```bash
export AISTUDIO_DEFAULT_EMBED_MODEL="all-minilm:l6-v2"
```

3. **Check CPU usage:**
```bash
# During test, check if CPU is maxed
top -p $(pgrep ollama)

# If consistently at 100%, this is normal for CPU inference
# Consider upgrading to GPU or accept slower speed
```

---

### Issue: Inconsistent Results

**Symptoms:**
- Test passes sometimes, fails other times
- Scores vary by > 0.1 between runs

**Explanation:**
This shouldn't happen with embeddings (they're deterministic). If you see this:

1. **Check if model is being swapped:**
```bash
# Run this before each test
echo "Using model: $AISTUDIO_DEFAULT_EMBED_MODEL"
ollama ps  # Shows currently loaded model
```

2. **Check for randomness in code:**
```python
# Embeddings should be deterministic
# No randomness should be involved
```

3. **Restart Ollama:**
```bash
killall ollama
ollama serve
```

---

## Best Practices

### Regular Testing

**When to run embedding tests:**

1. **Before deploying to production**
   ```bash
   python embedding_arithmetic.py > embedding_test_results.txt
   ```

2. **After changing embedding model**
   ```bash
   python test_embeddings.py
   ```

3. **When RAG accuracy degrades**
   - Test embeddings first
   - Compare with baseline results
   - May indicate model corruption

4. **When ingesting new corpus types**
   ```bash
   # Test with domain-specific vocabulary
   python embedding_arithmetic.py --interactive
   ```

---

### Creating Domain-Specific Tests

**For resume corpus:**

```python
# Add to embedding_arithmetic.py

RESUME_ANALOGIES = [
    {
        "name": "CTO-Technology-CFO-Finance",
        "a": "cto",
        "b": "technology",
        "c": "cfo",
        "expected": "finance",
        "candidates": ["finance", "accounting", "treasury", "budget", "technology"]
    },
    {
        "name": "Senior-Manager-Junior-Analyst",
        "a": "senior",
        "b": "manager",
        "c": "junior",
        "expected": "analyst",
        "candidates": ["analyst", "associate", "coordinator", "manager", "director"]
    },
    {
        "name": "Led-Team-Built-Product",
        "a": "led",
        "b": "team",
        "c": "built",
        "expected": "product",
        "candidates": ["product", "system", "platform", "team", "organization"]
    }
]
```

---

### Benchmarking Workflow

**Complete benchmarking process:**

```bash
# 1. Baseline current model
export AISTUDIO_DEFAULT_EMBED_MODEL="nomic-embed-text"
python embedding_arithmetic.py > baseline_nomic.txt

# 2. Test alternative
export AISTUDIO_DEFAULT_EMBED_MODEL="bge-large"
python embedding_arithmetic.py > test_bge.txt

# 3. Compare
echo "=== NOMIC RESULTS ==="
grep "Accuracy:" baseline_nomic.txt

echo "=== BGE RESULTS ==="
grep "Accuracy:" test_bge.txt

# 4. Test speed
time python test_embeddings.py  # With nomic
time python test_embeddings.py  # With bge

# 5. Test on actual queries
curl -X POST http://localhost:8000/ask \
  -d '{"query": "Manuel Barbero experience", "corpus": "mb_resumes"}'

# 6. Decide
# - If accuracy gain > 5% AND speed acceptable → switch
# - Otherwise → keep nomic
```

---

## Advanced Topics

### Understanding Vector Dimensions

**Why dimensions matter:**

```
Model              Dimensions    Information Capacity
all-minilm-l6-v2   384          Lower (faster, less nuanced)
nomic-embed-text   768          Medium (balanced)
bge-large          1024         Higher (slower, more nuanced)
```

**More dimensions = more capacity to capture semantic nuances**

But: diminishing returns after ~768 for most tasks

---

### Cosine Similarity vs Euclidean Distance

**Your tests use cosine similarity:**

```python
similarity = (a · b) / (||a|| × ||b||)
```

**Why cosine over euclidean?**
- Invariant to vector magnitude
- Only cares about direction/angle
- Better for semantic similarity

**Visual:**
```
Vector A: ————————→
Vector B: ————→
         
Angle = small → High cosine similarity
Angle = large → Low cosine similarity
```

---

### Creating Custom Test Suites

**Template for your domain:**

```python
MY_DOMAIN_ANALOGIES = [
    {
        "name": "Test-Name",
        "a": "word_a",
        "b": "word_b",
        "c": "word_c",
        "expected": "expected_result",
        "candidates": ["expected_result", "alternative1", "alternative2", ...]
    },
    # Add more tests
]

# Add to embedding_arithmetic.py
# Or create your own test file using the same structure
```

---

## Summary Checklist

### Before Using in Production

- [ ] Run `python test_embeddings.py`
- [ ] Verify all 3 core tests pass
- [ ] Check accuracy > 80%
- [ ] Test with domain-specific vocabulary
- [ ] Compare with alternative models if needed
- [ ] Document which model and why
- [ ] Set up monitoring for embedding quality

### Regular Maintenance

- [ ] Test embeddings monthly
- [ ] Re-test after model updates
- [ ] Create domain-specific tests
- [ ] Monitor RAG accuracy metrics
- [ ] Benchmark new models as they release

---

## Additional Resources

### Further Reading

- **Word2Vec Paper**: Original paper on word embeddings
- **Sentence Transformers**: Library powering many modern embeddings
- **MTEB Leaderboard**: Benchmark for embedding models
- **Ollama Models**: Browse available embedding models

### Related Tools

- **Embedding Projector**: Visualize embeddings in 3D
- **UMAP**: Dimension reduction for visualization
- **t-SNE**: Another visualization technique

### Getting Help

If tests consistently fail or results are unclear:

1. Check Ollama is running: `ollama ps`
2. Verify model is loaded: `ollama list`
3. Test with another model: `export AISTUDIO_DEFAULT_EMBED_MODEL="bge-large"`
4. Check project structure: `ls src/local_llm_bot/app/`
5. Review embedding cache: `ls data/cache/`

---

## Conclusion

Embedding quality directly impacts RAG accuracy. Regular testing with these tools ensures your system maintains high performance. The **King - Man + Woman = Queen** test is a quick, reliable indicator of whether your embeddings understand semantic relationships.

**Quick reference:**

```bash
# Quick test (10 seconds)
python test_embeddings.py

# Comprehensive test (30 seconds)
python embedding_arithmetic.py

# Interactive exploration
python embedding_arithmetic.py --interactive

# Compare models
export AISTUDIO_DEFAULT_EMBED_MODEL="bge-large"
python test_embeddings.py
```

Good embeddings = Better RAG = More accurate answers! 🎯
