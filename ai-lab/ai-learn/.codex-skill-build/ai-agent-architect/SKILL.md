---
name: ai-agent-architect
description: Design enterprise AI agent systems with LangGraph, multi-agent coordination, MCP, and FastAPI. Use when producing agent architecture, repository structure, service boundaries, implementation roadmaps, deployment plans, production best practices, reliability controls, security models, observability, or performance optimization guidance.
---

# AI Agent Architect

Design production-oriented agent systems from requirements through deployment and operations.

## Workflow

1. Identify business goals, actors, tools, data, trust boundaries, SLAs, deployment constraints, and failure costs. State assumptions when information is missing.
2. Decide whether multiple agents are justified. Prefer multi-agent decomposition for distinct responsibilities, permissions, contexts, or scaling profiles; avoid needless agent-to-agent indirection.
3. Prefer LangGraph for explicit state, routing, persistence, interrupts, retries, and human approval workflows.
4. Prefer MCP for standardized model-facing tools and context; keep core business capabilities behind stable service APIs where appropriate.
5. Prefer FastAPI for typed HTTP boundaries, streaming endpoints, health checks, and service integration.
6. Produce a Mermaid system architecture diagram with clients, API layer, orchestration, agents, MCP servers, data stores, queues, model providers, and observability as applicable.
7. Produce a concrete repository tree and explain component ownership.
8. Define development order using vertical slices: contract and evaluation baseline, minimal workflow, tool integration, persistence, safety, observability, load testing, then deployment hardening.
9. Define deployment topology, CI/CD, configuration and secrets, scaling, rollback, disaster recovery, and environment separation.
10. Recommend measurable performance improvements based on latency, throughput, quality, and cost bottlenecks.

## Rules

- Include directory structure, architecture diagram, development sequence, deployment plan, enterprise best practices, and performance recommendations in every full design.
- Define state ownership, agent contracts, tool schemas, timeout and retry policy, idempotency, checkpoints, and human escalation paths.
- Address authentication, authorization, tenant isolation, prompt-injection defenses, data classification, secret management, auditability, and supply-chain controls.
- Address tracing, structured logs, metrics, token and cost accounting, offline evaluations, online quality signals, and incident response.
- Prefer bounded workflows and deterministic routing for critical actions. Require approval for irreversible or high-impact operations.
- Recommend caching, model routing, batching, parallel safe tool calls, context reduction, streaming, connection pooling, and backpressure only where supported by measured bottlenecks.
- Separate logical architecture from deployable services; do not turn every agent into a microservice without an operational reason.
- State alternatives and tradeoffs for important architectural decisions.

## Response Shape

Provide: assumptions and requirements, architecture decisions, Mermaid diagram, repository tree, component responsibilities, request flow, development order, deployment plan, best practices, performance plan, risks, and validation criteria.
