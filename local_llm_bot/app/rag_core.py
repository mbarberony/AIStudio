from dataclasses import dataclass


@dataclass
class RetrievedDoc:
    """Simple placeholder for a retrieved document chunk."""

    id: str
    content: str
    score: float


# Temporary in-memory corpus for testing.
# We will replace this later with a real vector store.
_FAKE_DOCS: list[RetrievedDoc] = [
    RetrievedDoc(
        id="doc-1",
        content="AIStudio is a personal AI engineering environment for RAG, agentic workflows, and CI/CD experiments.",
        score=1.0,
    ),
    RetrievedDoc(
        id="doc-2",
        content="The local_llm_bot component provides a FastAPI-based API that exposes /health and /ask endpoints.",
        score=1.0,
    ),
    RetrievedDoc(
        id="doc-3",
        content="The agentic_lab component will host agents and tools that call into the RAG API and local filesystem.",
        score=1.0,
    ),
]


def retrieve(query: str, top_k: int = 3) -> list[RetrievedDoc]:
    """
    Placeholder retrieval:
    - Filters the in-memory docs by simple substring match.
    - In a real implementation, this will query a vector store.
    """
    query_lower = query.lower()
    scored: list[RetrievedDoc] = []

    for doc in _FAKE_DOCS:
        if any(word in doc.content.lower() for word in query_lower.split()):
            # Fake scoring: higher score if more words match.
            match_count = sum(1 for word in query_lower.split() if word in doc.content.lower())
            scored.append(RetrievedDoc(id=doc.id, content=doc.content, score=float(match_count)))

    # Sort by score descending and take top_k.
    scored.sort(key=lambda d: d.score, reverse=True)
    return scored[:top_k]


def generate_answer(query: str, docs: list[RetrievedDoc]) -> str:
    """
    Placeholder answer generation:
    - In a real implementation, this will build a prompt and call the local LLM.
    - For now, it just stitches together relevant doc snippets.
    """
    if not docs:
        return f"I don't have any relevant information yet, but you asked: {query}"

    bullet_points = "\n".join(f"- {doc.content}" for doc in docs)
    return (
        f"Here is what I know related to your question:\n\n{bullet_points}\n\n(query was: {query})"
    )


# from dataclasses import dataclass
# from typing import List
#
#
# @dataclass
# class RetrievedDoc:
#     """Simple placeholder for a retrieved document chunk."""
#     id: str
#     content: str
#     score: float
#
#
# # Temporary in-memory corpus for testing.
# # We will replace this later with a real vector store.
# _FAKE_DOCS: List[RetrievedDoc] = [
#     RetrievedDoc(
#         id="doc-1",
#         content="AIStudio is a personal AI engineering environment for RAG, agentic workflows, and CI/CD experiments.",
#         score=1.0,
#     ),
#     RetrievedDoc(
#         id="doc-2",
#         content="The local_llm_bot component provides a FastAPI-based API that exposes /health and /ask endpoints.",
#         score=1.0,
#     ),
#     RetrievedDoc(
#         id="doc-3",
#         content="The agentic_lab component will host agents and tools that call into the RAG API and local filesystem.",
#         score=1.0,
#     ),
# ]
#
#
# def retrieve(query: str, top_k: int = 3) -> List[RetrievedDoc]:
#     """
#     Placeholder retrieval:
#     - Filters the in-memory docs by simple substring match.
#     - In a real implementation, this will query a vector store.
#     """
#     query_lower = query.lower()
#     scored: List[RetrievedDoc] = []
#
#     for doc in _FAKE_DOCS:
#         if any(word in doc.content.lower() for word in query_lower.split()):
#             # Fake scoring: higher score if more words match.
#             match_count = sum(
#                 1 for word in query_lower.split() if word in doc.content.lower()
#             )
#             scored.append(RetrievedDoc(id=doc.id, content=doc.content, score=float(match_count)))
#
#     # Sort by score descending and take top_k.
#     scored.sort(key=lambda d: d.score, reverse=True)
#     return scored[:top_k]
#
#
# def generate_answer(query: str, docs: List[RetrievedDoc]) -> str:
#     """
#     Placeholder answer generation:
#     - In a real implementation, this will build a prompt and call the local LLM.
#     - For now, it just stitches together relevant doc snippets.
#     """
#     if not docs:
#         return f"I don't have any relevant information yet, but you asked: {query}"
#
#     bullet_points = "\n".join(f"- {doc.content}" for doc in docs)
#     return (
#         f"Here is what I know related to your question:\n\n"
#         f"{bullet_points}\n\n"
#         f"(query was: {query})"
#     )
