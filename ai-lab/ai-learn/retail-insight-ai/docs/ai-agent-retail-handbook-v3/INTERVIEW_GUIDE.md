# 日本项目面试讲解稿

这份文档用于日本项目面试场景。目标是把我负责设计和实现的企业 AI 后端项目讲清楚，并且让回答更符合日本现场对“结构、边界、职责、可维护性”的表达习惯。

## 项目一句话介绍

Retail Insight AI 是我负责设计和实现的企业 AI 后端项目，面向零售经营分析场景，已经打通任务、文档、检索、RAG、审批、安全、审计这条主链路，并且保留了后续接入真实 LLM、PostgreSQL、JWT/OAuth 的扩展位。

## 日本語一言紹介

Retail Insight AI は、私が設計・実装した企業向け AI バックエンドで、タスク、文書、検索、RAG、承認、RBAC、監査までの主経路をつないだシステムです。

## 项目背景

| 主题 | 中文说明 | 日本語要点 |
| --- | --- | --- |
| 为什么做这个项目 | 为了在可运行代码库里学习日本现场的 AI Agent 交付方式，同时保留面试时能讲清楚的边界 | 日本の現場に近い形で AI Agent の進め方を学びつつ、面接で説明できる境界を保つため |
| 业务价值 | 把经营分析从零散手工处理变成可重复、可追踪、可审计的系统 | 経営分析を繰り返し実行でき、追跡・監査できるシステムにするため |
| 当前阶段 | Local Static Provider、InMemory / Local Repository、FastAPI、SSE | Local Static Provider、InMemory / Local Repository、FastAPI、SSE |

## 我负责的范围

- 后端路由设计
- Service 层设计和实现
- Repository 接口和 InMemory 实现
- Workflow 编排
- Provider 抽象
- 审计和结构化日志
- 学习文档和面试文档

日语回答要点：

- `backend` 側のルート、Service、Repository、Workflow、Provider を担当しました。
- 文書だけでなく、運用しながら説明できる形を意識して整理しました。

## 系统架构怎么讲

```text
React -> FastAPI -> Task API -> TaskService -> Workflow -> KPI Engine -> Research Provider -> Report Generator -> SSE -> React
```

中文讲法：

- 前端只负责交互和展示。
- FastAPI 负责 HTTP 边界。
- TaskService 负责一次任务的生命周期。
- Workflow 负责流程编排。
- KPI 和 Research 分别负责确定性计算和本地研究。
- Report Generator 负责输出统一 Markdown。
- SSE 负责把进度实时推给前端。

日本語要点：

- フロントは操作と表示だけを担当します。
- FastAPI は HTTP 境界です。
- TaskService が 1 件のタスク全体をまとめます。
- Workflow が実行順序を制御します。
- SSE で進捗をフロントへ返します。

## Document Pipeline 怎么讲

中文讲法：

1. 先上传文档。
2. 再做 import，让文档进入可处理状态。
3. 再做 chunks，把内容切成可检索单元。
4. 再做 retrieval，在本地 chunk 上搜索。
5. 最后把检索结果送进 internal RAG。

日语回答要点：

- まず文書をアップロードします。
- 次に import で処理可能な状態へ進めます。
- その後 chunks を作成します。
- retrieval で検索し、最後に internal RAG へ渡します。

## RAG 怎么讲

中文讲法：

- 这里不是“接了一个大模型就叫 RAG”。
- 我这里的 RAG 是“文档切分 + 本地检索 + 证据组装 + 引用返回”。
- 当前默认是 deterministic，不依赖真实 LLM。
- 这样做的好处是可解释、可测试、可在面试里讲清楚。

日语回答要点：

- 単純に LLM をつなぐだけではなく、検索と根拠提示まで含めて RAG としています。
- 現在は deterministic で、説明しやすさとテスト容易性を優先しています。

## Approval Workflow 怎么讲

中文讲法：

- 报告生成后不会直接当成最终结论，而是进入审批流程。
- 审批动作分成 submit、list、detail、approve、reject、revise。
- 这样可以把“生成”与“发布”解耦，符合企业流程。

日语回答要点：

- レポート生成と公開を分離しています。
- submit / list / detail / approve / reject / revise に分けて、業務フローを明確にしています。

## RBAC / Audit 怎么讲

中文讲法：

- 审批接口不是所有人都能直接访问。
- 我在 approval API 上单独加了 RBAC。
- 拒绝访问时会写入 append-only audit fact。
- 这样既有安全边界，也有追踪能力。

日语回答要点：

- approval API にだけ RBAC をかけています。
- 拒否時は append-only の監査情報を残します。
- 監査と権限制御を分けて考えています。

## 为什么先用 InMemory

中文讲法：

- 先用 InMemory 是为了让项目在一台机器上就能跑起来。
- 这可以把学习重心放在架构和流程，而不是先被基础设施卡住。
- 后续切换 PostgreSQL 时，只需要替换 repository 实现，不需要重写 Service。

日语回答要点：

- まず 1 台の環境で動くことを優先しました。
- 学習初期はインフラよりも構造理解を優先しています。
- 将来は Repository の差し替えで PostgreSQL に拡張できます。

## 为什么用 Repository Pattern

中文讲法：

- Repository Pattern 让业务层只依赖抽象，不依赖存储细节。
- 这样 InMemory 和 PostgreSQL 可以共存于同一套 Service 接口下面。

日语回答要点：

- Service は保存方法の詳細に依存しません。
- Repository 抽象のおかげで InMemory と PostgreSQL を入れ替えやすくしています。

## 为什么用 Provider Pattern

中文讲法：

- Provider Pattern 让 Research、LLM、外部搜索这类可替换能力都挂在同一个接缝上。
- 现在先用本地静态 Provider，后续再替换真实实现。

日语回答要点：

- Provider は差し替え可能な外部能力の接続点です。
- 今は Static Provider、将来は実サービスに置き換えられます。

## 为什么真实 LLM / PostgreSQL / JWT 是后续扩展

中文讲法：

- 真实 LLM 会引入非确定性和成本问题，所以先冻结接口和流程。
- PostgreSQL 会引入迁移和部署复杂度，所以先把抽象层跑稳。
- JWT/OAuth 会引入身份体系和权限体系，所以先把 current user seam 和 RBAC contract 冻结。
- 这样后续扩展时，改的是实现，不是把主链路推倒重来。

日语回答要点：

- LLM は非決定性とコストがあるので後回しにしました。
- PostgreSQL は移行コストがあるので抽象層を先に固めました。
- JWT/OAuth は認証基盤なので、後段の拡張として扱っています。

## 当前可以演示的主链路

1. `POST /api/tasks`
2. `GET /api/tasks/{task_id}`
3. `GET /api/tasks/{task_id}/report`
4. `POST /api/v1/documents`
5. `POST /api/v1/documents/{document_id}/import`
6. `POST /api/v1/documents/{document_id}/chunks`
7. `POST /api/v1/document-retrieval/search`
8. `POST /api/v1/internal-rag/answer`
9. `POST /api/v1/reports/{task_id}/submit-approval`
10. `GET /api/v1/users/me`
11. `GET /api/v1/security/roles`
12. `GET /api/v1/security/permissions`
13. `GET /api/v1/audit-logs`

中文讲法：

- 我可以直接演示从任务创建到报告、再到文档、检索、RAG、审批、安全和审计的主链路。

日语回答要点：

- タスク作成からレポート、文書、検索、RAG、承認、RBAC、監査までをその場で見せられます。

## 面试官可能问的问题

| 问题 | 中文回答 | 日本語回答要点 |
| --- | --- | --- |
| 为什么先用 InMemory？ | 先跑通主链路，再谈基础设施替换。 | まず動く状態を作り、その後に基盤を差し替えます。 |
| 为什么不直接接真实 LLM？ | 先把确定性、可测性和可解释性做稳。 | 決定性、テスト容易性、説明しやすさを優先しました。 |
| 为什么只在 approval 上做 RBAC？ | 审批是高风险边界，先把最敏感区域收紧。 | 承認は高リスクなので、先に境界を厳しくしました。 |
| 以后怎么接 PostgreSQL？ | 通过 Repository 替换实现，不动 Service 和 API 合同。 | Repository 差し替えで対応し、Service と API 契約は維持します。 |
| 这个 RAG 和普通问答有什么区别？ | 它有检索证据、引用和 warning，不是黑盒回答。 | 根拠・引用・warning があり、ブラックボックスではありません。 |

## 面试收尾说法

中文：

这个项目我已经把主链路、契约边界和可扩展点都整理好了，所以它不是一个只能跑 Demo 的项目，而是一个可以继续往企业级方向扩展的后端基座。

日本語要点：

- 主経路、契約境界、拡張点を整理済みです。
- Demo だけでなく、企業向けに拡張できる backend 基盤として説明できます。

