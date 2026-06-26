# AI Learn

## 模型调用回退顺序

所有会调用 LLM 的 Python 示例共用 `llm_runtime.py`，默认顺序为：

1. OpenRouter（`OPENROUTER_API_KEY`，兼容旧变量名 `openRouter`）
2. NVIDIA NIM（`NVIDIA_API_KEY`）
3. 本地 Ollama（`qwen2.5-coder:1.5b`）
4. Mock（仅前三项全部调用失败时使用）

模型、地址和超时可参考 `.env.example` 覆盖。真实密钥只能放在 WSL 环境变量或被 Git 忽略的 `.env` 中，不能写入代码、README 或 `.env.example`。

`ai-learn/` 统一承载三条递进学习线：

```text
llm-lab → agent-lab → agent-advanced
```

从仓库根目录开始学习时，直接使用：

- [整体学习顺序与运行指南](./整体学习顺序与运行指南.md)：每个示例的名称、顺序、全局命令和配套文档。
- [LLM Lab](./llm-lab/README.md)：Python、模型调用、结构化输出和基础 RAG。
- [Agent Lab](./agent-lab/README.md)：Tool Calling、工作流、RAG API 和流式服务。
- [Agent Advanced](./agent-advanced/README.md)：高级 RAG、LangGraph、MCP、Multi-Agent、Deep Research 和业务作品集。
- [术语速查表](./术语速查表.md)：三条学习线共用术语。

所有总览文档中的命令默认在仓库根目录 `ai-lab/` 执行。

## 学习教材入口

- [2026 企业级 AI Agent 开发学习笔记（完整版）](./2026企业级AI-Agent开发学习笔记_完整版.md)：按 Python + FastAPI、RAG、LangChain、LangGraph、MCP、企业级完整项目六卷整理的系统化教材。
