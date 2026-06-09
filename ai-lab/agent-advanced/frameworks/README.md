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
