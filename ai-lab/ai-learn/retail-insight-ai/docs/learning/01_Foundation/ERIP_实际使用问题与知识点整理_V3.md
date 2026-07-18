# ERIP 实际使用问题与知识点整理

> 状态：持续整理版  
> 目的：记录 ERIP 实际运行、页面操作和架构理解中提出的问题，后续可继续增补。  
> 说明：本文区分“ERIP 当前实现”“企业常见做法”和“尚未交付能力”，避免把规划写成已完成。

## 1. ERIP 是什么项目

ERIP 的正式名称是 **Enterprise Retail Intelligence Platform**。它是一个面向企业经营分析的真实项目，不是学习项目。

项目中虽然提供 React Lifecycle Live Status、Learning Dashboard 等技术可视化功能，但这些只是附加的代码理解能力，不改变 ERIP 的企业项目定位。

当前主要业务链：

```text
登录与权限验证
→ 文書管理
→ Upload / Import / Chunk
→ RAG 检索与 Citation
→ 显式 AI分析
→ 生成取締役会报告
→ 提交审批
→ manager 审批
→ Persistent Audit 与 Usage Ledger
```

## 2. 三种运行与部署方式

| 方式 | 完整组成 | 页面入口 | 是否需要 Docker | 用途 |
|---|---|---|---|---|
| 本地完整开发 | WSL 宿主 PostgreSQL + FastAPI Backend + Vite Frontend | `http://127.0.0.1:5173` | 否 | 页面开发、调试和完整业务测试 |
| Docker Compose | 容器 PostgreSQL + Backend + Nginx Frontend | `http://127.0.0.1:8080` | 是 | 单机部署、验收和演示 |
| 正式生产 | HTTPS + 内网 Backend + 独立/托管 PostgreSQL | 正式域名 | 取决于部署平台 | 企业运行 |

### 2.1 本地日常启动

首次数据库初始化完成后，日常只需：

```bash
./scripts/start_local.sh
```

停止本地 Backend 与 Frontend：

```bash
./scripts/stop_local.sh
```

### 2.2 `5173` 能否完成业务测试

可以，但前提是通过 `start_local.sh` 启动完整本地环境：

```text
Browser :5173
→ Vite/React
→ FastAPI :8000
→ PostgreSQL erip_local
```

需要区分：

- **仅启动 Vite**：只能运行前端，真实登录、上传、RAG、审批等请求无法完成。
- **执行 `start_local.sh` 后访问 5173**：可以完成登录、文档、RAG、AI分析、报告和审批等完整业务测试。

### 2.3 端口分别负责什么

| 端口 | 作用 |
|---|---|
| `5173` | Vite 本地 Frontend |
| `8080` | Docker Compose 中的 Nginx Frontend |
| `8000` | FastAPI Backend、Health 和 Swagger |
| `5432` | 常见的宿主 PostgreSQL 端口 |
| `5433` | 端口冲突时可能使用的 Compose PostgreSQL 宿主映射端口 |

## 3. Docker、Container 与 Compose

### 3.1 Docker 是什么

Docker 将应用及其运行依赖制作成镜像，并通过相互隔离的 Container 运行。

### 3.2 Docker Compose 是什么

Docker Compose 是多容器编排工具。ERIP 的 Compose 方式统一管理：

- PostgreSQL + pgvector
- FastAPI Backend
- Nginx Frontend
- 网络和端口
- Health Check
- Alembic 启动链
- PostgreSQL Volume

Compose 不只是“把项目打包”，还负责多个服务的启动顺序、连接关系和持久化资源。

### 3.3 为什么本地开发通常不使用 Docker

Docker Desktop、镜像和多个容器会占用额外 CPU、内存和磁盘。本地页面开发可以直接运行宿主 PostgreSQL、Backend 和 Vite，资源更轻、代码热更新更直接。

### 3.4 Volume 是什么

Volume 是容器外的持久化数据区域。ERIP Compose PostgreSQL 使用：

```text
erip_postgres_data
```

普通容器停止或重启不会删除 Volume。禁止把下面命令当作普通停止方式：

```bash
docker compose down -v
```

其中 `-v` 会删除 Volume，可能造成数据库数据丢失。

## 4. 本地 PostgreSQL 与 Docker PostgreSQL

它们不是技术上必须分开，但当前默认属于两个不同数据库环境：

| 环境 | 数据库 | 用途 |
|---|---|---|
| 本地完整开发 | WSL 宿主 PostgreSQL `erip_local` | 5173 页面业务测试 |
| Docker Compose | Compose PostgreSQL + `erip_postgres_data` | 8080 部署/验收数据 |
| 自动化测试 | `erip_integration_test` | 测试运行与清理 |
| InMemory | 内存测试适配器 | unittest/故障隔离 |

本地与 Docker 可以配置为连接同一个 PostgreSQL，但通常不建议随意共用，因为：

- 两个 Backend 可能同时修改相同数据。
- Migration 与测试清理可能相互影响。
- 开发数据、验收数据和自动测试数据难以隔离。

`erip_integration_test` 不能作为日常页面数据库，因为测试可能清理或重建其中的数据。

## 5. `DATABASE_URL` 是什么

`DATABASE_URL` 告诉 Backend 应连接哪个 PostgreSQL 实例。

网络连接格式通常是：

```text
postgresql+psycopg://用户名:密码@主机:端口/数据库名
```

Unix Socket/peer 连接可能是：

```text
postgresql+psycopg:///erip_local?host=/var/run/postgresql
```

各部分含义：

| 部分 | 作用 |
|---|---|
| `postgresql+psycopg` | SQLAlchemy 使用的 PostgreSQL 驱动 |
| 用户名 | 数据库身份 |
| 密码 | 数据库认证信息，属于 Secret |
| 主机/Socket | PostgreSQL 所在位置 |
| 端口 | PostgreSQL 网络端口 |
| 数据库名 | Backend 实际使用的数据库 |

文档中的 `<本地 PostgreSQL连接>` 只是占位符，不能原样执行。ERIP 当前机器完成初始化后，真实连接由被 Git 忽略的本地 `.env` 保存，日常启动不应重复手动 `export`。

## 6. 首次初始化与日常启动

两者必须分开理解：

- **首次初始化**：创建数据库、授予权限、启用 pgvector、写入安全的本地配置、执行 Migration。这类操作可能需要一次 `sudo` 权限。
- **日常启动**：读取已经配置好的环境，检查数据库并启动 Backend 与 Frontend，只执行 `start_local.sh`。

AI 工具不能替用户输入 WSL 的 `sudo` 密码，因为这是操作系统管理员身份验证。输入密码时终端不显示字符属于正常安全行为。

数据库密码、JWT Secret 和 Provider Key 不应：

- 硬编码进脚本。
- 写进文档。
- 提交到 Git。
- 输出到日志或 Audit。
- 传给 Frontend 保存。

## 7. 文档上传后保存在哪里

ERIP 当前没有使用 S3/MinIO。当前实现将原文文本和业务记录保存在 PostgreSQL。

文档处理顺序：

```text
Upload
→ documents 保存文档主记录与原文
→ Import 解析和标准化
→ Chunk 拆分检索片段
→ 写入检索/向量数据
→ RAG 查询 Chunk
→ 返回 Citation
```

### 7.1 `documents.content` 是什么

`documents.content` 是文档主记录中的完整原文文本，不是单个 RAG Chunk。

| 数据 | 作用 |
|---|---|
| Document 主记录 | 文档身份、标题、状态、原文等 |
| Import 记录 | 导入、解析和校验过程 |
| Chunk | 被拆分的小段检索文本 |
| Vector/索引 | 支持语义或组合检索 |
| Citation | 指回命中的 `document_id` 与 `chunk_id` |

原文和 Chunk 同时存在的原因：

- 原文用于归档、追溯和重新处理。
- Chunk 是适合检索和引用的较小单元。
- Import 或 Chunk 失败时，可以保留文档状态并重试。
- RAG 不需要每次扫描完整原文。

文档上传完成不代表立即可检索；通常还必须完成 Import 和 Chunk，并达到 `searchable=true`。

## 8. S3 与 MinIO

### 8.1 S3 是什么

Amazon S3 是 AWS 提供的托管对象存储，适合保存 PDF、Word、Excel、图片和其他大文件。

### 8.2 MinIO 是什么

MinIO 是兼容 S3 API 的对象存储，可以部署在公司服务器、私有云、Docker 或 Kubernetes 中。它让企业能够在自己的基础设施内管理对象文件。

### 8.3 企业常见存储分工

| 存储 | 常见职责 |
|---|---|
| S3/MinIO | 原始 PDF、Word、Excel、图片等对象文件 |
| PostgreSQL | 文档元数据、状态、权限、Object Key 和业务关系 |
| PostgreSQL/pgvector | Chunk、Embedding Vector、Metadata 和 Citation |
| Audit 表 | 上传、导入、检索、归档等操作证据 |

企业常见流程：

```text
原始文件 → S3/MinIO
文件元数据 → PostgreSQL
解析文本 → Chunk
Chunk/Vector → PostgreSQL + pgvector
RAG Citation → 指回原文件与具体片段
```

ERIP 当前原文直接进入 PostgreSQL，适合当前规模和部署简化。S3/MinIO 属于未来企业存储演进项，不能写成已交付能力。

## 9. Alembic、Schema 与数据库文档

数据库结构的权威优先级是：

1. Alembic Migration。
2. PostgreSQL 实际 Schema。
3. SQLAlchemy/Domain Model 与 Repository。
4. `schema.sql` 审计基线。
5. `DATABASE.md` 说明文档。

### 9.1 Alembic 是什么

Alembic 是 Python/SQLAlchemy 项目的数据库版本迁移工具，用于按顺序升级或回退 PostgreSQL Schema。

当前 ERIP 已确认的 Migration head：

```text
20260717_08_ai_runtime
```

### 9.2 ER 图应该展示什么

当前 ER 图只能把真实物理表和真实关系画成“已实现”。`roles`、`permissions`、`organizations` 等如果只是规划或代码 Registry，就不能画成当前物理表。

合理的数据库文档应覆盖：

- 全部真实物理表。
- 字段与实际 PostgreSQL 类型。
- Primary Key、Foreign Key、Unique、Check。
- Partial Unique Index 和普通索引。
- 真实外键与仅业务引用的区别。
- Document/RAG、Report/Approval、Audit/LLM 等领域 ER 图。

## 10. PostgreSQL、pgvector 与检索

### 10.1 PostgreSQL 负责什么

PostgreSQL 保存 ERIP 的结构化业务数据、原文、Chunk、报告、审批、审计、LLM Usage 和 Runtime 设置。

### 10.2 pgvector 负责什么

pgvector 是 PostgreSQL Extension，用于保存向量并执行向量相似度检索。它让关系数据、Metadata 和 Vector 可以在同一数据库中管理。

### 10.3 Embedding 是什么

Embedding 把文本转换为一组数值向量，使语义相近的文本在向量空间中距离更近。

必须根据真实代码区分：

- Embedding 接口是否已经统一。
- 当前支持哪些真实 Provider。
- Hybrid Retrieval 和 Reranker 是否已经实现。
- 哪些仍属于规划。

不能仅因为面试文档写过，就将本地/OpenAI/OpenRouter Embedding、Hybrid Retrieval 或 Reranker 表述成已交付。

## 11. InMemory 与 PostgreSQL 的定位

ERIP 是真实企业项目，正式页面运行和企业验收使用 PostgreSQL。

InMemory 的正确定位是：

- 自动化单元测试适配器。
- 快速测试与故障隔离实现。
- 不作为正式页面 Repository。
- 不作为企业验收结果。

面试材料不应再写：

```text
React と FastAPI、InMemory 学習または PostgreSQL/pgvector
```

应表达为：

```text
React、FastAPI、PostgreSQL/pgvector を基盤とする企業向け経営分析プラットフォーム
```

如被问到测试架构，再说明 InMemory Repository 用于快速 unittest。

## 12. 已实现、测试能力与演进项

面试时必须区分三类内容：

| 类别 | 表达方式 |
|---|---|
| 已实现能力 | 可以说明代码、页面、数据表、测试和运行结果 |
| 测试能力 | 明确是 Stub、MockTransport、InMemory 或自动化验证 |
| 生产演进项 | 明确尚未交付，不写入当前架构成果 |

例如：

- Stub Provider 已实现，但不是某个真实大模型。
- Real Provider 接口存在不等于真实付费 smoke 已成功。
- Compose 验收不等于 Kubernetes/HA 已交付。
- Permission Registry 已实现不等于数据库一定存在 `roles/permissions` 表。
- S3/MinIO、企业 IdP、SIEM、WORM、Billing、多租户等应按实际状态说明。

## 13. ERIP 架构从旧版本到当前版本的变化

旧材料容易以 `TaskService → LangGraph → Research Agent` 为项目中心。当前架构范围更完整：

```text
React + Auth/RBAC
→ FastAPI API/Service
→ Document/RAG Evidence
→ LLM Gateway 与成本治理
→ Report/ReportVersion
→ Approval 状态机与 History
→ Persistent Audit / Usage Ledger
→ PostgreSQL + pgvector
```

因此面试材料需要同步：

- 正式项目名称 ERIP。
- PostgreSQL 正式 Repository。
- 文档到审批和审计的完整业务链。
- low_cost/high_quality 模型路由。
- Evidence Gate、幂等、额度、Decimal 成本和 Ledger。
- AI Runtime、readiness、version 与 Kill Switch。
- 本地、Compose 和生产环境边界。
- 未交付能力的诚实说明。

## 14. 当前待统一修改的文档问题

以下问题已标记，后续集中修改：

1. 修正“只启动 Vite 无法完成业务测试”的歧义：完整本地环境启动后，5173 可以完成业务测试。
2. `01_日本AI项目实战.md`：项目名称、第五章整体架构、第六章核心模块和全文旧状态需要更新。
3. `interview/02_日本AI现场面试.md`：全面删除学习项目定位，更新自我介绍、架构、数字与交付边界。
4. `interview/07_面试口头训练.md`：同步最新业务链、架构、成本治理、审批、审计和 Runtime。
5. `03_AI核心知识.md`：增加 ERIP 全技术知识点一览，每项提供一句话解释、项目职责和实现状态。
6. `interview/Enterprise_Retail_Intelligence_Platform_ERIP_Agent面试.md`：保留优秀结构并同步全部最新能力。
7. 所有面试材料必须将 ERIP 表述为真实企业项目，不能写成学习项目或 Current MVP。
8. 未实现的 Redis、RabbitMQ、OpenTelemetry、Kubernetes、IdP、SIEM、WORM、S3/MinIO 等不得冒充已完成。

## 15. 当前验证基线

本文记录时采用的已确认基线：

| 项目 | 基线 |
|---|---|
| PostgreSQL Backend | 297 tests，6 skipped |
| InMemory Backend | 286 tests，62 skipped；仅测试适配器 |
| Frontend | 116/116 |
| Alembic head | `20260717_08_ai_runtime` |
| 正式 Repository | PostgreSQL |
| 默认 LLM Runtime | Stub |
| 真实付费 smoke | 未执行 |
| 本地页面 | `http://127.0.0.1:5173` |
| Compose 页面 | `http://127.0.0.1:8080` |

这些数字以后如发生变化，应以最新实际测试报告为准，不应在多份文档中继续保留相互矛盾的旧数字。

## 16. 后续继续记录的主题

后续页面实际使用时，将继续记录：

- JWT、Bearer Token、sessionStorage。
- 401 与 403 的区别。
- RBAC、Permission、owner authorization。
- Document 状态、Import、Chunk 和 Citation。
- Keyword、Vector、Hybrid Retrieval 与 Reranker。
- AI分析、Provider、Model、Token、Cost 与 Quota。
- low_cost 与 high_quality。
- Idempotency-Key 和并发请求。
- Report、ReportVersion、task_id 与 approval_id。
- Approval 状态机、History、revise 和 resubmit。
- Persistent Audit、request_id 与事务一致性。
- Usage Ledger 与 AI Runtime。
- React State、Hook、Lifecycle、Mount/Update/Unmount。
- Health Check、Migration、Backup、Restore 与生产安全。

---

本文为集中整理稿。后续新增问题应先记录，达到一批后再统一更新，避免频繁修改多份项目文档。





# 17. 企业部署方案、迁移策略与成本比较

## 17.1 技术无缝迁移原则

ERIP 要实现从本地环境顺利迁移到 AWS，建议预先完成三层基础设施抽象：

```text
业务层
├── DocumentService
├── RetrievalService
├── AnalysisService
├── ApprovalService
└── AuditService
        │
        ▼
基础设施抽象
├── Repository
├── StorageService
└── LLMProvider
        │
        ▼
环境实现
├── PostgreSQLRepository / RDS PostgreSQL
├── LocalStorage / MinIOStorage / S3Storage
└── Stub / OpenRouter / Gemini / Bedrock
```

业务层始终调用统一接口：

```python
repository.save(...)
storage.save(...)
storage.read(...)
llm.generate(...)
```

业务层不应直接调用：

```python
open("/uploads/...")
boto3.client("s3")
bedrock_runtime.invoke_model(...)
```

迁移目标不是“任何内容完全零修改”，而是：

> 核心业务流程原则上不修改，变化集中在 Provider 实现、环境变量、云资源、数据迁移和部署脚本。

---

## 17.2 三类部署方案总览

| 方案 | 主要结构 | AWS账单 | 运维成本 | 高可用与扩展 | 适合ERIP |
|---|---|---:|---:|---|---|
| 方案A：单台 EC2 | EC2 内运行 Frontend、FastAPI、PostgreSQL、文件存储 | 低 | 高 | 弱 | PoC、演示、小规模试用 |
| 方案B：ECS Fargate + RDS + S3 | 容器、数据库和对象存储分别托管 | 中 | 中低 | 强 | **当前最推荐** |
| 方案C：EKS + 托管数据服务 | Kubernetes 运行 API 与 Worker | 高 | 高 | 最强 | 已有 Kubernetes 平台的大型企业 |

“成本低”必须同时考虑：

```text
AWS月度账单
+
服务器、数据库、备份、补丁、监控和故障处理的人力成本
```

方案A的云账单最低，但企业需要自行承担更多运维责任。方案B不是绝对最低价，但通常在成本、可靠性、安全性和运维负担之间最平衡。方案C只有在企业已经具备 Kubernetes/SRE 团队时才合理。

---

# 18. 方案A：单台 EC2 部署

## 18.1 开发环境

```text
开发者电脑 / WSL Ubuntu
│
├── React / Vite
│      └── 页面开发与热更新
│
├── FastAPI
│      └── API、RAG、分析、审批
│
├── PostgreSQL + pgvector
│      └── 业务数据、Chunk、Vector、Audit
│
├── LocalStorage
│      └── 本地文件或当前文档原文
│
└── Stub / OpenRouter / Gemini
       └── 开发阶段 LLM
```

## 18.2 企业验证环境

```text
企业测试用户
      │
      ▼
EC2 Public IP / 测试域名
      │
      ▼
Nginx
├── React 静态文件
└── /api 反向代理
      │
      ▼
Docker Compose
├── FastAPI Container
├── PostgreSQL Container
├── pgvector
├── LocalStorage 或 MinIO
└── 可配置 LLM Provider
    ├── OpenRouter
    ├── Gemini
    └── Amazon Bedrock
```

### 服务职责

| 服务 | 作用 |
|---|---|
| EC2 | 提供一台 AWS 虚拟服务器 |
| Docker Compose | 启动和连接多个容器 |
| Nginx | 提供前端静态文件并转发 API |
| PostgreSQL Container | 保存业务和向量数据 |
| LocalStorage/MinIO | 保存原始文件 |
| CloudWatch Agent（可选） | 收集 EC2 和应用日志 |

## 18.3 正式生产环境

```text
用户
 │
 ▼
Route 53 + ACM
 │
 ▼
Application Load Balancer（可选）
 │
 ▼
EC2
├── Nginx
├── React
├── FastAPI
├── Worker
├── PostgreSQL
└── LocalStorage / MinIO
     │
     ├── EBS Snapshot
     └── 定期备份
```

### 方案A的问题

- 应用、数据库和文件集中在同一台服务器。
- EC2 故障可能导致系统整体不可用。
- OS、Docker、PostgreSQL、MinIO 都由企业维护。
- 扩容通常需要升级机器或自行拆分服务。
- 正式生产需要额外设计备份、恢复和高可用。

### 从本地迁移到方案A需要修改什么

| 项目 | 需要处理的内容 |
|---|---|
| 应用代码 | 通常不改核心业务代码 |
| Docker | 制作 Backend/Frontend 镜像与 Compose |
| 数据库 | 将本地 Schema 和数据迁移到 EC2 PostgreSQL |
| Storage | LocalStorage 可继续使用，但必须改为持久化目录/EBS Volume |
| LLM | 修改 Provider 配置；可继续使用原开发 LLM |
| 配置 | 修改域名、CORS、DATABASE_URL、Secret |
| 运维 | 增加备份、日志、HTTPS、服务器补丁和恢复方案 |

---

# 19. 方案B：ECS Fargate + RDS + S3（ERIP推荐方案）

## 19.1 为什么这是ERIP当前最合适的方案

方案B适合 ERIP 当前规模，因为：

- FastAPI 和 Worker 可以容器化运行。
- 不需要自行管理 ECS 宿主服务器。
- RDS 托管 PostgreSQL 的备份、补丁和基础运行。
- S3 托管企业文档对象。
- IAM、Secrets Manager 和 CloudWatch 易于统一治理。
- 比单台 EC2 更可靠，比 EKS 简单。
- 后续可以按 API 与 Worker 分别扩容。

因此对当前 ERIP 而言：

> **方案B是企业验证环境和正式生产环境的首选基线。**

但这不代表所有企业都必须采用方案B。若客户已有统一 EKS 平台，则方案C可能更符合客户标准；若只是短期 PoC，则方案A成本更低。

## 19.2 开发环境

```text
开发者电脑 / WSL Ubuntu
│
├── React / Vite
├── FastAPI
├── PostgreSQL + pgvector
├── LocalStorage
└── LLMProvider
    ├── Stub
    ├── OpenRouter
    ├── Gemini
    └── Bedrock（开发账号允许时）
```

开发环境无需为了将来部署到 AWS 而强制使用 Bedrock。只要 `LLMProvider` 接口一致，本地可以继续使用 Stub、OpenRouter、Gemini 或其他模型。

## 19.3 企业验证环境

```text
测试用户 Browser
        │
        ▼
Application Load Balancer
        │
        │  API流量入口与健康检查
        ▼
Amazon ECS Fargate
├── FastAPI API Container
│      └── 登录、文档、RAG、分析、审批、审计
│
└── Worker Container
       └── Import、Chunk、Embedding、报告生成
        │
        ├──────────────────────┐
        ▼                      ▼
Amazon RDS PostgreSQL      Amazon S3
├── 业务数据               ├── PDF / Word / Excel
├── Chunk                  ├── 生成报告文件
├── Approval               └── Presigned URL 上传下载
├── Audit
└── pgvector
        │
        ▼
LLMProvider
├── OpenRouter
├── Gemini
└── Amazon Bedrock
        │
        ▼
CloudWatch
└── API日志、Worker日志、指标与告警

Secrets Manager
└── DATABASE_URL、JWT Secret、外部LLM API Key
```

企业验证阶段可以先不使用：

- CloudFront 文档分发。
- ElastiCache。
- RDS Multi-AZ。
- 多个 ECS API 实例。
- EKS。

这样可控制验证成本。

## 19.4 正式生产环境

```text
公司网络 / Internet
          │
          ▼
Route 53
└── 企业域名解析
          │
          ▼
AWS Certificate Manager
└── HTTPS证书
          │
          ▼
CloudFront
├── React静态资源缓存
├── 全球/跨地区访问加速
└── 可选的私有文件分发
          │
          ├──────────────► Amazon S3 Frontend Bucket
          │                 └── React build 静态文件
          │
          ▼
AWS WAF（需要时）
└── Web攻击和异常请求防护
          │
          ▼
Application Load Balancer
├── /api 流量入口
├── TLS终止
└── ECS健康检查
          │
          ▼
ECS Fargate Service
├── FastAPI API（至少2个Task时可实现跨AZ冗余）
└── Worker Service
          │
          ├──────────────► Amazon RDS PostgreSQL + pgvector
          │                 ├── Documents Metadata
          │                 ├── Chunk / Vector
          │                 ├── Report / Approval
          │                 ├── Audit / Usage Ledger
          │                 └── Multi-AZ（正式生产时考虑）
          │
          ├──────────────► Amazon S3 Private Bucket
          │                 ├── 原始文件
          │                 ├── 输出报告
          │                 └── Presigned URL
          │
          ├──────────────► Amazon ElastiCache
          │                 ├── Cache
          │                 ├── Session辅助
          │                 └── 队列/并发控制辅助
          │
          └──────────────► LLMProvider
                            ├── Amazon Bedrock
                            ├── OpenRouter
                            └── Gemini

Amazon ECR
└── 保存 FastAPI / Worker Docker Image

AWS Secrets Manager
└── 数据库密码、JWT Secret、外部Provider Key

Amazon CloudWatch
├── 日志
├── Metrics
├── Dashboard
└── Alarm

IAM Task Role
└── 限制 ECS 只能访问指定 S3、Secret 和 Bedrock 模型

Amazon VPC
├── Public Subnet：ALB
└── Private Subnet：ECS、RDS、ElastiCache
```

## 19.5 Amazon Bedrock“可选”的准确含义

`Amazon Bedrock（可选）` 表示：

> ERIP 部署在 AWS 上，并不代表 LLM 必须使用 Bedrock。

应用运行在 ECS Fargate 时，仍然可以通过 `LLMProvider` 使用：

```text
ECS Fargate
    │
    └── LLMProvider
         ├── Amazon Bedrock
         ├── OpenRouter
         ├── Gemini
         ├── OpenAI
         └── 其他企业允许的LLM
```

因此，可以继续指定开发环境中使用的 OpenRouter 或 Gemini，但需要满足：

- 企业安全和数据出境策略允许。
- ECS 私有子网具备访问外部 API 的网络出口。
- API Key 放在 Secrets Manager，不写入镜像。
- 对发送到外部 LLM 的文档内容进行权限与敏感信息治理。
- 成本、Token、审计和超时统一由 `LLMProvider`/Gateway 管理。

Bedrock 的主要优势是 AWS 账号、IAM、审计、网络与账单更容易统一管理；它不是 AWS 部署的强制条件。

## 19.6 从本地迁移到方案B需要修改什么

### 1. PostgreSQL → RDS PostgreSQL

业务代码原则上不改，主要处理：

```text
创建 RDS
→ 确认 PostgreSQL/pgvector 版本
→ 设置 VPC 与 Security Group
→ 执行 Alembic Migration
→ 迁移数据
→ 修改 DATABASE_URL
→ 执行集成与性能测试
```

### 2. LocalStorage → S3

若尚未实现 `StorageService + S3StorageProvider`，需要新增代码：

```text
StorageService
├── save()
├── read()
├── delete()
└── create_presigned_url()

LocalStorageProvider
└── 本地文件实现

S3StorageProvider
└── S3 SDK实现
```

完成抽象后，Document、RAG、Approval 等业务层原则上不改，只修改：

```env
STORAGE_PROVIDER=s3
S3_BUCKET=...
AWS_REGION=...
```

仍需执行：

- 将已有本地文件迁移到 S3。
- 将数据库中的本地路径转换为 Object Key。
- 配置 IAM Task Role。
- 前端若改为 Presigned URL 直传，需要适配上传 API 和前端流程。

### 3. 外部LLM → Bedrock

若已有 `LLMProvider` 抽象，只需新增或完善 `BedrockProvider`，并切换配置：

```env
LLM_PROVIDER=bedrock
BEDROCK_MODEL_ID=...
AWS_REGION=...
```

Provider 内部必须吸收：

- 不同模型请求格式。
- System Prompt 差异。
- Streaming 格式。
- Tool Calling 差异。
- Token Limit。
- JSON输出差异。
- Embedding维度差异。

若继续使用 OpenRouter/Gemini，则业务代码不变，只需把 API Key 迁移到 Secrets Manager，并配置网络出口。

### 4. 应用部署

必须新增或调整：

- Backend/Worker Dockerfile。
- Amazon ECR Repository。
- ECS Task Definition。
- ECS Service。
- ALB Target Group 和 Health Check。
- IAM Task Role。
- CloudWatch Log Group。
- Secrets Manager。
- VPC、Subnet 和 Security Group。
- CI/CD 或人工发布流程。

### 5. 不应修改的核心业务

在抽象正确的前提下，以下原则上不需要因 AWS 迁移而重写：

- 文档业务规则。
- Import/Chunk/RAG 主流程。
- Approval 状态机。
- Report/ReportVersion。
- RBAC 权限判断。
- Audit 业务记录。
- Usage Ledger 与成本治理逻辑。

---

# 20. 方案C：Amazon EKS（Kubernetes）

## 20.1 开发环境

```text
开发者电脑 / WSL
│
├── React / Vite
├── FastAPI
├── PostgreSQL
├── LocalStorage
└── Docker / 可选本地Kubernetes
```

日常开发不必强制运行完整 Kubernetes。可以继续使用本地进程或 Docker Compose，以降低资源消耗。

## 20.2 企业验证环境

```text
测试用户
   │
   ▼
AWS Load Balancer Controller / ALB
   │
   ▼
Amazon EKS Cluster
├── FastAPI Deployment
├── Worker Deployment
├── ConfigMap
├── Secret引用
├── Horizontal Pod Autoscaler
└── Kubernetes Service
   │
   ├────────► RDS PostgreSQL + pgvector
   ├────────► Amazon S3
   ├────────► ElastiCache
   └────────► Bedrock / External LLM

Amazon ECR
└── Container Image

CloudWatch / Managed Prometheus
└── 日志和集群监控
```

## 20.3 正式生产环境

```text
Internet / Company Network
          │
          ▼
Route 53 + ACM + CloudFront + WAF
          │
          ▼
Application Load Balancer
          │
          ▼
Amazon EKS（多AZ）
├── FastAPI Pods
├── Worker Pods
├── Scheduler Pods
├── HPA / Cluster Autoscaler
├── Ingress
├── Network Policy
└── Pod Identity / IAM Roles
          │
          ├────────► RDS PostgreSQL + pgvector Multi-AZ
          ├────────► S3 Private Bucket
          ├────────► ElastiCache
          └────────► Bedrock / External LLM

Secrets Manager
└── External Secrets等方式注入

CloudWatch / Prometheus / Grafana
└── 应用与集群监控
```

## 20.4 从本地迁移到方案C需要修改什么

除方案B的 Storage、LLM、数据库和数据迁移外，还需要：

- Kubernetes Deployment、Service、Ingress。
- Helm Chart 或 Kustomize。
- Pod Resource Request/Limit。
- Readiness/Liveness Probe。
- HPA 和集群扩容策略。
- Kubernetes Secret/External Secrets。
- Network Policy。
- Pod Identity 或 IAM Role。
- Rolling Update、Rollback 和灾难恢复流程。
- Kubernetes 日志、监控与告警体系。

核心业务代码仍可保持不变，但部署与运维资产明显多于方案B。

---

# 21. 三种方案按环境横向比较

## 21.1 开发环境

| 方案 | 推荐开发环境 | 是否必须连接AWS |
|---|---|---|
| A | WSL + PostgreSQL + LocalStorage | 否 |
| B | WSL + PostgreSQL + LocalStorage + Provider抽象 | 否 |
| C | WSL/Compose；必要时本地K8s | 否 |

三种方案的日常开发环境可以基本相同。部署方案的差异主要从企业验证环境开始出现。

## 21.2 企业验证环境

| 方案 | 计算 | 数据库 | 文件 | LLM | 特点 |
|---|---|---|---|---|---|
| A | 单EC2 | EC2内PostgreSQL | LocalStorage/MinIO | 任意Provider | 最便宜、单点 |
| B | ECS Fargate | RDS | S3 | Bedrock或外部LLM | 最平衡、推荐 |
| C | EKS | RDS | S3 | Bedrock或外部LLM | 复杂度最高 |

## 21.3 正式生产环境

| 方案 | 高可用 | 扩展 | 运维责任 | 适用企业 |
|---|---|---|---|---|
| A | 低，需自行增强 | 低到中 | 最大 | 小规模、特殊成本限制 |
| B | 高 | 高 | 中低 | 大多数中大型企业 |
| C | 很高 | 很高 | 最大 | 已有Kubernetes平台与SRE团队 |

---

# 22. ERIP最终推荐结论

ERIP 当前最合理的路线是：

```text
当前开发环境
PostgreSQL
LocalStorage / 当前PostgreSQL原文保存
Stub或外部LLM
        │
        │ 完成 Repository、StorageService、LLMProvider 抽象
        ▼
企业验证环境
ECS Fargate
RDS PostgreSQL
Amazon S3
OpenRouter/Gemini 或 Amazon Bedrock
CloudWatch
Secrets Manager
        │
        │ 验证性能、安全、成本、恢复与权限
        ▼
正式生产环境
CloudFront + WAF + ALB
ECS Fargate API + Worker
RDS PostgreSQL + pgvector
Amazon S3
ElastiCache（按需要）
Bedrock或企业批准的外部LLM
Secrets Manager + CloudWatch + IAM + VPC
```

选择原则：

- 短期演示或小规模 PoC：方案A。
- ERIP 企业验证和正式生产：**优先方案B**。
- 客户已有统一 Kubernetes 平台：方案C。
- AWS 部署不强制使用 Bedrock。
- 使用外部 LLM 时，必须确认网络、数据治理、安全、审计和成本策略。
- “无缝迁移”指业务逻辑不重写，不代表无需 Provider、配置、迁移、基础设施和回归测试。

