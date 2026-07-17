# Enterprise Retail Intelligence Platform（ERIP） 日本 Agent 面试攻略 V1.0
## Volume 01 - 项目介绍与系统架构（中日双语版）

> **项目定位（统一版）**
>
> **案件名：大手流通グループ向け Enterprise Retail Intelligence Platform（ERIP） AI経営分析基盤構築プロジェクト**
>
> 本资料与《技術履歴書》保持一致，以**大型流通集团内部AI经营分析平台项目**为背景，而非行业 Package。

---

# 1. 面试开场 / 面接冒頭

## 60秒（日文）

皆さま、はじめまして。

最近担当したプロジェクトは、**大手流通グループ向け Enterprise Retail Intelligence Platform（ERIP） AI経営分析基盤構築プロジェクト**です。

本プロジェクトは、全国展開する大手流通グループの経営分析基盤を刷新するための社内AIプラットフォーム構築案件です。

POS、商品、在庫、会員、販促、市場・競合情報を統合し、AI Agent を活用して経営分析レポートを自動生成します。

私は FastAPI、TaskService、LangGraph Workflow、Research Agent、SSE、Report Generator、および LangChain・RAG・pgvector アーキテクチャ設計を担当しました。

---

# 2. 项目概要 / プロジェクト概要

## 日文

Enterprise Retail Intelligence Platform（ERIP）は、

**大手流通グループの経営分析業務を支援するエンタープライズAIプラットフォーム**です。

店舗・商品・在庫・POS・会員・販促・市場・競合情報を統合し、AI Agent により経営分析レポートを生成します。

システム全体は FastAPI、TaskService、LangGraph を中心に設計し、LangChain、Hybrid Retrieval、pgvector を採用した企業向けアーキテクチャを採用しています。

## 中文理解

本项目不是行业产品（Package），而是**大型流通集团内部AI经营分析平台**。

介绍项目时统一使用：

- 大手流通グループ向け
- Enterprise Retail Intelligence Platform（ERIP）
- AI経営分析基盤構築プロジェクト

不要再使用：

- Retail Insight AI
- 小売業向けAIシステム
- Package

---

# 3. 履历书统一口径

案件名：

> 大手流通グループ向け Enterprise Retail Intelligence Platform（ERIP） AI経営分析基盤構築プロジェクト

プロジェクト概要：

全国展開する大手流通グループの社内AI経営分析基盤を構築するプロジェクト。POS・商品・在庫・会員・販促・市場・競合情報を統合し、AI Agent を活用した経営分析レポート生成基盤を構築する。

担当：

- FastAPI
- TaskService
- LangGraph Workflow
- Research Agent
- Repository Pattern
- SSE
- Report Generator
- LangChain / RAG Architecture Design

---

> 本文档后续章节（FastAPI、LangGraph、LangChain、RAG、pgvector 等）保持原版内容，仅统一项目名称与项目背景即可。

---

# 3. 系统架构 / システム構成

## 3.1 架构说明（日文）

システム全体の流れは以下の通りです。

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
  ├── Fixed KPI Workflow
  └── Research Agent
        ↓
Context Builder
        ↓
Report Generator
        ↓
Repository Pattern
        ↓
SQLite（Current）
        ↓
PostgreSQL / pgvector
```

FastAPI は HTTP Boundary、TaskService は Application Service、LangGraph は Workflow Orchestration を担当します。
LangChain は RAG Orchestration として、Retriever、Prompt Builder、Context Builder、Embedding Pipeline を担当しています。

## 3.2 中文理解

这个架构要这样理解：

- React：画面
- FastAPI：HTTP/API 边界
- TaskService：业务编排
- LangGraph：流程状态机
- Fixed KPI Workflow：固定 KPI
- Research Agent：调研
- LangChain：未来 RAG 编排
- Repository：数据库隔离
- SQLite：当前
- PostgreSQL / pgvector：未来企业目标

---

# 4. FastAPI 相关问答

## 4.1 面试官问题（日文）

なぜ FastAPI を使いましたか。

## 4.2 回答（日文）

FastAPI を使った理由は、Python ベースの AI Workflow と相性がよく、API 層をシンプルに設計できるためです。
本プロジェクトでは LangGraph、Research Agent、RAG 関連処理が Python 側にあるため、API も Python で統一するとデータモデルや例外処理を共有しやすくなります。

FastAPI は、Pydantic による入力検証、OpenAPI 自動生成、非同期処理、SSE との相性がよく、Task API の要件に合っていました。
ただし、FastAPI は HTTP Boundary に限定し、Workflow や業務ロジックは TaskService 以降に分離しています。

## 4.3 中文理解

重点：

- FastAPI 不是因为“简单”
- 是因为 AI Workflow 在 Python 侧
- Pydantic / OpenAPI / SSE 很适合
- FastAPI 只负责 HTTP Boundary
- 业务逻辑交给 TaskService

## 4.4 TL 追问（日文）

FastAPI に全部の処理を書けばよいのではないですか。

## 4.5 回答（日文）

FastAPI に Workflow や業務ロジックまで書くと、API 層の責務が大きくなり、テストや保守が難しくなります。
そのため、FastAPI は入力検証と HTTP 応答に限定し、タスクのライフサイクル管理は TaskService、状態遷移は LangGraph に分けました。

---

# 5. TaskService 相关问答

## 5.1 面试官问题（日文）

TaskService は何を担当しますか。

## 5.2 回答（日文）

TaskService は Application Service として、タスクのライフサイクルを管理します。
具体的には、タスク作成、状態更新、Workflow 起動、イベント発行、結果保存、失敗処理を担当します。

一方で、KPI 計算、Research Agent の Tool 選択、Report Generator の文面生成などの内部ロジックは持ちません。
TaskService はあくまで API と Workflow、Repository、SSE の間を調整する役割です。

## 5.3 中文理解

TaskService 是业务用例层，不是“大杂烩 Service”。

它负责：

- 创建 task
- 更新状态
- 启动 Workflow
- 发布事件
- 保存结果
- 失败处理

它不负责：

- KPI 算法
- Prompt
- RAG 检索
- 报告内容生成

---

# 6. LangGraph 相关问答

## 6.1 面试官问题（日文）

なぜ LangGraph を使いましたか。

## 6.2 回答（日文）

LangGraph を使った理由は、AI Workflow の状態管理と条件分岐を明確にするためです。
Enterprise Retail Intelligence Platform（ERIP） では、KPI 分析、Research、Report Generator など複数の処理があり、入力内容によって実行経路が変わります。

LangGraph を使うことで、State、Node、Edge を明示でき、どの処理で失敗したか、どこから再実行できるかを把握しやすくなります。
単純な一方向の Chain ではなく、状態を持つ業務 Workflow として管理したかったため、LangGraph を採用しました。

## 6.3 中文理解

回答核心：

- LangGraph 是 Workflow 状态管理
- 项目不是一次 Prompt
- 有 KPI、Research、Report 多节点
- 需要条件分支、失败定位、未来 checkpoint
- 所以用 LangGraph，而不是普通链式调用

## 6.4 TL 追问（日文）

LangChain だけではだめですか。

## 6.5 回答（日文）

LangChain は Retriever、Prompt、Tool Calling、Context Builder など、RAG の構成に向いています。
一方で、本プロジェクトではタスク全体の状態管理、条件分岐、失敗時の制御が重要です。

そのため、Workflow 全体は LangGraph、RAG 関連部品は LangChain という形で責務を分離しました。
LangGraph と LangChain は競合するものではなく、役割を分けて組み合わせる設計です。

---

# 7. LangChain 相关问答

## 7.1 面试官问题（日文）

LangChain はこのプロジェクトで何を担当しますか。

## 7.2 回答（日文）

LangChain は RAG Orchestration を担当しています。
具体的には、Retriever、Prompt Builder、Context Builder、Tool Calling、Embedding Pipeline などの RAG コンポーネントを管理します。

ただし、LangChain は Workflow 全体の状態管理には使いません。
Workflow の State、Node、Edge、条件分岐は LangGraph が担当し、LangChain はその中の RAG 部品として利用します。

## 7.3 中文理解

一句话：

- LangGraph 管流程
- LangChain 管 RAG
- 两者不是二选一
- 不能把 LangChain 说成整个系统的 Workflow 框架

---

# 8. RAG / Vector Database 相关问答

## 8.1 面试官问题（日文）

RAG はどこで使いますか。

## 8.2 回答（日文）

RAG は、Research Agent が社内の商品資料、月次報告、会議資料などを検索し、回答やレポート生成の根拠を補う部分で使います。
Keyword Retrieval を基盤にしつつ、文書を Chunk に分割し、Embedding を作成して、pgvector に保存する構成を採用しています。

検索時には、Keyword Retrieval と Vector Retrieval を組み合わせた Hybrid Retrieval を行い、必要に応じて Rerank し、最終的に Citation 付きの Context を Report Generator に渡します。

## 8.3 中文理解

RAG 的作用：

- 不是 KPI 计算
- 是内部资料检索
- 用于 Research Agent
- 当前 Keyword Retrieval
- 未来 Chunk → Embedding → pgvector → Hybrid Retrieval → Rerank → Citation

## 8.4 TL 追问（日文）

なぜ全部のデータを Vector Database に入れないのですか。

## 8.5 回答（日文）

すべてのデータを Vector Database に入れる必要はありません。
売上、在庫、商品、会員などの構造化データは PostgreSQL で管理し、SQL や KPI Workflow で処理します。

Vector Database は、社内資料や月次報告のような非構造化文書を意味検索するために使います。
構造化データと非構造化文書で保存方式と検索方式を分ける方が、精度と保守性の面で適切だと考えています。

---

# 9. pgvector 相关问答

## 9.1 面试官问题（日文）

なぜ pgvector を第一候補にしましたか。

## 9.2 回答（日文）

pgvector を第一候補にした理由は、PostgreSQL と同じ基盤でベクトル検索を扱えるためです。
企業システムでは、データベース、バックアップ、権限、監視、運用手順をできるだけ統一した方が保守しやすくなります。

もちろん、大規模なベクトル検索や専用の検索基盤が必要になった場合は、Qdrant や Milvus も選択肢になります。
ただし、Enterprise Retail Intelligence Platform（ERIP） の第一段階では PostgreSQL + pgvector の方が導入コストと運用コストのバランスが良いと考えています。

## 9.3 中文理解

回答重点：

- PostgreSQL 是企业目标 DB
- pgvector 可以和 PostgreSQL 一体化
- 运维成本低
- 备份、权限、监控统一
- 大规模场景再考虑 Qdrant / Milvus

---

# 10. Agent 设计相关问答

## 10.1 面试官问题（日文）

Research Agent は何をしますか。

## 10.2 回答（日文）

Research Agent は、市場動向、競合情報、社内資料などを調査し、Report Generator に渡すための要約と出典を作成します。
KPI の数値計算は担当せず、情報源が変わる調査処理だけを担当します。

Agent には Tool Allowlist、timeout、最大実行回数、出力形式を設定し、自由に何でも実行できる構成にはしません。
また、調査結果には source、updated_at、risk を付け、レポート生成時に根拠を追えるようにします。

## 10.3 中文理解

Research Agent 只管不确定性调查，不管确定性 KPI。

要说：

- Tool allowlist
- timeout
- max iterations
- source
- updated_at
- risk
- fallback

---

# 11. 日本 TL 连续追问模拟

## 11.1 问答链：LangGraph vs LangChain

### TL（日文）

LangGraph と LangChain の違いを説明してください。

### 回答（日文）

LangGraph は Workflow Orchestration、LangChain は RAG Orchestration として分けています。
LangGraph は State、Node、Edge を使って処理全体の状態遷移を管理します。
LangChain は Retriever、Prompt、Context Builder、Tool Calling など、RAG の部品を組み立てるために使います。

### 中文理解

区分：

- LangGraph = 流程状态
- LangChain = RAG 部件

---

### TL（日文）

なぜ LangChain で Workflow も管理しないのですか。

### 回答（日文）

一方向の処理であれば LangChain でも十分ですが、本プロジェクトでは KPI、Research、Report という複数の経路と失敗制御があります。
そのため、Workflow 全体は LangGraph で明示的に管理した方が、状態確認、再実行、レビューがしやすいと考えました。

---

# 12. 最终背诵版 / 最終暗記版

## 12.1 项目 1 分钟（日文）

Enterprise Retail Intelligence Platform（ERIP） は、日本の大手小売企業向け AI 経営分析システムです。
POS、在庫、商品、会員、販促データと市場・競合調査を組み合わせ、経営判断に使える日本語レポートを生成します。

私はバックエンドを中心に、FastAPI、TaskService、LangGraph Workflow、Research Agent、SSE、Report Generator を担当しました。
設計上は、FastAPI を HTTP Boundary、TaskService を Application Service、LangGraph を Workflow Orchestration として分離しています。

Keyword Retrieval を中心に構成しつつ、LangChain、Embedding、pgvector を使い、Hybrid Retrieval と Citation に対応しています。

## 12.2 中文理解

这段是 AI Agent 案件最推荐背诵版本。

结构：

1. 项目是什么
2. 用于什么业务
3. 我负责什么
4. 架构怎么分层
5. 当前与未来怎么区分

---

# 13. 本册训练方法

建议每天按以下顺序训练：

1. 先读中文理解
2. 再读日文回答
3. 关掉中文，只说日文
4. 让自己用 30 秒、1 分钟、3 分钟三个长度说明项目
5. 每次训练都要统一为正式交付口吻

---



---

# 14. ERIP V1.0 正式交付増補（增量，不删除前文）

> 前文的 FastAPI / LangGraph / RAG 原问答**全部保留**。本章按当前仓库交付能力校正口径。
> 数字：PostgreSQL **281 tests / 2 skipped**；InMemory **270 / 52 skipped**；Frontend **113/113**；Alembic **`20260717_07_fallback_chain`**。

## 14.1 30 秒 / 2 分钟 / 5 分钟（中日）

### 30 秒 日文

```text
ERIP V1.0 は小売経営分析の企業 AI 基盤です。React と FastAPI、PostgreSQL/pgvector、
JWT/RBAC、文書と RAG、LLM Gateway の双ルート、Approval、監査と Ledger、Compose 受入まで揃えています。
```

### 30 秒 中文

```text
ERIP V1.0 是零售经营分析企业 AI 平台：React+FastAPI+PostgreSQL/pgvector，
JWT/RBAC，文档与 RAG，LLM 双路由与审批审计，Compose 验收齐备。
```

### 2 分钟 日文

```text
業務主鎖は ログイン→文書管理→RAG/AI分析→KPI任务分析→承認管理 です。
通常 RAG は引用可能で既定 LLM 不要。AI 分析は low_cost、取締役会報告は high_quality。
Evidence Gate、Idempotency-Key、Decimal、Ledger で費用を統治します。
Fallback は OpenRouter→NVIDIA→Gemini→Local Qwen。Approval は 403/200 と ReportVersion。
Compose+Alembic+Stub E2E。テスト 281/270/113。有料 smoke と Billing UI は既定外です。
```

### 2 分钟 中文

```text
主链到审批。普通 RAG 默认可零 LLM；AI/董事会报告经 Gateway 与 Ledger。
Fallback 固定串行。Compose 验收。数字 281/270/113。未完成项不夸大。
```

### 5 分钟架构 日文要点

```text
1) 業務：会議前の根拠付き分析と承認
2) React：JWT、ProtectedRoute、Learning Dashboard、Lifecycle
3) FastAPI 境界と Service/Repository/Gateway
4) 文書パイプラインと通常 RAG
5) LLM 双ルートと fallback
6) Approval 状態機と Audit
7) InMemory と PostgreSQL、Compose 永続化
8) 数字と未完了境界
```

### 5 分钟架构 中文要点

同日文 8 段结构；强调 Gateway 唯一入口、fail-closed、普通 RAG 零 Provider、Ledger Decimal、Compose 禁 -v。

## 14.2 架构亮点（中日对照）

| 亮点 | 中文 | 日本語 | 源码方向 |
|---|---|---|---|
| 权限 | JWT+RBAC+fail-closed | 同上 | auth / Permission Registry |
| 会话错误 | 401/403 分流 | 同上 | API Client |
| 审批 | 状态机+owner+History+ReportVersion | 同上 | approvals / report |
| 审计 | request_id + Persistent Audit | 同上 | audit services |
| LLM | Gateway+Evidence+Idempotency | 同上 | gateway / ai_analysis |
| 成本 | low/high + Decimal + Ledger | 同上 | ledger |
| 韧性 | Fallback Chain + circuit | 同上 | provider attempts |
| RAG | 默认可零 LLM | 既定ゼロ LLM | internal_rag |
| 交付 | Compose+Alembic+Stub E2E | 同上 | scripts |
| 前端学习 | Lifecycle + Dashboard | 同上 | frontend |

## 14.3 当前实现 vs 未完成（禁止夸大）

**已交付（可讲）**

- FastAPI / React / PostgreSQL/pgvector
- JWT、ProtectedRoute、RBAC、401/403
- Approval 状态机、ReportVersion、History
- Persistent Audit、Ledger、Gateway、双路由、Fallback
- 普通 RAG 默认零真实 LLM
- Docker Compose、Alembic head `20260717_07_fallback_chain`、Stub E2E
- Lifecycle Live Status、Learning Dashboard
- 测试：281/2、270/52、113/113

**未完成（必须诚实）**

- 真实付费 smoke（仅 opt-in）
- Billing、多租户、管理员预算 UI
- SIEM、WORM、Streaming
- DeepSeek 默认启用

## 14.4 项目化 25 问（中日）


### 14.4.1 なぜ PostgreSQL と InMemory を両立しますか

**日文回答**

```text
学習は InMemory、企業受入は PostgreSQL で契約一致を証明します。
（根拠：repository switch）
```

**中文理解**

```text
学习与企业验收双轨。
（源码/边界：repository switch）
```

### 14.4.2 なぜ業務から LLM SDK を直接呼ばないか

**日文回答**

```text
Gateway に集約し、枠と監査を外さないためです。
（根拠：gateway）
```

**中文理解**

```text
收口到 Gateway。
（源码/边界：gateway）
```

### 14.4.3 なぜ双ルートか

**日文回答**

```text
分析と報告でコストと品質を分けます。
（根拠：operation policy）
```

**中文理解**

```text
成本质量分桶。
（源码/边界：operation policy）
```

### 14.4.4 なぜ Decimal か

**日文回答**

```text
金額計算に float は使いません。
（根拠：ledger）
```

**中文理解**

```text
金额不用 float。
（源码/边界：ledger）
```

### 14.4.5 なぜ Idempotency-Key か

**日文回答**

```text
再送による二重課金を防ぎます。
（根拠：AI/Executive API）
```

**中文理解**

```text
防重放双计费。
（源码/边界：AI/Executive API）
```

### 14.4.6 なぜ Evidence Gate か

**日文回答**

```text
証拠なしの有料分析を防ぎます。
（根拠：AI analysis）
```

**中文理解**

```text
无证据不分析。
（源码/边界：AI analysis）
```

### 14.4.7 Fallback 失敗時は

**日文回答**

```text
次 Provider へ。open 回路はスキップ。
（根拠：chain）
```

**中文理解**

```text
串行切换/熔断跳过。
（源码/边界：chain）
```

### 14.4.8 employee が approve すると

**日文回答**

```text
403 です。
（根拠：RBAC）
```

**中文理解**

```text
403。
（源码/边界：RBAC）
```

### 14.4.9 submit の HTTP は

**日文回答**

```text
201 と pending_approval。
（根拠：approvals）
```

**中文理解**

```text
201。
（源码/边界：approvals）
```

### 14.4.10 報告生成後すぐ承認？

**日文回答**

```text
いいえ。明示 submit が必要です。
（根拠：executive report）
```

**中文理解**

```text
不自动审批。
（源码/边界：executive report）
```

### 14.4.11 ReportVersion の意味

**日文回答**

```text
版を残し改訂を追跡します。
（根拠：report model）
```

**中文理解**

```text
版本追踪。
（源码/边界：report model）
```

### 14.4.12 401 の UX

**日文回答**

```text
セッションを破棄しログインへ。
（根拠：frontend）
```

**中文理解**

```text
清会话。
（源码/边界：frontend）
```

### 14.4.13 403 の UX

**日文回答**

```text
ページに留まり拒否を表示。
（根拠：frontend）
```

**中文理解**

```text
留页提示。
（源码/边界：frontend）
```

### 14.4.14 Audit に残さないもの

**日文回答**

```text
Token、Key、全文 Prompt。
（根拠：audit）
```

**中文理解**

```text
敏感内容不落日志。
（源码/边界：audit）
```

### 14.4.15 request_id の使い方

**日文回答**

```text
ログと監査の相関キーです。
（根拠：logging）
```

**中文理解**

```text
关联键。
（源码/边界：logging）
```

### 14.4.16 Compose down -v

**日文回答**

```text
受入では禁止です。
（根拠：compose_down）
```

**中文理解**

```text
验收禁止。
（源码/边界：compose_down）
```

### 14.4.17 Alembic head

**日文回答**

```text
20260717_07_fallback_chain。
（根拠：migrations）
```

**中文理解**

```text
同左。
（源码/边界：migrations）
```

### 14.4.18 テスト数字

**日文回答**

```text
281/2、270/52、113。
（根拠：TEST_CASES）
```

**中文理解**

```text
同左。
（源码/边界：TEST_CASES）
```

### 14.4.19 Lifecycle の目的

**日文回答**

```text
React 学習表示。Backend に送らない。
（根拠：frontend）
```

**中文理解**

```text
教学不回传。
（源码/边界：frontend）
```

### 14.4.20 Learning Dashboard

**日文回答**

```text
固定欄で学習導線を固定。
（根拠：sidebar）
```

**中文理解**

```text
固定学习栏目。
（源码/边界：sidebar）
```

### 14.4.21 pgvector の位置

**日文回答**

```text
PostgreSQL 上のベクトル拡張。
（根拠：compose postgres）
```

**中文理解**

```text
PG 向量扩展。
（源码/边界：compose postgres）
```

### 14.4.22 なぜ Stub E2E か

**日文回答**

```text
費用ゼロで業務鎖を回帰。
（根拠：e2e test）
```

**中文理解**

```text
零费用回归主链。
（源码/边界：e2e test）
```

### 14.4.23 concurrent approve

**日文回答**

```text
状態機と 409 で守る。
（根拠：ApprovalService）
```

**中文理解**

```text
状态机+409。
（源码/边界：ApprovalService）
```

### 14.4.24 次に足りないもの

**日文回答**

```text
Billing UI、SIEM、有料 smoke 運用。
（根拠：roadmap 边界）
```

**中文理解**

```text
诚实演进。
（源码/边界：roadmap 边界）
```

### 14.4.25 この案件の価値

**日文回答**

```text
AI だけでなく統治境界があること。
（根拠：全栈）
```

**中文理解**

```text
治理边界完整。
（源码/边界：全栈）
```

## 14.5 与前文的关系

- 第 1–13 章：保留原项目介绍、FastAPI/LangGraph/RAG 训练路径。
- 第 14 章：用 V1.0 **已交付**能力校正架构与问答，避免把「未来 PostgreSQL / 无 JWT」等过期表述当当前事实。
- 面试时优先背诵第 14 章 30 秒 / 2 分钟 / 5 分钟，再按追问回跳到前文专题。


# 下一册预告

Volume 02：LangGraph 深挖（中日双语版）

内容包括：

- State 是什么
- Node 怎么拆
- Edge 怎么设计
- Conditional Edge
- Checkpoint
- Interrupt
- Retry
- Fallback
- 为什么不用 Celery / Airflow / Temporal
- 日本 TL 连续追问
