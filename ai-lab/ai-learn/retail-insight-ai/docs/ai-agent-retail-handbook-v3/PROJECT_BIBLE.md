# PROJECT_BIBLE

本文件是 `ai-agent-retail-handbook-v3` 的唯一最高规则，也是 `Enterprise Retail Intelligence Platform (ERIP)` 的统一世界观。所有正文文档必须引用并遵守本文件。

# 项目名称

Enterprise Retail Intelligence Platform (ERIP)

# 日文名称

Enterprise Retail Intelligence Platform（ERIP）/ 小売業向け AI 経営分析プラットフォーム

# 项目世界观

Enterprise Retail Intelligence Platform（ERIP）V1.0 已正式交付，并投入企业使用。系统围绕经营会议、销售分析、库存分析、商品分析、会员分析、市场调查和管理层报告构建。

所有文档必须把 Enterprise Retail Intelligence Platform（ERIP）作为同一个连续项目来讲，不按孤立知识点拆散，不按技术名词堆砌。

# 项目定位

Enterprise Retail Intelligence Platform（ERIP）V1.0 已正式交付。

系统重点是：JWT/RBAC、文書管理、RAG/Citation、显式 AI 分析、董事会报告、Approval、Persistent Audit、LLM Gateway/Ledger，以及 KPI 任务分析辅线与日文经营报告。

# 项目背景

日本零售企业需要在经营会议前整合 POS、库存、商品、会员、销售、门店、CSV、Excel、日报和月报等数据，形成可以用于经营判断的分析报告。

# 客户背景

客户是日本中大型零售企业，拥有多门店、多商品、多销售渠道和固定经营会议流程。

# 行业背景（日本零售）

日本零售行业重视销售效率、库存周转、商品结构、会员行为、门店表现、促销效果和月次经营报告。系统必须支持数据追溯、经营指标解释、报告生成和 Review。

# 客户组织结构

- 经营层
- 经营企画
- 店铺管理
- 商品部
- 库存管理
- 会员运营
- 数据分析担当
- IT 部门
- 外部开发团队

# 业务流程

1. 收集 POS、库存、商品、会员、销售和门店数据
2. 整理 CSV、Excel、日报、月报
3. 分析 KPI
4. 检测库存和销售异常
5. 调查市场和竞品信息
6. 生成日文经营分析报告
7. 管理层 Review
8. 形成改善行动

# 系统整体架构

Enterprise Retail Intelligence Platform（ERIP）由前端、后端、LangGraph Workflow、Research Agent、数据层、Report Generator 和运用扩展组成。

## V1.0 企业业务主链

```text
文書管理
→ RAG検索
→ AI分析（low_cost）
→ 董事会报告（high_quality）
→ 承認管理
→ Persistent Audit
```

配套能力：JWT/RBAC、LLM Gateway/Ledger/Fallback、PostgreSQL/pgvector、Compose/Stub E2E、Lifecycle Live Status、Learning Dashboard。
默认 stub；真实付费 smoke / Billing UI / SIEM 等未完成项见面试材料与 ARCHITECTURE 摘要。

## 任务分析核心链路（保留）

```text
React
↓
FastAPI
↓
Task API
↓
TaskService
↓
LangGraph Workflow
↓
Fixed KPI Workflow / Research Agent
↓
SSE / Report
↓
日文经营分析报告
```

# 数据来源

- POS
- 库存
- 商品
- 会员
- 销售
- 门店
- CSV
- Excel
- API
- 日报
- 月报

# 技术架构

- React
- FastAPI
- Python
- LangGraph
- LangChain（RAG Orchestration）
- LangGraph Workflow
- Streaming
- SSE
- Research Agent
- RAG
- Report Generator
- Docker
- InMemory / PostgreSQL（V1.0 双轨；历史文档中的 SQLite 表述视为早期阶段）
- PostgreSQL
- Keyword Retrieval
- Hybrid Retrieval
- Vector Database（pgvector first）
- RBAC
- Audit Log
- OpenTelemetry
- Redis
- RabbitMQ
- Kubernetes

详细的 Technology Stack、Production Architecture、Runtime Architecture、Enterprise Deployment、Retrieval Pipeline 与 Deployment Topology，
统一以 `09_系统设计书.md` Chapter `7.0 Technical Architecture`
和 `08_架构图册.md` Figure `28~35`
为唯一维护入口；本文件不重复维护第二套技术演进说明。

# 我的职责

- Backend
- FastAPI
- API Design
- Workflow
- Prompt
- Streaming
- Research
- Architecture
- Review

统一职责表达：

```text
私は Enterprise Retail Intelligence Platform（ERIP）V1.0 の開発を担当しました。
担当範囲は Backend、FastAPI、Task API、TaskService、LangGraph Workflow、Research Agent、Report Generator、Streaming、Architecture、Review です。
```

# 项目开发流程

1. 需求分析
2. 基本设计
3. 详细设计
4. API 设计
5. 数据库设计
6. 开发
7. 测试
8. Review
9. 部署
10. 保守

# Production Gap

## 已实现能力

- Task API
- TaskService
- LangGraph Workflow
- Research Agent
- Fixed KPI Workflow
- Streaming / SSE
- Report Generator
- InMemory / PostgreSQL（V1.0 双轨；历史文档中的 SQLite 表述视为早期阶段）
- Docker
- 基础 Architecture
- Review 观点

## 企业运行能力

- PostgreSQL
- pgvector
- Hybrid Retrieval
- RBAC
- SSO
- Audit Log
- Redis
- LangChain
- CI/CD
- Kubernetes
- OpenTelemetry
- RabbitMQ
- Vector Database（pgvector first, Qdrant / Milvus extensible）
- API Gateway
- Secrets Manager
- 多租户
- 权限过滤
- 监控告警
- 负载测试
- 数据备份
- 灾害恢复

# 统一术语

- Enterprise Retail Intelligence Platform（ERIP）
- Retail Insight AI（**仅历史/早期 MVP 名称**，不作当前项目名）
- 小売業向け AI 経営分析プラットフォーム
- Research Agent
- Task API
- TaskService
- LangGraph Workflow
- Fixed KPI Workflow
- Report Generator
- Repository Pattern
- LangGraph = Workflow Orchestration
- LangChain = RAG Orchestration
- Embedding
- Keyword Retrieval
- Hybrid Retrieval
- Vector Database
- KPI
- 经营分析
- 销售分析
- 库存分析
- 商品分析
- 会员分析
- 市场调查
- 日文报告生成
- 管理层报告
- 已交付边界与未完成强化点（禁止把 JWT/Approval/PostgreSQL 说成未完成）

# 统一项目介绍

```text
Enterprise Retail Intelligence Platform（ERIP）V1.0 は、日本の小売業向け企業 AI 経営分析プラットフォームです。
文書根拠・RAG・明示 AI 分析・取締役会報告・承認・監査・LLM 台帳を一貫実装し、
POS/在庫/商品/会員などの経営判断を支援します。正式 Repository は PostgreSQL です。
（歴史名称：Retail Insight AI = 早期 MVP 名称のみ）
```

# 统一自我介绍

```text
私は Enterprise Retail Intelligence Platform（ERIP）V1.0 の開発を担当しました。
主に Backend/Frontend 連携、JWT/RBAC、文書パイプライン、RAG、LLM Gateway、
Approval、Persistent Audit、PostgreSQL、Docker Compose、テスト整備を担当しました。
```

# 统一项目说明

所有项目说明必须包含：

- 日本零售行业背景
- 客户业务流程
- POS / 库存 / 商品 / 会员 / 销售 / CSV / Excel / API
- 固定 KPI 分析
- Research Agent
- Workflow
- Streaming / SSE
- 日文报告生成
- 我的职责
- 已交付边界与未完成强化点（禁止把 JWT/Approval/PostgreSQL 说成未完成）

# 统一职责

统一使用“担当”表达：

```text
担当範囲は Backend、FastAPI、API Design、Workflow、Prompt、Streaming、Research、Architecture、Review です。
```

# 统一技术介绍

技术介绍必须回答：

- 该技术在 Retail Insight AI 中负责什么
- 与经营分析业务的关系
- 为什么采用该设计
- TL Review 会关注什么
- Production Gap 如何扩展

# 面试统一回答原则

所有面试回答必须引用本章原则：

1. 先说 Retail Insight AI 的业务背景
2. 再说小売業向け AI 経営分析システム的系统目标
3. 再说自己的担当范围
4. 再说技术设计
5. 最后说 Production Gap 和扩展方向

禁止先从框架名开始回答。

所有文档不得重复定义另一套项目背景、自我介绍、项目说明或职责表达。

# Book First Principle

V3 遵守一本书原则：

- 不拆散知识
- 不新增大量 Markdown
- 不为单个知识点创建文件
- 不为单个面试题创建文件
- 不为单个 Review 创建文件
- 优先使用 Markdown 标题组织章节
- 每个正文 Markdown 都必须像一本可以连续阅读的技术书

# 文档维护规则

- `PROJECT_BIBLE.md` 是唯一最高规则
- `README.md` 只做入口和维护说明
- 正文 Markdown 不超过 6 个
- 新增内容必须回到 Retail Insight AI
- 章节标题统一使用中文
- 技术名保留英文

## Handbook Trilingual Documentation Standard

### Handbook Trilingual Documentation Standard

为了保证整个 Handbook 长期一致性，所有新增或修改文档必须遵循以下规范：

1. 所有目录（Table of Contents）必须采用三语言格式：`English / 日本語 / 中文（简体）`。不得只保留英文目录。
2. 所有一级标题（H1）必须采用：`English / 日本語 / 中文（简体）`，例如：`Overall Architecture / アーキテクチャ全体 / 总体架构`。
3. 所有二级标题（H2）原则上也采用三语言格式。如果属于代码块、标准协议名称或 ADR 编号，可保持英文。
4. 所有核心 Mermaid 架构图必须维护 English、中文（简体）、日本語 三套版本，并保持语义一致。
5. 每个核心流程图必须注明 `Flow Type（流程类型）`，例如：Business Workflow、System Workflow、Data Flow、Architecture、Deployment、State Machine、Sequence Diagram。
6. 每个核心流程图建议增加 `中文学习版流程`，用于帮助阅读整体业务流程。
7. Handbook 属于 Living Document。新增 API、Workflow、Repository、Database、RAG、Infrastructure、Architecture 后，必须同步更新目录、架构图、三语言标题、流程图、中文学习版流程（如适用）。
8. 任何英文旧图可以保留作为历史参考或补充说明，但不得替代三语言基线图。

<!-- DOC-SYNC:START group=overview -->
## 文档同步块

- group: `overview`
- file: `ai-agent-retail-handbook-v3/PROJECT_BIBLE.md`
- self_sha256: `e1dc1118cf4a13b542ad81cdd9bfc63a872af5a6fc7ec93430d44ea5cead5860`
- peers:
- `retail-insight-ai/README.md` | sha256=51340b3878b7fccbd5a7bdcdcbc2ed0f4c0bab07fae94fe85b1ddfd54eeca283 | # Retail Insight AI / ## 明天先做什么 / 1. 运行 `check_env` / 2. 启动 Backend
- `ai-agent-retail-handbook-v3/README.md` | sha256=572e4166668f669ef002b0a0610c3d745b2b1529531a036afd19453db289a826 | # Retail Insight AI Handbook V3 / # 项目介绍 / Retail Insight AI 是《日本 AI Agent 企业开发与面试宝典》V3 的统一项目。 / 日文名称：小売業向け AI 経営分析システム。
- `ai-agent-retail-handbook-v3/02_日本AI现场面试.md` | sha256=713cdb0ae9c24284a5c62cbad95a808bf2bb530f2db5c514aae34e871dea816d | # 02_日本AI现场面试 / ## 目录 / - [第一章 面试表达总则](#第一章-面试表达总则) / - [第二章 自我介绍](#第二章-自我介绍)
- `ai-agent-retail-handbook-v3/07_面试口头训练.md` | sha256=af984812e08556e127ee61023203fc8e85957a971fe9c307a287dae27cd30fbe | # 07_面试口头训练 / 本文件只用于开口训练。练习时先遮住回答，听完问题后立即开口；说完再对照关键词，不逐字追求一致。 / ## 第一章 30秒回答训练 / ### 1. 自己紹介をお願いします。

说明：
- 这个块由 `scripts/sync_retail_handbook_docs.py` 自动维护。
- 只同步这个块，不覆盖各自正文。
- 任一组内文档正文变化时，整组文档的同步块都会一起刷新。
<!-- DOC-SYNC:END group=overview -->
