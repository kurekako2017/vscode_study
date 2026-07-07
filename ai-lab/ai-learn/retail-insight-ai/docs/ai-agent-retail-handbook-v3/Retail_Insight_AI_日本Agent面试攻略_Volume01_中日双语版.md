# Retail Insight AI 日本 Agent 面试攻略 V1.0
## Volume 01 - 项目介绍与系统架构（中日双语版）

> 适用对象：日本 AI Agent / Python Backend / LLM Application / RAG 工程师岗位  
> 用法：先读中文理解，再背日文回答。面试时优先使用日文回答，中文只作为自己的理解辅助。

---

# 1. 面试开场 / 面接冒頭

## 1.1 60秒自我介绍（日文）

皆さま、はじめまして。  
私はバックエンド開発を中心に、API 設計、業務ロジック、ワークフロー設計、データ連携を担当してきました。

最近の AI 関連プロジェクトでは、**Retail Insight AI** という小売業向け AI 経営分析システムに取り組みました。  
このシステムでは、POS、在庫、商品、会員、販促などのデータをもとに KPI を分析し、市場・競合情報の調査結果と合わせて、日本語の経営分析レポートを生成します。

私は主に、FastAPI による API 設計、TaskService、LangGraph Workflow、Research Agent、SSE による進捗通知、Report Generator、そして将来的な LangChain / RAG / Vector Database への拡張設計を担当しました。

## 1.2 中文理解

这段用于 AI Agent 案件的开场。重点不是说“我做了 AI”，而是说：

- 我是后端开发
- 最近做的是 Retail Insight AI
- 这是日本零售经营分析系统
- 我负责 API、TaskService、LangGraph、Research Agent、SSE、Report Generator
- LangChain / RAG / Vector Database 是未来企业化扩展方向

---

# 2. 项目概要 / プロジェクト概要

## 2.1 面试官问题（日文）

Retail Insight AI の概要を説明してください。

## 2.2 回答（日文）

Retail Insight AI は、日本の小売業向け AI 経営分析システムです。  
小売業では、経営会議の前に POS、在庫、商品、会員、販促など複数のデータを確認し、市場や競合の情報も合わせて分析する必要があります。

このプロジェクトでは、利用者が分析タスクを作成すると、TaskService がタスクの状態を管理し、LangGraph Workflow が KPI 分析、Research、Report Generator の処理を制御します。  
進捗は SSE で画面へ通知し、最終的に経営判断に使える日本語レポートを生成します。

現在は Keyword Retrieval を中心とした構成ですが、将来的には LangChain、Embedding、pgvector を使った Hybrid Retrieval へ拡張する設計にしています。

## 2.3 中文理解

这是项目概要的标准回答。回答顺序：

1. 日本零售业务背景
2. 系统要解决的问题
3. TaskService + LangGraph 的执行流程
4. SSE 进度通知
5. 未来 LangChain / Embedding / pgvector 扩展

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
PostgreSQL / pgvector（Target）
```

FastAPI は HTTP Boundary、TaskService は Application Service、LangGraph は Workflow Orchestration を担当します。  
将来的に LangChain は RAG Orchestration として、Retriever、Prompt Builder、Context Builder、Embedding Pipeline を担当する想定です。

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
Retail Insight AI では、KPI 分析、Research、Report Generator など複数の処理があり、入力内容によって実行経路が変わります。

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

LangChain は将来的に RAG Orchestration を担当する想定です。  
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
現在は Keyword Retrieval が中心ですが、将来的には文書を Chunk に分割し、Embedding を作成して、pgvector に保存する設計です。

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
ただし、Retail Insight AI の第一段階では PostgreSQL + pgvector の方が導入コストと運用コストのバランスが良いと考えています。

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

Retail Insight AI は、日本の小売業向け AI 経営分析システムです。  
POS、在庫、商品、会員、販促データと市場・競合調査を組み合わせ、経営判断に使える日本語レポートを生成します。

私はバックエンドを中心に、FastAPI、TaskService、LangGraph Workflow、Research Agent、SSE、Report Generator を担当しました。  
設計上は、FastAPI を HTTP Boundary、TaskService を Application Service、LangGraph を Workflow Orchestration として分離しています。

現在は Keyword Retrieval を中心に構成していますが、将来的には LangChain、Embedding、pgvector を使い、Hybrid Retrieval と Citation に対応する設計です。

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
5. 每次训练都不要夸大 Current / Planned / Target

---

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
