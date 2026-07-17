# Enterprise Retail Intelligence Platform（ERIP） 日本 Agent 面试攻略 V1.0

## Volume 01 - 项目介绍与系统架构（中日双语 · 权威合并版）

> 最后更新：2026-07-17  
> **权威状态：本文件是 Volume01 唯一活动权威稿**  
> 项目正式名称：**Enterprise Retail Intelligence Platform（ERIP）**  
> 早期 MVP 历史名称：Retail Insight AI（全文仅此处出现一次）  
> 旧稿 `Retail_Insight_AI_日本Agent面试攻略_Volume01_中日双语版.md` 已归档至 `docs/_archive_candidate/handbook-interview/`，不作面试背诵源。  
> 口径以当前仓库源码、PostgreSQL、正式页面、Compose/本地部署为准。

**配套权威材料（与本册一起使用）**

| 文件 | 用途 |
|---|---|
| `01_日本AI项目实战.md` | 业务主链、担当、深掘 |
| `02_日本AI现场面试.md` | 自介、压迫、速查 |
| `03_AI核心知识.md` | **技术版本矩阵 + 知识点表** |
| `07_面试口头训练.md` | 开口训练 |
| `INTERVIEW_GUIDE.md` | 讲解稿 |

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
| Seed | `scripts/seed_scenario01.sh`（PG-only、幂等、零 Provider） |

### 0.2 技术版本快查（详表见 `03_AI核心知识.md`）

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

## 1.1 60 秒（日文）

```text
本日は Enterprise Retail Intelligence Platform、略して ERIP の V1.0 についてご説明します。
日本の小売企業が経営会議前に、社内文書を根拠として分析し、取締役会向け報告を作成し、
上長が承認するまでの業務を、JWT/RBAC、RAG、LLM Gateway、Approval、監査、使用台帳で
一貫して実装した企業 AI プラットフォームです。
正式なデータ基盤は PostgreSQL、既定 LLM は stub、ローカル 5173 と Compose 8080 の両方で受入できます。
```

## 1.2 60 秒（中文）

```text
今天介绍 ERIP V1.0：面向日本零售经营会议的企业 AI 平台。
登录鉴权 → 文档入湖 → RAG 引用 → 显式 AI → 董事会报告 → 审批 → 审计与 LLM 台账。
正式 Repository 是 PostgreSQL，默认 stub，5173/8080 双路径验收。
```

## 1.3 开场注意

- 先业务，后技术。  
- 不把 InMemory 说成正式运行。  
- 未跑真实付费 smoke，不谈“已验证真实模型效果”。  

---

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

## 9.3 Evidence Gate

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

## 10.3 AI Runtime

```text
設定は PostgreSQL の ai_runtime_settings に永続化します。
mode / kill_switch / version。Secret は保存しません。
Admin API は GET/PATCH /api/v1/admin/ai-runtime。InMemory は 503。
既定 mode は stub。有料 smoke 未実施なら実モデル品質を語りません。
```

源码：`backend/app/llm/gateway.py`、`operation_policy.py`、`provider_chain.py`、`services/ai_runtime_service.py`。

---

# 11. Approval / ReportVersion

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

## 12.2 InMemory

```text
自動化ユニットテストの高速アダプタと障害隔離用です。
正式画面・企業受入・本番 Repository ではありません。
```

## 12.3 5173 vs 8080

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
5. 版本数字以 `03_AI核心知识.md` 为准  

---

# 19. 归档说明（合并结果）

| 文件 | 状态 |
|---|---|
| **本文件** | Volume01 **唯一活动权威** |
| `Retail_Insight_AI_日本Agent面试攻略_Volume01_中日双语版.md` | **已移动**至 `docs/_archive_candidate/handbook-interview/` |

旧稿中 Task/LangGraph/LangChain 有价值问答已并入本册第 6、7、13 章，并按 V1.0 主链校正。

# 下一册预告

Volume 02 建议：Approval 并发与 ownership、Ledger 会计一致性、故障演练、TL 代码审查对答。
