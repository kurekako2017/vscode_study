# AI Agent 设计指南

本文件说明 Retail Insight AI 中 `Workflow`、`Agent`、`Tool`、`Repository`、`Provider`、`Retrieval`、`RAGAnswerGenerator`、`Approval`、`RBAC`、`Audit` 的职责边界。中文为主，日本語为补足；英文只保留技术名词、类名、接口名和生态名称。

## 1. 目的

中文说明：

**V1.0 说明**：仓库已交付 LLM Gateway、Stub/Fallback Provider、普通 RAG 默认可零 LLM、JWT/审批治理。下文「当前阶段不接真实 LLM」指 *默认学习路径与 Agent 编码约束*，不是否定 Gateway 已落地。

本项目不是先做一个全自动 Agent，再回头补规则。当前阶段优先把业务流程拆成可解释、可测试、可审计的 `Workflow`，再在明确边界内引入 `Agent`、`Tool`、`Provider` 和未来 LLM 能力。

这份文档用于回答三个问题：

- 哪些能力应该放在确定性 `Workflow`。
- 哪些能力未来可以升级为 `Agent`。
- 哪些外部能力必须通过 `Provider` 或 `Tool` 接入，而不是直接写进业务服务。

日本語補足：

このプロジェクトでは、まず説明可能でテストしやすい `Workflow` を優先します。`Agent` は必要な場所に限定して導入します。

## 2. Workflow 和 Agent 的区别

中文说明：

`Workflow` 适合固定步骤、明确输入输出、需要审计的业务流程。`Agent` 适合开放式检索、工具选择、多轮推理和不确定路径，但必须有权限、预算、超时、审计和 fallback。

当前项目的经营分析、Document Pipeline、Internal RAG、Approval 都优先用 `Workflow` 表达，因为学习者需要看清楚程序从 API 到 Service、Repository、Response 的路径。

日本語補足：

`Workflow` は固定業務フローに向いています。`Agent` は自由度が高い一方で、制御と監査が必要です。

| 概念 | 适合场景 | 不适合场景 | 本项目例子 |
|---|---|---|---|
| `Workflow` | 固定业务流程、状态推进、审批、报告生成 | 开放式研究、动态工具选择 | Task Workflow、Document Import、Approval Workflow |
| `Agent` | 多步推理、动态选择 Tool、开放式证据收集 | 必须强一致、必须一步一步审计的核心交易 | 未来市场调研 Agent、未来资料检索 Agent |
| `Tool` | 外部能力调用、权限敏感操作、副作用操作 | 普通领域状态读写 | 未来 Search Tool、Future MCP Tool |
| `Provider` | 可替换的数据源、模型源、检索源 | 业务状态持久化 | `StaticResearchProvider`、未来 `LLMProvider` |

## 3. Tool

中文说明：

`Tool` 是 Agent 可以调用的能力边界。只要一个能力有外部依赖、副作用、权限风险、成本风险或超时风险，就不应该让 Agent 随意调用内部函数，而应该包装成有 schema、timeout、error mapping、audit 的 `Tool`。

在本项目默认学习阶段，Tool 不是主实现重点。原因是默认不接真实外部业务系统、不默认产生真实 LLM 费用、不接 MCP。未来引入 MCP 或搜索能力时，Tool 才会成为 Agent 与外部能力之间的标准边界。

日本語補足：

`Tool` は Agent が外部能力を安全に使うための境界です。権限、監査、タイムアウトを必ず設計します。

## 4. Repository

中文说明：

`Repository` 保存业务事实和状态历史，例如 Task、Report、Document、Chunk、Approval、AuditLog。Service 只能依赖 Repository interface，不能依赖具体存储细节。

当前默认路径是 `InMemoryRepository` / Local Repository。PostgreSQL 是可选演进方向，不是默认学习路径。不要把 Prompt 当状态存储，也不要把业务事实隐藏在 Agent 记忆里。

日本語補足：

`Repository` は業務データの保存境界です。Prompt や Agent Memory をデータベース代わりに使ってはいけません。

## 5. Provider

中文说明：

`Provider` 用于包装可替换的外部来源或模型来源。它解决的是“未来可以换供应商，但不改业务合同”的问题。

本项目中的 Provider 应该满足：

- Service 不直接知道外部供应商 SDK。
- Provider 负责 timeout、retry、provider error mapping。
- Provider 返回结构化结果，不返回随意文本。
- Provider 需要记录 provider name、model name、latency、token、cost 的占位字段。
- Provider 失败时，业务服务必须有明确 fallback 或稳定错误码。

日本語補足：

`Provider` は外部サービスやモデルを差し替え可能にするための層です。Service は SDK に直接依存しません。

## 6. RAGAnswerGenerator

中文说明：

`RAGAnswerGenerator` 是 Retrieval 结果和未来 `LLMProvider` 之间的答案生成边界。它不负责检索、不负责存储、不负责审批状态，只负责把已检索到的 evidence 组装成 answer，并校验输出是否满足 citation-safe contract。

当前默认实现应该继续支持 deterministic extractive mode，也就是不依赖真实 LLM 也能返回可解释答案。未来接入 LLM 后，如果 Provider 超时、返回无效、缺少 citation、超预算或触发安全规则，必须回退到 deterministic fallback。

日本語補足：

`RAGAnswerGenerator` は検索結果から回答を作る境界です。検索や保存や承認状態は持ちません。

## 7. LLMProvider

中文说明：

`LLMProvider` 是未来接入 OpenRouter、NVIDIA、Gemini、本地 Qwen 等模型后端的统一抽象。业务服务不应该知道具体模型平台，只应该依赖 `LLMProvider` interface。

未来接入建议：

| Provider | 接入方式 | 必须保持不变 | 风险控制 |
|---|---|---|---|
| OpenRouter | 新增 `OpenRouterLLMProvider` | API response contract、citation contract | timeout、model name、cost limit、provider error |
| NVIDIA | 新增 `NvidiaLLMProvider` | `RAGAnswerGenerator` 输入输出 | GPU / endpoint 不稳定时 fallback |
| Gemini | 新增 `GeminiLLMProvider` | Service 层接口 | safety block、quota、latency |
| 本地 Qwen | 新增 `LocalQwenLLMProvider` | 内部 RAG API contract | 本地资源、模型版本、响应格式 |

日本語補足：

モデルを切り替えても API 契約と Service 境界を変えないことが重要です。

## 8. Retrieval

中文说明：

`Retrieval` 负责查找证据，不负责生成最终答案。它可以包含关键词检索、metadata 过滤、top-k、score 排序、source trace 和未来 rerank。

本项目需要区分三类 Retrieval：

| 类型 | 数据来源 | 输出 | 注意点 |
|---|---|---|---|
| Business Retrieval | 销售、库存、会员、促销等结构化事实 | 结构化 business facts | 保持确定性和可审计 |
| Internal RAG Retrieval | 上传文档、制度、FAQ、内部资料 | chunks、citations、metadata | 必须保留 source trace 和 ACL |
| Internet Search | 公开网页、市场信息、竞品信息 | 外部 evidence | 需要可信度、新鲜度和引用检查 |

日本語補足：

`Retrieval` は証拠を探す層です。回答生成とは分離します。

## 9. Approval

中文说明：

`Approval` 用于高影响输出的发布前控制，例如经营分析报告、制度相关回答、对外展示内容。审批状态必须独立于 Task 执行状态，不能用 task completed 代表 report approved。

审批系统必须记录：

- actor
- action
- target
- before / after status
- reason
- request_id
- timestamp
- audit result

日本語補足：

承認状態とタスク実行状態は別です。承認履歴は監査可能でなければなりません。

## 10. RBAC / Audit

中文说明：

`RBAC` 负责判断“谁可以看什么、谁可以做什么”。`Audit` 负责记录“谁在什么时候做了什么、结果是什么”。两者不是可选功能，尤其在 Retrieval、Approval、Security API 中必须长期保留。

本项目中需要保护的风险包括：

- 未授权用户批准报告。
- 用户看到不属于自己权限范围的文档。
- 审批失败但没有 audit log。
- RAG 引用到没有权限访问的 chunk。
- 后台错误没有 request_id，无法追踪。

日本語補足：

`RBAC` は権限判断、`Audit` は操作記録です。検索と承認では必須です。

## 11. 为什么当前优先 Workflow，不直接做全自动 Agent

中文说明：

当前项目是学习型企业 AI 后端项目。优先 `Workflow` 的原因：

- 初学者能清楚看到 API、Service、Repository、Workflow 的调用路径。
- 每一步输入输出固定，便于 Swagger 验证和 unittest 覆盖。
- 审批、审计、错误码、SSE 事件都可以稳定设计。
- 不接真实 LLM 时仍可运行，避免学习被外部模型和账号问题阻塞。
- 未来接 Agent 时，可以只替换局部 Provider / Tool，不破坏主链路。

全自动 Agent 的风险：

- 行为不稳定，测试难度高。
- 容易绕过权限和审批边界。
- 调用成本和延迟不可控。
- 失败原因难以向面试官或团队解释。

日本語補足：

学習段階では、まず安定した `Workflow` を作り、その後必要な部分だけ `Agent` 化します。

## 12. 设计判断矩阵

| 需求 | 优先选择 | 原因 | 本项目落点 |
|---|---|---|---|
| 固定业务流程 | `Workflow` | 可测试、可审计、可解释 | Task、Document、Approval |
| 开放式证据收集 | `Agent + Tool` | 需要动态选择能力 | 未来市场调研 |
| 持久化业务事实 | `Repository` | 可回放、可替换存储 | TaskRepository、DocumentRepository |
| 可替换模型或来源 | `Provider` | 隔离供应商差异 | StaticResearchProvider、未来 LLMProvider |
| 内部文档问答 | `Retrieval + RAGAnswerGenerator` | 需要 citation 和 evidence | Internal RAG |
| 高风险发布 | `Approval + RBAC + Audit` | 需要责任边界 | Report Approval |

## 13. 推荐程序边界

```text
FastAPI Router
↓
Service
↓
Workflow / Domain Logic
↓
Repository / Provider / Retrieval
↓
RAGAnswerGenerator / Approval / Audit
↓
Response
```

## 14. 面试讲法

中文说明：

可以这样讲：

“这个项目没有一开始就做全自动 Agent，而是先用确定性 Workflow 固定业务流程。Repository 保存业务事实，Provider 隔离未来外部模型或搜索源，Retrieval 负责找证据，RAGAnswerGenerator 负责基于证据生成带 citation 的答案，Approval、RBAC、Audit 负责企业级治理。这样既能本地运行，也方便未来把某些节点替换成 OpenRouter、NVIDIA、Gemini 或本地 Qwen。”

日本語補足：

面接では「まず安定した Workflow を作り、Provider によって将来のモデル差し替えを可能にしている」と説明できます。
