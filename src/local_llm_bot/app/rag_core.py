# src/local_llm_bot/app/rag_core_enhanced.py
"""
Enhanced RAG core with citation support and conversation memory.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Dict, Optional

from local_llm_bot.app.config import CONFIG
from local_llm_bot.app.ingest.index_jsonl import read_jsonl
from local_llm_bot.app.ollama_client import ollama_generate
from local_llm_bot.app.utils.corpus_paths import corpus_paths
from local_llm_bot.app.utils.repo_root import find_repo_root

# Import existing retrieval logic
from local_llm_bot.app.rag_core import (
    RetrievedDoc,
    retrieve,
    _repo_root,
    _is_tax_corpus,
    _tokenize,
    compose_queries,
)


@dataclass
class Citation:
    """A citation reference to a source document"""
    index: int
    source: str
    page: Optional[int] = None
    chunk_id: Optional[str] = None
    score: float = 0.0


@dataclass
class AnswerWithCitations:
    """Answer with citation metadata"""
    answer: str
    citations: List[Citation]
    source_docs: List[RetrievedDoc]


def extract_page_number(source_path: str, chunk_id: str = "") -> Optional[int]:
    """
    Attempt to extract page number from source path or chunk_id.
    
    Examples:
    - "document.pdf#page=5" -> 5
    - "chunk-page-3" -> 3
    - "document_p12.pdf" -> 12
    """
    # Try from source path
    page_match = re.search(r'#page=(\d+)', source_path)
    if page_match:
        return int(page_match.group(1))
    
    page_match = re.search(r'[_\-]p(\d+)', source_path, re.IGNORECASE)
    if page_match:
        return int(page_match.group(1))
    
    # Try from chunk_id
    if chunk_id:
        page_match = re.search(r'page[_\-]?(\d+)', chunk_id, re.IGNORECASE)
        if page_match:
            return int(page_match.group(1))
    
    return None


def generate_answer_with_citations(
    *, 
    query: str, 
    docs: List[RetrievedDoc],
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> AnswerWithCitations:
    """
    Generate answer with citation markers and return citation metadata.
    
    The LLM will be instructed to cite sources using [1], [2], etc.
    We then extract these and build citation objects.
    """
    if not docs:
        return AnswerWithCitations(
            answer="I don't have any relevant documents to answer this question.",
            citations=[],
            source_docs=[]
        )
    
    # Build context with numbered sources
    context_parts = []
    for i, doc in enumerate(docs, 1):
        context_parts.append(f"[Source {i}] {doc.source}\n{doc.content}")
    
    context = "\n\n".join(context_parts)
    
    # Enhanced system prompt with citation instructions
    system = (
        "You are a helpful research assistant.\n"
        "Use the provided sources to answer questions accurately.\n"
        "IMPORTANT: When you use information from a source, cite it using [1], [2], etc.\n"
        "The number should match the source number in the context.\n"
        "You can cite multiple sources like [1,2] or [1][2].\n"
        "If the answer is not in the provided sources, say so clearly.\n"
        "Always cite your sources - every factual claim should have a citation."
    )
    
    # Build prompt with conversation history
    if conversation_history:
        # Include previous messages for context
        history_text = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in conversation_history[-6:]  # Last 3 exchanges (6 messages)
        ])
        prompt = f"Conversation History:\n{history_text}\n\nCurrent Question:\n{query}\n\nAvailable Sources:\n{context}\n\nAnswer:"
    else:
        prompt = f"Question:\n{query}\n\nAvailable Sources:\n{context}\n\nAnswer:"
    
    # Generate answer
    answer = ollama_generate(model=CONFIG.rag.default_model, prompt=prompt, system=system)
    
    # Extract citations from answer
    citations = []
    cited_indices = set()
    
    # Find all citation patterns: [1], [2,3], [1][2], etc.
    citation_patterns = re.findall(r'\[(\d+(?:,\d+)*)\]', answer)
    
    for pattern in citation_patterns:
        # Split comma-separated citations
        for idx_str in pattern.split(','):
            idx = int(idx_str.strip())
            if idx > 0 and idx <= len(docs) and idx not in cited_indices:
                doc = docs[idx - 1]
                page = extract_page_number(doc.source, doc.id)
                
                citations.append(Citation(
                    index=idx,
                    source=doc.source,
                    page=page,
                    chunk_id=doc.id,
                    score=doc.score
                ))
                cited_indices.add(idx)
    
    # Sort citations by index
    citations.sort(key=lambda c: c.index)
    
    return AnswerWithCitations(
        answer=answer,
        citations=citations,
        source_docs=docs
    )


# Backward compatible wrapper
def generate_answer(*, query: str, docs: List[RetrievedDoc]) -> str:
    """
    Backward compatible function that returns just the answer string.
    Use generate_answer_with_citations() for citation support.
    """
    result = generate_answer_with_citations(query=query, docs=docs)
    return result.answer
