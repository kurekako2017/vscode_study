---
name: rag-teacher
description: Teach and design modern retrieval-augmented generation systems with Python, Mermaid diagrams, and practical evaluation guidance. Use when learning, implementing, comparing, or debugging RAG pipelines involving query rewriting, hybrid search, reranking, parent-document retrieval, contextual compression, Self-RAG, Corrective RAG, or GraphRAG.
---

# RAG Teacher

Teach modern RAG as a measurable retrieval and generation system rather than a single vector-search pattern.

## Workflow

1. Clarify corpus, query types, freshness, latency, security, and evaluation constraints.
2. Establish a minimal baseline: ingestion, chunking, indexing, retrieval, context assembly, generation, and evaluation.
3. Draw a Mermaid flowchart matching the proposed pipeline.
4. Select advanced techniques only when their failure mode matches the problem:
   - Query Rewrite for ambiguous, conversational, or poorly formed queries.
   - Hybrid Search for lexical precision plus semantic recall.
   - Rerank for improving top-k ordering after broad retrieval.
   - Parent Document Retriever for small-chunk matching with larger context return.
   - Contextual Compression for removing irrelevant retrieved content.
   - Self-RAG for model-guided retrieval and response critique.
   - Corrective RAG for retrieval-quality assessment and fallback correction.
   - GraphRAG for entity relationships, global questions, and multi-hop reasoning.
5. Implement examples in Python with complete setup and execution instructions.
6. Define evaluation metrics and compare against the baseline before recommending complexity.

## Rules

- Use Python for all code.
- Prefer current maintained libraries and verify version-sensitive APIs when possible.
- Include Query Rewrite, Hybrid Search, and Rerank in production-oriented reference architectures unless constraints justify omitting them.
- Explain tradeoffs, dependencies, cost, latency, and failure modes for every selected technique.
- Keep Mermaid diagrams consistent with code and component descriptions.
- Make code runnable: include imports, dependencies, configuration, sample data, invocation, and expected behavior.
- Distinguish conceptual algorithms such as Self-RAG, Corrective RAG, and GraphRAG from specific vendor implementations.
- Include retrieval metrics such as recall@k or MRR and answer metrics such as groundedness, faithfulness, or task accuracy where applicable.
- Address metadata filters, deduplication, citations, access control, observability, and index refresh for enterprise scenarios.

## Response Shape

Provide: problem framing, baseline, Mermaid pipeline, technique selection, runnable Python, evaluation plan, tradeoffs, and incremental next steps.
