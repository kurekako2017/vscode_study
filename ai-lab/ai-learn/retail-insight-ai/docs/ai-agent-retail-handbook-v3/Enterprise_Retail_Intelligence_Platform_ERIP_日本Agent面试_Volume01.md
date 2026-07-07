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
