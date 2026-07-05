# Retail Insight AI

Retail Insight AI 是一个面向日本现场 AI Agent 学习的经营分析项目。它的目标不是只给出一个 Demo，而是让你能把一个完整链路跑通、看懂、讲清楚，再逐步向企业级架构演进。

项目主链路是：

```text
React → FastAPI → Task API → TaskService → Workflow → KPI Engine → Research Provider → Report Generator → SSE → React
```

当前项目定位是：

- 可运行
- 可学习
- 可面试讲解
- 可逐步企业级升级

## 当前阶段

当前默认阶段是：

- Local Static Provider
- InMemory / Local Repository
- FastAPI
- React
- SSE

当前明确不接入：

- 真实 OpenAI
- 真实 LLM
- PostgreSQL
- Redis
- RabbitMQ
- 真实外部业务系统

## 最短阅读路径

| 顺序 | 先看什么 | 目的 | 不建议一开始看什么 |
| --- | --- | --- | --- |
| 1 | `README.md` | 先知道项目是什么、当前边界是什么 | 全量 backlog 历史和长篇架构细节 |
| 2 | [docs/LEARNING_API_WALKTHROUGH.md](./docs/LEARNING_API_WALKTHROUGH.md) | 先知道怎么启动、怎么验证、怎么按接口学习 | 过深的实现细节和未来规划 |
| 3 | [CODE_STUDY_GUIDE.md](./CODE_STUDY_GUIDE.md) | 先知道代码应该按什么顺序读 | 先看前端细节或测试细枝末节 |

## 文档导航中心

这部分是整套文档的入口索引。目标是把“项目是什么、怎么启动、怎么学、怎么测、怎么面试、怎么维护”分开，避免同类内容分散维护。

### 各文档作用

| 文档 | 作用 | 适合谁 |
| --- | --- | --- |
| [README.md](./README.md) | 项目入口，看项目是什么、怎么启动、先读什么 | 所有人，尤其是第一次进入项目的人 |
| [RUNBOOK_LOCAL.md](./RUNBOOK_LOCAL.md) | 本地启动与排错 | 需要在本地把项目跑起来的人 |
| [VERIFY_CHECKLIST.md](./VERIFY_CHECKLIST.md) | 启动后怎么确认项目正常 | 想快速确认系统状态的人 |
| [CODE_STUDY_GUIDE.md](./CODE_STUDY_GUIDE.md) | 看源码的顺序 | 想读懂实现的人 |
| [docs/LEARNING_API_WALKTHROUGH.md](./docs/LEARNING_API_WALKTHROUGH.md) | 按 Swagger 跑完整主链路 | 初学者和需要跑通流程的人 |
| [docs/TEST_CASES.md](./docs/TEST_CASES.md) | 测试文件、测试输入、预期输出、测试命令 | 想知道“每个测试保护什么”的人 |
| [docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md](./docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md) | 日本项目面试讲解稿 | 要准备日本项目面试的人 |
| [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) | 系统架构 | 需要理解分层和边界的人 |
| [docs/API_CONTRACT.md](./docs/API_CONTRACT.md) | API 契约 | 需要确认接口合同的人 |
| [docs/EVENT_CONTRACT.md](./docs/EVENT_CONTRACT.md) | 事件契约 | 需要确认 SSE / event 语义的人 |
| [docs/ERROR_CATALOG.md](./docs/ERROR_CATALOG.md) | 错误码说明 | 排错、联调、测试设计的人 |
| [docs/DATABASE.md](./docs/DATABASE.md) | 数据库设计 | 需要看存储结构的人 |
| [TASK.md](./TASK.md) | 当前任务和阶段状态 | 需要知道现在在做什么的人 |
| [ROADMAP.md](./ROADMAP.md) | 路线图和阶段规划 | 需要知道后续方向的人 |
| [docs/PROJECT_BACKLOG.md](./docs/PROJECT_BACKLOG.md) | 项目待办和历史完成记录 | 需要追踪技术债和历史的人 |
| [docs/CHANGELOG.md](./docs/CHANGELOG.md) | 变更日志 | 需要看本次改了什么的人 |
| [docs/MASTER_PROMPT.md](./docs/MASTER_PROMPT.md) | AI 执行规则 | 所有 AI 工具和维护者 |
| [docs/CODING_STANDARD.md](./docs/CODING_STANDARD.md) | 编码规范 | 需要改代码的人 |
| [docs/DEVELOPMENT_GUIDE.md](./docs/DEVELOPMENT_GUIDE.md) | 开发流程 | 需要做功能修改的人 |

### 初学者先读的 5 个文档

1. `README.md`
2. `RUNBOOK_LOCAL.md`
3. `VERIFY_CHECKLIST.md`
4. `docs/LEARNING_API_WALKTHROUGH.md`
5. `CODE_STUDY_GUIDE.md`

### 面试准备先读的 3 个文档

1. `README.md`
2. `docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md`
3. `docs/ARCHITECTURE.md`

### 开发维护再看的详细设计文档

1. `docs/API_CONTRACT.md`
2. `docs/EVENT_CONTRACT.md`
3. `docs/ERROR_CATALOG.md`
4. `docs/DATABASE.md`
5. `docs/MASTER_PROMPT.md`
6. `docs/CODING_STANDARD.md`
7. `docs/DEVELOPMENT_GUIDE.md`
8. `TASK.md`
9. `ROADMAP.md`
10. `docs/PROJECT_BACKLOG.md`
11. `docs/CHANGELOG.md`

### 不要一开始看的文档

1. `docs/MASTER_PROMPT.md`
2. `docs/API_CONTRACT.md`
3. `docs/EVENT_CONTRACT.md`
4. `docs/DATABASE.md`
5. `docs/CHANGELOG.md`
6. `docs/PROJECT_BACKLOG.md`
7. `ROADMAP.md`
8. `TASK.md`

### 文档数量控制规则

- 不要随意新增 Markdown 文档。
- 同类内容优先合并到现有文档。
- `README.md` 负责导航。
- `docs/LEARNING_API_WALKTHROUGH.md` 负责运行学习。
- `docs/TEST_CASES.md` 负责测试学习。
- `docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md` 负责面试。
- `RUNBOOK_LOCAL.md` 负责启动排错。
- `VERIFY_CHECKLIST.md` 负责验证。
- `CODE_STUDY_GUIDE.md` 负责源码阅读。

## 第一次启动项目

第一次启动时，按下面顺序执行。每一步都只做一件事，便于你把“命令、作用、结果、排错”对应起来。

| 步骤 | 命令 | 作用 | 成功标志 | 失败现象 | 下一步操作 |
| --- | --- | --- | --- | --- | --- |
| 1 | `./scripts/check_env.sh` | 检查 Python、Node、npm 等本地环境是否满足最低要求 | 终端显示检查通过，且版本号满足要求 | 脚本报错、版本过低、找不到命令 | 先修复本地环境，再继续第 2 步 |
| 2 | `./scripts/start_backend.sh` | 启动 FastAPI 后端 | 终端出现 `Uvicorn running on http://127.0.0.1:8000` 和 `Application startup complete` | `ModuleNotFoundError`、`Address already in use`、`ImportError` | 先按后端终端日志排错，再回到第 2 步 |
| 3 | `./scripts/start_frontend.sh` | 启动 React 前端 | 终端出现 `Local: http://127.0.0.1:5173/` | 5173 端口占用、npm 依赖未安装、Vite 启动失败 | 先处理前端终端日志，再回到第 3 步 |
| 4 | 打开 `http://127.0.0.1:8000/docs` | 查看 Swagger，确认 API 已注册 | 页面能正常打开并列出接口 | 浏览器无法访问、页面空白、返回 404 | 回到第 2 步确认后端是否真的启动 |
| 5 | 打开 `http://127.0.0.1:5173` | 查看前端页面，确认页面能连到后端 | 页面可打开，能看到项目界面 | 页面白屏、按钮无响应、请求失败 | 检查前端终端和浏览器 Network |
| 6 | `./scripts/run_tests.sh` | 做一次完整的本地验证 | Backend tests、Frontend tests、Frontend build、Python compileall 都通过 | 某一阶段失败，脚本停在第一个错误处 | 先修复最早失败的阶段，再重新执行 |

如果你只想先快速确认最小运行链路，可以优先看 [docs/LEARNING_API_WALKTHROUGH.md](./docs/LEARNING_API_WALKTHROUGH.md)。

## 当前能力与边界

当前项目已经可以稳定运行的能力包括：

- `POST /api/tasks`
- `GET /api/tasks/{task_id}`
- `GET /api/tasks/{task_id}/events`
- `GET /api/tasks/{task_id}/report`
- `GET /api/v1/documents`
- `GET /api/v1/documents/{document_id}`
- `POST /api/v1/documents`
- `POST /api/v1/documents/{document_id}/import`
- `POST /api/v1/documents/{document_id}/chunks`
- `POST /api/v1/document-retrieval/search`
- `POST /api/v1/internal-rag/answer`
- `POST /api/v1/reports/{task_id}/submit-approval`
- `GET /api/v1/approvals`
- `GET /api/v1/approvals/{approval_id}`
- `POST /api/v1/approvals/{approval_id}/approve`
- `POST /api/v1/approvals/{approval_id}/reject`
- `GET /api/v1/users/me`
- `GET /api/v1/security/roles`
- `GET /api/v1/security/permissions`
- `GET /api/v1/audit-logs`

当前明确还没有接入的能力包括：

- 前端 UI 打磨
- PostgreSQL 仓库全面迁移
- 真实认证
- JWT / OAuth
- 真实 LLM 提供方
- pgvector
- 互联网搜索
- MCP
- 生产部署

## 项目结构

```text
retail-insight-ai/
├── backend/                    # FastAPI 后端，包含 API、Service、Repository、Model
│   ├── app/                    # 后端应用主体
│   │   ├── api/                # 接口层，负责 HTTP 路由和请求响应
│   │   ├── services/           # 业务服务层，负责用例编排
│   │   ├── workflow/           # 工作流层，负责任务流转和分支控制
│   │   ├── kpi/                # KPI 计算层，负责确定性指标
│   │   ├── agents/             # Agent 和 Provider 抽象
│   │   ├── reports/            # 报告生成层
│   │   ├── repositories/       # 仓储层，负责数据读写抽象
│   │   ├── errors/             # 错误码和异常处理
│   │   ├── events/             # 事件和 SSE 相关实现
│   │   ├── observability/      # 日志、request_id、观测相关
│   │   ├── models/             # 领域模型
│   │   ├── schemas/            # 请求/响应 DTO
│   │   └── config/             # 配置与依赖注入
│   ├── tests/                  # 后端测试
│   ├── Dockerfile              # 后端镜像
│   └── requirements.txt        # Python 依赖
├── frontend/                   # React 前端，目前不是主学习路径
│   ├── src/                    # 前端代码
│   ├── Dockerfile              # 前端镜像
│   ├── nginx.conf              # 静态页面与后端代理配置
│   └── package.json            # 前端依赖与脚本
├── docs/                       # 架构、学习、测试、面试和契约文档
├── scripts/                    # 启动、检查、验证脚本
└── docker-compose.yml          # PostgreSQL 等本地服务预留
```

## 文档同步

本项目与 `ai-agent-retail-handbook-v3` 共用文档同步机制。同步脚本位于 [ai-learn/scripts/sync_retail_handbook_docs.py](../scripts/sync_retail_handbook_docs.py)，同步范围由 [doc-sync.manifest.json](../doc-sync.manifest.json) 管理。

- 同步只刷新文档末尾的 `DOC-SYNC` 区块，不覆盖正文。
- 本项目文档变化后，需要刷新同步器，让 handbook 侧对应文档一起更新。

## 学习顺序建议

1. 先启动后端和前端。
2. 再用 Swagger 看接口形状。
3. 再按 [docs/LEARNING_API_WALKTHROUGH.md](./docs/LEARNING_API_WALKTHROUGH.md) 逐个接口验证。
4. 再看 [CODE_STUDY_GUIDE.md](./CODE_STUDY_GUIDE.md) 理解源码顺序。
5. 最后对照 [docs/TEST_CASES.md](./docs/TEST_CASES.md) 和 [VERIFY_CHECKLIST.md](./VERIFY_CHECKLIST.md) 做完整验证。

## 术语说明

- `StaticResearchProvider`：本地静态 Research 提供方。
- `InMemoryRepository`：进程内仓库实现。
- `TaskService`：任务生命周期协调层。
- `Workflow`：业务流程编排层。
- `SSE`：前端实时接收任务进度的通道。

## 运行提示

- 默认使用本地文件和 InMemory 数据，不需要 API Key。
- 如果你看到 `docker: command not found`，说明当前环境没有 Docker CLI，这不影响本地学习路径。
- 如果 8000 或 5173 端口被占用，先结束旧进程，再重新启动。
