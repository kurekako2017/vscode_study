# Retail Insight AI

README 是本项目总入口。

Retail Insight AI 是一个面向日本现场 AI Agent 开发学习、项目讲解和面试准备的经营分析后端项目。它不是只展示一个 Demo，而是把“怎么启动、怎么验证、怎么学习、怎么阅读源码、怎么做面试表达、怎么治理文档”串成一条可执行学习链。

主链路目标是：

```text
React
→ FastAPI
→ Task API
→ TaskService
→ Workflow
→ KPI Engine
→ Research Provider
→ Report Generator
→ SSE
→ React
```

## 1. 项目一句话介绍

Retail Insight AI 是一个以 `FastAPI + React + SSE + Local Static Provider + InMemory Repository` 为当前基线的零售经营分析 Agent 项目，用来学习企业级后端分层、接口合同、审批、审计、RAG 骨架和日本现场讲解方式。

## 2. 当前已经能跑的能力

- `GET /health` 健康检查。
- `POST /api/tasks` 到报告读取的主任务链路。
- `GET /api/tasks/{task_id}/events` 的 `SSE` 进度流。
- Document Upload / Read / Archive / Import / Chunk / Retrieval。
- `POST /api/v1/internal-rag/answer` 的本地 deterministic Internal RAG。
- 审批提交、审批列表/详情、批准、拒绝、修订。
- `GET /api/v1/users/me`、`roles`、`permissions`、`audit-logs` 的安全读模型。
- 本地 `StaticResearchProvider`、`InMemoryRepository`、`LocalBusinessDataProvider`。

## 3. 当前只是骨架或部分完成的能力

- `frontend/` 可以运行，但当前不是主学习入口。
- PostgreSQL Repository 仍是可选路径，不是默认运行路径。
- `LLM Provider` 接缝已留出，但默认不接真实模型。
- 真实认证、`JWT`、`OAuth`、`MCP`、互联网搜索仍未接入。
- 审批、安全、审计当前是本地学习型实现，不是生产级完整方案。

## 4. 未来规划能力

- 真实 `LLM` Provider。
- PostgreSQL 持久化默认化。
- `JWT/OAuth` 与企业身份系统接入。
- `pgvector`、更完整检索、企业级 RAG 评估。
- 更完整的 `RBAC`、审批、审计、运维观测。
- 前后端一体化联调和正式 `E2E` 路线。

## 5. 项目验证体系

Swagger（FastAPI 自动生成的 API 调试与验证工具）

项目验证体系分四层：

| 层级 | 工具 | 目的 |
|---|---|---|
| 单元测试（Unit Test） | python -m unittest | 验证单个模块或类的逻辑是否正确 |
| 接口验证（API Verification） | Swagger UI (/docs) | 手工验证 API 请求、响应和业务流程 |
| 前后端集成测试（Integration Test） | React + FastAPI | 验证完整用户操作流程 |
| 端到端测试（E2E Test） | Playwright / Cypress | 模拟真实用户完成整个业务流程 |

必须明确：

- Swagger 不是测试环境。
- Swagger 不是正式 UI。
- Swagger 是 API 调试与验证工具。
- UI 完成以后 Swagger 通常仍然保留。
- Swagger 和 React 调用的是同一套 FastAPI API。
- 当前阶段主要用 Swagger 验证后端骨架。
- UI 完成后再做前后端 Integration Test。
- 发布前再考虑 E2E Test。

## 6. 项目目录结构树

```text
retail-insight-ai/
├── backend/              # FastAPI 后端，包含 API、Service、Repository、Model
│   ├── app/
│   │   ├── api/          # API 路由层
│   │   ├── services/     # 业务服务层
│   │   ├── repositories/ # 数据访问层
│   │   ├── models/       # 领域模型
│   │   ├── schemas/      # 请求与响应 DTO
│   │   ├── providers/    # LLM / Search Provider 抽象
│   │   ├── workflow/     # Workflow / LangGraph 相关流程
│   │   ├── errors/       # 错误码与异常
│   │   ├── config/       # 配置与依赖注入
│   │   └── observability/# 日志与观测
│   └── tests/            # 后端自动化测试
├── frontend/             # React 前端，目前不是主学习入口
├── docs/                 # 技术文档、学习文档、handbook
├── scripts/              # 启动、检查、测试脚本
└── docker-compose.yml    # PostgreSQL 等本地服务预留
```

补充说明：

- `README.md` 负责项目总入口和阅读顺序。
- `RUNBOOK_LOCAL.md` 负责启动与排错。
- `VERIFY_CHECKLIST.md` 负责逐项验证。
- `docs/` 下的 `ARCHITECTURE`、`API_CONTRACT`、`DATABASE`、`ERROR_CATALOG` 等负责技术规范。
- `docs/ai-agent-retail-handbook-v3/` 是长期学习和日本面试中心。

## 7. 文档导航中心

README 是项目总入口。

`docs/ai-agent-retail-handbook-v3/` 是长期学习和日本面试中心。

`docs/ARCHITECTURE.md`、`docs/API_CONTRACT.md`、`docs/DATABASE.md`、`docs/EVENT_CONTRACT.md`、`docs/ERROR_CATALOG.md` 等是技术规范文档，不要误当成日常学习第一入口。

不要因为文件看起来重复就直接删除。要先合并有用内容，再移动到 `docs/_archive_candidate/`，不能直接删除。

### 【日常学习主线】

```text
README.md
→ RUNBOOK_LOCAL.md
→ Swagger
→ docs/LEARNING_API_WALKTHROUGH.md
→ docs/TEST_CASES.md
→ CODE_STUDY_GUIDE.md
→ docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md
```

### 【技术设计查阅】

```text
docs/ARCHITECTURE.md
docs/API_CONTRACT.md
docs/EVENT_CONTRACT.md
docs/ERROR_CATALOG.md
docs/DATABASE.md
docs/DECISIONS.md
docs/CODING_STANDARD.md
docs/DEVELOPMENT_GUIDE.md
docs/MASTER_PROMPT.md
```

### 【项目管理查阅】

```text
TASK.md
ROADMAP.md
docs/PROJECT_BACKLOG.md
docs/CHANGELOG.md
```

### 【handbook 学习中心】

```text
docs/ai-agent-retail-handbook-v3/README.md
docs/ai-agent-retail-handbook-v3/01_日本AI项目实战.md
docs/ai-agent-retail-handbook-v3/02_日本AI现场面试.md
docs/ai-agent-retail-handbook-v3/03_AI核心知识.md
docs/ai-agent-retail-handbook-v3/04_日本现场开发.md
docs/ai-agent-retail-handbook-v3/05_TL代码审查.md
docs/ai-agent-retail-handbook-v3/06_学习路线.md
docs/ai-agent-retail-handbook-v3/07_面试口头训练.md
docs/ai-agent-retail-handbook-v3/08_架构图册.md
docs/ai-agent-retail-handbook-v3/09_系统设计书.md
docs/ai-agent-retail-handbook-v3/10_Production_Roadmap.md
docs/ai-agent-retail-handbook-v3/11_Project_Structure.md
docs/ai-agent-retail-handbook-v3/12_ADR.md
docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md
docs/ai-agent-retail-handbook-v3/PROJECT_BIBLE.md
```

## 8. 学习路线

推荐学习顺序：

1. 先看 `README.md`，确认项目边界、目录和文档入口。
2. 再看 `RUNBOOK_LOCAL.md`，把后端、Swagger、ReDoc、OpenAPI JSON 跑起来。
3. 打开 Swagger，先执行 `GET /health`，再按 `docs/LEARNING_API_WALKTHROUGH.md` 学主链路。
4. 再读 `docs/TEST_CASES.md`，理解每个能力由哪个测试文件保护。
5. 最后进入 `CODE_STUDY_GUIDE.md` 和 handbook，做源码阅读和面试表达训练。

## 9. 测试路线

推荐测试路线：

1. 先用 Swagger 做接口验证，确认后端确实启动。
2. 再在 `backend/` 目录执行 `python3 -m unittest ...` 做单元测试验证。
3. 再做 React + FastAPI 的联调验证。
4. 最后再考虑 `Playwright / Cypress` 的正式 `E2E` 路线。

特别注意：

- `unittest` 命令必须在 `backend/` 目录执行。
- 不要在项目根目录直接执行 `python3 -m unittest tests.test_api -v`。
- 如果看到 `ModuleNotFoundError: No module named tests`，通常不是代码坏了，而是执行目录错了。

## 10. 源码阅读路线

源码阅读顺序建议固定为：

```text
Swagger
→ backend/app/api/
→ backend/app/services/
→ backend/app/workflow/
→ backend/app/repositories/
→ backend/app/models/
→ backend/tests/
```

阅读理由：

- 先从 Swagger 看输入输出，避免一上来就迷失在源码细节里。
- 再从 `api` 看路由层。
- 再看 `services` 和 `workflow` 理解业务编排。
- 再看 `repositories` 和 `models` 理解数据边界。
- 最后用 `tests` 反向确认哪些能力被保护。

## 11. 面试准备路线

推荐顺序：

1. `README.md`
2. `docs/LEARNING_API_WALKTHROUGH.md`
3. `docs/TEST_CASES.md`
4. `CODE_STUDY_GUIDE.md`
5. `docs/ai-agent-retail-handbook-v3/README.md`
6. `docs/ai-agent-retail-handbook-v3/06_学习路线.md`
7. `docs/ai-agent-retail-handbook-v3/07_面试口头训练.md`
8. `docs/ai-agent-retail-handbook-v3/INTERVIEW_GUIDE.md`

面试表达时要能说清：

- 项目当前已完成什么。
- 哪些能力只是骨架或冻结合同。
- 为什么当前阶段先用本地 Provider / InMemory。
- 为什么 Swagger、unittest、审批、审计、RAG 骨架对企业项目讲解有价值。

## 12. 文档治理规则

文档治理原则：

1. 不要把完整学习内容压缩成一张表。
2. 不要把主链路接口写成一长行表格。
3. 不要删除已有内容，先补充、整理、合并。
4. 目录结构必须保留树形图 + 中文说明。
5. `docs/TEST_CASES.md` 必须保持为测试学习文档，不能退化成命令列表。
6. `docs/LEARNING_API_WALKTHROUGH.md` 必须保持为分接口学习文档，不能退化成接口表格。
7. 企业项目测试体系要长期保留在 `README.md`、`docs/LEARNING_API_WALKTHROUGH.md`、`docs/TEST_CASES.md`、`RUNBOOK_LOCAL.md`、`VERIFY_CHECKLIST.md`。
8. 重复文档先进入治理清单，明确主维护文档，再决定是否归档。
9. 如果文件需要废弃，先确认内容已经并入主文档，再移动到 `docs/_archive_candidate/`，不能直接删除。
10. handbook 根目录是学习和面试中心，`handbook/docs` 是技术规范镜像和治理记录。

## 13. 第一次启动项目

1. 先执行 `./scripts/check_env.sh`。
2. 再执行 `./scripts/start_backend.sh`。
3. 打开 `http://127.0.0.1:8000/docs` 验证 Swagger。
4. 打开 `http://127.0.0.1:8000/redoc` 阅读 ReDoc。
5. 打开 `http://127.0.0.1:8000/openapi.json` 确认 OpenAPI JSON。
6. 如需前端联调，再执行 `./scripts/start_frontend.sh`。
7. 最后按 `VERIFY_CHECKLIST.md` 做逐项验证。

## 14. 当前实现边界

当前明确不宣称已完成：

- 真实 OpenAI / 真实 LLM 接入。
- PostgreSQL 默认化。
- Redis / RabbitMQ。
- 企业级正式认证。
- 生产级前端体验。
- 正式 `E2E` 自动化。

当前环境如果没有 Docker CLI，不应把 Docker Build 或 PostgreSQL 验证写成已通过。
