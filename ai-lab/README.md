# AI Lab

`ai-lab/` 是本工作区里生成 AI 学习资料的总入口，把原来的 `llm-lab/` 和 `agent-lab/` 放到同一个大目录下，方便在 IDE 里一次展开和查找。

建议顺序很简单：

1. 先走 [llm-lab](./llm-lab/README.md)：模型调用、结构化输出、RAG、FastAPI、评估与日本现场对照。
2. 再走 [agent-lab](./agent-lab/README.md)：Tool Calling、Agent 工作流、工具循环和进阶项目。

## 目录职责

| 目录 | 定位 | 适合什么时候看 |
| --- | --- | --- |
| [llm-lab](./llm-lab/README.md) | LLM 应用开发主线 | 想先做能落地的 `Python + RAG + FastAPI` PoC |
| [agent-lab](./agent-lab/README.md) | Agent 进阶专题和可运行 demo | 已经理解模型调用、结构化输出、RAG 后继续进阶 |

## 最短学习路线

1. [LLM 应用框架系统知识](./llm-lab/LLM应用框架系统知识.md)
2. [Python 学习范围](./llm-lab/00-Python学习范围（面向LLM应用开发）.md)
3. [LLM 学习路线](./llm-lab/01-学习路线.md)
4. [模型调用基础](./llm-lab/02-模型调用基础.md)
5. [结构化输出](./llm-lab/03-结构化输出.md)
6. [RAG](./llm-lab/04-RAG.md)
7. [FastAPI 与企业集成](./llm-lab/05-FastAPI与企业集成.md)
8. [Agent 学习路线](./agent-lab/01-学习路线.md)

## 可运行 Demo

可运行示例统一维护在 [agent-lab/projects](./agent-lab/projects/README.md)：

| 主题 | Demo |
| --- | --- |
| 模型调用 | [chat_cli](./agent-lab/projects/chat_cli/README.md) |
| 结构化输出 | [structured_output_demo](./agent-lab/projects/structured_output_demo/README.md) |
| 本地文档问答 RAG | [doc_qa_agent](./agent-lab/projects/doc_qa_agent/README.md) |
| FastAPI RAG 服务 | [rag_api_demo](./agent-lab/projects/rag_api_demo/README.md) |
| Tool Calling | [tool_agent_demo](./agent-lab/projects/tool_agent_demo/README.md) |
| Agent 工作流 | [workflow_agent](./agent-lab/projects/workflow_agent/README.md) |

## 常用命令

从工作区根目录运行：

```bash
python3 ai-lab/agent-lab/projects/chat_cli/main.py --mock "用一句话解释什么是 RAG"
python3 ai-lab/agent-lab/projects/structured_output_demo/main.py --mock "做一个客服 Agent 的开发计划"
python3 ai-lab/agent-lab/projects/doc_qa_agent/main.py --mock --docs ai-lab "这个目录的学习主线是什么？"
```

进入某个 demo 目录运行：

```bash
cd ai-lab/agent-lab/projects/chat_cli
python3 main.py --mock "你好"
```

## 目录结构

```text
ai-lab/
|-- README.md
|-- llm-lab/
|   |-- README.md
|   |-- 00-Python学习范围（面向LLM应用开发）.md
|   |-- 01-学习路线.md
|   |-- ...
|   `-- projects/
`-- agent-lab/
    |-- README.md
    |-- 01-学习路线.md
    |-- ...
    `-- projects/
        |-- chat_cli/
        |-- structured_output_demo/
        |-- doc_qa_agent/
        |-- rag_api_demo/
        |-- tool_agent_demo/
        `-- workflow_agent/
```
