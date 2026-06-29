# ai-lab Codex Root Rules

> 放置位置：`ai-lab/AGENTS.md`
>
> 作用：作为整个 `ai-lab` 仓库的最上层规则。这里不要写太多技术细节，只负责规则继承、目录判断和输出要求。

---

## 1. 规则优先级

Codex 执行任务时，必须按以下顺序读取规则：

```text
当前项目目录 AGENTS.md
>
技术方向目录 AGENTS.md
>
ai-learn/AGENTS.md
>
ai-lab/AGENTS.md
```

如果多个规则冲突，以更靠近当前工作目录的 `AGENTS.md` 为准。

---

## 2. ai-learn 任务识别

只要任务涉及以下内容，默认属于 `ai-learn/` 范围：

- AI Agent
- RAG
- LangChain
- LangGraph
- MCP
- Tool Calling
- Retriever
- Chunk
- Embedding
- Vector Store / VectorDB
- Ollama
- OpenAI / Azure OpenAI
- FastAPI + React AI 项目
- retail-insight-ai
- internal-knowledge-approval-agent
- ai-agent-retail-handbook-v3

涉及这些任务时，Codex 必须继续读取并遵守：

```text
ai-learn/AGENTS.md
```

---

## 3. 默认工作目录

AI 学习、Agent 项目、RAG 项目、LangGraph 项目，默认应在：

```text
ai-lab/ai-learn/
```

下执行。

不要在 `ai-lab` 根目录直接生成学习项目代码，除非用户明确要求。

---

## 4. 修改前必须检查

开始修改前，Codex 必须优先检查：

```text
README.md
PROJECT_BIBLE.md
当前项目 AGENTS.md
ai-learn/AGENTS.md
```

如果用户明确禁止修改某些目录，必须严格遵守。

---

## 5. 禁止行为

- 不要忽略 `ai-learn/AGENTS.md`
- 不要把所有规则都复制到根目录
- 不要修改用户明确禁止的目录
- 不要为了“整理”而删除已有学习资料
- 不要自动接入真实 API Key、真实 LLM、真实外部服务

---

## 6. 输出要求

每次完成任务后，必须说明：

1. 修改了哪些文件
2. 新增了哪些文件
3. 没有修改哪些被保护目录
4. 如何启动
5. 如何测试
6. 当前实现边界
7. 下一步建议
