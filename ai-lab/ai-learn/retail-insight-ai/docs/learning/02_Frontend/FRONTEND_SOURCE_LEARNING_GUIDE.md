# ERIP 前端页面、企业业务测试与源码学习指南

## 1. 这份文档解决什么问题

本指南把浏览器中的实际操作，连接到 React、API Client 和 FastAPI 源码。

学习目标不是记住页面文案，而是能回答：

```text
用户在什么页面输入什么？
→ React 哪个事件处理函数接收输入？
→ frontend/src/api.ts 发出哪个 HTTP 请求？
→ Backend 的 Router、Service、Repository / Workflow 如何处理？
→ 页面最终显示哪些真实字段或错误？
```

当前系统正式名称是 **Enterprise Retail Intelligence Platform（ERIP）**。Dashboard 是中文的学习总览；业务操作 UI 保持日语。技术名词如 React、FastAPI、SSE、RAG、InMemory、LLM 保持英文。

## 2. ERIP 页面与企业业务流程总览

统一案例：某零售企业发现**关东地区饮料分类销售额下降**，需要登记资料、验证内部检索、生成经营分析、提交负责人审批，并保留可追踪依据。

```text
文書管理
  产生：document_id、import_id、Chunk
  ↓ 手动衔接（输入相同的检索条件）
RAG検索
  读取：Chunk；返回：document_id、chunk_id、citation
  ↓ 手动衔接（把结论写入分析问题）
分析依頼
  产生：task_id、SSE 进度、report
  ↓ 手动衔接（复制已完成的 task_id）
承認管理
  产生：approval_id、report_version_id、审批事件
  ↓
最终可审计报告
  当前未连接：没有单独的前端汇总页
```

这里的“手动衔接”非常重要：当前前端没有自动把 `document_id`、RAG citation 或 `task_id` 带到下一页。不要把四个独立 API 页面误解为已实现的端到端自动编排。

| 页面     | 主要对象                                    | 当前连接状态                             |
| -------- | ------------------------------------------- | ---------------------------------------- |
| 文書管理 | `document_id`、`import_id`、Chunk       | 文档和 Chunk 在 Backend 内已连接         |
| RAG検索  | `document_id`、`chunk_id`、`citation` | 与文档通过存储数据连接；前端条件手动输入 |
| 分析依頼 | `task_id`、`report`                     | 当前不读取 RAG 的答案或 citation         |
| 承認管理 | `approval_id`、`report_version_id`      | 手动输入 TasksPage 产生的`task_id`     |

## 3. App.tsx 如何决定显示哪个页面

页面入口：`frontend/src/App.tsx`。

页面看到什么
→ 顶部导航的「学习总览」「文書管理」「RAG検索」「分析依頼」「承認管理」。

点击后发生什么
→ `setActiveView()` 改变本地 `useState`。

调用哪个 API
→ 不调用 API。导航只是 React 本地状态切换。

Backend 经过什么
→ 不经过 Backend。

返回后页面怎么变化
→ `App` 根据 `activeView` 渲染对应 Page Component。各页面自己的 `useEffect` 或提交动作才可能发请求。

关键代码：

```tsx
const [activeView, setActiveView] = useState<ViewTab>("dashboard");
{activeView === "documents" && <DocumentsPage />}
```

源码阅读顺序：

1. `frontend/src/App.tsx`
2. `frontend/src/pages/DashboardPage.tsx`
3. `frontend/src/pages/DocumentsPage.tsx`
4. `frontend/src/pages/RagPage.tsx`
5. `frontend/src/pages/TasksPage.tsx`
6. `frontend/src/pages/ApprovalPage.tsx`
7. `frontend/src/api.ts`

## 4. DashboardPage 学习什么

文件：`frontend/src/pages/DashboardPage.tsx`

页面看到什么
→ 「企业业务流程」「推荐学习顺序」「企业综合测试案例 ERIP-E2E-001」以及当前能力边界。

点击后发生什么
→ 流程卡片调用 `onNavigate(target)`，由 `App.tsx` 切换到业务页面。

调用哪个 API
→ Dashboard 本身不调用 API。

Backend 经过什么
→ 不经过 Backend。

返回后页面怎么变化
→ 跳转到对应页面；真正的数据请求由目标页面发起。

应确认的真实边界：

- 数据存储是 `InMemory`。
- 检索方式是 Keyword Retrieval。
- Internal RAG 回答是 deterministic assembly。
- 真实 LLM 未启用。
- PostgreSQL 在当前运行环境尚未验证，`pgvector` 尚未实现。

## 5. DocumentsPage：页面操作 → React → API → Backend → 结果

文件：`frontend/src/pages/DocumentsPage.tsx`

### 5.1 在页面做什么

标准业务流程是：

```text
Upload → Import → Chunk → RAG検索
```

以 `docs/learning/sample-data/Scenario01_Sales_Decline/02_関東地域在庫レポート.md` 为例：

1. 在「文書アップロード」选择 markdown/text 文件，填写タイトル、担当者、言語；tags 是可选项。
2. 点击「文書をアップロード」，确认 HTTP `201`、`upload_id`、`document_id`、上传会话 `status=completed`，再确认文档详情的实际状态是 `uploaded`。
3. 选择该文档并点击 Import。Import 没有独立 validate 按钮；它在内部校验后，成功时返回 `import_id`、`status=completed`，并把文档状态更新为 `validated`。
4. 确认文档为 `validated` 且类型为 markdown/text 后点击「Chunk実行」，确认 HTTP `201`、`items`、`chunk_id` 和 Chunk 数量。
5. 进入 RAG検索 执行 `RAG-BIZ-001`，确认检索结果引用当前 Chunk。

`Archive` 是维护操作，不是上述标准步骤。用于资料过期、内容错误或新版替换旧版；不能把它理解为 `Upload → Archive → Import → Chunk`。

### 5.2 上传流程

页面看到什么
→ 文件、标题、担当者、标签和上传结果。

点击后发生什么
→ `submitUpload()` 读取 `File` 和 metadata，调用 `uploadDocument()`；成功后调用 `loadDocuments(false)` 并选中返回的 `document_id`。

调用哪个 API

```text
POST /api/v1/documents
multipart: file、metadata、可选 Idempotency-Key
成功：201，data.upload_id、data.document_id、data.status=completed
```

注意：`completed` 是上传会话状态。成功创建的文档实体初始状态是 `uploaded`；只有 Import 成功后才会成为 `validated`。

Backend 经过什么

```text
backend/app/api/documents.py upload_document()
→ backend/app/services/document_upload_service.py DocumentUploadService.upload_document()
→ backend/app/repositories/implementations/in_memory/document_repository.py InMemoryDocumentRepository.create()
→ DocumentUploadSessionResponse
```

返回后页面怎么变化
→ 成功提示显示真实 `document_id`，列表刷新。后端错误经 `ApiClientError` 显示 code 和 message。

### 5.3 列表、详情、Import、Chunk、归档

| 页面操作   | React / API                                               | 实际 Backend 链                                                                                                                                    |
| ---------- | --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| 加载列表   | `loadDocuments()` → `listDocuments()`                | `documents.py list_documents()` → `DocumentReadService.list_documents()` → `InMemoryDocumentRepository.list_all()`                         |
| 选择详情   | `refreshSelectedDocument()` → `getDocument()`        | `documents.py get_document()` → `DocumentReadService.get_document()` → `InMemoryDocumentRepository.get()`                                  |
| Import     | `runDocumentAction("import")` → `importDocument()`   | `document_imports.py import_document()` → `DocumentImportService.import_document()` → 文档 Repository 的真实 get/update                      |
| Chunk      | `runDocumentAction("chunk")` → `chunkDocument()`     | `document_chunks.py chunk_document()` → `DocumentChunkService.chunk_document()` → `InMemoryDocumentChunkRepository.replace_for_document()` |
| 读取 Chunk | `refreshSelectedDocument()` → `getDocumentChunks()`  | `document_chunks.py get_document_chunks()` → `DocumentChunkService.get_chunks()` → `InMemoryDocumentChunkRepository.list_for_document()`   |
| 归档       | `runDocumentAction("archive")` → `archiveDocument()` | `documents.py archive_document()` → `DocumentArchiveService.archive_document()` → `InMemoryDocumentRepository.update()`                    |

Import 允许未归档的 `uploaded` 或 `validated` markdown/text/csv/json；Chunk 当前严格要求未归档的 `validated` markdown/text。文档不存在是实际 `404 document_not_found`；归档文档 Import/Chunk 返回 `409 document_archived`，未验证 Chunk 返回 `409 document_not_validated`，不支持类型返回 `415 unsupported_document_type`。

默认 `GET /api/v1/documents` 与 RAG 检索都排除 `archived`。勾选「アーカイブ済みを含める」会让列表请求带上 `include_archived=true`；RAG 请求也只有 `include_archived=true` 才会包含归档资料。归档后仍可读取历史详情和 Chunk，但不能继续 Import 或 Chunk。

### 5.4 建议企业测试 Case

- `DOC-BIZ-001`：完整标准流程，确认 Upload → Import → Chunk → RAG検索。
- `DOC-BIZ-002`：清空必填项，确认按钮不可点击或显示 Backend 校验错误。
- `DOC-BIZ-003`：对 uploaded 文档直接 Chunk，或对 archived 文档 Import/Chunk，确认实际 409 错误。
- `DOC-BIZ-004`：读取或操作不存在 `document_id`，确认 `404 document_not_found`。
- `DOC-BIZ-005`：Archive 维护场景。确认 `202 archived`、默认列表/RAG 排除，以及 `include_archived=true` 的显式包含。

### 5.5 Design Decision：Learning Mode 与 Enterprise Mode

#### 为什么当前采用 Learning Mode

当前 ERIP 是学习环境，因此故意保留完整知识库生命周期：

```text
Upload
↓
Import
↓
Chunk
↓
RAG
↓
Analysis
↓
Approval
```

这样设计的目的，是让学习者可以完整观察并理解以下内容：

- 学习 Upload API
- 学习 Import API
- 学习 Chunk API
- 学习 RAG API
- 学习完整 Backend 数据流
- 学习 Repository Pattern
- 学习 LangGraph Workflow

因此，Import 和 Chunk 被设计成可观察、可操作的独立步骤。
这属于 Learning Mode 当前设计，不是企业唯一实现方式。
换句话说，当前并不是因为企业一定要这样做，而是为了让学习者能看见 API、RAG、FastAPI、LangGraph 的完整生命周期。

#### Enterprise Mode（推荐实现）

未来企业模式推荐采用自动流程：

```text
Upload
↓
Auto Import
↓
Auto Chunk
↓
RAG
↓
Analysis
↓
Approval
```

在 Enterprise Mode 推荐实现中，最终用户通常不会直接看到以下技术步骤：

- Import
- Chunk
- Chunk List
- Chunk API

这些步骤属于系统内部处理，页面不需要暴露给业务用户。

#### 为什么企业通常隐藏 Chunk

Chunk 属于 AI 系统内部的知识切分步骤。
企业用户通常只关心“上传了什么文档、能不能检索到、分析结果是什么”，而不会关心每个文档被切成了多少段。

例如以下企业 AI 产品，后台都会执行类似流程：

```text
Document
↓
Chunk
↓
Embedding
↓
Vector
↓
Retrieval
```

但前端页面通常不会直接暴露 Chunk。
这是因为 Chunk 是内部实现细节，属于系统能力，不属于用户业务语言。

#### 为什么学习项目保留 Chunk

Learning Mode 保留 Chunk，是为了帮助学习者理解：

- Document Processing
- Chunk Generation
- Retrieval
- Citation
- RAG 生命周期

同时也方便阅读源码中的以下模块：

- `DocumentChunk`
- `ChunkRepository`
- `Chunk API`

如果不保留 Chunk，学习者会很难看清“文档进入系统以后，如何变成可检索知识”的完整路径。

#### 为什么 Import 单独存在

Import 不一定由管理员执行。企业里通常有三种方式：

1. 上传人自己确认 Import
2. 部门负责人确认 Import
3. 系统自动 Import

当前学习项目采用的是手动 Import。
这样做的目的是让学习者能清楚观察：

```text
Upload → Import → Chunk
```

三个 API 如何逐步推进，同一份文档如何从“上传完成”进入“可检索状态”。

#### 两种模式对比

| 维度         | Learning Mode（当前）                               | Enterprise Mode（推荐实现）      |
| ------------ | --------------------------------------------------- | -------------------------------- |
| 上传后处理   | Upload 后手动 Import、手动 Chunk                    | Upload 后自动 Import、自动 Chunk |
| Chunk 可见性 | 页面可查看 Chunk、Chunk API、Chunk List             | 页面隐藏 Chunk，作为内部处理     |
| 学习目标     | 学习 API、Repository、RAG、LangGraph 的完整生命周期 | 面向真实业务用户的自动化体验     |
| 用户认知     | 需要理解文档如何变成知识                            | 只需要理解文档已可检索、可分析   |
| 适用场景     | 学习、源码阅读、调试、面试讲解                      | 企业正式使用、规模化运维         |

#### 读者需要明确的边界

当前 Learning Mode 的设计决策是：

- 保留 Import
- 保留 Chunk
- 保留 Chunk 的可视化与可操作性
- 保留完整后台数据流的可观察性

这不是说企业一定要这样实现。
而是为了让学习者在 ERIP 中把 API、RAG、FastAPI、LangGraph 的生命周期一次看完整。

## 6. RagPage：页面操作 → React → API → Backend → 结果

文件：`frontend/src/pages/RagPage.tsx`

### 6.1 RAG 输入规则

第一次实际操作时，优先看 RAG 页面底部的「业务测试与源码学习」。该区域提供当前推荐上传文档、可直接复制的検索語与質問、不推荐问题、预期结果和 `insufficient_context` 排查顺序。

需要理解完整规则、六份文档的对应关系和源码调用链时，再查看本章。Scenario01 的 `07_RAG質問集.md` 是更多可选问题的扩展问题库，不是第一次测试时唯一入口。

当前 ERIP RAG 不是联网搜索，不是通用 ChatGPT，不会根据外部常识补充企业数据，也不会自行推理企业业务。它只从已经完成 Upload、Import、Chunk 的内部文档中检索；当前使用 Keyword Retrieval，Internal RAG 是 Deterministic Answer，真实 LLM、Embedding、pgvector 和 Vector Search 均未接入。

核心规则是：上传什么文档，就围绕该文档正文中真实存在的主题、关键词和事实提问。如果问题涉及的事实不存在于任何已完成 Chunk 的文档中，Backend 返回 `insufficient_context` 属于正常结果，不是系统故障。

| 已上传并完成 Chunk 的文档 | 文档主题 | 推荐検索語 | 推荐質問 | 不适合单独询问的主题 |
| --- | --- | --- | --- | --- |
| `01_関東地域飲料売上分析.md` | 关东地区销售、地区别销售、商品分类、同比和环比变化 | `関東地区 飲料売上 前年比`、`炭酸飲料 無糖飲料 欠品` | `関東地区の飲料売上が前年同月比で低下した主な要因は何ですか。`<br />`炭酸飲料と無糖飲料の売上変化を教えてください。` | 详细库存配送原因、顾客投诉、竞争店价格、促销 ROI。 |
| `02_関東地域在庫レポート.md` | 库存、缺货率、库存日数、补充达成率、配送延迟 | `神奈川 配送遅延 夕方欠品`、`炭酸飲料 欠品率 補充達成率` | `神奈川で夕方欠品が増加した理由は何ですか。`<br />`関東地域の飲料在庫における主な問題を要約してください。` | 顾客满意度、竞争店促销、促销 ROI。 |
| `03_販促キャンペーン結果.md` | 初夏水分补给活动、店头 POP、应用优惠券、SNS 广告、参加率 | `初夏の水分補給フェア クーポン 利用率`、`SNS広告 CTR 店頭POP` | `初夏の水分補給フェア 2026 の実績は目標と比べてどうでしたか。`<br />`アプリクーポンの利用率が低かった理由は何ですか。` | 门店配送延迟详情、顾客满意度、竞争店单品价格。 |
| `04_顧客アンケート集計.md` | 购买和未购买理由、满意度、自由意见、顾客年龄层 | `未購入理由 棚 競合店`、`満足度 品揃え クーポン` | `買わなかった理由の上位は何ですか。`<br />`顧客満足度はどの項目が低いですか。` | 具体配送计划、竞争店的单品价格、促销活动 CTR。 |
| `05_競合店舗調査.md` | 竞争店价格、促销、会员活动、广告、新品和市场变化 | `競合C店 箱買い 価格`、`会員活動 新商品 無糖炭酸` | `競合店はどの販促で集客していますか。`<br />`競合C店の価格と販促の特徴は何ですか。` | 自社顾客满意度、库存周转率、优惠券实际利用率。 |
| `06_KPI月次報告.md` | 销售额、客数、客单价、库存周转率、缺货率、促销参加率和投诉率 | `欠品率 在庫回転率 客単価`、`売上額 販促参加率 苦情率` | `6月のKPIで目標未達となった指標は何ですか。`<br />`客数の落ち幅より売上低下が大きい理由は何ですか。` | 单店配送细节、竞争店新品细节、顾客自由意见全文。 |

例如只上传 `02_関東地域在庫レポート.md`，却提问“競合店舗はなぜ値下げしましたか。”，当前 Chunk 没有竞争店价格或促销证据，Backend 应返回 `insufficient_context`。这是正常业务结果。

单文档问题只要求回答一份文档覆盖的内容。例如只上传库存报告，可以询问库存、缺货和配送问题。综合经营问题则需要完成相关资料的 Chunk：

```text
関東地域の飲料カテゴリの売上減少原因を、
売上、在庫、販促、顧客、競合、KPIの観点から整理してください。
```

执行该问题前，应将 `01` 销售分析、`02` 库存报告、`03` 促销结果、`04` 顾客调查、`05` 竞争店调查、`06` KPI 月报全部或至少相关资料完成 Chunk。一份库存报告不能独立证明全部销售下降原因；当前 RAG 只能根据已存在证据回答，不应补造缺失资料。

### 6.2 页面操作

先在 DocumentsPage 准备可检索 Chunk。推荐操作顺序是：

1. 确认相关文档已完成 `Upload → Import → Chunk`。
2. 先执行 Document Retrieval，使用与正文直接相关的短关键词。
3. 确认 `results > 0`、`document_id` 正确、存在 `chunk_id`、Chunk 内容相关且有 `score`。
4. Retrieval 成功后，再执行 Internal RAG Answer。
5. 确认 `answer`、`citations`、`confidence`、`warnings`、`retrieval_mode`、`answer_mode`。
6. 如果 `results = 0`，不建议直接执行 Internal RAG Answer；当前没有相关 Chunk，回答大概率返回 `insufficient_context`。

库存报告的首次测试可输入：

```text
検索語：神奈川 配送遅延 夕方欠品
取得件数：5
質問：神奈川で夕方欠品が増加した理由は何ですか。
回答方式：extractive
引用を必須にする：true
```

### 6.3 Document Retrieval

页面看到什么
→ 文書 ID、Chunk ID、score、source、metadata 和 retrieval mode。

点击后发生什么
→ `submitRetrieval()` 读取表单，调用 `searchDocumentRetrieval()`，然后 `setRetrievalResult(response)`。

调用哪个 API

```text
POST /api/v1/document-retrieval/search
JSON：query、limit、include_archived、document_type、language、tags
成功：200，results、total、query、retrieval_mode
```

Backend 经过什么

```text
backend/app/api/document_retrieval.py search_documents()
→ backend/app/services/document_retrieval_service.py DocumentRetrievalService.search()
→ DocumentRetrievalProvider.search()
→ backend/app/repositories/implementations/in_memory/document_retrieval.py InMemoryKeywordRetrieval.search()
```

返回后页面怎么变化
→ 有结果时显示真实 Chunk 摘要；无结果时 `results` 是空数组，页面显示「検索結果はありません。」。

### 6.4 Internal RAG Answer

页面看到什么
→ answer、confidence、warnings、citation。

点击后发生什么
→ `submitInternalRag()` 调用 `answerInternalRag()`，再 `setRagResult(response)`。

调用哪个 API

```text
POST /api/v1/internal-rag/answer
JSON：question、limit、filters、answer_mode、require_citations
成功：200，answer、citations、retrieval_mode、answer_mode、confidence、warnings
```

Backend 经过什么

```text
backend/app/api/internal_rag.py answer_internal_rag()
→ backend/app/services/internal_rag_service.py InternalRagService.answer()
→ DocumentRetrievalProvider.search()
→ RAGAnswerGenerator.generate()
→ InternalRagEvaluationService
```

返回后页面怎么变化
→ 页面只渲染 Backend 返回的 answer/citations，不自行拼装答案。资料不足时显示实际 `insufficient_context` 等错误。

### 6.5 清除按钮为什么没有 Network 请求

```text
「結果をクリア」 → setRetrievalResult(null) → 不请求 Backend
「回答をクリア」 → setRagResult(null) → 不请求 Backend
```

这是页面状态操作，不是业务数据删除。

### 6.6 建议企业测试 Case

- `RAG-BIZ-001`：库存报告的正常 Retrieval → Internal RAG 流程，确认 `results`、`score`、`document_id`、`answer` 与 citation。
- `RAG-BIZ-002`：在无 filter 的首次成功检索后，逐个测试真实支持的 `document_type`、`language` 或 `tags` filter。
- `RAG-BIZ-003`：输入与任何 Chunk 不匹配的关键词，确认 Retrieval 空结果而非伪造答案。
- `RAG-BIZ-004`：以库存资料询问竞争店主题，确认 `insufficient_context` 是正常证据不足结果。
- `RAG-BIZ-005`：清除 Retrieval 和 Answer，确认只改 React state，不发送 API。

## 7. TasksPage：页面操作 → React → API → Backend → 结果

文件：`frontend/src/pages/TasksPage.tsx`

### 7.1 页面操作

输入：

```text
確認したい経営課題：関東地域の飲料カテゴリの売上減少を分析してください
分析モード：hybrid
```

点击「分析を開始」，观察执行状态与分析报告。

### 7.2 创建任务和 SSE

页面看到什么
→ `task_id`、queued/running/completed 状态、SSE 事件与最终报告。

点击后发生什么
→ `submit()` 调用 `createTask()`；成功后 `subscribeToTask(task_id)`；收到 done 事件时调用 `loadReport()`。

调用哪个 API

```text
POST /api/tasks                     → 202，task_id、status
GET /api/tasks/{task_id}/events     → text/event-stream
GET /api/tasks/{task_id}/report     → 200，task_id、markdown、provider、created_at
```

Backend 经过什么

```text
tasks.py create_task()
→ TaskService.create_task()
→ InMemoryTaskRepository.create()
→ BackgroundTasks.add_task(TaskService.run_task)
→ AnalysisWorkflow.stream()
→ route → kpi / research → report
→ InMemoryReportRepository.save()
→ SSE EventRepository
```

`POST /api/tasks` 的 202 表示任务已受理，不表示报告已完成。报告尚未生成时，`TaskService.get_report()` 使用实际 409 表示状态冲突。

### 7.3 建议企业测试 Case

- `TASK-BIZ-001`：hybrid 分析关东饮料销售下降，确认 SSE 与 report。
- `TASK-BIZ-002`：清空问题，确认按钮不可点击。
- `TASK-BIZ-003`：读取不存在 task 的报告，确认实际 404。
- `TASK-BIZ-004`：任务未完成时读取报告，确认实际 409。
- `TASK-BIZ-005`：再次提交，确认旧报告和旧 SSE 状态被清理。

## 8. ApprovalPage：页面操作 → React → API → Backend → 结果

文件：`frontend/src/pages/ApprovalPage.tsx`

### 8.1 页面操作

完成分析后，手动复制 `task_id` 到「承認依頼を送信」。成功后选择审批记录，执行「承認」「却下」或「修正依頼」。

### 8.2 列表、详情和提交

页面看到什么
→ `approval_id`、`task_id`、`report_version_id`、status、决策信息。

点击后发生什么
→ `loadApprovals()`、`loadApprovalDetail()` 或 `handleSubmitApproval()` 调用 API Client；成功后 `refreshAfterChange()` 同时刷新列表和详情。

调用哪个 API

```text
GET  /api/v1/approvals
GET  /api/v1/approvals/{approval_id}
POST /api/v1/reports/{task_id}/submit-approval     → 201
```

Backend 经过什么

```text
backend/app/api/approvals.py list_approvals() / get_approval() / submit_approval()
→ _run_audited_operation()
→ AuditMiddleware.run()
→ ApprovalService.list_approvals() / get_approval() / submit_approval()
→ InMemoryApprovalRepository
```

### 8.3 审批决策和修正

| 操作     | API                                              | 实际 Service                  |
| -------- | ------------------------------------------------ | ----------------------------- |
| 承認     | `POST /api/v1/approvals/{approval_id}/approve` | `ApprovalService.approve()` |
| 却下     | `POST /api/v1/approvals/{approval_id}/reject`  | `ApprovalService.reject()`  |
| 修正依頼 | `POST /api/v1/reports/{task_id}/revise`        | `ApprovalService.revise()`  |

这三条 Router 都先经过 `_run_audited_operation()` 与 `AuditMiddleware.run()`，再写入 `InMemoryApprovalRepository` 的审批请求、报告版本或审批事件。当前 API 需要权限；权限不足会返回实际 403 `permission_denied`。对已决策的审批重复操作会返回实际 409。

### 8.4 建议企业测试 Case

- `APR-BIZ-001`：为完成任务提交审批，确认 201、`approval_id` 和 `report_version_id`。
- `APR-BIZ-002`：清空 Task ID，确认不能提交。
- `APR-BIZ-003`：使用不存在或未完成 task，确认真实 Backend 业务错误。
- `APR-BIZ-004`：审批、重复审批、权限不足，确认成功、409、403 三类结果。
- `APR-BIZ-005`：对 rejected 记录修正，确认新 report version；刷新不改变状态。

## 9. 页面之间的数据关系

| 对象            | 产生页面        | 使用页面                                    | 自动传递？                                |
| --------------- | --------------- | ------------------------------------------- | ----------------------------------------- |
| `document_id` | 文書管理        | 文書管理详情、Import、Chunk；RAG 结果会返回 | 否                                        |
| `import_id`   | 文書管理 Import | 当前页面仅显示 import 状态                  | 否，前端未调用 import detail API          |
| Chunk           | 文書管理 Chunk  | RAG検索的 Backend retrieval                 | Backend 存储层已连接；页面条件手动输入    |
| `citation`    | RAG検索         | 当前只在 RAG 页面显示                       | 否                                        |
| `task_id`     | 分析依頼        | 承認管理提交审批                            | 否，手动复制                              |
| `report`      | 分析依頼        | 承認管理通过`task_id` 读取报告版本        | Backend 通过 task_id 连接；页面未自动传递 |
| `approval_id` | 承認管理        | 承認管理详情与决策                          | 是，页面内部选中状态                      |

## 10. 推荐实际操作顺序

1. 打开「文書管理」，上传 markdown/text 文档并确认 `document_id`。
2. 按真实文档状态执行 Import、Chunk；若 Backend 拒绝，先读错误 code。
3. 打开「RAG検索」，用与文档内容有关的日语检索词确认 `results` 和 citation。
4. 打开「分析依頼」，以关东饮料销售下降为问题，选择 hybrid，等待 SSE done 和 report。
5. 复制已完成的 `task_id` 到「承認管理」，提交审批并验证状态机。
6. 展开各页面的「业务测试与源码学习」，对照 API Path、函数名和 Backend 文件。

## 11. 如何对照源码学习

每次只沿一条请求走读：

```text
页面按钮
→ frontend/src/pages/<Page>.tsx 的 handler
→ frontend/src/api.ts 的 API Client 函数
→ backend/app/api 的 Router 函数
→ backend/app/services 的 Service 方法
→ backend/app/repositories 或 backend/app/workflow
→ schemas response
→ React state 与页面显示
```

建议打开浏览器 DevTools：

- **Network**：确认 Method、Path、status、request body 与 response envelope。
- **Console**：确认没有前端异常。
- **Elements**：查看业务测试说明不改变日语操作 UI。

清除按钮或顶部导航没有 Network 请求时，不是故障：它们只修改 React state。

## 12. 常见错误定位

### 固定右侧学习面板

桌面宽屏下，`App.tsx` 将当前业务页和 `LearningSidebar` 放入 `app-learning-layout`。侧栏以 `position: sticky` 保持可见，窄屏（1100px 以下）降级为主内容下方。

页面只通过 `onLearningEvent` 上报最近一次已有 handler 的操作，例如 `submitUpload()`、`submitRetrieval()`、`submit()`、`handleApprove()`。LearningSidebar 显示当前页面用途、组件树、Props、输入、最近事件与关键 State、主要 API、Backend 调用链、结果解释、业务关系、源码和测试 Case；它不拦截全局 fetch、不保存历史，也不改变业务状态。

业务页面与学习面板统一使用以下顺序：

```text
文書管理 → RAG検索 → 分析依頼 → 承認管理
```

其中顶部导航只经过 `App.tsx → changeView() → setActiveView() → activeView`，不发送 Backend API。分析依頼的初始 `IDLE` 表示尚未提交；`POST /api/tasks` 的 `202 Accepted` 表示 BackgroundTasks 已受理，SSE 收到 `done` 后才由 `loadReport()` 请求最终 report。

RAG 的 `insufficient_context` 在面板中解释为：Backend 未找到足够相关 Chunk，可能是输入不匹配或文档尚未 Chunk；这不是页面故障。

| 现象         | 先看哪里                                     | 常见含义                                       |
| ------------ | -------------------------------------------- | ---------------------------------------------- |
| 文档列表为空 | DocumentsPage 的`loadDocuments()`、Network | 当前 InMemory 中没有匹配文档，或归档过滤未勾选 |
| Chunk 失败   | `DocumentChunkService` 错误 code           | 文档不存在、已归档、未 validated 或类型不支持  |
| RAG 无结果   | `DocumentRetrievalService.search()`        | 没有匹配的 Chunk；不是前端生成错误             |
| RAG 422      | `InternalRagService.answer()`              | 问题为空、资料不足或 citation 要求无法满足     |
| 任务没有报告 | TasksPage SSE、`TaskService.get_report()`  | 任务仍在运行或失败；未完成报告是 409           |
| 审批 403     | `AuditMiddleware.run()`                    | 当前用户没有 approval API 所需权限             |
| 审批 409     | `ApprovalService`                          | 已提交、已决策或状态机不允许当前动作           |

当前学习边界：不接真实 LLM、Embedding、PostgreSQL、pgvector 或自动跨页面编排。页面展示的链路以现有源码为准，不代表未来目标架构已经实现。

## V1.0 前端交付要点（增量）

正式导航（与 `App.tsx` 一致）：

```text
学习总览 → 文書管理 → RAG検索 → 分析依頼 → 承認管理
```

| 主题 | 现状 | 源码方向 |
|---|---|---|
| JWT | Access Token 仅 sessionStorage；恢复经 `/users/me` | AuthContext / API Client |
| ProtectedRoute | 未登录跳转登录并保留目标 | routes / ProtectedRoute |
| RBAC UI | 冻结权限镜像；未知角色 fail-closed | permission helpers |
| 401 / 403 | 401 清会话；403 保持会话显示无权 | fetch client |
| Lifecycle Live Status | mount/update/unmount 本地 ring buffer | LifecycleProbe / LearningTrace |
| Learning Dashboard | 固定栏目教学侧栏，不替代业务页 | LearningSidebar |
| AI 成本展示 | Provider/Model/route/Token/Cost（无 Key） | RAG/Analysis 页 |

验收：Frontend **113/113**；权威启动见 RUNBOOK Appendix L；企业 Compose 见 Appendix M。
