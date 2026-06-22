# Codex + AGENTS.md 使用教程（ai-learn专用版）

## 为什么需要 AGENTS.md

AGENTS.md 用于统一 Codex、Claude Code、Cursor、Aider 等 AI 编程工具的行为规范。

作用：
- 项目开发规范
- AI助手工作规范
- 长期记忆与统一风格

避免：
- README风格不统一
- 代码结构不统一
- 模型调用方式不统一
- 测试命令不统一

---

## 推荐目录结构

ai-lab/
├── AGENTS.md
└── ai-learn/
    ├── AGENTS.md
    ├── agent-lab/
    ├── rag-lab/
    ├── langgraph-lab/
    ├── mcp-lab/
    └── projects/

---

## AGENTS.md 的作用范围

### 根目录
ai-lab/AGENTS.md

负责：
- Git规范
- 代码规范
- 文档规范

### 学习仓库
ai-learn/AGENTS.md

负责：
- OpenRouter优先
- NVIDIA第二优先
- Ollama第三优先
- Mock最后兜底

### 项目目录
projects/doc_qa_agent/AGENTS.md

负责：
- 项目特殊规则
- RAG要求
- README要求

---

## Codex 如何读取 AGENTS.md

进入目录：

cd ai-learn
codex

Codex 会自动读取：

ai-learn/AGENTS.md

通常不需要每次手动输入：

请先读取 AGENTS.md

---

## 如何确认规则生效

直接询问：

请告诉我当前生效的 AGENTS.md 规则

或者：

你当前读取到了哪些 AGENTS.md

---

## 推荐模型优先级

OpenRouter
↓
NVIDIA NIM
↓
Ollama(qwen2.5-coder:1.5b)
↓
Mock

---

## README统一规范

每个示例必须包含：

- 项目目标
- 项目结构
- 运行方式
- Real Mode
- Mock Mode
- 测试清单
- 学习重点
- 常见问题

---

## 命令统一规范

禁止：

cd example
python main.py

推荐：

python agent-lab/projects/demo/main.py

所有命令从 ai-learn 根目录执行。

---

## 测试清单规范

OpenRouter：
python xxx.py --provider openrouter

NVIDIA：
python xxx.py --provider nvidia

Ollama：
python xxx.py --provider ollama

Mock：
python xxx.py --mock

---

## Agent教学规范

每个 Agent 示例必须说明：

- Prompt
- Model
- Tool
- Memory
- State
- Workflow

执行链路：

输入 -> Agent -> Tool -> LLM -> 输出

---

## LangGraph教学规范

必须解释：

- State
- Node
- Edge
- Conditional Edge
- Graph执行流程

---

## RAG教学规范

Loader -> Chunk -> Embedding -> VectorStore -> Retriever -> Generation

---

## 多层 AGENTS 最佳实践

项目规则 > 子目录规则 > ai-learn规则 > 根目录规则

---

## 最常用 Codex 指令

创建项目：
按照 AGENTS 规则创建一个 LangGraph 项目

检查项目：
检查当前项目是否符合 AGENTS 规范

生成 README：
根据 AGENTS 规范补全 README

增加测试：
根据 AGENTS 规范生成测试清单

重构项目：
按照 AGENTS 规范重构整个项目

---

## 推荐工作流

1. 编写 AGENTS.md
2. 创建项目
3. 让 Codex 按规则生成代码
4. 自动生成 README
5. 补充测试清单
6. 提交 Git

形成统一风格的学习仓库。
