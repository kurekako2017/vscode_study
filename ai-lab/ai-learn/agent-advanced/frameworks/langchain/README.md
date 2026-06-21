# LangChain

这个章节讲 LangChain 的链式编排思路。

如果你是从“图片里的学习内容”过来的，建议先看这份更完整的入门笔记：

- [LangChain 学习笔记](./LangChain学习笔记.md)

## 业务场景说明

- 适用场景：业务流程可以拆成多个可复用步骤，例如提示词组织、模型调用、输出解析和结果加工。
- 如果不用这种方式：相关逻辑容易散在各处，修改链路时会更难维护和复用。
- 解决的问题：用链式编排把步骤连起来，适合构建稳定、可替换的模型处理流水线。
- 举例说明：例如先做一个“输入问题 -> 检索资料 -> 生成摘要”的小链路，确认 LangChain 的串联方式是否适合当前项目。

## 先看什么

1. `LangChain` 解决什么问题
2. `Prompt -> Model -> Parser` 这条最小链路长什么样
3. `Runnable` 为什么能把组件串起来

## 对应代码

- [projects/langchain_chain_demo](../../projects/langchain_chain_demo/README.md)

## 学习目标

- 看懂 Prompt 模板
- 看懂 Runnable 组合
- 看懂结构化输出
- 理解什么时候适合自己写，什么时候适合用框架
- 看懂 Tool Calling、Memory、Retriever、RAG、Agent 这些概念分别在解决什么问题
