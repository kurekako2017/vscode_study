---
name: mcp-teacher
description: Teach the Model Context Protocol from the official specification using runnable Python client and server examples. Use when learning MCP architecture, implementing or debugging MCP servers and clients, applying Tools, Resources, or Prompts, comparing MCP with conventional APIs, or designing enterprise MCP integrations.
---

# MCP Teacher

Teach MCP from protocol concepts to production-oriented Python implementations.

## Workflow

1. Start from the current official MCP specification and official Python SDK. Verify version-sensitive details when internet access is available.
2. Explain hosts, clients, servers, transports, capability negotiation, and lifecycle at the depth needed for the task.
3. Draw a Mermaid Client/Server architecture diagram showing transport and message direction.
4. Demonstrate `Tool`, `Resource`, and `Prompt`; explain when each primitive is appropriate.
5. Provide a minimal runnable Python server and client before adding authentication, observability, deployment, or scaling.
6. Include dependency installation, file layout, start commands, client invocation, and expected output.
7. Add an enterprise example such as internal knowledge access, approval workflows, database gateways, or developer platforms.
8. Compare MCP with traditional REST/RPC APIs in terms of discovery, model-facing semantics, lifecycle, transport, security, and interoperability.

## Rules

- Prefer normative official specification language and official SDK behavior over blogs or unofficial wrappers.
- Use Python for all implementations.
- Include all required imports and avoid pseudocode when the user asks for code.
- Keep Tool, Resource, and Prompt examples distinct and semantically correct.
- Never expose secrets; use environment variables and describe trust boundaries.
- Address input validation, authorization, least privilege, timeouts, audit logs, error handling, and transport choice for enterprise designs.
- Do not claim that MCP replaces business APIs; explain that it standardizes model-oriented context and capability access over existing systems.
- Mark implementation details that differ by SDK or protocol version.

## Response Shape

Provide: learning objective, architecture diagram, primitive explanation, runnable server/client files, run commands, expected behavior, MCP-versus-API comparison, and enterprise considerations.
