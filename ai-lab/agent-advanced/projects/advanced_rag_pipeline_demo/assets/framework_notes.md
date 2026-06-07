# Framework Notes

LangChain 适合做链式编排、prompt 组合和工具调用。

LlamaIndex 更强调文档索引、节点化检索和查询引擎。

LangGraph 适合把复杂 Agent / RAG 流程拆成状态图，便于控制分支和回路。

## 什么时候自己写

- 只需要极简单的 RAG
- 需要完全可控的成本和行为
- 想先做原型，再考虑引入框架

## 什么时候上框架

- 有稳定的工程团队
- 需要统一抽象和可维护性
- 需要多节点、多工具、多 Agent 协调
