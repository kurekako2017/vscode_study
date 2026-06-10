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

理解要点：

- Qdrant 版更像远端服务接入模板。
- Chroma 版更像本地原型和持久化模板。
- 两个版本都先做 embedding，再入库，再检索。
