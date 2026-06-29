# frameworks

这个目录放框架专题的说明和 demo。

这里优先看文档，再跳到 `projects/` 里的可运行案例。

- `langchain/`
- `llamaindex/`
- `langgraph/`

每个框架建议都包含：

1. 解决什么问题
2. 核心抽象是什么
3. 最小运行示例
4. 和自研实现的对比

## 业务场景说明

- 适用场景：你已经知道要做什么问题，但还不确定该用哪类框架、哪个抽象最合适。
- 如果不用这种方式：很容易只记住 API 用法，却不知道框架适合解决什么业务问题。
- 解决的问题：先按问题域理解框架，再去看 demo 和代码，学习路径会更清晰。
- 举例说明：例如先拿“文档问答”或“工具调用”这类小问题比较 LangChain、LlamaIndex 和 LangGraph，看看哪种抽象最适合当前需求。

## 学习顺序

1. [langchain/](./langchain/README.md)
2. [llamaindex/](./llamaindex/README.md)
3. [langgraph/](./langgraph/README.md)

## 对应代码案例

| 框架 | 文档入口 | 代码入口 |
| --- | --- | --- |
| LangChain | [langchain/README.md](./langchain/README.md) | [projects/langchain_chain_demo](../projects/langchain_chain_demo/README.md) |
| LlamaIndex | [llamaindex/README.md](./llamaindex/README.md) | [projects/llamaindex_index_demo](../projects/llamaindex_index_demo/README.md) |
| LangGraph | [langgraph/README.md](./langgraph/README.md) | [projects/langgraph_workflow_demo](../projects/langgraph_workflow_demo/README.md) |

## 结构整理补充

### 1. 目录作用

`frameworks/` 是框架知识入口，负责解释框架解决什么问题、核心抽象、适用边界和学习顺序。完整可运行项目继续放在 `../projects/`，本目录通过链接与其关联。

### 2. 适合学习内容

- LangChain 的 Prompt、Runnable、Parser、Tool、Memory 和 Retriever。
- LangGraph 的 State、Node、Edge、条件路由、Checkpoint 和 Interrupt。
- LlamaIndex 的 Document、Node、Index 和 QueryEngine。
- 三类框架与自研实现、RAG、Agent 工作流之间的取舍。

### 3. 子目录说明

| 子目录 | 负责内容 | 项目关联页 |
| --- | --- | --- |
| [langchain](./langchain/README.md) | 链式编排、模型调用、解析、Tool 与 RAG 基础 | [相关项目链接](./langchain/相关项目链接.md) |
| [langgraph](./langgraph/README.md) | 状态图、分支、循环、多 Agent 与企业恢复能力 | [相关项目链接](./langgraph/相关项目链接.md) |
| [llamaindex](./llamaindex/README.md) | 文档、节点、索引、查询引擎与知识库概念 | [相关项目链接](./llamaindex/相关项目链接.md) |

### 4. 推荐学习顺序

1. LangChain：先理解线性组合和组件替换。
2. LlamaIndex：再理解文档到索引和查询的组织方式。
3. LangGraph：最后学习显式状态、条件路由、循环与恢复。
4. 每学一个框架，立即从关联页选择一个 demo 验证。

### 5. 相关实战项目

- [projects 总入口](../projects/README.md)
- [Agent Advanced 总索引](../INDEX.md)
- [RAG 专题](../rag/README.md)
- [Multi-Agent 专题](../multi-agent/README.md)

### 6. 注意事项

- 框架文档与项目代码保持物理分离，禁止为了目录整齐直接移动 demo。
- 关联页是导航，不复制项目 README 的完整运行说明。
- 项目是否真实依赖某框架，以代码导入和 requirements 为准。
- 新增框架时必须同时补 README、相关项目链接和总索引。
