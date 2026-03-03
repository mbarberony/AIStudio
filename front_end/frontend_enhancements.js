/**
 * RAG Studio Frontend Enhancements
 * 
 * Add this to your existing rag_studio.html to enable:
 * 1. Citation rendering as superscript with footnotes
 * 2. Conversation memory for follow-up questions
 * 
 * INTEGRATION INSTRUCTIONS:
 * 1. Add the CSS to your existing <style> section
 * 2. Add the JavaScript to your existing <script> section
 * 3. Replace the sendQuery() function with the enhanced version
 */

/* ============================================================================
   PART 1: CSS - Add to <style> section
   ============================================================================ */

/* Citation superscripts */
.citation-ref {
    color: var(--accent-secondary);
    font-size: 0.75em;
    vertical-align: super;
    cursor: pointer;
    text-decoration: none;
    font-weight: 600;
    margin: 0 1px;
    transition: all 0.2s;
}

.citation-ref:hover {
    color: var(--accent-primary);
    text-decoration: underline;
}

/* Footnotes section */
.footnotes-section {
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px solid var(--border-color);
}

.footnotes-title {
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-secondary);
    margin-bottom: 12px;
}

.footnote-item {
    margin-bottom: 12px;
    padding-left: 24px;
    position: relative;
    font-size: 13px;
    line-height: 1.6;
    color: var(--text-secondary);
}

.footnote-number {
    position: absolute;
    left: 0;
    color: var(--accent-secondary);
    font-weight: 600;
}

.footnote-source {
    color: var(--text-primary);
    font-weight: 500;
}

.footnote-page {
    color: var(--accent-primary);
    margin-left: 8px;
}

.footnote-link {
    color: var(--accent-secondary);
    text-decoration: none;
    margin-left: 8px;
    font-size: 11px;
}

.footnote-link:hover {
    text-decoration: underline;
}

/* Conversation context indicator */
.context-indicator {
    display: inline-block;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 11px;
    color: var(--text-secondary);
    margin-left: 8px;
}

.context-indicator.active {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
}

/* Clear conversation button */
.clear-conversation {
    background: transparent;
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 8px 12px;
    color: var(--text-secondary);
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s;
    margin-top: 12px;
}

.clear-conversation:hover {
    border-color: var(--danger);
    color: var(--danger);
}


/* ============================================================================
   PART 2: JavaScript - Add to <script> section
   ============================================================================ */

// Conversation memory storage
let conversationHistory = [];

// Maximum conversation turns to keep (configurable)
const MAX_CONVERSATION_TURNS = 10;

/**
 * Add message to conversation history
 */
function addToConversation(role, content) {
    conversationHistory.push({
        role: role,
        content: content
    });
    
    // Keep only last N turns (N*2 messages since each turn has user + assistant)
    if (conversationHistory.length > MAX_CONVERSATION_TURNS * 2) {
        conversationHistory = conversationHistory.slice(-MAX_CONVERSATION_TURNS * 2);
    }
    
    updateContextIndicator();
}

/**
 * Clear conversation history
 */
function clearConversation() {
    conversationHistory = [];
    updateContextIndicator();
    showStatus('Conversation cleared', 'success');
}

/**
 * Update the context indicator in UI
 */
function updateContextIndicator() {
    const indicator = document.getElementById('contextIndicator');
    if (!indicator) return;
    
    const turns = Math.floor(conversationHistory.length / 2);
    
    if (turns > 0) {
        indicator.textContent = `${turns} turn${turns > 1 ? 's' : ''} in memory`;
        indicator.classList.add('active');
    } else {
        indicator.textContent = 'No context';
        indicator.classList.remove('active');
    }
}

/**
 * Parse citations from answer text and create clickable superscripts
 */
function parseCitations(answer, citations) {
    if (!citations || citations.length === 0) {
        return answer;
    }
    
    // Replace citation patterns [1], [2], etc. with clickable superscripts
    let parsedAnswer = answer;
    const citationPattern = /\[(\d+(?:,\d+)*)\]/g;
    
    parsedAnswer = parsedAnswer.replace(citationPattern, (match, numbers) => {
        const nums = numbers.split(',').map(n => n.trim());
        const links = nums.map(num => 
            `<a href="#footnote-${num}" class="citation-ref">[${num}]</a>`
        ).join('');
        return links;
    });
    
    return parsedAnswer;
}

/**
 * Render footnotes section
 */
function renderFootnotes(citations) {
    if (!citations || citations.length === 0) {
        return '';
    }
    
    let footnotesHTML = `
        <div class="footnotes-section">
            <div class="footnotes-title">References</div>
    `;
    
    citations.forEach(citation => {
        const fileName = citation.source.split('/').pop();
        const pageInfo = citation.page ? `<span class="footnote-page">Page ${citation.page}</span>` : '';
        const link = `<a href="#" class="footnote-link" onclick="openSource('${citation.source}', ${citation.page}); return false;">↗ Open</a>`;
        
        footnotesHTML += `
            <div class="footnote-item" id="footnote-${citation.index}">
                <span class="footnote-number">[${citation.index}]</span>
                <span class="footnote-source">${fileName}</span>
                ${pageInfo}
                ${link}
            </div>
        `;
    });
    
    footnotesHTML += '</div>';
    return footnotesHTML;
}

/**
 * Open source document (placeholder - implement based on your file storage)
 */
function openSource(sourcePath, page) {
    // TODO: Implement based on your file storage system
    // Options:
    // 1. If files are web-accessible: window.open(url, '_blank')
    // 2. If using API: fetch file and display in modal
    // 3. If local files: show path to user
    
    console.log('Opening source:', sourcePath, 'page:', page);
    alert(`Would open: ${sourcePath}${page ? ` (page ${page})` : ''}\n\nImplement file serving to enable this feature.`);
}

/**
 * Enhanced sendQuery function with citations and conversation memory
 * REPLACE your existing sendQuery() function with this
 */
async function sendQuery() {
    const queryInput = document.getElementById('queryInput');
    const chatMessages = document.getElementById('chatMessages');
    const query = queryInput.value.trim();
    
    if (!query) return;
    
    // Add user message to UI
    appendMessage('user', query);
    queryInput.value = '';
    
    // Add to conversation history
    addToConversation('user', query);
    
    // Show loading state
    const loadingId = Date.now();
    appendMessage('assistant', '...', loadingId);
    
    try {
        const corpus = document.getElementById('corpusSelect').value;
        const topK = parseInt(document.getElementById('topK').value) || 5;
        
        // Build request with conversation history
        const requestBody = {
            query: query,
            corpus: corpus,
            top_k: topK,
            conversation_history: conversationHistory.length > 0 ? conversationHistory : null
        };
        
        const response = await fetch('http://localhost:8000/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Remove loading message
        document.getElementById(`msg-${loadingId}`)?.remove();
        
        // Parse citations if present
        let answerHTML = data.answer;
        let footnotesHTML = '';
        
        if (data.has_citations && data.citations) {
            answerHTML = parseCitations(data.answer, data.citations);
            footnotesHTML = renderFootnotes(data.citations);
        }
        
        // Add assistant message with citations
        appendMessage('assistant', answerHTML + footnotesHTML);
        
        // Add to conversation history
        addToConversation('assistant', data.answer);
        
    } catch (error) {
        console.error('Error:', error);
        document.getElementById(`msg-${loadingId}`)?.remove();
        appendMessage('assistant', `Error: ${error.message}`, null, true);
    }
}

/**
 * Enhanced appendMessage to handle HTML content
 * UPDATE your existing appendMessage() function
 */
function appendMessage(role, content, id = null, isError = false) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message${isError ? ' error-message' : ''}`;
    if (id) messageDiv.id = `msg-${id}`;
    
    // Use innerHTML for assistant messages to render citations
    if (role === 'assistant') {
        messageDiv.innerHTML = content;
    } else {
        messageDiv.textContent = content;
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/* ============================================================================
   PART 3: HTML Updates - Add to your HTML
   ============================================================================ */

/*
Add this somewhere in your sidebar or header:

<div class="sidebar-section">
    <div class="sidebar-section-title">Conversation</div>
    <div>
        <span id="contextIndicator" class="context-indicator">No context</span>
    </div>
    <button class="clear-conversation" onclick="clearConversation()">
        Clear Conversation
    </button>
</div>
*/

/* ============================================================================
   PART 4: Initialization - Add to your existing initialization code
   ============================================================================ */

// Initialize context indicator on page load
document.addEventListener('DOMContentLoaded', function() {
    updateContextIndicator();
    
    // Optional: Add Enter key support for sending messages
    const queryInput = document.getElementById('queryInput');
    if (queryInput) {
        queryInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendQuery();
            }
        });
    }
});
