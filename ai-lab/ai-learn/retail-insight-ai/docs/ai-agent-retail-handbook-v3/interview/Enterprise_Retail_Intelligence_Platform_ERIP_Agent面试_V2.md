# Enterprise Retail Intelligence Platform（ERIP）Agent 面试指南 V1.0

## Volume 01 - 项目介绍与系统架构（中日双语 · 权威合并版）

> 最后更新：2026-07-17
> **权威状态：本文件是 Volume01 唯一活动权威稿**
> 项目正式名称：**Enterprise Retail Intelligence Platform（ERIP）**
> 早期 MVP 历史名称：Retail Insight AI（全文仅此处出现一次）
> 旧稿 `Retail_Insight_AI_日本Agent面试攻略_Volume01_中日双语版.md` 已归档至 `docs/_archive_candidate/ai-agent-retail-handbook-v3/`，不作面试背诵源。
> 口径以当前仓库源码、PostgreSQL、正式页面、Compose/本地部署为准。

**配套权威材料（与本册一起使用）**

| 文件 | 用途 |
|---|---|
| [`../01_日本AI项目实战.md`](../01_日本AI项目实战.md) | 业务主链、担当、深掘 |
| [`02_日本AI现场面试.md`](02_日本AI现场面试.md) | 自介、压迫、速查 |
| [`../03_AI核心知识.md`](../03_AI核心知识.md) | **技术版本矩阵 + 知识点表** |
| [`07_面试口头训练.md`](07_面试口头训练.md) | 开口训练 |
| [`INTERVIEW_GUIDE.md`](INTERVIEW_GUIDE.md) | 讲解稿 |

---

## 0. 统一事实基线

### 0.1 验收与运行

| 项 | 值 |
|---|---|
| 正式 Repository | **PostgreSQL** |
| InMemory | 仅自动化单元测试适配器 / 故障隔离（**非**正式页面 Repository） |
| Alembic head | **`20260717_08_ai_runtime`** |
| PostgreSQL Backend | **297 tests / 6 skipped** |
| InMemory Backend | **286 tests / 62 skipped** |
| Frontend | **116/116**；production build 通过 |
| 本地完整开发 | 宿主 PostgreSQL + FastAPI + Vite → **5173**（完整启动后可业务测） |
| Compose | PostgreSQL + Backend + Nginx Frontend → **8080** |
| 默认 LLM | **stub**（默认测试不跑真实付费模型） |
| Runtime 表 | **`ai_runtime_settings`**（mode / kill_switch / version；无 Secret） |
| 就绪探针 | `/ready`（readiness）与 `/health` 分离；DB/依赖不可用时就绪失败 |
| Seed | `scripts/seed_scenario01.sh`（PG-only、幂等、零 Provider） |

### 0.2 技术版本快查（详表见 [`../03_AI核心知识.md`](../03_AI核心知识.md)）

| 技术 | 版本 | 来源 |
|---|---|---|
| Python | 3.12（镜像 `python:3.12-slim`） | `backend/Dockerfile` |
| FastAPI | **0.136.3** | `backend/requirements.txt` |
| Uvicorn | **0.49.0** | requirements |
| Starlette | **1.3.1** | venv（FastAPI 依赖） |
| Pydantic | **2.13.4** | requirements |
| pydantic-settings | **2.14.1** | requirements |
| SQLAlchemy | **2.0.51** | venv |
| Alembic | **1.16.5** | requirements |
| psycopg | **3.2.9** | requirements |
| httpx | **0.28.1** | requirements |
| PyJWT | **2.10.1** | requirements |
| passlib / bcrypt | **1.7.4** / **4.0.1** | requirements |
| langgraph | **1.1.10** | requirements（KPI/Task 辅线相关栈） |
| React / react-dom | 声明 `^19.1.0` / lock **19.2.7** | package.json / package-lock |
| Vite | 声明 `^7.0.0` / lock **7.3.6** | package-lock |
| TypeScript | lock **5.9.3** | package-lock |
| Vitest | lock **3.2.6** | package-lock |
| PostgreSQL + pgvector | **pg16**（`pgvector/pgvector:pg16`） | docker-compose |
| Nginx | **1.29-alpine** | frontend Dockerfile |
| Node（build） | **22-alpine** | frontend Dockerfile |

### 0.3 业务主链（必须统一）

```text
登录/JWT/RBAC
→ 文書管理 → Upload → Import → Chunk
→ RAG検索/Citation
→ 显式 AI分析（low_cost）
→ 生成取締役会报告（high_quality）
→ Report/ReportVersion
→ 提交 Approval → manager审批
→ Persistent Audit → LLM Usage Ledger
```

**辅线（可讲，不作唯一主链）：** KPI任务分析 `/analysis` + `/api/tasks`（TaskService / SSE / LangGraph 相关能力）。

### 0.4 正式页面（`frontend/src/App.tsx`）

| 标签 | 路径 | 权限要点 |
|---|---|---|
| 学习总览 | `/dashboard` | 已登录 |
| 文書管理 | `/documents` | `documents.read` |
| RAG/AI分析 | `/rag` | `retrieval.query` / `analysis.execute` |
| KPI任务分析 | `/analysis` | `analysis.execute` |
| 承認管理 | `/approval` | approval.* |
| AI管理 | `/ai-admin` | `security.manage` |

---

# 1. 面试开场 / 面接冒頭

## 1.1 日文自我介绍（60 秒）

```text
本日は Enterprise Retail Intelligence Platform、略して ERIP の V1.0 についてご説明します。
大手流通グループの地域本部・事業会社・経営企画部門が、経営会議前に社内文書を根拠として分析し、取締役会向け報告を作成し、
上長が承認するまでの業務を、JWT/RBAC、RAG、LLM Gateway、Approval、監査、使用台帳で
一貫して実装した企業 AI プラットフォームです。
正式なデータ基盤は PostgreSQL、既定 LLM は stub、ローカル 5173 と Compose 8080 の両方で受入できます。
```

## 1.2 中文自我介绍（60 秒）

```text
今天介绍 ERIP V1.0：面向大型流通集团区域本部、事业公司和经营分析部门的企业 AI 平台。
登录鉴权 → 文档入湖 → RAG 引用 → 显式 AI → 董事会报告 → 审批 → 审计与 LLM 台账。
正式 Repository 是 PostgreSQL，默认 stub，5173/8080 双路径验收。
```

## 1.25 30 秒项目介绍（中日）

**中文：** ERIP 是面向大型流通集团、首期服务于区域或事业部经营分析部门的企业 AI 平台。React + FastAPI，正式库 PostgreSQL；文档入湖后 RAG 引用，显式 AI 走 low_cost，董事会报告 high_quality，再进审批与审计。默认 stub，InMemory 仅测试。

**日文：** ERIP は小売経営分析の企業 AI 基盤です。React と FastAPI、正式 DB は PostgreSQL。文書取込後に RAG 引用、明示 AI は low_cost、取締役会報告は high_quality、その後承認と監査。既定 stub、InMemory はテストのみ。

## 1.3 开场注意

- 先业务，后技术。
- 不把 InMemory 说成正式运行。
- 未跑真实付费 smoke，不谈“已验证真实模型效果”。

---

## 1.4 2 分钟项目介绍（中日）

### 日文

```text
ERIP V1.0 は小売経営会議向けの企業 AI 基盤です。
ログイン/JWT/RBAC の後、文書を Upload/Import/Chunk し、RAG で Citation を取り、
明示 AI 分析（low_cost）と取締役会報告（high_quality）を Gateway 経由で生成します。
ReportVersion を残し、manager が Approval し、Persistent Audit と LLM Usage Ledger で追跡します。
正式 Repository は PostgreSQL。InMemory は unittest のみ。既定 LLM は stub。
ローカル完全起動は 5173、Compose 受入は 8080。テストは 297/6・286/62・116。
原文は documents.content。S3/MinIO は未接入。有料 smoke 未実施ならモデル効果は語りません。
```

### 中文

```text
ERIP V1.0 服务零售经营会议：登录鉴权后完成文档入湖与切片，RAG 给引用，
显式 AI（low_cost）与董事会报告（high_quality）走 Gateway 与 Ledger。
报告有 ReportVersion，经理审批，审计可追踪。
正式库是 PostgreSQL；InMemory 只做测试。默认 stub。5173 完整本地 / 8080 Compose。
原文在 documents.content，未接 S3。未跑真实付费 smoke 不谈模型效果。
```


# 2. 项目概要 / プロジェクト概要

## 2.1 日文

```text
ERIP V1.0 は小売経営インテリジェンス基盤です。
経営企画が文書を取り込み、RAG で出典付き根拠を取り、明示操作で AI 分析を行い、
取締役会報告を版管理し、manager が承認し、監査とコスト台帳を残します。

技術は React、FastAPI、PostgreSQL/pgvector、Alembic、Docker Compose です。
InMemory は自動テスト用アダプタのみで、正式画面や企業受入の Repository ではありません。
```

## 2.2 中文理解

ERIP 解决的是“会前如何稳定产出有依据的分析与可审批报告”，不是聊天 Demo。
栈已落地：React + FastAPI + PostgreSQL。

## 2.3 面试官常问

**Q（日）：このプロジェクトの概要を説明してください。**
按 2.1 回答，再补一句测试数字与默认 stub。

---

# 2.4 项目规模定位 / システム規模の位置付け

## 中文统一口径

ERIP 的业务背景按照 AEON 级大型流通集团想定，但 V1.0 的首期导入范围不是集团全社，而是：

```text
大型流通集团
└── 某个事业公司 / 区域本部 / 经营分析部门
    └── ERIP 部门级核心系统
```

因此当前定位是：

- 大型企业部门级核心系统。
- 也可对应中型企业核心系统。
- 不是小企业内部工具。
- 尚不能表述为已经支持集团全部门店和全部员工。

## 日文面试回答

```text
ERIP は大手流通グループを想定した経営分析基盤ですが、
V1.0 の初期導入範囲はグループ全社ではなく、
地域本部、事業会社、または経営企画部門を対象とした部門級コアシステムです。

JWT/RBAC、文書管理、RAG、AI 分析、ReportVersion、Approval、
Persistent Audit、LLM Usage Ledger を実装しているため、
小規模企業向けの単純な社内ツールではありません。

一方で、全グループ・全店舗・全社員向けの大規模性能、
組織マルチテナント、企業 SSO、Multi-Region、SIEM/WORM までは
V1.0 の完了範囲としては説明しません。
```

## 30秒回答

```text
業務背景は大手流通グループですが、現在の実装範囲は
地域本部や事業会社の経営分析部門を対象とする部門級コアシステムです。
小規模ツールではありませんが、全グループ展開済みとも言いません。
ECS Fargate、RDS、S3 を本番基線とし、将来の事業会社・グループ展開を想定しています。
```

## 为什么采用方案B

```text
React / FastAPI / PostgreSQL / pgvector / API / Worker
```

当前服务数量有限，还没有复杂到必须使用 Kubernetes。因此优先：

```text
CloudFront / ALB
→ ECS Fargate API + Worker
→ RDS PostgreSQL + pgvector
→ Amazon S3
→ Bedrock 或企业批准的外部LLM
```

这是大型企业部门级系统在成本、可靠性、扩展性和运维复杂度之间较平衡的部署方式。

## 面试官追问

**Q（日）：大手企業向けなら、なぜ最初から EKS にしないのですか。**

```text
企業規模だけで EKS を選ぶのではなく、サービス数、運用体制、SRE 能力、
既存クラウド標準で判断します。
ERIP V1.0 は API、Worker、PostgreSQL、Object Storage、LLM Provider が中心で、
ECS Fargate の方が運用複雑度を抑えながら十分に水平拡張できます。
顧客に統一 Kubernetes 基盤がある場合は EKS を選択肢にします。
```

**Q（日）：AEON 全社で利用できますか。**

```text
全社利用済みとは説明しません。
V1.0 は地域・事業会社・経営分析部門向けの初期導入範囲です。
全社展開には Organization/Tenant、企業 SSO、店舗・地域データ分離、
高並行 Worker、Multi-AZ、DR、SIEM などの追加が必要です。
```

**Q（日）：将来どう拡張しますか。**

```text
第一段階は部門・地域、第二段階は事業会社、第三段階はグループ共通基盤です。
Repository、StorageService、LLMProvider の境界を維持し、
必要に応じて SQS/EventBridge、ElastiCache、複数 ECS Service、
または既存 Kubernetes 基盤へ拡張します。
```

# 3. 履历书统一口径

| 项目 | 写法 |
|---|---|
| 项目名称 | Enterprise Retail Intelligence Platform（ERIP） |
| 时期 | V1.0 正式交付（以仓库为准） |
| 角色 | Backend / Frontend 連携、AI 业务设计、安全、数据持久化 |
| 技术 | FastAPI 0.136.3, React 19, JWT/RBAC, PostgreSQL/pgvector, Alembic, LLM Gateway, Docker Compose |
| 成果 | 文書→RAG→AI→取締役会報告→Approval→Audit→Ledger 企业主链 |
| 测试 | PG 297/6skip, IM 286/62skip, FE 116/116 |
| 禁止写法 | 学習プロジェクト / Current MVP 当现名 / PostgreSQL 未完成 / Approval 无 API / JWT 未完成 |

**简历 bullet 示例**

- JWT Access Token + 冻结 RBAC（admin/manager/employee）
- 文档 Upload/Import/Chunk + Scenario01 幂等种子
- Internal RAG（默认零真实 LLM）+ Citation
- LLM Gateway 双路由 + Decimal Ledger + Fallback
- Approval 状态机 + ReportVersion + ownership
- Persistent Audit；AI Runtime `ai_runtime_settings`
- Compose 8080 / 本地 5173

---

# 4. 系统架构 / システム構成

## 4.1 架构说明（日文）

```text
Browser
  → React（Login / ProtectedRoute / 権限ナビ / 正式ページ）
  → FastAPI Routes
  → Auth / Documents / Retrieval / Internal RAG
  → AI Analysis（LLM Gateway low_cost + Evidence + Idempotency + Ledger）
  → Executive Report（high_quality + ReportVersion、自動承認なし）
  → Approval State Machine
  → Persistent Audit + request_id
  → PostgreSQL / pgvector（正式）
  → AI Runtime settings（stub 既定）
```

## 4.2 中文理解

前端持会话与权限 UX；后端持权威授权、状态机、审计与费用台账。
LLM 只经 Gateway。普通 RAG 默认可不调用 Provider。

## 4.3 纯文本主流程

```text
用户登录 → JWT + /users/me
→ 文書 Upload → Import → Chunk
→ RAG/AI分析（Citation；可选显式 AI；可选董事会报告）
→ 承認管理 submit → manager approve/reject
→ Persistent Audit +（AI 路径）LLM Usage Ledger
```

## 4.4 与 KPI/Task 辅线的关系

| 路径 | 定位 |
|---|---|
| 文書→RAG→AI→报告→审批 | **企业主链** |
| `/analysis` + `/api/tasks` + SSE | **辅线**（KPI/Research 任务化） |

面试主讲主链；被问 Task/SSE/LangGraph 时再展开辅线。

---

# 5. FastAPI 相关问答

## 5.1 问题（日文）

```text
なぜ FastAPI を使いましたか。
```

## 5.2 回答（日文）

```text
企業 API の境界として、型付き schema、依存注入、OpenAPI、非同期 I/O が適しているためです。
Route は薄く、業務は Service、永続化は Repository、LLM は Gateway に分離しています。
バージョンは FastAPI 0.136.3、Uvicorn 0.49.0、Pydantic 2.13.4 です。
```

## 5.3 中文理解

FastAPI 管 HTTP 边界，不直连 LLM SDK、不堆业务。

## 5.4 TL 追问

```text
主要な API 群は何ですか。
```

## 5.5 回答

```text
auth、documents、document-retrieval、internal-rag、ai-analysis、executive-reports、
reports catalog、approvals、admin/ai-runtime、tasks、health です。
源码：backend/app/api/*.py
```

---

# 6. TaskService / SSE（辅线，从旧 Volume 合并并校正）

## 6.1 问题

```text
TaskService はなぜ必要ですか。
```

## 6.2 回答（日文）

```text
KPI任务分析など、時間がかかる処理を HTTP 同期で待ち続けると timeout と UX 劣化が起きます。
Task API が task_id を即返し、TaskService が状態を管理し、必要に応じて SSE で進捗を通知します。
ただし ERIP V1.0 の企業主鎖は文書→RAG→AI→取締役会報告→承認であり、
Task/SSE は KPI 辅線として説明します。
```

## 6.3 中文理解

TaskService 解决长任务状态；不要把整个 ERIP 讲成“只有 Task Demo”。

## 6.4 SSE

```text
SSE は主に Task 進捗通知です。承認や AI 分析の中心は request/response + 状態取得です。
error の後に done を送らない、という契約を守ります。
```

源码方向：`backend/app/api/tasks.py`、`backend/app/services/task_service.py`、events。

---

# 7. LangGraph / LangChain（辅线，从旧 Volume 合并并校正）

## 7.1 为什么还要会讲

旧 Volume 以 LangGraph 为中心。V1.0 面试仍可能被追问，但必须说明：

- **主链**是 Service 状态机 + Gateway + PostgreSQL
- LangGraph（依赖 **1.1.10**）服务于 **KPI/Task 类 workflow 能力**
- 业务收费 LLM **不**经业务层直连 LangChain SDK，而经 **LLMGatewayService**

## 7.2 问题

```text
なぜ LangGraph を使いますか。
```

## 7.3 回答（日文）

```text
KPI/Task 辅線では、route、KPI、research、report のような状態遷移を
State / Node / Edge で明示できるためです。
一方、文書 Import、Approval、Ledger 予約など決定的処理は固定 Service と状態機で実装し、
全部を Agent にしません。
```

## 7.4 LangChain 的位置

```text
LangChain は RAG Orchestration の概念整理や将来拡張に使えますが、
ERIP の課金 side-effect は Gateway が唯一入口です。
通常 Internal RAG は既定で実 Provider を呼びません。
```

---

# 8. JWT / RBAC

## 8.1 问题

```text
権限制御はどう実装しましたか。
```

## 8.2 日文回答

```text
JWT で本人確認し、role から Permission Registry で権限を導出します。
admin / manager / employee を固定し、未知 role は空権限の fail-closed です。
Frontend は ProtectedRoute とボタン制御、Backend の require_permission が権威です。
employee の approve は 403、manager は 200 です。
Token は sessionStorage（erip.access_token）のみ。PyJWT 2.10.1 です。
```

## 8.3 源码

- `backend/app/security/*`
- `frontend/src/auth/AuthContext.tsx`、`permissions.ts`
- `frontend/src/routing/ProtectedRoute.tsx`

---

# 9. 文档与 RAG

## 9.1 问题

```text
RAG はどこで使っていますか。
```

## 9.2 日文回答

```text
文書を Chunk したあと、document-retrieval と internal-rag で出典付き回答を返します。
通常 RAG は既定で実 LLM を呼びません。明示 AI 分析だけ Gateway を通ります。
文書ページから /rag?document_id= で衔接します。
```

## 9.3 证据门禁（Evidence Gate）

```text
分析に必要な根拠が足りないとき拒否するゲートです。幻覚と無駄な課金を防ぎます。
```

源码：`document_*_service.py`、`internal_rag_service.py`、`frontend/src/pages/DocumentsPage.tsx`、`RagPage.tsx`。

---

# 10. LLM Gateway / 双路由 / Ledger / Runtime

## 10.1 问题

```text
なぜ LLM SDK を業務から直接呼ばないのですか。
```

## 10.2 日文回答

```text
課金、タイムアウト、証跡、権限、モデル切替を一箇所で統治するためです。
LLMGatewayService が唯一の外向き入口です。
ai_analysis は low_cost、executive_report は high_quality。
金額は Decimal、使用は llm_usage_ledger、Fallback は OpenRouter→NVIDIA→Gemini→Local Qwen。
```

## 10.3 AI 运行时配置（AI Runtime）

```text
設定は PostgreSQL の ai_runtime_settings に永続化します。
mode / kill_switch / version。Secret は保存しません。
Admin API は GET/PATCH /api/v1/admin/ai-runtime。InMemory は 503。
既定 mode は stub。有料 smoke 未実施なら実モデル品質を語りません。
```

源码：`backend/app/llm/gateway.py`、`operation_policy.py`、`provider_chain.py`、`services/ai_runtime_service.py`。

---

# 11. 审批与报告版本（Approval / ReportVersion）

## 11.1 问题

```text
承認ワークフローを説明してください。
```

## 11.2 日文回答

```text
報告書生成後に自動承認はしません。
submit-approval で pending_approval（201）。
manager が approve/reject。reject 後は revise で新 ReportVersion、resubmit で再申請。
History は approval_events、監査は audit_logs で分離します。
同一 task の二重 pending は 409、権限不足は 403 です。
```

源码：`backend/app/api/approvals.py`、`services/approval_service.py`、`frontend/src/pages/ApprovalPage.tsx`。

---

# 12. PostgreSQL / InMemory / 部署

## 12.1 为什么 PostgreSQL 正式

```text
ページ業務、企業受入、Approval、Audit、Ledger、ReportVersion、AI Runtime を
永続化し、トランザクションと行ロックで整合を取る必要があるからです。
Alembic 1.16.5、head 20260717_08_ai_runtime、psycopg 3.2.9、SQLAlchemy 2.0.51。
```

## 12.2 InMemory 测试适配器

```text
自動化ユニットテストの高速アダプタと障害隔離用です。
正式画面・企業受入・本番 Repository ではありません。
```

## 12.3 本地 5173 与 Compose 8080

```text
5173：宿主 PostgreSQL + Backend + Vite（start_local.sh）。フル起動後に業務テスト可。Vite 単独は不可。
8080：Compose（compose_up.sh）。データソースは 5173 と別。
down -v は通常禁止（erip_postgres_data 喪失）。
```

---

# 13. Agent 设计（从旧 Volume 合并）

## 13.1 问题

```text
Agent 設計で一番大事なことは何ですか。
```

## 13.2 回答

```text
全部を Agent にしないことです。
決定的な状態遷移（Import、Approval、Ledger）は固定実装で検証可能にし、
不確実な調査や生成だけを Gateway 配下のモデル呼び出しに限定します。
権限、証跡、版管理、コストを業務主鎖に組み込みます。
```

---

# 14. 日本 TL 连续追问模拟

### TL：コア価値は？

```text
AI を呼ぶこと自体ではなく、根拠・権限・版管理・承認・監査・コストを
経営会議業務に組み込んだことです。
```

### TL：未完成を隠していないか？

```text
有料 smoke 既定化、Billing UI、多テナント予算、SIEM/WORM は未完了と説明します。
JWT/RBAC、Approval API、PostgreSQL 永続化は完了済みで、未完成とは言いません。
```

### TL：テストで何を保証？

```text
PostgreSQL 297、InMemory 286、Frontend 116、production build、
stub 前提の API E2E。有料モデル品質は別途 smoke が必要です。
```

### TL：LangGraph と主鎖の関係は？

```text
LangGraph は KPI/Task 辅線の workflow 表現に寄与します。
企業主鎖の中心説明は Service 状態機 + Gateway + PostgreSQL です。
```

---

# 15. 最终背诵版

## 15.1 1 分钟（日文）

```text
ERIP V1.0 は小売経営向け企業 AI 基盤です。
ログインから文書、RAG、明示 AI、取締役会報告、承認、監査、Ledger まで通します。
React と FastAPI、正式 Repository は PostgreSQL、Alembic head は 08_ai_runtime。
既定 LLM は stub。ローカル 5173、Compose 8080。テスト 297/286/116。
```

## 15.2 5 分钟架构要点

1. 业务课题
2. 正式页面与权限
3. 文档主链
4. 普通 RAG 零真实 LLM
5. Gateway 双路由 + Ledger + Fallback
6. ReportVersion + Approval
7. Persistent Audit
8. PostgreSQL 权威 / InMemory 测试
9. 5173 / 8080
10. 数字与未完成项

---

# 16. 项目化 25 问（中日速答）

| # | 日文问 | 日文要点 | 中文要点 |
|---|---|---|---|
| 1 | なぜ PostgreSQL が正式？ | 業務状態・監査・台帳の権威 | 事务与持久权威 |
| 2 | InMemory の位置 | テストアダプタのみ | 仅 unittest |
| 3 | なぜ Gateway？ | 課金 side-effect 唯一入口 | 唯一外呼 |
| 4 | なぜ双ルート？ | 分析と取締役会報告で枠分離 | 成本/质量分桶 |
| 5 | なぜ Decimal？ | 金額 float 禁止 | 金额精度 |
| 6 | Idempotency-Key | 二重課金防止 | 防双计费 |
| 7 | Evidence Gate | 根拠不足拒否 | 无证据拒分析 |
| 8 | Fallback 失敗 | 失敗記録、成功扱いしない | 不伪造成功 |
| 9 | employee approve | 403 | 403 |
| 10 | submit HTTP | 201 pending_approval | 201 |
| 11 | 報告後すぐ承認？ | しない | 不自动审批 |
| 12 | ReportVersion | 不変スナップショット | 不可变快照 |
| 13 | 401 UX | セッション破棄 | 清会话 |
| 14 | 403 UX | セッション維持拒否 | 保会话 |
| 15 | Audit に残さない | Key/全文 Prompt/文書全文 | 密钥与全文 |
| 16 | request_id | 横断追跡 | 全链路 |
| 17 | Compose down -v | 通常禁止 | 通常禁止 |
| 18 | Alembic head | 20260717_08_ai_runtime | 同左 |
| 19 | テスト数字 | 297/6、286/62、116 | 同左 |
| 20 | Lifecycle | ローカル診断、送信しない | 不回传 |
| 21 | 5173 業務テスト | フル起動後可 | 完整启动可 |
| 22 | なぜ stub E2E | 費用ゼロで主鎖証明 | 零费用主链 |
| 23 | concurrent approve | 行ロックと 409 | 行锁 |
| 24 | 次に足りない | 有料 smoke、Billing UI、SIEM | 同左 |
| 25 | 案件の価値 | 企業統治を AI 業務に実装 | 治理进业务链 |

---

# 17. 已交付 vs 未完成

## 已交付（可讲）

- JWT / RBAC / ProtectedRoute / 401·403
- 文書 Upload/Import/Chunk + seed_scenario01
- RAG/Citation（默认零真实 LLM）
- 显式 AI + 董事会报告 + ReportVersion
- Approval API 状态机 + History
- Persistent Audit
- LLM Gateway / Decimal Ledger / Fallback / Circuit
- AI Runtime 持久化
- 正式 Frontend 导航与 handoff
- Docker Compose + Alembic + Stub E2E
- 测试：297/6、286/62、116/116

## 未完成（必须诚实）

- 真实付费 smoke 默认化 / 真实模型效果验证
- Billing UI / 多租户预算 UI
- SIEM / WORM / 全量生产 Streaming
- DeepSeek 默认启用
- Redis / RabbitMQ / K8s 作为本仓默认可运行栈

---

# 18. 本册训练方法

1. 每天背 60 秒 + 1 分钟 + 主链
2. 隔天练 25 问中的 8 题
3. 每周一次 5 分钟架构
4. 辅线（Task/LangGraph）单独练，避免抢主链
5. 版本数字以 [`../03_AI核心知识.md`](../03_AI核心知识.md) 为准

---



---

# 20. 从旧 Volume 合并：完整中日双语模块问答（V1.0 校正）

> 以下问答来自历史 `Retail_Insight_AI_日本Agent面试攻略_Volume01` 的独有结构，**内容已全部改写为 ERIP V1.0 事实**。
> KPI/Task/LangGraph 明确标注为**辅线**；企业主链仍是 登录→文書→RAG→AI→报告→审批→审计→Ledger。

## 20.1 FastAPI 完整问答（旧 §4 合并）

### 面试官（日）

```text
なぜ FastAPI を使いましたか。
```

### 回答（日）

```text
Python ベースの AI / RAG / LLM Gateway と相性がよく、API 層をシンプルに保てるためです。
Pydantic による入力検証、OpenAPI 自動生成、非同期 I/O、Task 辅線の SSE と相性が良いです。
バージョンは FastAPI 0.136.3、Uvicorn 0.49.0、Pydantic 2.13.4 です。
FastAPI は HTTP Boundary に限定し、業務は Service、永続化は Repository、課金 LLM は Gateway に分離しています。
```

### 中文理解

- 选 FastAPI 是因为 Python AI 栈统一与契约能力，不是“因为简单”
- 只做 HTTP 边界
- 业务不写在 Route

### TL 追问（日）

```text
FastAPI に全部の処理を書けばよいのではないですか。
```

### 回答（日）

```text
API 層に Workflow・Ledger・Approval まで書くと責務が肥大し、テストと保守が難しくなります。
そのため Route は薄く、Service / Repository / Gateway に分けています。
```

## 20.2 TaskService 完整问答（旧 §5 合并 · 辅线）

### 面试官（日）

```text
TaskService は何を担当しますか。
```

### 回答（日）

```text
KPI任务分析辅線における Application Service です。
タスク作成、状態更新、Workflow 起動、イベント発行、結果保存、失敗処理を担当します。
KPI 計算式そのもの、Prompt 本文、RAG 検索本体は持ちません。
企業主鎖の中心は文書→RAG→AI→取締役会報告→承認であり、TaskService は会議資料の KPI 補完位置付けです。
```

### 中文理解

TaskService 是用例协调层（辅线），不是大杂烩，也不是整站唯一核心。

## 20.3 LangGraph / LangChain 完整问答（旧 §6–7 合并 · 辅线）

### 面试官（日）

```text
なぜ LangGraph を使いましたか。LangChain だけではだめですか。
```

### 回答（日）

```text
LangGraph（1.1.10）は KPI/Task 辅線で State / Node / Edge を明示し、条件分岐と失敗位置の把握を容易にします。
LangChain 系依存は RAG 部品概念やライブラリ依存として現れますが、
課金 side-effect の唯一入口は LLMGatewayService であり、業務から SDK を直接呼びません。
通常 Internal RAG は既定で実 Provider を呼びません。
LangGraph と主鎖 Service 状態機は役割分担であり、全部を Agent/Graph にしないのが設計です。
```

### 中文理解

- LangGraph：辅线流程状态
- LangChain 依赖：RAG 相关库生态
- Gateway：收费调用唯一入口
- 主链：Service + PostgreSQL 状态机

## 20.4 RAG / Vector / pgvector 完整问答（旧 §8–9 合并 · V1.0 校正）

### 面试官（日）

```text
RAG はどこで使いますか。なぜ全部を Vector DB に入れないのですか。
```

### 回答（日）

```text
文書 Upload → Import → Chunk の後、document-retrieval と internal-rag で Citation 付き回答を返します。
原文は PostgreSQL documents.content に保存します。S3/MinIO は未接入です。
Keyword retrieval が中心の実運用経路で、通常 RAG は既定で実 LLM Provider を呼びません。
Embedding / vector 能力は schema と EmbeddingService 境界があり、provider が disabled の場合もあります。
未実行の有料 Embedding/LLM smoke を「検証済み」とは言いません。
構造化 KPI は Task/固定計算、非構造文書は RAG、と保存・検索方式を分けます。
pgvector は PostgreSQL 同一基盤でベクトル列を扱えるため採用（イメージ pgvector/pgvector:pg16）。
大規模専用 VectorDB（Qdrant/Milvus）は将来拡張候補です。
```

### 中文理解

- 原文在 PG，不在 S3
- 普通 RAG 默认可零真实 LLM
- Embedding 能力存在但可 disabled，禁止夸大
- 结构化 vs 非结构化分流

## 20.5 Research Agent / Agent 设计（旧 §10 合并 · 辅线）

### 面试官（日）

```text
Research Agent は何をしますか。なぜ全部 Agent にしないのですか。
```

### 回答（日）

```text
Research は不確実な調査・補足情報に限定し、KPI の決定的計算や Approval 状態遷移は固定実装にします。
Tool allowlist、timeout、出典付与、失敗時 fallback を意識します。
全部 Agent にすると、Import/Approval/Ledger の検証可能性が下がるためです。
```

## 20.6 生产故障与调查案例（面试可用 · V1.0）

| 案例 | 现象 | 调查顺序 | 设计对应 |
|---|---|---|---|
| A | AI 分析 429 | request_id → Ledger reserved → quota 桶 | 额度预占 |
| B | employee approve 403 | 权限 registry + Audit denied | RBAC 职责分离 |
| C | submit 409 | pending partial unique + 行锁 | 并发状态机 |
| D | Runtime 409 | expected_version | 乐观锁 |
| E | Runtime 503 | InMemory 调 admin AI Runtime | PG-only 企业能力 |
| F | RAG 无结果 | 未 Import/Chunk 或 document_id 过滤 | 文档主链 |
| G | 5173 不能业务测 | 只起了 Vite | 必须完整 start_local |
| H | 费用异常 | effective_mode 是否离开 stub | Kill Switch / Runtime |
| I | 报告有了但无审批 | 未 submit（设计如此） | 生成≠批准 |
| J | Compose unhealthy | PG → alembic → backend → frontend | entrypoint 顺序 |

### 日文口述模板

```text
障害調査は request_id を起点に、Audit、業務状態、Ledger / provider attempts、
Backend ログ、PostgreSQL 行、Frontend セッションの順で切り分けます。
```

## 20.7 压迫面试（日中）

### Q. 実務経験ですか？

```text
企業要件に基づき ERIP V1.0 を設計・実装・受入可能な状態まで担当しました。
商用 SaaS 全顧客運用件数は盛りません。実装済みと未完了を分けて説明します。
```

### Q. 本当に一人で？

```text
中核の Backend/Frontend 連携、RBAC、文書/RAG、Gateway、Approval、DB/Compose、テストを担当しました。
本番 SRE チーム規模と同一とは言いません。
```

### Q. 本番障害件数は？

```text
件数を作りません。代わりに 403/409/429/Ledger/Compose の調査手順を説明できます。
```

### Q. 弱点は？

```text
有料 smoke 既定化、Billing UI、多テナント予算、SIEM/WORM、S3、企業 IdP です。
JWT/Approval/PostgreSQL を弱点としての「未完成」には挙げません。
```

## 20.8 TL 连续追问链（旧 §11 扩展）

```text
Q: なぜ Gateway か → 課金と証跡の唯一入口
Q: なぜ双ルートか → 分析頻度 vs 取締役会品質
Q: なぜ ReportVersion か → 承認対象の不変化
Q: なぜ InMemory を残すか → 高速 unittest / 故障隔離のみ
Q: なぜ 5173 と 8080 を分けるか → 開発と Compose 受入のデータ境界
Q: LangGraph は主鎖か → 否、KPI/Task 辅線
```

## 20.9 合并对照证明（源→目标）

| 旧 Volume 章节 | 已并入本文件位置 | 校正要点 |
|---|---|---|
| §1 开场 | §1 | ERIP 主链，非 Task-only |
| §2 概要 | §2 | PostgreSQL 正式 |
| §3 架构 | §4 | Gateway/Approval/Audit |
| §4 FastAPI | §5 + §20.1 | 版本号 + 薄 Route |
| §5 TaskService | §6 + §20.2 | 标注辅线 |
| §6–7 LangGraph/LangChain | §7 + §20.3 | 辅线 + Gateway 主入口 |
| §8–9 RAG/pgvector | §9 + §20.4 | content 在 PG；S3 未接入；Embedding 边界 |
| §10 Agent | §13 + §20.5 | 不全 Agent 化 |
| §11 TL 链 | §14 + §20.8 | 增加 V1.0 追问 |
| §12–13 背诵/训练 | §15 + §18 | 统一数字 |
| §14 增量 25 问 | §16 | 297/286/116/08 |
| （新增）故障/压迫 | §20.6–20.7 | V1.0 真实边界 |


# 19. 归档说明（合并结果）

| 文件 | 状态 |
|---|---|
| **本文件** | Volume01 **唯一活动权威** |
| `Retail_Insight_AI_日本Agent面试攻略_Volume01_中日双语版.md` | **已移动**至 `docs/_archive_candidate/ai-agent-retail-handbook-v3/` |

旧稿中 Task/LangGraph/LangChain 有价值问答已并入本册第 6、7、13 章，并按 V1.0 主链校正。

# 下一册预告

Volume 02 建议：Approval 并发与 ownership、Ledger 会计一致性、故障演练、TL 代码审查对答。
