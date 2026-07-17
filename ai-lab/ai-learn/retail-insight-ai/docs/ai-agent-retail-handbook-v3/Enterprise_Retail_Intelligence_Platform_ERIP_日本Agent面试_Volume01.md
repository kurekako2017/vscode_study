# Enterprise Retail Intelligence Platform（ERIP） 日本 Agent 面试攻略 V1.0

## Volume 01 - 项目介绍与系统架构（中日双语版）

> 最后更新：2026-07-17  
> 项目正式名称：**Enterprise Retail Intelligence Platform（ERIP）**  
> 早期 MVP 历史名称：Retail Insight AI（全文仅此处出现一次）  
> 本文按当前仓库源码、PostgreSQL、正式页面、Compose/本地部署校正，禁止旧 MVP 口径。

**验收基线**

| 项 | 值 |
|---|---|
| 正式 Repository | PostgreSQL |
| InMemory | 仅自动化单元测试适配器 / 故障隔离 |
| Alembic head | `20260717_08_ai_runtime` |
| PostgreSQL Backend | 297 tests / 6 skipped |
| InMemory Backend | 286 tests / 62 skipped |
| Frontend | 116/116；production build 通过 |
| 本地完整开发 | 宿主 PostgreSQL + FastAPI + Vite → **5173** |
| Compose | PostgreSQL + Backend + Nginx Frontend → **8080** |
| 默认 LLM | stub |
| Runtime 表 | `ai_runtime_settings` |

**技术版本基线（声明 / 解析）**

| 技术 | 版本 | 来源 |
|---|---|---|
| Python | 3.12-slim | `backend/Dockerfile` |
| FastAPI | 0.136.3 | `backend/requirements.txt` |
| Uvicorn | 0.49.0 | requirements |
| Pydantic | 2.13.4 | requirements |
| Alembic | 1.16.5 | requirements |
| psycopg | 3.2.9 | requirements |
| SQLAlchemy | 2.0.51 | venv |
| PyJWT | 2.10.1 | requirements |
| React | lock 19.2.7（`^19.1.0`） | package-lock / package.json |
| Vite | lock 7.3.6 | package-lock |
| TypeScript | lock 5.9.3 | package-lock |
| Vitest | lock 3.2.6 | package-lock |
| PostgreSQL+pgvector | pg16 | docker-compose |
| Nginx | 1.29-alpine | frontend Dockerfile |
| Node | 22-alpine | frontend Dockerfile |

知识点详表：`03_AI核心知识.md` 第一章 B。

**业务主链**

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

---

# 1. 面试开场 / 面接冒頭

## 60 秒（日文）

```text
本日は Enterprise Retail Intelligence Platform、略して ERIP の V1.0 についてご説明します。
日本の小売企業が経営会議前に、社内文書を根拠として分析し、取締役会向け報告を作成し、
上長が承認するまでの業務を、JWT/RBAC、RAG、LLM Gateway、Approval、監査、使用台帳で
一貫して実装した企業 AI プラットフォームです。
正式なデータ基盤は PostgreSQL で、既定の LLM は stub、Docker Compose とローカル開発の両方で受入できます。
```

## 60 秒（中文）

```text
今天介绍 Enterprise Retail Intelligence Platform（ERIP）V1.0。
它是面向日本零售经营会议的企业 AI 平台：登录鉴权、文档入湖、RAG 引用、显式 AI 分析、
董事会报告、审批、持久审计与 LLM 使用台账一条链打通。
正式 Repository 是 PostgreSQL，默认 LLM 为 stub，本地 5173 与 Compose 8080 均可验收。
```

---

# 2. 项目概要 / プロジェクト概要

## 日文

```text
ERIP V1.0 は小売経営インテリジェンス基盤です。
経営企画が文書を取り込み、RAG で出典付き根拠を取り、明示操作で AI 分析を行い、
取締役会報告を版管理し、manager が承認し、監査とコスト台帳を残します。

技術スタックは React、FastAPI、PostgreSQL/pgvector、Alembic、Docker Compose です。
InMemory は自動テスト用アダプタのみで、正式画面や企業受入の Repository ではありません。
```

## 中文理解

```text
ERIP 解决的是“经营会议前如何稳定产出有依据的分析与可审批报告”，不是聊天 Demo。
技术栈已落地为 React + FastAPI + PostgreSQL。
InMemory 只服务单元测试，不参与正式页面与企业验收叙事。
```

---

# 3. 履历书统一口径

| 项目 | 写法 |
|---|---|
| 项目名称 | Enterprise Retail Intelligence Platform（ERIP） |
| 时期 | V1.0 正式交付（以仓库为准） |
| 角色 | Backend / Frontend 連携、AI Agent 業務設計、セキュリティ、データ永続化 |
| 技术 | FastAPI, React, JWT/RBAC, PostgreSQL/pgvector, Alembic, LLM Gateway, Docker Compose |
| 成果 | 文書→RAG→AI→取締役会報告→Approval→Audit→Ledger の企業主鎖を実装 |
| 测试 | PG 297/6skip, IM 286/62skip, FE 116/116 |
| 禁止写法 | 学習プロジェクト / Current MVP を現名称にする / PostgreSQL 未完成 / Approval 未完成 |

担当关键词（可写进简历 bullet）：

- JWT Access Token + 冻结 RBAC（admin/manager/employee）
- 文档 Upload/Import/Chunk 与 Scenario01 幂等种子
- Internal RAG（默认零真实 LLM）+ Citation
- LLM Gateway 双路由 low_cost / high_quality + Decimal Ledger
- Provider Fallback Chain + Circuit Breaker
- Approval 状态机 + ReportVersion + ownership
- Persistent Audit（append-only）
- AI Runtime 持久化 `ai_runtime_settings`
- Compose 8080 / 本地 5173 双路径

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
```

## 4.2 中文理解

```text
前端持会话与权限 UX；后端持权威授权、业务状态机、审计与费用台账。
LLM 只经 Gateway。普通 RAG 默认可不调用 Provider。
PostgreSQL 是权威状态持有者。
```

## 4.3 正式页面导航

| 标签 | 路径 | 权限要点 |
|---|---|---|
| 学习总览 | `/dashboard` | 已登录 |
| 文書管理 | `/documents` | documents.read |
| RAG/AI分析 | `/rag` | retrieval.query / analysis.execute |
| KPI任务分析 | `/analysis` | analysis.execute |
| 承認管理 | `/approval` | approval.* |
| AI管理 | `/ai-admin` | security.manage |

## 4.4 纯文本主流程

```text
用户登录
│
▼
JWT + /users/me → 权限镜像
│
▼
文書管理：Upload → Import → Chunk
│
▼
RAG/AI分析：Retrieval / Internal RAG（Citation）
│  可选：显式 AI分析（low_cost）
│  可选：生成取締役会报告（high_quality）→ ReportVersion
│
▼
承認管理：submit → manager approve/reject → revise/resubmit
│
▼
Persistent Audit +（AI 路径）LLM Usage Ledger
```

---

# 5. FastAPI 相关问答

## 5.1 面试官问题（日文）

```text
なぜ FastAPI を使いましたか。
```

## 5.2 回答（日文）

```text
企業 API の境界として、型付き schema、依存注入、OpenAPI、非同期 I/O が適しているためです。
Route は薄く保ち、業務は Service、永続化は Repository、LLM は Gateway に分離しています。
```

## 5.3 中文理解

FastAPI 负责 HTTP 边界，不负责直接堆业务与模型调用。

## 5.4 TL 追问

```text
主要な API 群は何ですか。
```

## 5.5 回答

```text
auth、documents、document-retrieval、internal-rag、ai-analysis、executive-reports、
reports catalog、approvals、admin/ai-runtime、tasks、health です。
```

---

# 6. JWT / RBAC 问答

## 6.1 问题

```text
権限制御はどう実装しましたか。
```

## 6.2 日文回答

```text
JWT で本人確認し、role から Permission Registry で権限を導出します。
admin / manager / employee を固定し、未知 role は空権限の fail-closed です。
Frontend は ProtectedRoute とボタン制御、Backend の require_permission が権威です。
employee の approve は 403、manager は 200 です。
```

## 6.3 中文理解

Token 不塞易过期的 permission 列表；服务端 Registry 是政策源。

---

# 7. 文档与 RAG 问答

## 7.1 问题

```text
RAG はどこで使っていますか。
```

## 7.2 日文回答

```text
文書を Chunk したあと、document-retrieval と internal-rag で出典付き回答を返します。
通常 RAG は既定で実 LLM を呼びません。明示 AI 分析だけ Gateway を通ります。
文書ページから /rag?document_id= で衔接します。
```

## 7.3 中文理解

RAG 的价值是 Citation 与证据，不是默认烧钱调用模型。

## 7.4 TL 追问

```text
Evidence Gate とは何ですか。
```

## 7.5 回答

```text
分析に必要な根拠が足りないとき拒否するゲートです。幻覚と無駄な課金を防ぎます。
```

---

# 8. LLM Gateway / 双路由 / Ledger

## 8.1 问题

```text
なぜ LLM SDK を業務から直接呼ばないのですか。
```

## 8.2 日文回答

```text
課金、タイムアウト、証跡、権限、モデル切替を一箇所で統治するためです。
LLMGatewayService が唯一の外向き入口です。
ai_analysis は low_cost、executive_report は high_quality。
金額は Decimal、使用は llm_usage_ledger、Fallback は OpenRouter→NVIDIA→Gemini→Local Qwen。
```

## 8.3 中文理解

Gateway 是窄门；双路由把高频分析与董事会报告成本分离。

## 8.4 AI Runtime

```text
設定は PostgreSQL の ai_runtime_settings に永続化します。
mode / kill_switch / version。Secret は保存しません。
Admin API は GET/PATCH /api/v1/admin/ai-runtime。InMemory は 503。
既定 mode は stub。有料 smoke 未実施なら実モデル品質を語りません。
```

---

# 9. Approval / ReportVersion

## 9.1 问题

```text
承認ワークフローを説明してください。
```

## 9.2 日文回答

```text
報告書生成後に自動承認はしません。
submit-approval で pending_approval（201）。
manager が approve/reject。reject 後は revise で新 ReportVersion、resubmit で再申請。
History は approval_events、監査は audit_logs で分離します。
同一 task の二重 pending は 409、権限不足は 403 です。
```

## 9.3 中文理解

审批看的是不可变版本，不是可变正文。

---

# 10. PostgreSQL / InMemory / 部署

## 10.1 问题

```text
なぜ PostgreSQL と InMemory があるのですか。
```

## 10.2 日文回答

```text
PostgreSQL が正式 Repository です。ページ、企業受入、Approval、Audit、Ledger の権威です。
InMemory はユニットテストを速く回すためのアダプタで、正式画面には使いません。
```

## 10.3 部署问题

```text
ローカルと Compose の違いは。
```

## 10.4 回答

```text
ローカル完全開発は宿主 PostgreSQL + FastAPI + Vite の 5173。
Compose は PostgreSQL + Backend + Nginx Frontend の 8080。
5173 はフル起動後に実業務テスト可能、Vite 単独では不可。
データソースは共有しません。Alembic head は 20260717_08_ai_runtime。
```

---

# 11. 日本 TL 连续追问模拟

### TL

```text
この案件のコア価値は何ですか。
```

### 回答

```text
AI を呼ぶこと自体ではなく、根拠・権限・版管理・承認・監査・コストを
経営会議業務に組み込んだことです。
```

### TL

```text
未完成を隠していませんか。
```

### 回答

```text
いいえ。有料 smoke の既定化、Billing UI、多テナント予算、SIEM/WORM は未完了と説明します。
一方で JWT/RBAC、Approval API、PostgreSQL 永続化は完了済みで、未完成とは言いません。
```

### TL

```text
テストで何を保証しますか。
```

### 回答

```text
PostgreSQL 297、InMemory 286、Frontend 116、production build、
および stub 前提の API E2E です。有料モデル品質は別途 smoke が必要です。
```

---

# 12. 最终背诵版 / 最終暗記版

## 12.1 项目 1 分钟（日文）

```text
ERIP V1.0 は小売経営向け企業 AI 基盤です。
ログインから文書、RAG、明示 AI、取締役会報告、承認、監査、Ledger まで通します。
React と FastAPI、正式 Repository は PostgreSQL、Alembic head は 08_ai_runtime。
既定 LLM は stub。ローカル 5173、Compose 8080。テスト 297/286/116。
```

## 12.2 中文理解

一分钟只讲：业务主链、正式技术栈、默认 stub、测试数字、诚实边界。

## 12.3 5 分钟架构要点

1. 业务课题：会议前证据与审批  
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

# 13. 项目化 25 问（中日）

### 1. なぜ PostgreSQL が正式ですか

**日** 業務状態・監査・台帳・版管理の権威が必要だからです。  
**中** 需要事务与持久权威状态。

### 2. InMemory の位置

**日** 自動テストアダプタのみ。  
**中** 仅单元测试适配器。

### 3. なぜ Gateway か

**日** 課金 side-effect の唯一入口。  
**中** 唯一外呼窄门。

### 4. なぜ双ルートか

**日** 分析と取締役会報告でコストと品質を分離。  
**中** 成本与质量分桶。

### 5. なぜ Decimal か

**日** 金額の float 誤差を避ける。  
**中** 金额精度。

### 6. Idempotency-Key

**日** 二重課金防止。  
**中** 防双计费。

### 7. Evidence Gate

**日** 根拠不足を拒否。  
**中** 无证据拒分析。

### 8. Fallback 失敗時

**日** 失敗として記録し成功扱いしない。  
**中** 记失败，不伪造成功。

### 9. employee approve

**日** 403。  
**中** 403。

### 10. submit HTTP

**日** 201 pending_approval。  
**中** 201。

### 11. 報告後すぐ承認？

**日** しない。人が submit。  
**中** 不自动审批。

### 12. ReportVersion

**日** 不変スナップショット。  
**中** 不可变快照。

### 13. 401 UX

**日** セッション破棄。  
**中** 清会话。

### 14. 403 UX

**日** セッション維持して拒否。  
**中** 保会话拒操作。

### 15. Audit に残さないもの

**日** Key、全文 Prompt、文書全文。  
**中** 密钥与全文。

### 16. request_id

**日** 横断追跡。  
**中** 全链路追踪。

### 17. Compose down -v

**日** 通常禁止。  
**中** 通常禁止。

### 18. Alembic head

**日** 20260717_08_ai_runtime。  
**中** 同左。

### 19. テスト数字

**日** 297/6、286/62、116。  
**中** 同左。

### 20. Lifecycle

**日** ローカル診断、送信しない。  
**中** 本地诊断不回传。

### 21. 5173 業務テスト

**日** フル起動後は可、Vite 単独は不可。  
**中** 完整启动可，单 Vite 不可。

### 22. なぜ stub E2E か

**日** 費用ゼロで業務主鎖を証明。  
**中** 零费用证明主链。

### 23. concurrent approve

**日** 行ロックと状態機で 409 等。  
**中** 行锁与状态机。

### 24. 次に足りないもの

**日** 有料 smoke、Billing UI、SIEM 等。  
**中** 同左。

### 25. この案件の価値

**日** 企業運用に必要な根拠・権限・承認・監査・コスト統治を実装した点。  
**中** 把企业治理做进 AI 业务链。

---

# 14. 本册训练方法

1. 每天背 60 秒 + 1 分钟 + 主链  
2. 隔天练 25 问中的 8 题  
3. 每周一次 5 分钟架构  
4. 压迫题必须练“诚实边界”  
5. 口误清单每天过一遍（禁止把 ERIP 说成学习项目）

---

# 15. 已交付 vs 未完成

## 已交付（可讲）

- JWT / RBAC / ProtectedRoute / 401·403
- 文書 Upload/Import/Chunk + Scenario01 seed
- RAG/Citation（默认零真实 LLM）
- 显式 AI 分析 + 董事会报告 + ReportVersion
- Approval API 状态机 + History
- Persistent Audit
- LLM Gateway / Decimal Ledger / Fallback / Circuit
- AI Runtime 持久化 `ai_runtime_settings`
- 正式 Frontend 导航与 handoff
- Docker Compose + Alembic + Stub E2E
- 测试：297/6、286/62、116/116

## 未完成（必须诚实）

- 真实付费 smoke 默认化 / 真实模型效果验证
- Billing UI / 多租户预算 UI
- SIEM / WORM / 全量生产 Streaming 方案
- DeepSeek 默认启用
- Redis / RabbitMQ / K8s 作为本仓默认可运行栈

---

# 下一册预告

Volume 02 建议深入：Approval 并发与 ownership、Ledger 会计一致性、故障演练话术、TL 代码审查对答。
