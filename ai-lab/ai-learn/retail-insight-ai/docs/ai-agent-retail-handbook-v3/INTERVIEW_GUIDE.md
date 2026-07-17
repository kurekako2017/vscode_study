# 日本项目面试讲解稿

这份文档用于日本项目面试场景。Enterprise Retail Intelligence Platform（ERIP）V1.0 已正式交付，面试说明统一基于企业正式上线项目展开，而不是把它描述成单纯的学习项目。

> 更新说明（V1.0 交付口径）：下文在保留原讲解骨架的同时，按当前仓库已交付能力统一数字与边界。
> 自动化基线：PostgreSQL **297 tests / 6 skipped**；InMemory **286 / 62 skipped**；Frontend **116/116**；Alembic head **`20260717_08_ai_runtime`**。

## 项目介绍

### 中文说明

Enterprise Retail Intelligence Platform（ERIP）是面向零售经营分析场景的企业 AI 后端平台，已经正式交付并投入企业使用。我作为项目开发团队的一员（SE），参与了企业 AI 后端系统的设计、开发、联调、测试和持续完善。

项目围绕零售经营分析场景，构建任务流程、文档管理、Internal RAG、审批流程、安全控制、审计、`LLM` 成本治理、`PostgreSQL`/`pgvector` 以及 React 前端联动等核心能力。

### 日本語説明

Enterprise Retail Intelligence Platform（ERIP）は正式に導入された企業向け AI バックエンドプラットフォームです。

私は開発メンバー（SE）の一員として、

設計、
実装、
テスト、
結合、
改善

などに参加しました。

主に、

・タスク処理
・ドキュメント管理
・Internal RAG
・承認ワークフロー
・JWT / RBAC
・監査
・LLM Gateway / コスト統制
・PostgreSQL / Docker 受け入れ

などの機能開発に携わりました。

---

## 30 秒项目介绍

### 中文

「ERIP 是零售经营分析用的企业 AI 平台。前端 React，后端 FastAPI，正式 Repository 为 PostgreSQL/pgvector；InMemory 仅自动化单元测试适配器。文档上传后经检索与引用生成分析；AI 分析必须显式确认，经 LLM Gateway 走 low_cost；董事会报告走 high_quality，再进入审批状态机。权限是 JWT+RBAC+fail-closed，并有持久审计与 Usage Ledger。默认 stub 验收，零真实 LLM 费用。」

### 日本語

「ERIP は小売の経営分析向け企業 AI 基盤です。Frontend は React、Backend は FastAPI、正式 Repository は PostgreSQL/pgvector。InMemory は自動ユニットテスト用アダプタのみ。文書アップロード後に検索・引用し、AI 分析は明示確認のうえ LLM Gateway の low_cost、取締役会報告は high_quality、その後 Approval 状態機へ進みます。JWT・RBAC・fail-closed、永続監査と Usage Ledger を持ち、既定は stub で実 LLM 費用ゼロです。」

---

## 2 分钟项目介绍

### 中文

「我参与的是 ERIP V1.0。业务主链是：登录 → 文書管理 → RAG検索/AI分析 → 董事会报告 → 承認管理。
正式导航标签：学习总览 → 文書管理 → RAG/AI分析 → KPI任务分析 → 承認管理（admin 另有 AI管理）。
技术上 FastAPI 做 HTTP 边界；React 负责 Login、ProtectedRoute、权限按钮与 Learning Dashboard。
文档链路是 Upload → Import → Chunk → Retrieval；普通 Internal RAG 默认不走真实 Provider。
真正的 LLM 调用只允许经 LLM Gateway：AI 分析 low_cost，董事会报告 high_quality，带 Evidence Gate、Idempotency-Key、Decimal 额度与 PostgreSQL Ledger。
AI Runtime（mode/kill_switch）可经 PostgreSQL 持久化并由 admin 二次确认切换；默认 stub 零费用。
Provider 失败时可走 OpenRouter → NVIDIA → Gemini → Local Qwen 的串行 fallback（熔断与 attempt ledger）。
审批有 owner、History、ReportVersion 与 403/409 边界；Persistent Audit 记录 request_id 与关键动作。
验收：InMemory 测试、PostgreSQL suite、Frontend 116、Docker Compose + Alembic + Stub E2E。
未默认做真实付费 smoke、Billing UI、多租户预算台、SIEM/WORM/Streaming 与 DeepSeek 启用。」

### 日本語

「担当したのは ERIP V1.0 です。業務主鎖は ログイン → 文書管理 → RAG検索/AI分析 → 取締役会報告 → 承認管理 です。
正式ナビ：学習総覧 → 文書管理 → RAG/AI分析 → KPI任务分析 → 承認管理（admin は AI管理）。
FastAPI が HTTP 境界、React が Login / ProtectedRoute / 権限制御と Learning Dashboard を担います。
文書は Upload → Import → Chunk → Retrieval。通常の Internal RAG は既定で実 Provider を呼びません。
LLM は LLM Gateway のみ：AI 分析は low_cost、取締役会報告は high_quality。Evidence Gate、Idempotency-Key、Decimal 枠、PostgreSQL Ledger を伴います。
AI Runtime（mode/kill_switch）は PostgreSQL に永続化し、admin が二次確認で切替。既定は stub。
失敗時は OpenRouter → NVIDIA → Gemini → Local Qwen の直列 fallback（遮断と attempt ledger）。
Approval は owner / History / ReportVersion、403/409。Persistent Audit が request_id と重要操作を残します。
受入は InMemory、PostgreSQL suite、Frontend 116、Compose + Alembic + Stub E2E。
有料 smoke・Billing UI・マルチテナント予算画面・SIEM/WORM/Streaming・DeepSeek 有効化は既定範囲外です。」

---

## 5 分钟架构讲解

### 中文

「从用户请求看：React 先登录拿 JWT，Access Token 只放 sessionStorage；ProtectedRoute 与 API Client 自动带 Bearer。401 清会话回登录；403 保持会话只拒操作——这是 fail-closed 权限模型。

FastAPI 分路由：文档、检索、Internal RAG、AI Analysis、Executive Report、Approval、Audit。业务不直接碰 LLM SDK，统一走 LLM Gateway + Operation Policy + Model Router。AI 分析要求 confirmed 与证据；董事会报告必须绑定已成功分析，且不自动 submit approval。

数据：正式与页面验收为 PostgreSQL（REPOSITORY_BACKEND=postgres）；Alembic head 为 20260717_08_ai_runtime，含 usage ledger、attempt、circuit 状态表。Compose 起 postgres(pgvector)/backend/frontend，entrypoint 先迁移再 uvicorn；compose_down 禁止 -v，保证持久化验收。

审批：submit 创建 pending_approval；employee approve 403；manager approve 200；状态写 Report 与 ReportVersion，History 追加。审计：Persistent Audit + request_id，不落 Token/Key/完整 Prompt。

前端还有 React Lifecycle Live Status 与固定栏目 Learning Dashboard，本地诊断 trace（不回传后端），不回传后端。
自动化：PG 297/6 skip，InMemory 286/62 skip，Frontend 116/116，Stub E2E 覆盖三角色业务链。」

### 日本語

「リクエスト経路：React で JWT を取得し Access Token は sessionStorage のみ。ProtectedRoute と API Client が Bearer を付与。401 はセッション破棄、403 はセッション維持で操作のみ拒否（fail-closed）。

FastAPI は Document / Retrieval / Internal RAG / AI Analysis / Executive Report / Approval / Audit に分割。業務は LLM SDK を直接呼ばず LLM Gateway 経由。AI 分析は confirmed と証拠必須、取締役会報告は成功分析に紐づき自動 submit しない。

正式データは PostgreSQL。InMemory はユニットテスト用。Alembic head は 20260717_08_ai_runtime。Compose は pgvector / backend / frontend、起動時 Alembic、down は -v 禁止。

Approval は pending_approval → manager approve、employee は 403。ReportVersion と History を保持。Audit は request_id、Token/Key/全文 Prompt は残さない。

Frontend は Lifecycle Live Status と Learning Dashboard。検証は PG 297、InMemory 286、Frontend 116、Stub E2E。」

---

## 当前实现

### 中文

- `FastAPI` 后端入口、路由、结构化日志、`request_id`
- `Task API`、`TaskService`、`LangGraph Workflow`、`Fixed KPI Workflow`、`Research Agent`、`Report Generator`、`SSE`
- Document Upload / Import / Chunk / Retrieval、`Internal RAG`（默认不强制真实 LLM）
- `JWT` 登录、`/users/me`、React `ProtectedRoute`、冻结 Permission Registry、`401/403`
- Approval 状态机、owner 读详情、History、`ReportVersion`、403/409
- Persistent Audit、事务内额度预占/结算、Decimal 价格快照、`llm_usage_ledger`
- LLM Gateway：`low_cost` / `high_quality`、Evidence Gate、`Idempotency-Key`
- Provider Chain：OpenRouter → NVIDIA → Gemini → Local Qwen（attempt ledger + circuit）
- PostgreSQL / pgvector、Alembic、Docker Compose、Stub API E2E
- React Lifecycle Live Status、Frontend Learning Dashboard
- 自动化：PG **297/6 skip**，InMemory **286/62 skip**，Frontend **116/116**，head **`20260717_08_ai_runtime`**

### 日本語

- `FastAPI`、構造化ログ、`request_id`
- Task / LangGraph / KPI / Research / Report / SSE
- Document パイプライン、既定で実 LLM を強制しない Internal RAG
- JWT、ProtectedRoute、RBAC、401/403、fail-closed
- Approval 状態機、owner、History、ReportVersion
- Persistent Audit、Ledger、Decimal、Idempotency
- LLM Gateway 双路由と Provider Fallback Chain
- PostgreSQL/pgvector、Alembic、Compose、Stub E2E
- Lifecycle Live Status、Learning Dashboard
- 数値：PG 297/6 skip、InMemory 286/62 skip、Frontend 116、Alembic `20260717_08_ai_runtime`

## 我的职责

### 中文

- 参与后端模块开发
- `FastAPI` `API` 开发
- `Service` 层开发
- `Repository` 层开发
- 文档处理流程开发
- `Internal RAG` 功能开发
- `Approval` 工作流开发
- `JWT` / `RBAC` 与 `Audit` 功能开发
- LLM Gateway / 成本治理 / Fallback Chain
- `Swagger` 联调与 Stub E2E
- `unittest` / Frontend 测试编写
- `Bug` 修复与文档维护
- 与团队成员协作完成开发

### 日本語

- バックエンドモジュール開発への参加
- `FastAPI` `API` 開発
- `Service` / `Repository` 層
- 文書処理、`Internal RAG`
- `Approval`、JWT/RBAC、Audit
- LLM Gateway / コスト / Fallback
- 結合試験、unittest、Frontend テスト
- `Bug` 修正、文書、チーム協働

## 系统架构

```text
React (Login/JWT/ProtectedRoute/RBAC UI/Learning Dashboard)
  → FastAPI
  → Auth / Documents / Retrieval / Internal RAG
  → AI Analysis (low_cost via LLM Gateway)
  → Executive Report (high_quality via LLM Gateway)
  → Approval State Machine + ReportVersion
  → Persistent Audit + Usage Ledger
  → PostgreSQL/pgvector 或 InMemory
  → SSE / JSON → React
```

### 中文讲法

- 前端只负责交互、鉴权展示与学习看板。
- `FastAPI` 负责 `HTTP` 边界与统一错误。
- 文档与普通 RAG 保证可引用、默认可零 LLM。
- 显式 AI 分析与董事会报告必须经 Gateway 与额度。
- 审批与审计保证权责可追。
- 存储可在 InMemory 与 PostgreSQL 间切换而不改业务主链。

### 日本語講法

- frontend は操作、権限表示、学習ダッシュボード。
- FastAPI は HTTP 境界。
- 通常 RAG は引用可能で、既定は LLM 不要。
- 明示 AI / 取締役会報告のみ Gateway と枠を通す。
- 承認と監査で責任を追える。
- InMemory と PostgreSQL を切替可能。

## 为什么这样设计

### 中文

- 先 InMemory 是为了学习路径零摩擦；企业验收用 PostgreSQL 证明合同一致。
- `Repository` / Provider / Gateway 把可替换点收口，避免业务散落。
- 双路由隔离成本：分析便宜、报告高质量，额度桶不串。
- 审批与 AI 成本动作 fail-closed，避免静默越权与静默计费。
- Compose + Stub E2E 保证交付可回归且默认零费用。

### 日本語

- InMemory で学習摩擦を下げ、PostgreSQL で契約一致を証明。
- Repository / Provider / Gateway で差し替え点を集約。
- 双ルートでコスト分離。
- 承認と課金は fail-closed。
- Compose + Stub E2E で回帰と費用安全。

## 日本项目表达

### 中文回答

“这个项目我负责的是企业 AI 后端主链路与治理边界：文档与 RAG、JWT/RBAC、审批状态机、LLM Gateway 成本与 fallback、PostgreSQL/Compose 验收。重点不是堆模型，而是可运行、可解释、可审计、可扩展。”

### 日本語回答

「企業向け AI バックエンドの主経路と統治境界を担当しました。文書/RAG、JWT/RBAC、Approval、LLM Gateway のコストと fallback、PostgreSQL/Compose 受入です。モデルを増やすより、動作・説明・監査・拡張を固めることを重視しました。」

## 当前边界

### 中文（诚实边界，不把未完成说成已完成）

- 默认验收使用 `LLM_PROVIDER_MODE=stub`；**真实付费 smoke 非默认**（需显式 opt-in）
- **Billing 产品化、多租户、管理员预算 UI 未作为完成项**
- **SIEM、WORM、Streaming 未作为当前交付完成项**
- **DeepSeek 未作为已启用默认 Provider**
- 生产级多区域高可用、完整 SSO 产品化可继续演进

### 日本語

- 既定は stub。有料 smoke は opt-in のみ
- Billing / マルチテナント / 予算 UI は未完成扱い
- SIEM / WORM / Streaming は未完了
- DeepSeek は既定有効化していない
- 本番 HA やフル SSO は今後の拡張

## 未来扩展

### 中文

- 真实认证/SSO 可替换 current user 来源，保留 Permission Registry。
- 真实 LLM 只替换 Provider，不绕过 Gateway/Evidence/Quota/Ledger。
- Billing UI 与多租户预算可叠在现有 Ledger 之上。
- SIEM/WORM 可消费现有 audit 事实流。

### 日本語

- SSO は identity 源の差し替え、権限レジストリは維持。
- 実 LLM は Provider 差し替えのみ、Gateway を迂回しない。
- Billing/マルチテナントは既存 Ledger 上に拡張。
- SIEM/WORM は audit を消費。

## ERIP 完整业务链（面试口述）

```text
Login (JWT)
→ 文書管理 Upload → Import → Chunk
→ RAG検索 Retrieval + Citation（普通 RAG 可不调用真实 LLM）
→ AI分析 confirmed + Evidence Gate + low_cost + Usage/Cost
→ 取締役会報告 high_quality + ReportVersion（不自动审批）
→ submit-approval (pending_approval)
→ employee approve → 403
→ manager detail/history → approve → approved
→ Audit + Ledger 可核对
```

正式导航：`学习总览 → 文書管理 → RAG/AI分析 → KPI任务分析 → 承認管理`（admin：`AI管理`）

## 企业级架构亮点（口述清单）

1. JWT + ProtectedRoute + 冻结 RBAC + fail-closed
2. 401 清会话 / 403 保会话
3. Approval 状态机 + owner + History + ReportVersion + 409 冲突
4. Persistent Audit + request_id
5. LLM Gateway 唯一外呼边界
6. Evidence Gate + Idempotency-Key + Decimal 额度 + Ledger
7. low_cost / high_quality 双路由不串桶
8. Fallback Chain + circuit + attempt ledger
9. 普通 RAG 默认零 Provider
10. Compose + Alembic + Stub E2E + volume 持久化
11. Lifecycle Live Status + Learning Dashboard

## 面试常问问题（项目化高频 ≥25）

| # | 问题 | 中文回答要点 | 日本語回答要点 | 源码/设计取舍 | 风险与演进 |
| --- | --- | --- | --- | --- | --- |
| 1 | 为什么用 FastAPI？ | 异步 HTTP、OpenAPI、依赖注入清晰 | OpenAPI と DI が明確 | `backend/app/main.py`、`api/` | 演进：网关层限流 |
| 2 | React 扮演什么？ | 鉴权 UI、业务链、学习看板，不替代后端治理 | 権限 UI と業務導線 | `frontend/src/App.tsx`、Auth | 演进：设计系统 |
| 3 | 为何 PostgreSQL/pgvector？ | 企业验收持久化与向量扩展 | 永続化とベクトル拡張 | postgres repos、Compose | 演进：只读副本 |
| 4 | JWT 存在哪？ | 仅 sessionStorage，刷新经 `/users/me` | sessionStorage のみ | AuthContext | 风险：XSS，需 CSP |
| 5 | ProtectedRoute 做什么？ | 未登录跳转登录并保留原目标 | 未ログインを遮断 | ProtectedRoute | 与后端权限双检 |
| 6 | RBAC 如何 fail-closed？ | 未知角色空权限 | 未知 role は空 | Permission Registry | 禁止默认 admin |
| 7 | 401 与 403？ | 401 未认证清会话；403 已认证拒操作 | 401 破棄、403 維持 | API Client | 面试必问 |
| 8 | Approval 状态有哪些？ | generated→pending_approval→approved/rejected… | generated 等 | `models/report.py` | 不跳态 |
| 9 | owner 规则？ | submitter 可读自己；review 才批 | owner 読取、review 決裁 | approvals API | 越权风险 |
| 10 | History 为何追加？ | 审计可追、不可改写 | 追記のみ | Approval history | WORM 未来 |
| 11 | ReportVersion？ | 报告版本与审批解耦 | 版管理 | executive report | 修订链 |
| 12 | 并发 approve？ | 409 冲突 / 状态机守卫 | 409 | ApprovalService | DB 行锁加强 |
| 13 | Persistent Audit 记什么？ | actor/action/resource/request_id，不记 Key/Prompt | request_id 中心 | audit services | SIEM 未接 |
| 14 | 事务一致性？ | 额度预占短事务结算 | 短トランザクション | ledger repos | 分布式事务慎用 |
| 15 | 为何 LLM Gateway？ | 唯一 Provider 入口 | 唯一入口 | gateway.py | 禁旁路 |
| 16 | Evidence Gate？ | 无证据不分析 | 証拠必須 | AI analysis | 防幻觉计费 |
| 17 | Idempotency-Key？ | 防双计费 | 二重課金防止 | AI/Executive API | 键冲突 409 |
| 18 | low/high 为何分离？ | 成本与质量分桶 | 枠を分離 | Operation Policy | 禁止串模型 |
| 19 | Decimal 为何？ | 金额不用 float | float 禁止 | ledger | 财务一致 |
| 20 | Ledger 作用？ | 成功/失败/幂等事实 | 利用実績 | llm_usage_ledger | Billing UI 未做 |
| 21 | Fallback 顺序？ | OpenRouter→NVIDIA→Gemini→Local Qwen | 固定直列 | provider chain | DeepSeek 未默认启用 |
| 22 | 普通 RAG 为何零 LLM？ | 默认可解释、零费用 | 既定ゼロ費用 | Internal RAG | INTERNAL_RAG_USE_LLM 慎开 |
| 23 | Compose 验收？ | healthy + Alembic + Stub E2E + 无 -v | down -v 禁止 | scripts/compose_* | daemon 依赖环境 |
| 24 | Lifecycle Live Status？ | 本地 mount/update/unmount 诊断 | 前端诊断 | frontend lifecycle | 不回传后端 |
| 25 | Learning Dashboard？ | 固定栏目学习路径 | 固定 15 欄 | LearningSidebar | 不替代业务页 |
| 26 | 测试数字？ | PG 297/6、IM 286/62、FE 113 | 同左 | RUNBOOK N / TEST_CASES | 日常一次 suite |
| 27 | Alembic head？ | `20260717_08_ai_runtime` | 同左 | migrations | 禁止手改 prod |
| 28 | 最弱一环？ | 真实多租户预算与 SIEM 未产品化 | 予算 UI/SIEM 未 | 边界诚实 | 下一阶段 |
| 29 | 如何防费用失控？ | stub 默认 + 额度 + 幂等 + 显式按钮 | stub 既定 | Gateway/Quota | 真实 smoke opt-in |
| 30 | 与 Demo 区别？ | 权限/审计/Ledger/E2E/Compose 齐 | 統治境界あり | 全栈交付 | 可持续演进 |

## 收尾说法

### 中文

这个项目我已经把主链路、契约边界、权限审计、LLM 成本治理和验收数字都整理好了。它不是只能跑 Demo 的项目，而是可解释、可审计、可企业扩展的后端与前端基座。未完成项我会诚实说明，不会夸大成已交付。

### 日本語

主経路、契約、権限・監査、LLM コスト統治、受入数字を整理済みです。Demo ではなく、説明可能で監査可能、企業拡張できる基盤です。未完了は誇張しません。
