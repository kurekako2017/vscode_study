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

## 结构整理补充

### 1. 目录作用

本目录是 LangChain 学习文档入口，负责概念、抽象、适用场景和学习顺序；可运行代码保持在 `../../projects/`。

### 2. 适合学习内容

- `Prompt → Model → Parser` 最短链路。
- Runnable 组合、结构化输出和组件替换。
- Tool Calling、Memory、Retriever、RAG 与 Agent 的职责区别。

### 3. 子目录与文件说明

当前没有下级子目录，学习入口由以下文件组成：

| 文件 | 用途 |
| --- | --- |
| [README.md](./README.md) | LangChain 章节入口与学习目标 |
| [LangChain学习笔记.md](./LangChain学习笔记.md) | 更完整的概念学习笔记 |
| [相关项目链接.md](./相关项目链接.md) | 从文档跳转到基础 demo、RAG 和企业检索项目 |

### 4. 推荐学习顺序

1. 阅读本 README 建立链式编排概念。
2. 阅读 LangChain 学习笔记。
3. 运行 `langchain_chain_demo` 的 mock 模式。
4. 进入 `advanced_rag_pipeline_demo` 看真实 LangChain 组件。

### 5. 相关实战项目

统一查看 [LangChain 相关项目链接](./相关项目链接.md)。

### 6. 注意事项

- 并非所有相关 RAG 项目都直接依赖 LangChain。
- 不要把真实 API Key 写入命令、README 或代码；优先使用 mock 模式。
- 不移动 `projects/` 中的 demo，避免破坏 assets、requirements 和运行路径。
