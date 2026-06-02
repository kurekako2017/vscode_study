# LLM Lab

`llm-lab/` 是生成 AI 应用开发的主线目录，目标是先把日本现场更常见、更容易交付的能力跑通：

- 模型调用
- 结构化输出
- `RAG / 社内検索`
- `FastAPI` 后端集成
- 评估与运维
- 日本现场应用和岗位关键词

这条线先解决“能做一个可靠 PoC”的问题；Agent 进阶统一放在 [../agent-lab](../agent-lab/README.md)。

## 推荐入口

如果第一次进入，按这个顺序看：

1. [LLM应用框架系统知识.md](./LLM应用框架系统知识.md)
2. [00-Python学习范围（面向LLM应用开发）.md](./00-Python学习范围（面向LLM应用开发）.md)
3. [01-学习路线.md](./01-学习路线.md)
4. [02-模型调用基础.md](./02-模型调用基础.md)
5. [03-结构化输出.md](./03-结构化输出.md)
6. [04-RAG.md](./04-RAG.md)
7. [05-FastAPI与企业集成.md](./05-FastAPI与企业集成.md)
8. [06-评估与运维.md](./06-评估与运维.md)
9. [07-日本现场应用与案件关键词.md](./07-日本现场应用与案件关键词.md)
10. [08-云平台与企业环境.md](./08-云平台与企业环境.md)
11. [09-岗位与技能要求对照.md](./09-岗位与技能要求对照.md)
12. [10-作品集与面试准备.md](./10-作品集与面试准备.md)

辅助资料：

- [术语速查表.md](./术语速查表.md)
- [日语对照速查表.md](./日语对照速查表.md)

## 学习主线

```text
Python 基础范围
  -> 模型调用
  -> 结构化输出
  -> RAG
  -> FastAPI 服务化
  -> 评估与运维
  -> 日本现场表达
  -> Agent 进阶
```

重点判断：

- 想找日本现场或派遣案件：优先打牢 `Python + RAG + FastAPI`。
- 想做作品集：优先打磨 `doc_qa_agent` 和 `rag_api_demo`。
- 想学 Agent：先完成本目录主线，再进入 [../agent-lab](../agent-lab/README.md)。

## 文档和 Demo 对应关系

可运行 demo 统一维护在 [../agent-lab/projects](../agent-lab/projects/README.md)，`llm-lab` 只保留教程、基础示例和评估资料。

| 学习主题 | 教程文档 | 对应 demo / 资料 |
| --- | --- | --- |
| 模型调用 | [02-模型调用基础.md](./02-模型调用基础.md) | [chat_cli](../agent-lab/projects/chat_cli/README.md) |
| 结构化输出 | [03-结构化输出.md](./03-结构化输出.md) | [structured_output_demo](../agent-lab/projects/structured_output_demo/README.md) |
| RAG | [04-RAG.md](./04-RAG.md) | [doc_qa_agent](../agent-lab/projects/doc_qa_agent/README.md) |
| FastAPI + RAG API | [05-FastAPI与企业集成.md](./05-FastAPI与企业集成.md) | [rag_api_demo](../agent-lab/projects/rag_api_demo/README.md) |
| 评估与运维 | [06-评估与运维.md](./06-评估与运维.md) | [rag_eval_notes.md](./rag_eval_notes.md) |
| Agent 进阶 | [../agent-lab/README.md](../agent-lab/README.md) | [tool_agent_demo](../agent-lab/projects/tool_agent_demo/README.md)、[workflow_agent](../agent-lab/projects/workflow_agent/README.md) |

## 常用命令

从工作区根目录运行：

```bash
# mock 模式运行 chat_cli
python3 ai-lab/agent-lab/projects/chat_cli/main.py --mock "用一句话解释什么是 agent"
# mock 模式运行 structured_output_demo
python3 ai-lab/agent-lab/projects/structured_output_demo/main.py --mock "做一个读取 Markdown 的摘要工具"
# mock 模式运行 doc_qa_agent 并指定文档目录
python3 ai-lab/agent-lab/projects/doc_qa_agent/main.py --mock --docs ai-lab "这个目录主要讲什么？"
```

进入 demo 目录运行：

```bash
# 进入 demo 目录
cd ai-lab/agent-lab/projects/chat_cli
# mock 模式快速测试
python3 main.py --mock "你好"
```

## 每篇文档的作用

| 文档 | 解决的问题 |
| --- | --- |
| [LLM应用框架系统知识.md](./LLM应用框架系统知识.md) | 先建立模型调用、RAG、评估、API 集成的系统视角 |
| [00-Python学习范围（面向LLM应用开发）.md](./00-Python学习范围（面向LLM应用开发）.md) | 明确 Python 学什么、暂时不学什么 |
| [01-学习路线.md](./01-学习路线.md) | 安排阶段路线和练习顺序 |
| [02-模型调用基础.md](./02-模型调用基础.md) | 跑通最小模型调用闭环 |
| [03-结构化输出.md](./03-结构化输出.md) | 用 schema 和 Pydantic 稳定输出 JSON |
| [04-RAG.md](./04-RAG.md) | 学文档读取、切分、检索、引用来源 |
| [05-FastAPI与企业集成.md](./05-FastAPI与企业集成.md) | 把能力包装成后端 API |
| [06-评估与运维.md](./06-评估与运维.md) | 建立测试观点、失败案例和上线意识 |
| [07-日本现场应用与案件关键词.md](./07-日本现场应用与案件关键词.md) | 对齐日本企业常见应用形态 |
| [08-云平台与企业环境.md](./08-云平台与企业环境.md) | 理解权限、网络、成本、云平台约束 |
| [09-岗位与技能要求对照.md](./09-岗位与技能要求对照.md) | 把学习内容翻译成岗位关键词 |
| [10-作品集与面试准备.md](./10-作品集与面试准备.md) | 把 demo 整理成可讲的 PoC 和作品集 |

## 目录结构

```text
llm-lab/
|-- README.md
|-- 00-Python学习范围（面向LLM应用开发）.md
|-- 01-学习路线.md
|-- 02-模型调用基础.md
|-- 03-结构化输出.md
|-- 04-RAG.md
|-- 05-FastAPI与企业集成.md
|-- 06-评估与运维.md
|-- 07-日本现场应用与案件关键词.md
|-- 08-云平台与企业环境.md
|-- 09-岗位与技能要求对照.md
|-- 10-作品集与面试准备.md
|-- examples/
`-- projects/
```
