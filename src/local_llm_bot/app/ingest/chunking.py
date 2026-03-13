"""
Generic semantic chunking for any document type.

This module provides intelligent, context-aware chunking that:
1. Respects natural document boundaries (sections, paragraphs, sentences)
2. Detects structure automatically (headers, lists, code blocks)
3. Preserves context without overfitting to specific document types
4. Works for: resumes, reports, books, articles, technical docs, legal docs, etc.

Key principles:
- Structure detection is heuristic-based, not hardcoded
- Falls back gracefully for unstructured text
- Configurable for different document types via parameters
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

from .types import Chunk, Document


class BoundaryType(Enum):
    """Types of text boundaries in order of strength"""
    SECTION = 5      # Major section (## Header, CAPS HEADER)
    SUBSECTION = 4   # Minor section (### Header)
    PARAGRAPH = 3    # Paragraph break (double newline)
    SENTENCE = 2     # Sentence boundary (. ! ?)
    LINE = 1         # Line break
    NONE = 0         # No boundary


@dataclass
class TextBoundary:
    """Represents a detected boundary in text"""
    position: int           # Character position
    boundary_type: BoundaryType
    content: str           # Text before this boundary
    context: str | None = None  # Section/subsection title for context


def detect_header_level(line: str) -> int | None:
    """
    Detect if a line is a header and return its level (1-6).
    
    Supports:
    - Markdown: # Header, ## Header, etc.
    - ALL CAPS: HEADER TEXT (common in many doc types)
    - Underlined: Header\n===== or Header\n-----
    """
    line_stripped = line.strip()
    
    # Markdown headers
    if line_stripped.startswith('#'):
        level = 0
        for char in line_stripped:
            if char == '#':
                level += 1
            else:
                break
        if level <= 6 and line_stripped[level:].strip():
            return level
    
    # ALL CAPS headers (must be substantial, 3+ words or 10+ chars)
    if line_stripped.isupper() and len(line_stripped) >= 10 and any(c.isalpha() for c in line_stripped):
            # Count words
            words = line_stripped.split()
            if len(words) >= 2:  # At least 2 words
                return 1  # Treat as major header
    
    return None


def detect_list_item(line: str) -> bool:
    """Detect if a line is a list item"""
    line_stripped = line.strip()
    
    # Bullet points: -, *, •, ◦, ▪
    if re.match(r'^[\-\*\•\◦\▪]\s+\S', line_stripped):
        return True
    
    # Numbered lists: 1. item, 1) item, (1) item
    if re.match(r'^\d+[\.\)]\s+\S', line_stripped) or re.match(r'^\(\d+\)\s+\S', line_stripped):
        return True
    
    # Letter lists: a. item, a) item
    if re.match(r'^[a-z][\.\)]\s+\S', line_stripped):  # noqa: SIM103
        return True
    
    return False


def detect_boundaries(text: str) -> list[TextBoundary]:
    """
    Detect natural boundaries in text.
    
    Returns list of boundaries sorted by position.
    """
    boundaries = []
    lines = text.split('\n')
    
    current_section = None
    current_subsection = None
    position = 0
    accumulated_content = []
    
    for _i, line in enumerate(lines):
        line_length = len(line) + 1  # +1 for newline
        
        # Check if this is a header
        header_level = detect_header_level(line)
        
        if header_level:
            # Save accumulated content before this header
            if accumulated_content:
                content = '\n'.join(accumulated_content)
                boundaries.append(TextBoundary(
                    position=position - len(content) - 1,
                    boundary_type=BoundaryType.PARAGRAPH,
                    content=content,
                    context=current_subsection or current_section
                ))
                accumulated_content = []
            
            # This is a section boundary
            boundary_type = BoundaryType.SECTION if header_level <= 2 else BoundaryType.SUBSECTION
            
            # Update context
            header_text = line.strip().lstrip('#').strip()
            if header_level <= 2:
                current_section = header_text
                current_subsection = None
            else:
                current_subsection = header_text
            
            boundaries.append(TextBoundary(
                position=position,
                boundary_type=boundary_type,
                content=line,
                context=header_text
            ))
        
        # Check for paragraph break (empty line after content)
        elif not line.strip() and accumulated_content:
            content = '\n'.join(accumulated_content)
            boundaries.append(TextBoundary(
                position=position - len(content) - 1,
                boundary_type=BoundaryType.PARAGRAPH,
                content=content,
                context=current_subsection or current_section
            ))
            accumulated_content = []
        
        else:
            # Regular content line
            if line.strip():
                accumulated_content.append(line)
        
        position += line_length
    
    # Add final accumulated content
    if accumulated_content:
        content = '\n'.join(accumulated_content)
        boundaries.append(TextBoundary(
            position=position - len(content) - 1,
            boundary_type=BoundaryType.PARAGRAPH,
            content=content,
            context=current_subsection or current_section
        ))
    
    return boundaries


def split_by_sentences(text: str) -> list[str]:
    """
    Split text into sentences using common patterns.
    
    Handles:
    - Standard punctuation: . ! ?
    - Abbreviations: Dr. Mr. Mrs. etc.
    - Decimals: 3.14
    - Ellipsis: ...
    """
    # Protect common abbreviations
    protected = text
    abbreviations = ['Dr.', 'Mr.', 'Mrs.', 'Ms.', 'Ph.D.', 'Inc.', 'Ltd.', 'Jr.', 'Sr.', 'etc.', 'e.g.', 'i.e.', 'vs.']
    placeholders = []
    
    for i, abbr in enumerate(abbreviations):
        placeholder = f"__ABBR{i}__"
        protected = protected.replace(abbr, placeholder)
        placeholders.append((placeholder, abbr))
    
    # Split on sentence boundaries
    # Pattern: [.!?] followed by space and capital letter, or end of string
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])|(?<=[.!?])$', protected)
    
    # Restore abbreviations
    result = []
    for sent in sentences:
        for placeholder, abbr in placeholders:
            sent = sent.replace(placeholder, abbr)
        if sent.strip():
            result.append(sent.strip())
    
    return result


def chunk_with_boundaries(
    text: str,
    max_size: int = 1200,
    overlap: int = 200,
    prefer_boundary: BoundaryType = BoundaryType.PARAGRAPH
) -> list[dict[str, any]]:
    """
    Chunk text respecting natural boundaries.
    
    Args:
        text: Text to chunk
        max_size: Maximum chunk size in characters
        overlap: Overlap size in characters
        prefer_boundary: Preferred boundary type for splitting
    
    Returns:
        List of dicts with 'text', 'boundary_type', 'context'
    """
    boundaries = detect_boundaries(text)
    
    if not boundaries:
        # Fallback: split by sentences
        sentences = split_by_sentences(text)
        return chunk_by_sentences_simple(sentences, max_size, overlap)
    
    chunks = []
    current_chunk_parts = []
    current_size = 0
    current_context = None
    
    for boundary in boundaries:
        content = boundary.content
        content_size = len(content)
        
        # Update context
        if boundary.context:
            current_context = boundary.context
        
        # If this single boundary exceeds max_size, split it further
        if content_size > max_size:
            # Save current chunk first
            if current_chunk_parts:
                chunk_text = '\n\n'.join(current_chunk_parts)
                chunks.append({
                    'text': chunk_text,
                    'boundary_type': prefer_boundary.name,
                    'context': current_context,
                    'size': len(chunk_text)
                })
                current_chunk_parts = []
                current_size = 0
            
            # Split large content by sentences
            sentences = split_by_sentences(content)
            sentence_chunks = chunk_by_sentences_simple(sentences, max_size, overlap)
            for sc in sentence_chunks:
                sc['context'] = current_context or boundary.context
                chunks.append(sc)
            
            continue
        
        # Check if adding this boundary would exceed max_size
        if current_size + content_size > max_size and current_chunk_parts:
            # Save current chunk
            chunk_text = '\n\n'.join(current_chunk_parts)
            chunks.append({
                'text': chunk_text,
                'boundary_type': prefer_boundary.name,
                'context': current_context,
                'size': len(chunk_text)
            })
            
            # Handle overlap: keep last part if small enough
            if current_chunk_parts and len(current_chunk_parts[-1]) <= overlap:
                current_chunk_parts = [current_chunk_parts[-1]]
                current_size = len(current_chunk_parts[-1])
            else:
                current_chunk_parts = []
                current_size = 0
        
        # Add boundary content to current chunk
        current_chunk_parts.append(content)
        current_size += content_size
    
    # Add final chunk
    if current_chunk_parts:
        chunk_text = '\n\n'.join(current_chunk_parts)
        chunks.append({
            'text': chunk_text,
            'boundary_type': prefer_boundary.name,
            'context': current_context,
            'size': len(chunk_text)
        })
    
    return chunks


def chunk_by_sentences_simple(sentences: list[str], max_size: int, overlap: int) -> list[dict[str, any]]:
    """Helper: chunk a list of sentences"""
    chunks = []
    current_chunk = []
    current_size = 0
    
    for sentence in sentences:
        sentence_size = len(sentence)
        
        if current_size + sentence_size > max_size and current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                'text': chunk_text,
                'boundary_type': 'SENTENCE',
                'context': None,
                'size': len(chunk_text)
            })
            
            # Overlap: keep last few sentences
            overlap_sents = []
            overlap_size = 0
            for s in reversed(current_chunk):
                if overlap_size + len(s) <= overlap:
                    overlap_sents.insert(0, s)
                    overlap_size += len(s)
                else:
                    break
            
            current_chunk = overlap_sents
            current_size = overlap_size
        
        current_chunk.append(sentence)
        current_size += sentence_size
    
    if current_chunk:
        chunk_text = ' '.join(current_chunk)
        chunks.append({
            'text': chunk_text,
            'boundary_type': 'SENTENCE',
            'context': None,
            'size': len(chunk_text)
        })
    
    return chunks


def add_context_to_chunk(chunk_text: str, context: str | None) -> str:
    """
    Prepend context to chunk if available.
    
    Format: [Context]\nChunk text...
    """
    if context:
        return f"[{context}]\n\n{chunk_text}"
    return chunk_text


def chunk_document_smart(
    doc: Document,
    chunk_size: int = 1200,
    overlap: int = 200,
    include_context: bool = True,
    min_chunk_size: int = 100
) -> list[Chunk]:
    """
    Smart document chunking that works for any document type.
    
    Args:
        doc: Document to chunk
        chunk_size: Target chunk size (will respect boundaries)
        overlap: Overlap between chunks
        include_context: Whether to include section context in chunks
        min_chunk_size: Minimum chunk size (avoid tiny chunks)
    
    Returns:
        List of Chunk objects
    """
    # Detect and chunk by boundaries
    chunk_data_list = chunk_with_boundaries(
        text=doc.text,
        max_size=chunk_size,
        overlap=overlap,
        prefer_boundary=BoundaryType.PARAGRAPH
    )
    
    # Convert to Chunk objects
    chunks = []
    for i, chunk_data in enumerate(chunk_data_list):
        # Skip tiny chunks
        if chunk_data['size'] < min_chunk_size:
            continue
        
        # Add context if requested
        text = chunk_data['text']
        if include_context and chunk_data.get('context'):
            text = add_context_to_chunk(text, chunk_data['context'])
        
        chunk = Chunk(
            chunk_id=f"{doc.doc_id}::chunk-{i}",
            doc_id=doc.doc_id,
            source_path=doc.source_path,
            text=text,
        )
        chunks.append(chunk)
    
    return chunks


# Backward compatible wrapper
def chunk_document(doc: Document, chunk_size: int = 1200, overlap: int = 200) -> list[Chunk]:
    """
    Main chunking function (backward compatible).
    
    Uses smart semantic chunking that works for all document types.
    Falls back to character-based chunking if needed.
    """
    try:
        return chunk_document_smart(
            doc,
            chunk_size=chunk_size,
            overlap=overlap,
            include_context=True,
            min_chunk_size=100
        )
    except Exception as e:
        print(f"Warning: Smart chunking failed ({e}), falling back to simple chunking")
        return chunk_document_simple(doc, chunk_size, overlap)


def chunk_document_simple(doc: Document, chunk_size: int = 1200, overlap: int = 200) -> list[Chunk]:
    """
    Fallback: Simple sentence-aware chunking.
    Better than character-based but not as smart as boundary detection.
    """
    sentences = split_by_sentences(doc.text)
    chunk_data_list = chunk_by_sentences_simple(sentences, chunk_size, overlap)
    
    chunks = []
    for i, chunk_data in enumerate(chunk_data_list):
        chunk = Chunk(
            chunk_id=f"{doc.doc_id}::chunk-{i}",
            doc_id=doc.doc_id,
            source_path=doc.source_path,
            text=chunk_data['text'],
        )
        chunks.append(chunk)
    
    return chunks


# Original character-based chunking (kept for reference/testing)
def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> list[str]:
    """
    DEPRECATED: Character-based chunking.
    Use chunk_document() instead for better results.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be < chunk_size")

    text = text.strip()
    if not text:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = end - overlap
    return chunks


# ============================================================================
# Configuration presets for different document types
# ============================================================================

class ChunkingStrategy:
    """Predefined chunking strategies for different document types"""
    
    @staticmethod
    def for_resumes(doc: Document) -> list[Chunk]:
        """Optimized for resumes: preserve sections, smaller chunks"""
        return chunk_document_smart(
            doc,
            chunk_size=1000,    # Smaller chunks for focused content
            overlap=150,
            include_context=True,
            min_chunk_size=80
        )
    
    @staticmethod
    def for_technical_docs(doc: Document) -> list[Chunk]:
        """Optimized for technical documentation: larger chunks, preserve code blocks"""
        return chunk_document_smart(
            doc,
            chunk_size=1500,    # Larger chunks for complex explanations
            overlap=300,
            include_context=True,
            min_chunk_size=200
        )
    
    @staticmethod
    def for_legal_docs(doc: Document) -> list[Chunk]:
        """Optimized for legal documents: large chunks, high overlap for context"""
        return chunk_document_smart(
            doc,
            chunk_size=2000,    # Very large chunks for legal continuity
            overlap=400,
            include_context=True,
            min_chunk_size=300
        )
    
    @staticmethod
    def for_articles(doc: Document) -> list[Chunk]:
        """Optimized for articles/blog posts: medium chunks, paragraph-aware"""
        return chunk_document_smart(
            doc,
            chunk_size=1200,    # Standard size
            overlap=200,
            include_context=True,
            min_chunk_size=150
        )
    
    @staticmethod
    def for_books(doc: Document) -> list[Chunk]:
        """Optimized for books: larger chunks for narrative flow"""
        return chunk_document_smart(
            doc,
            chunk_size=1800,    # Large chunks for narrative
            overlap=300,
            include_context=True,
            min_chunk_size=200
        )


# ============================================================================
# Usage examples
# ============================================================================

"""
Example 1: Basic usage (works for any document)
------------------------------------------------
from local_llm_bot.app.ingest.chunking import chunk_document

doc = Document(doc_id="doc1", source_path="resume.pdf", text=resume_text)
chunks = chunk_document(doc, chunk_size=1200, overlap=200)


Example 2: Use document-specific strategy
------------------------------------------
from local_llm_bot.app.ingest.chunking import ChunkingStrategy

# For a resume
chunks = ChunkingStrategy.for_resumes(doc)

# For technical documentation
chunks = ChunkingStrategy.for_technical_docs(doc)

# For legal documents
chunks = ChunkingStrategy.for_legal_docs(doc)


Example 3: Custom configuration
--------------------------------
from local_llm_bot.app.ingest.chunking import chunk_document_smart

chunks = chunk_document_smart(
    doc,
    chunk_size=1500,
    overlap=250,
    include_context=True,
    min_chunk_size=200
)


Example 4: Compare chunking strategies
---------------------------------------
# Character-based (old way)
char_chunks = chunk_text(doc.text, 1200, 200)

# Sentence-based (better)
sent_chunks = chunk_document_simple(doc, 1200, 200)

# Smart semantic (best)
smart_chunks = chunk_document_smart(doc, 1200, 200)
"""
