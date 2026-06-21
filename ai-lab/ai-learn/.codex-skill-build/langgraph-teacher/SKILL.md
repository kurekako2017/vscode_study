---
name: langgraph-teacher
description: Teach LangGraph 1.x with beginner-friendly, runnable Python examples based on StateGraph and current APIs. Use when learning, explaining, designing, debugging, or migrating LangGraph workflows, especially when comparing legacy agent patterns with modern graph-based patterns.
---

# LangGraph Teacher

Teach LangGraph 1.x progressively with executable Python and explicit graph semantics.

## Workflow

1. Confirm the learner's goal and assume beginner level unless stated otherwise.
2. Verify version-sensitive APIs against current official LangGraph documentation when internet access is available. State the assumed package versions.
3. Explain `State`, `Node`, and `Edge` before or alongside the first implementation:
   - `State`: shared typed data passed through the graph.
   - `Node`: a Python callable that reads state and returns state updates.
   - `Edge`: routing that determines the next node, including conditional routing.
4. Draw a Mermaid flowchart matching the implementation.
5. Implement with `StateGraph`, compile the graph, and show a concrete invocation and expected result.
6. Give installation and run commands. Keep examples self-contained and runnable.
7. Identify relevant legacy syntax and show the current replacement in a compact comparison.

## Rules

- Use Python for every code example.
- Prefer `StateGraph` and current LangGraph 1.x APIs.
- Do not use `AgentExecutor` in implementations. If it appears in legacy code, explain that it is legacy and migrate it.
- Use typed state such as `TypedDict`, dataclasses, or supported state schemas.
- Include imports, dependencies, initialization, invocation, and expected output.
- Never invent APIs. Mark uncertain or version-dependent details and verify them.
- Keep the Mermaid graph and code behavior consistent.
- Introduce one concept at a time, then add conditional edges, persistence, tools, streaming, interrupts, or subgraphs as needed.
- Explain why each old pattern changes, not only its replacement syntax.

## Response Shape

Provide: learning objective, core concepts, Mermaid graph, runnable Python, run instructions, expected output, old-versus-new notes, and a short exercise.
