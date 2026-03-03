# Citations & Conversation Memory Implementation Guide

## Overview

This guide shows you how to add two powerful features to your RAG Studio:

1. **Citation Rendering**: Superscript citation numbers [1], [2] with footnotes showing source file, page number, and clickable links
2. **Conversation Memory**: Ask follow-up questions that remember previous context

## Architecture

```
Frontend                  Backend                    LLM
   ↓                         ↓                        ↓
Query → [with history] → retrieve() → docs      
                           ↓                          
                    generate_answer_with_citations()
                           ↓                          ↓
                    "Answer [1][2]"  ←─── "Use [1] for facts..."
                    + Citation objects
                           ↓
                    Response with citations
   ↓                         ↓
Parse citations      
Display with superscripts
Render footnotes
```

## Features

### Feature 1: Citations as Footnotes

**What it does:**
- LLM generates answers with citation markers: `[1]`, `[2]`, etc.
- Frontend renders these as clickable superscripts
- Footnotes section shows source details at bottom
- Each footnote includes: file name, page number (if available), and "Open" link

**Example Output:**
```
Manuel Barbero has over 20 years of experience in technology leadership[1]. 
He previously served as CTO at TechCorp[2] and led engineering teams of 120+ people[1].

References:
[1] Manuel_Barbero_Resume_2025.pdf Page 1 ↗ Open
[2] Manuel_Barbero_Experience.pdf Page 2 ↗ Open
```

### Feature 2: Conversation Memory

**What it does:**
- Stores last 10 conversation turns in memory
- Sends conversation history with each new query
- LLM can reference previous questions and answers
- "Clear Conversation" button to start fresh

**Example:**
```
User: "What is Manuel Barbero's experience?"
Bot: "Manuel has 20 years in technology leadership..."

User: "What companies did he work for?"  ← Remembers "he" = Manuel
Bot: "Based on our previous discussion about Manuel Barbero, he worked at..."
```

## Implementation Steps

### Step 1: Install Enhanced Backend

#### 1a. Add rag_core_enhanced.py

```bash
# Copy the enhanced RAG core
cp rag_core_enhanced.py src/local_llm_bot/app/rag_core_enhanced.py
```

**What it adds:**
- `Citation` dataclass for citation metadata
- `AnswerWithCitations` dataclass for response with citations
- `extract_page_number()` to extract page numbers from source paths
- `generate_answer_with_citations()` main function with citation support
- Conversation history support

#### 1b. Update API

```bash
# Backup current API
cp src/local_llm_bot/app/api_extended.py src/local_llm_bot/app/api_extended_backup.py

# Install enhanced API
cp api_extended_full.py src/local_llm_bot/app/api_extended.py
```

**What it adds:**
- `conversation_history` field in `AskRequest`
- `CitationResponse` model
- `citations` and `has_citations` fields in `AskResponse`
- Enhanced `/ask` endpoint that returns citations

#### 1c. Restart Backend

```bash
# Stop current server (Ctrl+C)

# Start with new code
python -m uvicorn src.local_llm_bot.app.api_extended:app --reload --port 8000
```

### Step 2: Update Frontend

The frontend enhancement is provided as JavaScript snippets in `frontend_enhancements.js`.

**Three integration options:**

#### Option A: Manual Integration (Recommended)

Add the code snippets from `frontend_enhancements.js` to your existing `rag_studio.html`:

1. **Add CSS** (lines marked "PART 1") to your `<style>` section
2. **Add JavaScript functions** (lines marked "PART 2") to your `<script>` section  
3. **Add HTML** (lines marked "PART 3") to your sidebar
4. **Replace** your existing `sendQuery()` and `appendMessage()` functions with the enhanced versions

#### Option B: Quick Test (Separate File)

Create a simple test page:

```bash
# See COMPLETE_EXAMPLE.html at the end of this guide
```

#### Option C: Full Replacement

We can create a completely updated `rag_studio.html` with all features integrated.

### Step 3: Test Citations

#### Test 1: Simple Query

```bash
curl -X POST http://localhost:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "What is Manuel Barbero experience?",
    "corpus": "mb_resumes",
    "top_k": 5
  }'
```

**Expected response:**
```json
{
  "answer": "Manuel Barbero has over 20 years of experience in technology leadership[1]. He served as CTO at multiple organizations...[2]",
  "citations": [
    {
      "index": 1,
      "source": "data/corpora/mb_resumes/Manuel_Barbero_Resume.pdf",
      "page": 1,
      "chunk_id": "doc1::chunk-0",
      "score": 0.234
    },
    {
      "index": 2,
      "source": "data/corpora/mb_resumes/Experience.pdf",
      "page": 2,
      "chunk_id": "doc2::chunk-1",
      "score": 0.456
    }
  ],
  "has_citations": true
}
```

#### Test 2: Conversation Memory

```bash
# First message
curl -X POST http://localhost:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "Who is Manuel Barbero?",
    "corpus": "mb_resumes"
  }'

# Follow-up (with history)
curl -X POST http://localhost:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "What companies did he work for?",
    "corpus": "mb_resumes",
    "conversation_history": [
      {"role": "user", "content": "Who is Manuel Barbero?"},
      {"role": "assistant", "content": "Manuel Barbero is a technology executive..."}
    ]
  }'
```

### Step 4: Test in UI

1. Open `http://localhost:3000/rag_studio.html`
2. Ask: "What is Manuel Barbero's experience?"
3. Check for:
   - ✅ Superscript citation numbers [1], [2] in answer
   - ✅ References section at bottom
   - ✅ Each reference shows filename, page, and Open link
   - ✅ Context indicator shows "1 turn in memory"

4. Ask follow-up: "What were his main achievements?"
5. Check for:
   - ✅ Bot understands "his" refers to Manuel
   - ✅ Context indicator shows "2 turns in memory"

6. Click "Clear Conversation"
7. Check for:
   - ✅ Context indicator shows "No context"
   - ✅ Next query has no memory of previous questions

## Customization

### Customize Citation Style

**Change superscript color:**
```css
.citation-ref {
    color: #ff6b6b;  /* Red instead of blue */
}
```

**Change to brackets style:**
```css
.citation-ref::before { content: '['; }
.citation-ref::after { content: ']'; }
```

### Customize Memory Limits

**Keep more/fewer turns:**
```javascript
const MAX_CONVERSATION_TURNS = 20;  // Increase to 20 turns
```

**Clear automatically after N minutes:**
```javascript
let conversationTimeout;

function addToConversation(role, content) {
    // ... existing code ...
    
    // Auto-clear after 10 minutes of inactivity
    clearTimeout(conversationTimeout);
    conversationTimeout = setTimeout(() => {
        clearConversation();
    }, 10 * 60 * 1000);
}
```

### Implement File Opening

**For web-accessible files:**
```javascript
function openSource(sourcePath, page) {
    // If files are served at /files/
    const url = `/files/${sourcePath}${page ? `#page=${page}` : ''}`;
    window.open(url, '_blank');
}
```

**For API-served files:**
```javascript
async function openSource(sourcePath, page) {
    try {
        const response = await fetch(`http://localhost:8000/files/${encodeURIComponent(sourcePath)}`);
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        window.open(url, '_blank');
    } catch (error) {
        alert('Could not open file: ' + error.message);
    }
}
```

**For local files (desktop app):**
```javascript
function openSource(sourcePath, page) {
    // Show path for user to open manually
    const fullPath = `/path/to/data/corpora/${sourcePath}`;
    alert(`Open this file:\n${fullPath}\n${page ? `Go to page ${page}` : ''}`);
}
```

## Page Number Extraction

The system attempts to extract page numbers from:

1. **Source path**: `document.pdf#page=5` → Page 5
2. **Chunk ID**: `doc1::page-3::chunk-0` → Page 3
3. **Filename**: `resume_p12.pdf` → Page 12

**To improve page extraction**, modify the chunking process to include page info:

```python
# In chunking.py
chunk = Chunk(
    chunk_id=f"{doc.doc_id}::page-{page_num}::chunk-{i}",
    # ... other fields
)
```

## Troubleshooting

### Issue: No citations appear

**Check:**
1. Is `rag_core_enhanced.py` installed?
   ```bash
   ls src/local_llm_bot/app/rag_core_enhanced.py
   ```

2. Is backend using enhanced version?
   ```bash
   curl http://localhost:8000/ask -X POST -d '{"query":"test","corpus":"default"}' -H 'Content-Type: application/json' | jq '.has_citations'
   # Should return: true
   ```

3. Is LLM generating citations?
   - The LLM must be instructed to use [1], [2] format
   - Check system prompt in `generate_answer_with_citations()`

### Issue: Citations don't match sources

**Cause:** LLM generates citation numbers that don't exist

**Solution:** Validate citations in backend:
```python
# In generate_answer_with_citations()
max_citations = len(docs)
for idx in cited_indices:
    if idx > max_citations:
        # Log warning
        print(f"Warning: Citation [{idx}] exceeds {max_citations} sources")
```

### Issue: Follow-up questions don't work

**Check:**
1. Is conversation history being sent?
   ```javascript
   console.log('Sending history:', conversationHistory);
   ```

2. Is backend receiving it?
   ```python
   # In api.py /ask endpoint
   print(f"Received history: {req.conversation_history}")
   ```

3. Is LLM using the history?
   - Check prompt includes history
   - Verify `conversation_history` parameter is passed

### Issue: Memory grows too large

**Solution:** Implement sliding window:
```javascript
// Keep only last 10 messages (5 turns)
if (conversationHistory.length > 10) {
    conversationHistory = conversationHistory.slice(-10);
}
```

## Advanced Features

### Add "Copy Citation" Button

```javascript
function copyCitation(index, source, page) {
    const citation = `[${index}] ${source}${page ? `, p. ${page}` : ''}`;
    navigator.clipboard.writeText(citation);
    showStatus('Citation copied!', 'success');
}

// In renderFootnotes()
const copyBtn = `<button class="copy-citation" onclick="copyCitation(${citation.index}, '${citation.source}', ${citation.page})">📋</button>`;
```

### Add Citation Preview

```javascript
function previewCitation(citationIndex) {
    // Show chunk content in modal
    const doc = sourceDocs[citationIndex - 1];
    showModal('Citation Preview', doc.content);
}
```

### Export Conversation

```javascript
function exportConversation() {
    const text = conversationHistory.map((msg, i) => 
        `${msg.role.toUpperCase()}: ${msg.content}`
    ).join('\n\n');
    
    downloadFile('conversation.txt', text);
}
```

## Complete Example HTML

Here's a minimal complete example:

```html
<!DOCTYPE html>
<html>
<head>
    <title>RAG Studio - Citations Test</title>
    <style>
        /* Add all CSS from frontend_enhancements.js PART 1 */
    </style>
</head>
<body>
    <div id="contextIndicator">No context</div>
    <button onclick="clearConversation()">Clear</button>
    
    <div id="chatMessages"></div>
    
    <input type="text" id="queryInput" placeholder="Ask a question...">
    <button onclick="sendQuery()">Send</button>
    
    <script>
        /* Add all JavaScript from frontend_enhancements.js PART 2 */
    </script>
</body>
</html>
```

## Summary

### What You Get

✅ **Citations**
- Automatic citation extraction from LLM responses
- Superscript rendering [1], [2]
- Footnotes with source file, page, and link
- Clickable references

✅ **Conversation Memory**
- Last 10 turns remembered
- Context-aware follow-up questions
- Visual indicator of conversation state
- Easy clear function

✅ **Better UX**
- Professional citation formatting
- Traceable answers
- Natural conversation flow
- Source transparency

### File Checklist

- [x] `rag_core_enhanced.py` - Enhanced RAG with citations
- [x] `api_extended_full.py` - API with citation support
- [x] `frontend_enhancements.js` - Frontend code snippets
- [x] This guide

### Next Steps

1. Install backend enhancements
2. Integrate frontend code
3. Test with your corpus
4. Customize styling
5. Implement file opening based on your setup

Enjoy your enhanced RAG Studio with citations and conversation memory! 🎉
