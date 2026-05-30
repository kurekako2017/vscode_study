# LLM Lab Projects

> 归位说明：可运行 demo 统一维护在 [../../agent-lab/projects](../../agent-lab/projects/README.md)。本目录只保留 `llm-lab` 主线的案例索引和评估资料，避免同一套运行说明在两个目录里重复维护。

## 1. 这个目录负责什么

`llm-lab/projects/` 负责回答：

```text
学习 LLM 应用主线时，应该跑哪些 demo？这些 demo 分别对应哪一章？
```

它不负责重复维护：

- demo 源码
- 每个 demo 的安装命令
- 每个 demo 的详细 README

这些内容统一看：

- [../../agent-lab/projects/README.md](../../agent-lab/projects/README.md)

## 2. 主线文档和案例对应关系

| 学习主题 | 主线文档 | 推荐 demo / 资料 | demo 实际位置 |
| --- | --- | --- | --- |
| 模型调用 | [../02-模型调用基础.md](../02-模型调用基础.md) | `chat_cli` | [../../agent-lab/projects/chat_cli](../../agent-lab/projects/chat_cli/README.md) |
| 结构化输出 | [../03-结构化输出.md](../03-结构化输出.md) | `structured_output_demo` | [../../agent-lab/projects/structured_output_demo](../../agent-lab/projects/structured_output_demo/README.md) |
| RAG | [../04-RAG.md](../04-RAG.md) | `doc_qa_agent` | [../../agent-lab/projects/doc_qa_agent](../../agent-lab/projects/doc_qa_agent/README.md) |
| FastAPI + RAG API | [../05-FastAPI与企业集成.md](../05-FastAPI与企业集成.md) | `rag_api_demo` | [../../agent-lab/projects/rag_api_demo](../../agent-lab/projects/rag_api_demo/README.md) |
| 评估与运维 | [../06-评估与运维.md](../06-评估与运维.md) | `rag_eval_notes.md` | [./rag_eval_notes.md](./rag_eval_notes.md) |

## 3. 推荐学习顺序

```text
chat_cli
  -> structured_output_demo
  -> doc_qa_agent
  -> rag_api_demo
  -> rag_eval_notes.md
```

这样安排的原因：

| 顺序 | 为什么 |
| --- | --- |
| `chat_cli` | 先确认你会调用模型 |
| `structured_output_demo` | 再让输出变成程序可处理的数据 |
| `doc_qa_agent` | 再进入 RAG 和社内搜索 |
| `rag_api_demo` | 再把 RAG 做成 HTTP API |
| `rag_eval_notes.md` | 最后学习如何判断质量和记录问题 |

## 4. 和 agent-lab/projects 的区别

| 目录 | 负责什么 |
| --- | --- |
| `agent-lab/projects/` | 保存可运行 demo、运行脚本、每个项目的 README / 设计 / 测试资料 |
| `llm-lab/projects/` | 保存 LLM 主线案例索引，以及 LLM 主线自己的评估笔记 |

也就是说：

- 想运行 demo：去 [../../agent-lab/projects](../../agent-lab/projects/README.md)。
- 想知道 LLM 主线该跑哪个 demo：看本文。
- 想学 RAG 评估：看 [rag_eval_notes.md](./rag_eval_notes.md)。

## 5. 日本现场作品集优先级

如果目标是日本现场或派遣案件，建议优先打磨：

1. `doc_qa_agent`
2. `rag_api_demo`
3. `rag_eval_notes.md`
4. `structured_output_demo`
5. `chat_cli`

原因：

- `RAG / 社内検索` 更贴近实际落地。
- `FastAPI + RAG API` 更像后端案件交付物。
- 评估资料能证明你不是只会“跑通 demo”。
- 结构化输出能体现你会把模型结果接到程序流程。
- 纯聊天 demo 主要用于证明基础，不适合作为作品集核心。

## 6. 成本与注意点

- 只要调用模型 API，就可能产生费用。
- demo 是学习版 PoC，不是企业正式系统。
- 不要复制多份 demo 源码造成维护混乱；优先复用 `agent-lab/projects`。
- 如果确实需要在 `llm-lab/projects` 下维护副本，再单独复制指定 demo。
