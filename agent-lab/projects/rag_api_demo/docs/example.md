# 示例文档：RAG 演示用

本文件为 rag_api_demo 的示例文档，用于本地 smoke-test 与教学演示。

## 项目简介

这个示例文档用于展示如何从本地文本中抽取信息并进行检索式问答（RAG）。

主要点：

- 本仓库包含多个教学用的 Agent demo（chat_cli、doc_qa_agent、rag_api_demo 等）。
- rag_api_demo 会把文档切分为多个 chunk，并基于关键词进行简单检索以构建上下文。

## 使用建议

1. 以 mock 模式运行服务以验证流程。
2. 将检索替换为 embeddings + 向量检索作为进阶任务。

示例问题：请总结上面项目简介与主要点。
