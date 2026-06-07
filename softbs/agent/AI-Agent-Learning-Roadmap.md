# AI Agent 开发学习路线（2026）

> 面向：
>
> - Python 开发者
> - 想学习 AI Agent / 自动化 / Coding Agent
> - 使用 VSCode / WSL / Codex / Cursor 的开发者

---

# 一、什么是 Agent？

Agent（智能代理）本质上是：

```text
LLM（大模型）
+
工具调用（Tools）
+
记忆（Memory）
+
工作流（Workflow）
+
自动执行能力
```

Agent 不只是聊天机器人。

它真正强的是：

- 自动读取文件
- 自动修改代码
- 自动操作浏览器
- 自动执行命令
- 自动完成工作流

---

# 二、推荐学习顺序（非常重要）

很多人一开始：

- RAG
- 向量数据库
- 多 Agent
- AutoGPT

全部一起学。

结果：

> 什么都懂一点，但不会真正开发。

正确路线：

```text
单 Agent
↓
Tool Calling
↓
Workflow
↓
状态管理
↓
多 Agent
↓
长期记忆
↓
RAG
↓
生产部署
```

---

# 三、最推荐的 GitHub 学习项目

---

## 1. ai-agents-from-zero（中文最佳）

GitHub：

https://github.com/didilili/ai-agents-from-zero

特点：

- 中文
- 从零开始
- 完整教程
- 有代码
- 有路线图
- 有实战

内容包括：

- Prompt
- RAG
- LangChain
- LangGraph
- MCP
- 多 Agent
- Workflow

推荐指数：

⭐⭐⭐⭐⭐

适合：

- 初学者
- Python 开发者
- 想做 Coding Agent 的人

---

## 2. Microsoft AI Agents for Beginners

GitHub：

https://github.com/microsoft/ai-agents-for-beginners

特点：

- 微软官方
- 教程结构清晰
- 适合入门
- 有图
- 有练习

推荐指数：

⭐⭐⭐⭐⭐

适合：

- 第一次接触 Agent
- 想理解 Tool Calling
- 想知道 Agent 如何工作

---

## 3. LangGraph（当前主流）

GitHub：

https://github.com/langchain-ai/langgraph

中文文档：

https://github.com/jurnea/LangGraph-Chinese

特点：

- 当前最主流 Agent Workflow 框架
- 状态管理强
- 企业级
- 非常适合 Coding Agent

推荐指数：

⭐⭐⭐⭐⭐

适合：

- 自动化
- Coding Agent
- 企业 Workflow

---

## 4. CrewAI（最容易做 AI 团队）

GitHub：

https://github.com/crewAIInc/crewAI

案例：

https://github.com/crewAIInc/crewAI-examples

特点：

- 最容易实现多 Agent
- AI 员工协作
- AI 团队系统

例如：

- PM Agent
- Dev Agent
- Review Agent
- Writer Agent

推荐指数：

⭐⭐⭐⭐

---

## 5. GenAI_Agents（案例库）

GitHub：

https://github.com/NirDiamant/GenAI_Agents

特点：

- 50+ Agent 案例
- Notebook
- 实战代码
- Tool Calling
- RAG
- 多 Agent

推荐指数：

⭐⭐⭐⭐⭐

---

## 6. Awesome AI Agents（资源导航）

GitHub：

https://github.com/jim-schwoebel/awesome_ai_agents

特点：

- Agent 项目大全
- 资源导航
- 持续更新

推荐指数：

⭐⭐⭐⭐

---

# 四、真正建议学习的技术栈

| 技术 | 推荐度 |
|---|---|
| Python | ⭐⭐⭐⭐⭐ |
| OpenAI API | ⭐⭐⭐⭐⭐ |
| LangGraph | ⭐⭐⭐⭐⭐ |
| Tool Calling | ⭐⭐⭐⭐⭐ |
| FastAPI | ⭐⭐⭐⭐ |
| MCP | ⭐⭐⭐⭐ |
| Redis | ⭐⭐⭐ |
| Docker | ⭐⭐⭐ |

---

# 五、推荐开发环境（适合你）

推荐：

```text
Windows
↓
WSL2 Ubuntu
↓
VSCode Remote WSL
↓
Python venv
↓
uv / pip
↓
Codex CLI
```

推荐工具：

| 工具 | 用途 |
|---|---|
| VSCode | 主开发 |
| Codex CLI | Coding Agent |
| Cursor | AI IDE |
| Ollama | 本地模型 |
| FastAPI | Agent API |
| Docker | 部署 |
| MCP | 工具连接 |

---

# 六、最适合练习的 Agent 项目

不要先做聊天机器人。

推荐：

---

## 1. 文件总结 Agent

功能：

- 自动读取目录
- 自动总结 README
- 自动生成文档

学习内容：

- Tool Calling
- 文件操作

---

## 2. Coding Agent

功能：

- 自动修复 Bug
- 自动修改代码
- 自动生成代码

学习内容：

- Workflow
- 状态管理

---

## 3. Browser Agent

功能：

- 自动操作网页
- 自动登录
- 自动填写表单

学习内容：

- Playwright
- MCP

---

## 4. Multi-Agent 系统

角色：

- PM Agent
- Dev Agent
- QA Agent

学习内容：

- CrewAI
- 多 Agent 协作

---

# 七、Agent 开发核心概念

---

## 1. Tool Calling

核心：

```python
def search_weather(city):
    return "25°C"
```

LLM 自动决定：

- 是否调用工具
- 调用哪个工具
- 如何使用结果

---

## 2. Memory（记忆）

包括：

- 短期记忆
- 长期记忆
- 向量记忆

---

## 3. Workflow

例如：

```text
用户输入
↓
分析任务
↓
调用工具
↓
生成结果
↓
保存记忆
```

---

## 4. MCP（非常重要）

MCP：

Model Context Protocol

作用：

让 AI：

- 控制 VSCode
- 控制浏览器
- 控制文件系统
- 控制终端

未来非常重要。

---

# 八、建议学习路线（按周）

---

## 第1周

学习：

- Prompt
- OpenAI API
- Function Calling

项目：

- 天气 Agent
- 文件读取 Agent

---

## 第2周

学习：

- LangChain
- LangGraph

项目：

- 文件总结
- 自动日报

---

## 第3周

学习：

- 多 Agent
- CrewAI

项目：

- AI 团队

---

## 第4周

学习：

- MCP
- Browser Agent
- Coding Agent

项目：

- 自动修 Bug
- 自动改代码

---

# 九、免费/低成本开发方案

推荐：

---

## 本地模型

推荐：

```text
Qwen2.5-Coder
DeepSeek
Gemma
Llama3
```

工具：

```text
Ollama
LM Studio
OpenWebUI
```

---

## API 节流

推荐：

- OpenRouter
- DeepSeek API
- Gemini Flash
- 本地模型 + 云模型混合

---

# 十、最终建议（非常重要）

不要：

- 一上来做 AutoGPT
- 一上来研究 RAG
- 一上来做超级复杂系统

先：

```text
小 Agent
↓
Workflow
↓
Tool Calling
↓
多步骤执行
```

真正能做项目后，再学习：

- 多 Agent
- 长期记忆
- 企业部署

成长会快很多。

---

# 十一、推荐收藏网站

OpenAI：

https://openai.com/

LangGraph：

https://langchain-ai.github.io/langgraph/

CrewAI：

https://docs.crewai.com/

LangChain：

https://python.langchain.com/

---

# 十二、最终推荐路线（最适合当前）

推荐：

```text
Python
↓
OpenAI API
↓
Tool Calling
↓
LangGraph
↓
Coding Agent
↓
MCP
↓
Browser Agent
↓
多 Agent
```

这是现在最主流、最实用的路线。

