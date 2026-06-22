# Codex 企业级开发手册（2026版）
适用目录：`ai-lab/ai-learn`

## 1. 这份手册解决什么问题

你的 `ai-learn` 仓库会逐渐包含：

- LangChain 1.x 示例
- LangGraph 示例
- MCP 示例
- RAG 示例
- Agent 项目
- 企业级实战案例

如果没有统一规则，Codex 每次生成的目录、README、测试命令、模型调用方式都会不一样。

所以建议用：

```text
AGENTS.md
+
统一项目模板
+
统一测试命令
+
统一模型调用策略
```

把整个学习仓库固定下来。

---

## 2. 推荐总目录结构

```text
ai-lab/
├── AGENTS.md
└── ai-learn/
    ├── AGENTS.md
    ├── .env
    ├── .env.example
    ├── requirements.txt
    ├── llm_runtime.py
    ├── README.md
    │
    ├── agent-lab/
    │   ├── AGENTS.md
    │   └── projects/
    │
    ├── rag-lab/
    │   ├── AGENTS.md
    │   └── projects/
    │
    ├── langgraph-lab/
    │   ├── AGENTS.md
    │   └── projects/
    │
    ├── mcp-lab/
    │   ├── AGENTS.md
    │   └── projects/
    │
    └── projects/
        └── doc_qa_agent/
```

---

## 3. AGENTS.md 分层规则

### ai-lab/AGENTS.md

放整个仓库通用规则：

- 不破坏已有结构
- 修改前先阅读 README
- 修改后说明改了哪些文件
- 所有文档优先使用中文

### ai-learn/AGENTS.md

放学习仓库规则：

- OpenRouter 第一优先
- NVIDIA 第二优先
- Ollama qwen2.5-coder:1.5b 第三优先
- Mock 最后兜底
- README 必须包含真实模型命令和 Mock 命令
- 所有命令必须从 `ai-learn` 根目录执行

### 子目录 AGENTS.md

例如：

```text
rag-lab/AGENTS.md
langgraph-lab/AGENTS.md
mcp-lab/AGENTS.md
```

放该技术方向的专属规则。

### 项目级 AGENTS.md

例如：

```text
projects/doc_qa_agent/AGENTS.md
```

放当前项目的特殊规则。

---

## 4. 模型调用统一策略

统一优先级：

```text
OpenRouter
↓
NVIDIA NIM
↓
Ollama qwen2.5-coder:1.5b
↓
Mock
```

原则：

- 不要默认直接 Mock
- 有真实 Key 时优先跑真实模型
- OpenRouter 和 NVIDIA 都失败后再跑本地 Ollama
- Ollama 也不可用时才用 Mock
- 所有示例必须保留 Mock 命令，方便无网络复习

---

## 5. .env.example 标准模板

```env
# OpenRouter
OPENROUTER_API_KEY=
OPENROUTER_MODEL=openai/gpt-4o-mini

# NVIDIA
NVIDIA_API_KEY=
NVIDIA_MODEL=nvidia/llama-3.1-nemotron-70b-instruct

# Ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:1.5b

# Default
DEFAULT_PROVIDER=openrouter
```

---

## 6. llm_runtime.py 标准职责

建议在 `ai-learn/llm_runtime.py` 里统一封装模型调用。

职责：

- 读取 `.env`
- 判断 provider
- 调用 OpenRouter
- 调用 NVIDIA
- 调用 Ollama
- 最后 fallback 到 Mock
- 给每个例子提供统一接口

示例接口：

```python
def call_llm(prompt: str, provider: str = "auto") -> str:
    pass
```

建议所有项目都调用这个统一入口，不要每个项目各写一套模型调用代码。

---

## 7. README 标准结构

每个项目 README 必须包含：

```md
# 项目名称

## 1. 这个例子学什么

## 2. 项目结构

## 3. 核心流程

## 4. Real Mode 运行

## 5. Mock Mode 运行

## 6. 测试清单

## 7. 核心代码说明

## 8. 常见错误

## 9. 下一步学习
```

---

## 8. 测试命令规范

所有命令必须从 `ai-learn` 根目录执行。

### OpenRouter

```bash
python agent-lab/projects/demo/main.py --provider openrouter
```

### NVIDIA

```bash
python agent-lab/projects/demo/main.py --provider nvidia
```

### Ollama

```bash
python agent-lab/projects/demo/main.py --provider ollama
```

### Mock

```bash
python agent-lab/projects/demo/main.py --mock
```

---

## 9. LangChain 项目模板

```text
langchain-lab/projects/example_name/
├── README.md
├── main.py
├── chains.py
├── prompts.py
├── mock.py
└── tests/
```

README 必须解释：

- Prompt 是什么
- Chain 是什么
- Runnable 是什么
- 输入输出是什么

---

## 10. LangGraph 项目模板

```text
langgraph-lab/projects/example_name/
├── README.md
├── main.py
├── graph.py
├── state.py
├── nodes.py
├── edges.py
├── mock.py
└── tests/
```

README 必须解释：

- State
- Node
- Edge
- Conditional Edge
- Graph 执行顺序

---

## 11. RAG 项目模板

```text
rag-lab/projects/example_name/
├── README.md
├── main.py
├── loader.py
├── splitter.py
├── retriever.py
├── generator.py
├── data/
├── mock.py
└── tests/
```

README 必须解释：

```text
Document
→ Chunk
→ Embedding
→ VectorStore
→ Retriever
→ LLM
→ Answer
```

---

## 12. MCP Server 项目模板

```text
mcp-lab/projects/example_name/
├── README.md
├── server.py
├── client_demo.py
├── tools.py
├── resources.py
├── prompts.py
└── tests/
```

README 必须解释：

- MCP 是什么
- Tool 是什么
- Resource 是什么
- Prompt 是什么
- Client 如何调用 Server

---

## 13. Agent 项目模板

```text
agent-lab/projects/example_name/
├── README.md
├── main.py
├── agent.py
├── tools.py
├── memory.py
├── mock.py
└── tests/
```

README 必须解释：

- Agent 接收什么输入
- Agent 如何决定是否调用工具
- Tool 如何执行
- LLM 如何生成最终回答
- Memory 是否参与

---

## 14. Codex 常用指令模板

### 创建新项目

```text
请按照 ai-learn/AGENTS.md 规则，在 langgraph-lab/projects 下创建一个新的 LangGraph 示例项目。
要求包含 README、main.py、graph.py、state.py、nodes.py、mock.py。
所有运行命令必须从 ai-learn 根目录执行。
```

### 检查项目

```text
请检查当前项目是否符合 ai-learn/AGENTS.md 规范。
重点检查 README、真实模型命令、Mock命令、目录结构、模型优先级。
```

### 重构项目

```text
请按照 ai-learn/AGENTS.md 规则重构当前项目。
不要删除已有学习内容。
优先保持初学者能看懂。
```

### 补全 README

```text
请根据当前代码补全 README。
必须包含项目目标、项目结构、运行方式、Real Mode、Mock Mode、测试清单、学习重点、常见问题。
```

---

## 15. 推荐 Git 提交规范

```bash
git add .
git commit -m "docs: add codex agents guide"
git commit -m "feat: add langgraph demo"
git commit -m "refactor: unify llm runtime"
git commit -m "test: add mock mode commands"
```

---

## 16. 最佳工作流

1. 先写 AGENTS.md
2. 再让 Codex 创建项目
3. 让 Codex 生成 README
4. 手动运行真实模型命令
5. 如果 Key 不通，运行 Ollama
6. 如果 Ollama 不通，运行 Mock
7. 让 Codex 修复错误
8. 提交 Git

---

## 17. 你的 ai-learn 仓库最终目标

让它变成一个长期可复习的 AI Agent 学习仓库：

```text
LangChain 1.x
→ LangGraph
→ RAG
→ MCP
→ Agent
→ 企业级项目
```

核心原则：

```text
能运行
能理解
能复习
能扩展
```
