# 日本项目面试讲解稿

这份文档用于日本项目面试场景。它把 Retail Insight AI 作为一个**企业 AI 后端项目**来说明，而不是把它描述成单纯的学习项目。

## 项目介绍

### 中文说明

Retail Insight AI 是一个企业级 AI 后端项目，面向零售经营分析场景。我作为项目开发团队的一员（SE），参与了企业 AI 后端系统的设计、开发、联调、测试和持续完善。

项目围绕零售经营分析场景，构建任务流程、文档管理、Internal RAG、审批流程、安全控制和审计等核心能力，并预留真实 `LLM`、`PostgreSQL` 以及前端系统接入能力。

### 日本語説明

Retail Insight AI は企業向け AI バックエンドプロジェクトです。

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
・RBAC
・監査

などの機能開発に携わりました。

## 当前实现

### 中文

- `FastAPI` 后端入口、路由、结构化日志、请求上下文
- `Task API`、`TaskService`、`Workflow`、`KPI Engine`、`Research Provider`、`Report Generator`
- `SSE` 任务进度推送
- `Document Upload`、`Document Read`、`Document Archive`、`Document Import`、`Document Chunk`、`Document Retrieval`
- `Internal RAG without LLM`
- 审批工作流、审批 `RBAC`、审计读模型
- 本地 `StaticResearchProvider`、`InMemoryRepository`、`LocalBusinessDataProvider`

### 日本語

- `FastAPI` の入口、ルート、構造化ログ、request context
- `Task API`、`TaskService`、`Workflow`、`KPI Engine`、`Research Provider`、`Report Generator`
- `SSE` による進捗通知
- `Document Upload`、`Document Read`、`Document Archive`、`Document Import`、`Document Chunk`、`Document Retrieval`
- `LLM` なしの `Internal RAG`
- 承認ワークフロー、承認 `RBAC`、監査 read model
- ローカルの `StaticResearchProvider`、`InMemoryRepository`、`LocalBusinessDataProvider`

## 我的职责

### 中文

- 参与后端模块开发
- `FastAPI` `API` 开发
- `Service` 层开发
- `Repository` 层开发
- 文档处理流程开发
- `Internal RAG` 功能开发
- `Approval` 工作流开发
- `RBAC` 与 `Audit` 功能开发
- `Swagger` 联调
- `unittest` 编写
- `Bug` 修复
- 文档维护
- 与团队成员协作完成开发

### 日本語

- バックエンドモジュール開発への参加
- `FastAPI` `API` 開発
- `Service` 層の開発
- `Repository` 層の開発
- 文書処理フローの開発
- `Internal RAG` 機能の開発
- `Approval` ワークフローの開発
- `RBAC` と `Audit` 機能の開発
- `Swagger` 連携
- `unittest` の作成
- `Bug` 修正
- 文書メンテナンス
- チームメンバーと協力して開発を進めました

## 系统架构

```text
React -> FastAPI -> Task API -> TaskService -> Workflow -> KPI Engine -> Research Provider -> Report Generator -> SSE -> React
```

### 中文讲法

- 前端只负责交互和展示。
- `FastAPI` 负责 `HTTP` 边界。
- `TaskService` 负责一次任务的生命周期。
- `Workflow` 负责流程编排。
- `KPI` 和 `Research` 分别负责确定性计算和本地研究。
- `Report Generator` 负责输出统一 `Markdown`。
- `SSE` 负责把进度实时推给前端。

### 日本語講法

- frontend は操作と表示だけを担当します。
- `FastAPI` は `HTTP` 境界です。
- `TaskService` が 1 件のタスク全体をまとめます。
- `Workflow` が実行順序を制御します。
- `KPI` と `Research` はそれぞれ確定的計算とローカル調査を担当します。
- `Report Generator` が統一 `Markdown` を出力します。
- `SSE` で進捗を frontend へ返します。

## 为什么这样设计

### 中文

- 先用 InMemory，是为了让项目在一台机器上就能跑起来，学习重点先放在架构和流程。
- 用 `Repository`，是为了把业务和存储细节隔离开，未来替换 `PostgreSQL` 不需要重写 `Service`。
- 用 `Provider`，是为了把 Research、`LLM`、外部搜索这类可替换能力都放在同一个接缝上。
- 用 `Workflow`，是为了把多步骤流程显式化，方便解释、测试和扩展。
- 先冻结接口和流程，再逐步升级基础设施，这样更符合企业项目演进方式。

### 日本語

- まず `InMemory` にするのは、1 台で動かして構造理解を優先するためです。
- `Repository` を使うのは、業務ロジックと保存方式を分離して、将来 `PostgreSQL` に差し替えやすくするためです。
- `Provider` を使うのは、Research や `LLM` のような差し替え可能な能力を同じ接続点にまとめるためです。
- `Workflow` を使うのは、多段階の処理順序を明示して、説明・テスト・拡張をしやすくするためです。
- まず契約と流れを固定し、その後に基盤を段階的に強化する方が、企業案件の進め方に近いです。

## 日本项目表达

### 中文回答

“这个项目我负责的是企业 AI 后端的主链路设计和实现。当前已经把任务、文档、检索、RAG、审批、安全和审计串起来了。现在的实现重点不是追求一次性接入所有外部系统，而是先把可运行、可解释、可扩展的后端基座做稳。”

### 日本語回答

「このプロジェクトでは、企業向け AI バックエンドの主経路設計と実装を担当しました。タスク、文書、検索、RAG、承認、セキュリティ、監査までをつないでいます。今は外部システムを一気に増やすより、動作可能で説明しやすく、拡張しやすい backend 基盤を固めることを重視しています。」

## 当前边界

### 中文

- 还没有真实 `JWT` / `OAuth`
- 还没有真实 `PostgreSQL` 生产迁移
- 还没有真实 `LLM` 接入
- 还没有把 `frontend` 作为主展示入口
- 还没有把 `MCP` 当作当前完成项

### 日本語

- 実 `JWT` / `OAuth` はまだありません
- 実 `PostgreSQL` への本番移行はまだです
- 実 `LLM` 接続はまだありません
- `frontend` はまだ主展示入口ではありません
- `MCP` はまだ現在の完了範囲ではありません

## 未来扩展

### 中文

- 接入真实认证后，可以把 current user seam 替换成真正的身份来源。
- 接入真实 `PostgreSQL` 后，可以保留 `Service` 和 `API` 合同，只替换 `Repository`。
- 接入真实 `LLM` 后，可以保留 `RAG` 的引用和错误语义，只替换 `Provider`。
- 继续扩展 `frontend`、`MCP` 和生产部署时，仍要保持现有接口契约不变。

### 日本語

- 実認証を入れれば、current user seam を本当の identity source に差し替えられます。
- 実 `PostgreSQL` を入れても、`Service` と `API` 契約は維持し、`Repository` だけを差し替えられます。
- 実 `LLM` を入れても、`RAG` の引用やエラーの意味は維持し、`Provider` だけを差し替えられます。
- `frontend`、`MCP`、本番デプロイを広げる時も、既存の契約は壊さない方針です。

## 面试常问问题

| 问题 | 中文回答 | 日本語回答要点 |
| --- | --- | --- |
| 为什么先用 InMemory？ | 先跑通主链路，再谈基础设施替换。 | まず動く状態を作り、その後に基盤を差し替えます。 |
| 为什么不直接接真实 `LLM`？ | 先把确定性、可测性和可解释性做稳。 | 決定性、テスト容易性、説明しやすさを優先しました。 |
| 为什么只在 approval 上做 `RBAC`？ | 审批是高风险边界，先把最敏感区域收紧。 | 承認は高リスクなので、先に境界を厳しくしました。 |
| 以后怎么接 `PostgreSQL`？ | 通过 `Repository` 替换实现，不动 `Service` 和 `API` 合同。 | `Repository` の差し替えで対応し、`Service` と `API` 契約は維持します。 |
| 这个 `RAG` 和普通问答有什么区别？ | 它有检索证据、引用和 warning，不是黑盒回答。 | 根拠、引用、warning があり、ブラックボックスではありません。 |

## 收尾说法

### 中文

这个项目我已经把主链路、契约边界和可扩展点都整理好了，所以它不是一个只能跑 `Demo` 的项目，而是一个可以继续往企业级方向扩展的后端基座。

### 日本語

主経路、契約境界、拡張点を整理済みです。`Demo` だけでなく、企業向けに拡張できる backend 基盤として説明できます。
