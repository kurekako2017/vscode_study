# ai-learn Codex Rules

> 放置位置：`ai-learn/AGENTS.md`
>
> 作用：作为 `ai-learn` 目录下所有 AI Agent / RAG / LangGraph / MCP / FastAPI / React 学习项目的总规则。
>
> 核心目标：生成的内容必须同时满足：
>
> ```text
> 可运行
> +
> 可学习
> +
> 可面试讲解
> +
> 可逐步企业级升级
> ```

---

# 0. Codex 自动调用 Skill / Teacher 规则

`ai-learn` 目录下存在本地 Teacher Skill 源码目录：

```text
ai-learn/
└── .codex-skill-build/
    ├── ai-agent-architect/
    ├── langgraph-teacher/
    ├── mcp-teacher/
    └── rag-teacher/
```
Codex 在回答、修改代码、补全文档、生成 README、解释示例、设计项目结构时，必须根据任务主题自动参考对应 Teacher Skill，不需要用户每次手动输入“使用某某 teacher”。

---

## 0.1 RAG Teacher 自动调用

涉及以下主题时，必须自动参考：

```text
.codex-skill-build/rag-teacher/
```

触发主题：

- RAG
- Retriever
- Embedding
- Vector Store / VectorDB
- FAISS / Chroma / Qdrant / Milvus
- Chunk
- Top-K
- Hybrid Search
- Rerank
- Context 组装
- 文档问答
- 知识库问答
- 来源引用
- 检索评估
- 企业级 RAG

默认解释链路：

```text
文档
→ Chunk
→ 检索
→ Top-K
→ Context
→ LLM / Answer Generator
→ 答案与来源
```

不允许只写“以后换成向量数据库”，必须说明当前代码中哪个函数、类或数据结构会被生产组件替换。

---

## 0.2 LangGraph Teacher 自动调用

涉及以下主题时，必须自动参考：

```text
.codex-skill-build/langgraph-teacher/
```

触发主题：

- LangGraph
- StateGraph
- State
- Node
- Edge
- 条件路由
- Workflow
- Checkpoint
- Interrupt
- Human in the loop
- 循环终止
- Supervisor
- 多 Agent 编排
- 状态持久化
- 失败恢复

默认解释方式：

```text
State
→ Node
→ Edge
→ 条件路由
→ Checkpoint / 恢复
→ Human Approval
→ 完成 / 失败
```

修改 LangGraph 示例时，必须解释每个 Node 的：

- 输入
- 输出
- 状态更新
- 为什么需要
- 企业级替换方向

---

## 0.3 MCP Teacher 自动调用

涉及以下主题时，必须自动参考：

```text
.codex-skill-build/mcp-teacher/
```

触发主题：

- MCP
- Model Context Protocol
- Tool Calling
- MCP Server
- MCP Client
- tools schema
- 参数校验
- 工具发现
- 权限控制
- 外部系统调用
- API 工具封装
- 人工审批
- 审计日志

默认解释链路：

```text
模型发现工具
→ 理解 Schema
→ 生成参数
→ 校验权限
→ 执行工具
→ 回填结果
→ 审计日志
```

---

## 0.4 AI Agent Architect 自动调用

涉及以下主题时，必须自动参考：

```text
.codex-skill-build/ai-agent-architect/
```

触发主题：

- AI Agent
- Agent 架构
- 多 Agent
- Planner / Executor
- Memory
- Tool Use
- Agentic Workflow
- 企业级 Agent
- 项目结构设计
- 从 Demo 升级真实项目
- LangChain + LangGraph + MCP 综合项目

默认设计视角：

- 角色
- 状态
- 工具
- 记忆
- 权限
- 失败处理
- 评估
- 监控
- 成本
- 人工审批

---

## 0.5 多主题组合规则

```text
RAG + LangGraph
=> rag-teacher + langgraph-teacher

RAG + MCP
=> rag-teacher + mcp-teacher

LangGraph + MCP
=> langgraph-teacher + mcp-teacher

Agent 综合项目
=> ai-agent-architect
=> 再按实际内容补充 rag-teacher / langgraph-teacher / mcp-teacher
```

---

# 1. 代码教学模式（强制）

## 1.1 项目定位

`ai-learn` 下所有项目不是单纯商业交付代码，而是：

```text
可运行项目
+
学习教材
+
日本现场面试素材
+
企业级升级样板
```

所以代码不能只追求短和快，必须方便初级学习者理解。

---

## 1.2 Backend 注释规则

所有核心 Backend 文件必须包含中文教学注释。

重点文件包括：

```text
main.py
api/routes/*.py
services/*.py
workflow/*.py
rag/*.py
agents/*.py
repositories/*.py
schemas/*.py
events/*.py
observability/*.py
config/*.py
```

每个核心文件顶部必须说明：

```text
文件职责
谁调用它
它调用谁
输入是什么
输出是什么
为什么需要这一层
日本现场面试怎么讲
```

---

## 1.3 Frontend 注释规则

所有核心 Frontend 文件必须包含中文教学注释。

重点文件：

```text
frontend/src/App.tsx
frontend/src/api.ts
frontend/src/components/*.tsx
frontend/src/features/**/*.tsx
frontend/src/types/*.ts
```

必须说明：

- 页面职责
- API 调用流程
- 状态变化
- SSE 如何连接
- 错误如何显示
- 与 Backend 哪个接口对应

---

## 1.4 Workflow 注释规则

所有 Workflow Node 必须说明：

- Node 名称
- 输入 State
- 输出 State
- 状态变化
- 为什么需要
- 企业级替换方案

---

## 1.5 Repository 注释规则

Repository 必须说明：

```text
当前实现
↓
未来企业级实现
```

例如：

```text
当前：
    SQLite / InMemory

未来：
    PostgreSQL + Alembic + Repository Interface
```

Service 层必须依赖 Interface 或抽象边界，不要直接绑定未来不可替换的实现。

---

## 1.6 日志注释规则

结构化日志字段必须说明用途：

```text
request_id    追踪一次 HTTP 请求
question_id   追踪业务对象
task_id       追踪异步任务
event         追踪状态变化
status        当前业务状态
error_code    错误分类
duration_ms   性能分析
```

禁止日志输出：

- API Key
- Secret
- 完整 Prompt
- 个人敏感信息
- 内部文档全文

---

## 1.7 缺失注释视为不合格

Codex 修改代码后必须检查：

- 是否有中文教学注释
- 是否有输入输出说明
- 是否有调用链说明
- 是否有面试讲解说明
- 是否有企业级映射说明

缺失时必须自动补充。

---

# 2. README / 学习文档强制结构

每个可运行项目至少应包含：

```text
README.md
RUNBOOK_LOCAL.md
CODE_STUDY_GUIDE.md
VERIFY_CHECKLIST.md
```

README 必须包含：

1. 项目定位
2. 快速启动
3. 核心调用链
4. 当前实现边界
5. 学习顺序
6. 面试讲解
7. 企业级扩展方向

---

# 3. 流程图展开规则

只要出现流程图，必须同时提供纯文本流程图，保证 VS Code 和 GitHub 都能看懂。

统一格式：

```text
用户输入 / HTTP 请求
│
▼
入口：FastAPI Route / React Event
│
▼
参数校验
├── 失败 -> Error Response
└── 成功
    │
    ▼
Service
│
▼
Workflow / Retriever / Agent
│
▼
Repository / Event Publisher
│
▼
最终输出
```

Mermaid 可以作为辅助，但不能代替纯文本主流程图。

---

# 4. 企业级演进规则

解释当前教学项目时，必须写出：

```text
当前实现
=
模拟的真实工程能力

↓ 企业级替换

生产组件 / 真实系统
```

例如：

```text
LocalStaticDocumentProvider
=
本地模拟社内文档检索

↓ 企业级 RAG

Wiki / FAQ / 工单
→ Chunk
→ Embedding
→ VectorDB / OpenSearch
→ ACL
→ Hybrid Search
→ Rerank
→ Context
→ LLM
→ Answer + Citation
```

---

# 5. RAG 类项目固定展开

RAG / 文档问答 / 社内知识库项目必须解释：

1. 文档来源
2. 文档切分
3. Retriever
4. Top-K
5. Rerank
6. Context
7. Answer Generator
8. Citation
9. ACL
10. 评估与监控

---

# 6. API / Streaming / Frontend 项目固定展开

涉及 FastAPI、SSE、React 时，必须说明：

- API 请求体
- API 响应体
- 统一错误结构
- request_id
- SSE event 类型
- error 后不能再发送 done
- Frontend 如何订阅事件
- Frontend 如何处理 loading / error / completed

---

# 7. 测试清单两列规则

测试文档中出现“测试清单”时，必须优先写成两列：

| 真实模型 / 真实服务命令 | 纯本地 / 本地 Provider 命令 |
|---|---|

如果项目当前不接真实服务，左列写：

```text
不适用（当前不调用真实服务）
```

右列写本地命令。

---

# 8. Codex 完成后的自检

每次修改后必须输出：

```text
修改文件:
新增文件:
未修改目录:
启动命令:
测试命令:
当前实现边界:
下一步建议:
```

如果是代码修改，还必须输出：

```text
注释覆盖:
日志覆盖:
测试结果:
学习文档是否同步:
```

# AI-LAB Project Governance V2

本项目继承 AI-LAB V2 全局治理规则。

开发前必须阅读：

1. `AGENTS.md`
2. `ROADMAP.md`
3. `docs/PROJECT_BACKLOG.md`
4. `TASK.md`

开发前还必须确认当前阶段、最高优先级任务、技术债和已知问题。

架构变化必须更新 `docs/ARCHITECTURE.md`；重要决策必须追加到 `docs/DECISIONS.md`。

开发完成后必须更新 `TASK.md`、`docs/PROJECT_BACKLOG.md` 和 `docs/CHANGELOG.md`，并保留全部历史记录。
