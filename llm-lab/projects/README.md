# Projects

`llm-lab/projects/` 用来整理这条主学习线里推荐优先看的案例。

当前为了避免重复维护，先直接复用 `agent-lab/projects/` 中已经完成的可运行样例。

## 推荐案例

1. [chat_cli](D:/dev/source_code/vscode_study/agent-lab/projects/chat_cli/README.md)
2. [structured_output_demo](D:/dev/source_code/vscode_study/agent-lab/projects/structured_output_demo/README.md)
3. [doc_qa_agent](D:/dev/source_code/vscode_study/agent-lab/projects/doc_qa_agent/README.md)
4. [rag_api_demo](D:/dev/source_code/vscode_study/agent-lab/projects/rag_api_demo/README.md)
5. [rag_eval_notes.md](D:/dev/source_code/vscode_study/llm-lab/projects/rag_eval_notes.md)

## 为什么先复用这些

因为这几项正好对应日本现场更常见的主线：

- 模型调用
- 结构化输出
- `RAG`
- `FastAPI + RAG API`
- `RAG` 评估意识

等后面内容继续增加，再考虑把这些样例独立复制或迁移到 `llm-lab/projects/`。

## 案例和案件能力映射表

| 案例 | 学习阶段 | 日本案件高频关键词 | 现场对应场景 | 可展示能力 | 注意点 |
|---|---|---|---|---|---|
| `chat_cli` | 阶段 1 | `Python`, `OpenAI API`, `PoC` | 最小模型调用验证 | 会调模型、会处理最基础请求与返回 | 现场价值有限，不能只停在这里 |
| `structured_output_demo` | 阶段 1 | `構造化出力`, `JSON`, `分類` | 需求整理、分类、任务清单、标签输出 | 会把自然语言结果稳定转成结构化数据 | 结果稳定性比“聊天效果”更重要 |
| `doc_qa_agent` | 阶段 2 | `RAG`, `社内検索`, `ナレッジ検索` | 规程问答、设计书检索、FAQ | 会做最小本地检索、带出处回答、基础资料问答 | 当前还是关键词检索，不是向量检索 |
| `rag_api_demo` | 阶段 3 | `FastAPI`, `RAG`, `PDF`, `API連携` | 社内検索 API、生成 AI 后端 PoC | 会把 `RAG` 做成可调用 API，支持 PDF | 最贴案件要求，建议优先打磨 |
| `rag_eval_notes` | 阶段 5 | `評価`, `精度確認`, `PoC結果整理` | `RAG` 试验结果整理、精度确认 | 会从“能跑”走向“可评估” | 不是代码案例，而是评估思路案例 |

## 如果按日本案件要求来准备作品集

建议优先展示顺序：

1. `doc_qa_agent`
2. `rag_api_demo`
3. `structured_output_demo`
4. `chat_cli`

原因是：

- `RAG` 更贴日本现场
- `FastAPI + RAG API` 更贴案件
- 结构化输出能体现可落地能力
- 纯聊天样例更多是入门证明，不是核心卖点

## 成本与注意点

- 当前这些案例大多还是学习版 / PoC 版，不是正式企业版系统。
- 只要发生模型调用，就会产生实际 API 成本。
- 如果用于找日本现场案件，最值得继续增强的是：
  - `doc_qa_agent`
  - `rag_api_demo`
- 如果后面要继续补案例，优先方向建议是：
  - 向量检索版 `RAG`
  - 带认证的 `RAG API`
  - 检索评估样例
