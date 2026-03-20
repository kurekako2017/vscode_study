# Projects

`agent-lab/projects/` 用来存放这条学习线里的可运行样例。

这些样例不是按“技术炫酷程度”排，而是按更贴近日本 IT 现场和派遣案件需求的顺序整理。

## 推荐查看顺序

1. [chat_cli](D:/dev/source_code/vscode_study/agent-lab/projects/chat_cli/README.md)
2. [structured_output_demo](D:/dev/source_code/vscode_study/agent-lab/projects/structured_output_demo/README.md)
3. [doc_qa_agent](D:/dev/source_code/vscode_study/agent-lab/projects/doc_qa_agent/README.md)
4. [rag_api_demo](D:/dev/source_code/vscode_study/agent-lab/projects/rag_api_demo/README.md)
5. [tool_agent_demo](D:/dev/source_code/vscode_study/agent-lab/projects/tool_agent_demo/README.md)
6. [workflow_agent](D:/dev/source_code/vscode_study/agent-lab/projects/workflow_agent/README.md)

## 样例一览

| 项目 | 学习阶段 | 主要技术 | 现场对应场景 | 当前形态 |
|---|---|---|---|---|
| `chat_cli` | 阶段 1 | OpenAI API | 最基础模型调用验证 | CLI |
| `structured_output_demo` | 阶段 1 | Structured Output, Pydantic | 需求整理、分类、任务清单输出 | CLI |
| `doc_qa_agent` | 阶段 2 | 本地 RAG | 社内搜索、知识问答、资料检索 | CLI |
| `rag_api_demo` | 阶段 3 | FastAPI, RAG, PDF | 社内搜索 API、生成 AI 后端 PoC | API |
| `tool_agent_demo` | 阶段 4 | Tool Calling | 半自动资料调查助手 | CLI |
| `workflow_agent` | 阶段 5 | Workflow, Structured Output | 固定流程型 Agent、可控 PoC | CLI |

## 每个项目在日本现场里的意义

### `chat_cli`

- 作用：验证最基础的模型调用链路
- 对应能力：`Python + LLM API`
- 现场价值：低
- 学习价值：高

### `structured_output_demo`

- 作用：把自然语言请求稳定转成结构化数据
- 对应能力：`構造化出力`
- 现场价值：中
- 学习价值：高

### `doc_qa_agent`

- 作用：做最小 `RAG`
- 对应能力：`社内検索 / ナレッジ検索`
- 现场价值：高
- 学习价值：高

### `rag_api_demo`

- 作用：把 `RAG` 服务化
- 对应能力：`FastAPI + RAG + PDF`
- 现场价值：很高
- 学习价值：高

### `tool_agent_demo`

- 作用：做有限工具调用
- 对应能力：`Tool Calling`
- 现场价值：中
- 学习价值：高

### `workflow_agent`

- 作用：做固定步骤型工作流
- 对应能力：`Workflow Agent`
- 现场价值：中
- 学习价值：高

## 当前文档配套情况

| 项目 | README | 需求概要 | 基本设计 | 测试观点 | 简单测试用例表 |
|---|---|---|---|---|---|
| `chat_cli` | 有 | 无 | 无 | 无 | 无 |
| `structured_output_demo` | 有 | 无 | 无 | 无 | 无 |
| `doc_qa_agent` | 有 | 有 | 有 | 有 | 有 |
| `rag_api_demo` | 有 | 有 | 有 | 有 | 有 |
| `tool_agent_demo` | 有 | 有 | 有 | 有 | 有 |
| `workflow_agent` | 有 | 无 | 无 | 无 | 无 |

## 推荐继续补的顺序

如果继续往“更像日本现场交付物”的方向做，建议优先顺序是：

1. 给 `workflow_agent` 补 `需求概要` 和 `基本设计`
2. 给 `chat_cli` 或 `structured_output_demo` 补更进一步的测试资料
3. 给重点案例补更正式的 API / 评估资料
4. 再给后续项目补测试资料

## 成本与注意点

- 当前这些项目大多还是 PoC / 学习版，不是正式企业版系统。
- 只要发生模型调用，就会产生实际 API 成本。
- 当前最贴近案件要求的是 `doc_qa_agent` 和 `rag_api_demo`，建议优先打磨这两个。
- 如果要做作品集，优先展示：
  - `RAG`
  - `FastAPI`
  - `PDF / 文档处理`
  - 简化版需求与设计文档
