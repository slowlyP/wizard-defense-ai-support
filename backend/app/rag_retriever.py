"""Deterministic keyword and topic retrieval for the local RAG baseline."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .rag_knowledge_base import KnowledgeChunk, RAG_KNOWLEDGE_CHUNKS


TOKEN_RE = re.compile(r"[0-9a-zA-Z가-힣]+")


@dataclass(frozen=True)
class RetrievalResult:
    chunk: KnowledgeChunk
    score: int
    matched_terms: tuple[str, ...]


def _normalize(text: str) -> str:
    return " ".join(TOKEN_RE.findall(text.casefold()))


def _tokens(text: str) -> set[str]:
    return set(TOKEN_RE.findall(text.casefold()))


def _score(query: str, query_tokens: set[str], chunk: KnowledgeChunk) -> tuple[int, tuple[str, ...]]:
    matched: list[str] = []
    score = 0
    for keyword in chunk.keywords:
        normalized_keyword = _normalize(keyword)
        if normalized_keyword and normalized_keyword in query:
            score += 12 + len(normalized_keyword.split()) * 2
            matched.append(keyword)

    title_tokens = _tokens(chunk.title)
    topic_tokens = _tokens(chunk.topic.replace("_", " "))
    content_tokens = _tokens(chunk.content)
    score += len(query_tokens & title_tokens) * 5
    score += len(query_tokens & topic_tokens) * 4
    score += len(query_tokens & content_tokens)
    return score, tuple(sorted(set(matched), key=str.casefold))


def retrieve_support_chunks(text: str, language: str = "ko", top_k: int = 3) -> list[RetrievalResult]:
    """Return stable, positive-score local knowledge matches.

    Empty, unrelated, and non-positive ``top_k`` inputs safely return an empty
    list. Same-language chunks are ranked first only after relevance score.
    """
    if top_k <= 0:
        return []
    query = _normalize(text)
    if not query:
        return []
    selected_language = "en" if language == "en" else "ko"
    query_tokens = _tokens(query)
    results: list[RetrievalResult] = []
    for chunk in RAG_KNOWLEDGE_CHUNKS:
        score, matched_terms = _score(query, query_tokens, chunk)
        if score > 0:
            results.append(RetrievalResult(chunk=chunk, score=score, matched_terms=matched_terms))

    results.sort(
        key=lambda result: (
            -result.score,
            result.chunk.language != selected_language,
            result.chunk.id,
        )
    )
    return results[:top_k]

