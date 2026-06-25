# 函数调用流程说明

这份说明把 `projects/` 下的 Python demo 按“入口函数 -> 核心调用链 -> 关键名词”整理起来，方便快速建立整体理解。

## 概念对照

| 概念 | 一句话理解 | 在代码里的例子 |
| --- | --- | --- |
| 链路 | 一串按顺序连接的处理步骤，前一步输出给下一步输入 | `prompt | llm | parser` |
| 工作流 | 比链路更完整的流程，通常包含分支、回路、条件判断 | `LangGraph` 里的 `review -> revise -> review` |
| 图 | 用节点和边描述整个流程的结构 | `StateGraph` |
| 节点 | 流程里的一个处理步骤 | `classify_intent()`、`research()` |
| 边 | 节点之间的连接关系 | `START -> classify_intent -> research` |
| 状态 | 流程中持续传递的共享数据 | `WorkflowState` |
| 解析 | 把模型输出整理成更规整的数据结构 | `parse_response()` |
| 原始输出 | 模型直接吐出来的文本 | `raw_message.content` |
| 结构化结果 | 解析后更适合程序继续处理的结果 | `dict` / `JSON` |

## LangChain vs LangGraph

| 维度 | LangChain | LangGraph |
| --- | --- | --- |
| 核心形态 | 链路 / 管道 | 图 / 工作流 |
| 重点 | 把 prompt、模型、解析器串起来 | 把多个处理步骤组织成可分支、可循环的流程 |
| 适合场景 | 单次问答、简单转换、固定顺序处理 | 多步骤任务、审校回路、条件分支 |
| 流程表达 | `prompt | llm | parser` | `state + node + edge + conditional edge` |
| 运行方式 | 一路往下执行 | 可能回到前一步，也可能走不同分支 |
| 你可以把它理解成 | 一条流水线 | 一张流程图 |

## 1. LangChain 风格链路

文件：`langchain_chain_demo/main.py`

调用流程：

`main()（程序入口）` -> `parse_args()（解析参数）` -> `print(模式)（打印运行模式）` -> `build_chain(use_mock)（组装解析链路）` / `build_generation_chain(use_mock)（只保留原始输出链路）` -> `build_prompt()（构造提示词）` -> `build_real_llm()（真实模型）` / `mock_llm()（本地模拟模型）` -> `parse_response()（解析输出）` -> `print(mermaid)（打印链路图）` -> `chain.invoke(...)（执行并打印解析后结果）` / `generation_chain.invoke(...)（执行并打印原始结果）`

关键名词：

- `Prompt Template / 提示词模板`：把问题包装成统一输入格式。
- `Runnable / 可组合执行单元`：LangChain 里的可组合执行单元。
- `AIMessage / 模型消息`：模型输出消息对象。
- `JSON / JSON 结构`：示例里要求输出的结构化结果。
- `raw_message.content / 原始文本`：模型直接返回的原始文本。
- `parse_response() / 输出解析`：把原始文本重新组装成结构化字典。
理解要点：

- “链路”就是一串按顺序衔接的处理步骤，前一步的输出会变成下一步的输入。
- `build_prompt()` 负责定义输入格式。
- `build_chain()` 负责把 prompt、模型和解析器串起来。
- `build_generation_chain()` 负责只拿原始模型输出，方便对比解析前后差异。
- `mock_llm()` 负责在不联网时模拟模型输出。
- `parse_response()` 负责把模型消息整理成字典。
- `main()` 负责选择模式，默认先尝试真实模型，失败后回退到 mock。

链路小图：

```text
用户问题 / User question
   |
   v
build_prompt() / Prompt 模板
   |
   v
mock_llm() / real llm / 模型调用
   |
   v
parse_response() / 输出解析
   |
   v
最终结果 / Final result
```

工作流小图：

```text
用户问题 / User question
   |
   v
build_prompt() / 提示词模板
   |
   v
mock_llm() / real llm / 模型调用
   |
   v
parse_response() / 输出解析
   |
   v
最终结果 / Final result
```

## 2. LangGraph 工作流

文件：`langgraph_workflow_demo/main.py`

调用流程：

`main()（程序入口）` -> `parse_args()（解析参数）` -> `build_app()（构建图）` -> `classify_intent()（判断意图）` -> `research()（收集要点）` -> `draft()（生成草稿）` -> `review()（审核草稿）` -> `route_after_review()（选择分支）` -> `revise()（修订草稿）` / `finalize()（生成最终结果）` -> `app.invoke(...)（运行图）` -> `print(mermaid)（打印图）` -> `print(final_answer)（打印最终结果）`

关键名词：

- `State / 状态`：贯穿整个图的共享状态。
- `Node / 节点`：图里的一个处理步骤。
- `Edge / 边`：节点之间的固定连线。
- `Conditional Edge / 条件边`：根据状态决定下一步走向。
- `Loop / 循环`：`revise()` 和 `review()` 之间的循环。

理解要点：

- `classify_intent()` 先判断问题类型。
- `research()` 根据意图准备要点。
- `draft()` 把要点整理成草稿。
- `review()` 检查草稿是否够完整。
- `route_after_review()` 决定继续修订还是结束。
- `revise()` 形成一次回路修订。
- `finalize()` 汇总最终输出。

工作流小图：

```text
用户问题 / User question
   |
   v
classify_intent() / 判断意图
   |
   v
research() / 收集要点
   |
   v
draft() / 生成草稿
   |
   v
review() / 审核草稿
   |
   v
route_after_review() / 分支判断
  ├─ 不通过 -> revise() / 修订草稿 -> 返回 review()
  └─ 通过    -> finalize() / 生成最终结果
```

## 3. 高级 RAG 管线

文件：`advanced_rag_pipeline_demo/main.py`

调用流程：

`main()（程序入口）` -> `parse_args()（解析参数）` -> `load_documents()（加载文档）` -> `chunk_documents()（切分文档）` -> `retrieve()（初步检索）` -> `rerank()（二次重排）` -> `synthesize_answer()（合成答案）` -> `print(文档统计)（打印原始文档统计）` -> `print(chunk 数量)（打印分块数量）` -> `print(retrieval)（打印检索 + 重排结果）` -> `print(answer)（打印最终回答）`

关键名词：

- `Document / 文档对象`：LangChain 文档对象。
- `Chunk / 文本块`：切分后的文本片段。
- `rewrite query / 查询改写`：把问题改写成更适合检索的版本。
- `retrieve / 初步检索`：初步召回相关 chunk。
- `rerank / 二次重排`：对召回结果二次排序。
- `synthesize answer / 合成答案`：把结果组织成最终回答。

理解要点：

- `load_documents()` 读入原文。
- `chunk_documents()` 负责切块。
- `expand_terms()` 和 `rewrite_queries()` 负责扩展检索词。
- `score_chunk()` 负责打分。
- `retrieve()` 负责召回。
- `rerank()` 负责补分和重排。
- `synthesize_answer()` 负责输出带引用的答案。

工作流小图：

```text
用户问题 / User question
   |
   v
load_documents() / 加载文档
   |
   v
chunk_documents() / 切分文档
   |
   v
retrieve() / 初步检索
   |
   v
rerank() / 二次重排
   |
   v
synthesize_answer() / 合成答案
   |
   v
print() / 打印结果
```

## 4. 社内文件 + Wiki 混合检索

文件：`internal_hybrid_rag_demo/main.py`

调用流程：

`main()（程序入口）` -> `parse_args()（解析参数）` -> `load_documents()（加载文档）` -> `filter_by_role()（按角色过滤）` -> `retrieve()（初步检索）` -> `rerank()（二次重排）` -> `synthesize_answer()（合成答案）` -> `print_section()（打印分段标题）` -> `print(接入层统计)（打印载入/可访问/过滤统计）` -> `print(权限层)（打印权限过滤明细）` -> `print(检索层)（打印检索与重排结果）` -> `print(引用层)（打印最终答案）`

关键名词：

- `catalog / 文档清单`：文档清单。
- `ACL / 访问控制列表`：访问控制列表。
- `role / 角色`：当前用户角色。
- `server_docs` / `wiki_docs`：两类来源文档。
- `权限过滤 / Access filter`：先把不可见内容剔除，再做检索。

理解要点：

- `load_catalog()` 读目录配置。
- `load_documents()` 把文件内容变成 `KnowledgeDoc`。
- `can_access()` 判断权限。
- `filter_by_role()` 先做权限过滤。
- `expand_query_terms()` 根据问题类型扩词。
- `score_document()` 计算相关度。
- `retrieve()` 做初步召回。
- `rerank()` 再根据来源和命中数微调。
- `synthesize_answer()` 把答案、引用和权限概况一起输出。

工作流小图：

```text
用户问题 / User question
   |
   v
load_documents() / 加载文档目录
   |
   v
filter_by_role() / 按角色过滤权限
   |
   v
retrieve() / 初步检索
   |
   v
rerank() / 二次重排
   |
   v
synthesize_answer() / 合成带引用答案
   |
   v
print_section() / print()（打印结果）
```

## 5. LlamaIndex 概念版索引

文件：`llamaindex_index_demo/main.py`

调用流程：

`main()（程序入口）` -> `parse_args()（解析参数）` -> `load_documents()（加载文档）` -> `split_into_nodes()（切分节点）` -> `build_inverted_index()（构建倒排索引）` -> `retrieve()（召回节点）` -> `synthesize_answer()（合成答案）` -> `print(文档统计)（打印文档大小）` -> `print(node 数量)（打印节点数量）` -> `print(召回结果)（打印检索结果）` -> `print(最终答案)（打印最终回答）`

关键名词：

- `Document / 原始文档`：原始文档。
- `Node / 节点`：切分后的节点。
- `Inverted Index / 倒排索引`：倒排索引。
- `QueryEngine / 查询引擎`：查询引擎思路。
- `QueryResult / 查询结果`：检索结果对象。

理解要点：

- `split_into_nodes()` 把长文拆成小节点。
- `build_inverted_index()` 建索引。
- `expand_query()` 让问题更容易命中相关词。
- `retrieve()` 先用索引召回，再做轻微加分。
- `synthesize_answer()` 用结果拼出带引用的回答。

工作流小图：

```text
用户问题 / User question
   |
   v
load_documents() / 加载文档
   |
   v
split_into_nodes() / 切分节点
   |
   v
build_inverted_index() / 构建倒排索引
   |
   v
retrieve() / 召回节点
   |
   v
synthesize_answer() / 合成答案
   |
   v
print() / 打印结果
```

## 6. 多 Agent 协作

文件：`multi_agent_team_demo/main.py`

调用流程：

`main()（程序入口）` -> `parse_args()（解析主题）` -> `supervisor()（总调度）` -> `planner_agent()（规划任务）` -> `researcher_agent()（调研资料）` -> `writer_agent()（生成草稿）` -> `critic_agent()（审校问题）` -> `writer_agent()（修订草稿）` -> `critic_agent()（再次审校）` -> `print(final_answer)（打印最终答案）`

关键名词：

- `Supervisor / 总调度者`：总调度者。
- `Planner / 任务拆分者`：任务拆分者。
- `Researcher / 资料收集者`：资料收集者。
- `Writer / 内容组织者`：内容组织者。
- `Critic / 审核者`：审核者。
- `TeamState / 共享状态`：共享状态容器。

理解要点：

- `planner_agent()` 把主题拆成任务。
- `expand_keywords()` 找知识库关键词。
- `researcher_agent()` 生成调研要点。
- `writer_agent()` 生成草稿。
- `critic_agent()` 找缺项。
- `supervisor()` 串起整个协作闭环。

工作流小图：

```text
主题 / Topic
   |
   v
supervisor() / 总调度
   |
   v
planner_agent() / 规划任务
   |
   v
researcher_agent() / 调研资料
   |
   v
writer_agent() / 生成草稿
   |
   v
critic_agent() / 审校问题
   |
   v
writer_agent() / 修订草稿
   |
   v
print(final_answer) / 最终答案
```

## 7. 容器化服务

文件：`deployment/container_demo/app.py`

调用流程：

`main()（程序入口）` -> `HTTPServer(...)（启动 HTTP 服务）` -> `print(Serving on ...)（打印启动地址）` -> `Handler.do_GET()（处理 GET 请求）` -> 返回 JSON

关键名词：

- `HTTPServer / HTTP 服务`：标准库 HTTP 服务。
- `Handler / 请求处理器`：请求处理器。
- `Health Check / 健康检查`：健康检查接口。
- `Environment Variable / 环境变量`：环境变量配置。

理解要点：

- `do_GET()` 负责构造响应体。
- `log_message()` 被重写为静默输出。
- `main()` 负责启动服务。

工作流小图：

```text
HTTPServer(...) / 启动服务
   |
   v
等待请求 / Wait for request
   |
   v
Handler.do_GET() / 处理 GET
   |
   v
返回 JSON / Return JSON
```

## 8. RAG 评估脚本

文件：`eval/rag_eval_demo/eval_rag.py`

调用流程：

`main()（程序入口）` -> `load_samples()（加载样本）` -> `coverage()（计算覆盖率）` / `precision()（计算精确率）` -> `print(report)（打印逐条报表）` -> `print(summary)（打印汇总结果）`

关键名词：

- `Sample / 样本`：评估样本。
- `gold_sources / 标准来源`：标准来源。
- `retrieved_sources / 检索来源`：检索结果来源。
- `coverage / 覆盖率`：覆盖率。
- `precision / 精确率`：精确率。

理解要点：

- `load_samples()` 读取样本数据。
- `coverage()` 看标准来源覆盖了多少。
- `precision()` 看召回结果有多少是对的。
- `main()` 逐条输出报表并计算平均值。

工作流小图：

```text
样本数据 / Samples
   |
   v
load_samples() / 加载样本
   |
   v
coverage() / 计算覆盖率
   |
   v
precision() / 计算精确率
   |
   v
print(report) / 打印报表
   |
   v
print(summary) / 打印汇总
```

## 9. 快速记忆版

- “加载数据”的函数通常在前面：`load_*`
- “预处理”的函数通常负责切分、扩展、过滤：`chunk_*`、`split_*`、`filter_*`、`expand_*`
- “打分”的函数通常是：`score_*`
- “召回”的函数通常是：`retrieve()`
- “重排”的函数通常是：`rerank()`
- “生成答案”的函数通常是：`synthesize_answer()`
- “主流程”的函数通常是：`main()`

## 10. 向量数据库骨架

### 10.0 最小教学版

文件：`vector_db_demo/main.py`

调用流程：

`main()（程序入口）` -> `load_documents()（加载样本文档）` -> `build_store()（选择后端风格）` -> `upsert() / add_documents()（写入 collection）` -> `search() / query()（相似度检索）` -> `print_hits()（打印结果）`

关键名词：

- `Document / 文档对象`：一篇待检索的示例文本。
- `collection / 集合`：向量和文档的存储容器。
- `metadata / 元数据`：来源、主题等附加信息。
- `vector / 向量`：文本转成的数值表示。
- `top-k / 前 K 条`：只返回最相关的几条结果。

理解要点：

- `load_documents()` 会把 `assets/` 里的 markdown 文件读进来。
- `embed_text()` 会把文本变成固定长度向量。
- `MemoryVectorDB` 负责保存文档和向量。
- `QdrantLikeStore` 和 `ChromaLikeStore` 只是接口风格不同，底层流程一样。
- `main()` 根据 `--backend` 选择不同的演示后端。

工作流小图：

```text
用户问题 / User question
   |
   v
load_documents() / 加载样本文档
   |
   v
build_store() / 选择后端风格
   |
   v
upsert() / add_documents() / 写入 collection
   |
   v
search() / query() / 相似度检索
   |
   v
print_hits() / 打印 top-k 结果
```

### 10.1 真实 Qdrant 版

文件：`vector_db_qdrant_demo/main.py`

调用流程：

`main()（程序入口）` -> `parse_args()（解析参数）` -> `load_documents()（加载文档）` -> `build_embedder()（构造向量化方案）` -> `run_mock() / run_real()（按模式执行）` -> `upsert()（写入 collection）` -> `search()（相似度检索）` -> `print_hits()（打印结果）`

关键名词：

- `Qdrant Client / 客户端`：真实 Qdrant 接入层
- `collection / 集合`：存储文档向量的容器
- `payload / 元数据`：随向量一起保存的文本与来源信息
- `upsert / 写入`：新增或更新文档
- `search / 检索`：按向量相似度召回结果

工作流小图：

```text
用户问题 / User question
   |
   v
build_embedder() / 构造 embedding
   |
   v
run_mock() / run_real() / 选择执行模式
   |
   v
upsert() / 写入 collection
   |
   v
search() / 相似度检索
   |
   v
print_hits() / 打印命中结果
```

### 10.2 真实 Chroma 版

文件：`vector_db_chroma_demo/main.py`

调用流程：

`main()（程序入口）` -> `parse_args()（解析参数）` -> `load_documents()（加载文档）` -> `build_embedder()（构造向量化方案）` -> `run_mock() / run_real()（按模式执行）` -> `collection.upsert()（写入 collection）` -> `collection.query()（查询）` -> `print_hits()（打印结果）`

关键名词：

- `PersistentClient / 持久化客户端`：本地持久化接入层
- `collection / 集合`：存储文档的集合
- `metadata / 元数据`：文档附带信息
- `query / 查询`：检索相似内容
- `persist_dir / 持久化目录`：本地落盘目录

工作流小图：

```text
用户问题 / User question
   |
   v
build_embedder() / 构造 embedding
   |
   v
run_mock() / run_real() / 选择执行模式
   |
   v
collection.upsert() / 写入 collection
   |
   v
collection.query() / 查询相似内容
   |
   v
print_hits() / 打印命中结果
```

理解要点：

- Qdrant 版更像远端服务接入模板。
- Chroma 版更像本地原型和持久化模板。
- 两个版本都先做 embedding，再入库，再检索。

## 11. 日本小売经营分析 Agent

文件：`japan_retail_analysis_agent/main.py`、`japan_retail_analysis_agent/server.py`、`japan_retail_analysis_agent/frontend/src/main.tsx`

CLI 调用流程：

`main.py` -> `retail_agent.cli.main()（解析问题、模式和输出路径）` -> `RetailAnalysisOrchestrator.run()（路由 data/research/hybrid）` -> `FixedBusinessWorkflow.run()（固定经营数据工作流）` / `ResearchAgent.run()（自主研究 Agent）` -> `RetailDataWarehouse.query_template()（白名单 SQL 查询）` / `ResearchAgent.plan() + tool（选择市场、竞品、社内资料工具）` -> `ReportComposer.run()（合成日文报告）` -> `print()` / `write_text()`（输出 Markdown）

后端调用流程：

`server.py` -> `create_app()` -> `interfaces/http/routers/tasks.py` -> `TaskService.create_task()` -> `TaskRepository.create()` -> `TaskService.run_task()` 后台执行 -> `RetailAnalysisOrchestrator.run()` -> `StateGraph(route/data/research/report)` -> `SqliteSaver` 保存 LangGraph checkpoint -> `EventBus.publish()` 推送 SSE/WebSocket -> `TaskRepository.save_state()` 保存最终报告 -> `GET /api/tasks/{task_id}` 查询结果

前端调用流程：

`frontend/src/main.tsx` -> `fetch('/api/tasks')` 创建任务 -> `EventSource('/api/tasks/{task_id}/events')` 订阅 SSE -> React state 更新固定工作流面板、研究 Agent 面板、执行时间线和 Markdown 报告

关键名词：

- `Orchestrator / 编排器`：根据问题决定走结构化数据、调查 Agent，还是两者组合。
- `FixedBusinessWorkflow / 固定工作流`：只允许白名单 SQL 模板，适合売上、粗利、在庫、欠品等 KPI。
- `ResearchAgent / 研究 Agent`：根据问题选择市场趋势、竞争情报、社内资料工具。
- `EvidenceBlock / 证据块`：统一承载表格、调查内容、来源、图表类型和选择理由。
- `AuditEvent / 审计事件`：记录路由、SQL、工具调用和报告生成步骤。
- `human_confirmation / 人工确认`：记录价格、仕入、补货规则等需要人工审批的事项。
- `SQLiteCheckpointStore / checkpoint`：持久化任务、事件和最终报告。
- `LangGraph SqliteSaver / 图 checkpoint`：按 task id 保存 StateGraph 执行检查点。
- `EventBus / 事件总线`：把同一套任务事件分发给 SSE 和 WebSocket。
- `SSE / WebSocket`：浏览器和其他客户端实时观察任务执行过程。

理解要点：

- 可验证经营数据不交给自主 Agent 任意生成 SQL，而是走固定模板和 SELECT-only guard。
- 月次売上、地域別売上、在庫风险适合固定图，因为它们是重复出现的经营 KPI。
- 市场趋势、竞争情报、社内资料调查适合 Agent，因为来源和步骤会随问题变化。
- 最终报告同时保留数据库来源、调查来源、风险提示、人工确认和审计日志，方便日本现场说明治理边界。

工作流小图：

```text
业务问题 / Business question
   |
   v
FastAPI / CLI / Frontend
   |
   v
RetailAnalysisOrchestrator.run() / 路由 data-research-hybrid
   |
   +--> FixedBusinessWorkflow.run() / 固定经营数据工作流
   |       |
   |       v
   |    RetailDataWarehouse.query_template() / 白名单 SQL
   |
   +--> ResearchAgent.run() / 自主研究 Agent
           |
           v
        plan() + tools / 市场・竞品・社内资料
   |
   v
ReportComposer.run() / 日文报告、风险、HITL、审计
   |
   v
SQLiteCheckpointStore + SSE + WebSocket
```
