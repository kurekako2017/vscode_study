# LlamaIndex

这个章节讲 LlamaIndex 的索引和查询引擎思路。

## 业务场景说明

- 适用场景：文档较多、需要先建索引再查询的知识库、文档检索和问答系统。
- 如果不用这种方式：每次都全量扫文档会慢，而且数据一多就不利于扩展和复用。
- 解决的问题：用索引和查询引擎把文档处理流程标准化，方便组织检索和回答。
- 举例说明：例如先用一批项目文档建索引，再问“报销流程在哪一页提到过”，看看检索和引用效果是否稳定。

## 先看什么

1. Document 如何变成 Node
2. Node 如何进入 Index
3. QueryEngine 如何把检索和回答组织起来

## 对应代码

- [projects/llamaindex_index_demo](../../projects/llamaindex_index_demo/README.md)

## 学习目标

- 看懂索引和节点的关系
- 看懂查询引擎的职责
- 理解 LlamaIndex 在知识库检索里的位置

## 结构整理补充

### 1. 目录作用

本目录是 LlamaIndex 心智模型入口，负责 Document、Node、Index、Retriever 和 QueryEngine 的职责关系；代码示例保持在 `../../projects/`。

### 2. 适合学习内容

- 文档如何切成可检索节点。
- 索引与向量数据库的关系。
- QueryEngine 如何组织检索、上下文和回答。
- LlamaIndex、LangChain RAG 与自研管线的边界。

### 3. 子目录与文件说明

当前没有下级子目录，学习入口由以下文件组成：

| 文件 | 用途 |
| --- | --- |
| [README.md](./README.md) | LlamaIndex 核心概念和学习目标 |
| [相关项目链接.md](./相关项目链接.md) | 概念 demo、向量库和 RAG 项目导航 |

### 4. 推荐学习顺序

1. 阅读本 README 建立 Document → Node → Index → QueryEngine 链路。
2. 运行 `llamaindex_index_demo` 概念版。
3. 运行向量数据库最小 demo。
4. 比较高级 RAG 管线和企业混合检索。

### 5. 相关实战项目

统一查看 [LlamaIndex 相关项目链接](./相关项目链接.md)。

### 6. 注意事项

- 当前 `llamaindex_index_demo` 是概念教学版，不代表已接入真实 `llama_index` SDK。
- 生产实现还需要真实向量后端、持久化、ACL、引用和评估。
- 不移动 demo，避免破坏 assets 和运行命令。
