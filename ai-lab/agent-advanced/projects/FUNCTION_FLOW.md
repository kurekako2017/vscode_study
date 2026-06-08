# 函数调用流程说明

这份说明把 `projects/` 下的 Python demo 按“入口函数 -> 核心调用链 -> 关键名词”整理起来，方便快速建立整体理解。

## 1. LangChain 风格链路

文件：`langchain_chain_demo/main.py`

调用流程：

`main()（程序入口）` -> `parse_args()（解析参数）` -> `build_chain(use_mock)（组装链路，优先 LangChain，缺包时走本地兼容实现）` -> `build_prompt()（构造提示词）` -> `build_real_llm()（真实模型）` / `mock_llm()（本地模拟模型）` -> `parse_response()（解析输出）` -> `chain.invoke(...)（执行链路）`

关键名词：

- `Prompt Template`：把问题包装成统一输入格式。
- `Runnable`：LangChain 里的可组合执行单元。
- `AIMessage`：模型输出消息对象。
- `JSON`：示例里要求输出的结构化结果。
- `Fallback`：没有安装 `langchain_core` 时，脚本内置的兼容实现。

理解要点：

- `build_prompt()` 负责定义输入格式。
- `build_chain()` 负责把 prompt、模型和解析器串起来，并在缺包时切到本地兼容实现。
- `mock_llm()` 负责在不联网时模拟模型输出。
- `parse_response()` 负责把模型消息整理成字典。
- `main()` 负责选择模式，并确保 mock 也能独立运行。

## 2. LangGraph 工作流

文件：`langgraph_workflow_demo/main.py`

调用流程：

`main()（程序入口）` -> `parse_args()（解析参数）` -> `build_app()（构建图）` -> `classify_intent()（判断意图）` -> `research()（收集要点）` -> `draft()（生成草稿）` -> `review()（审核草稿）` -> `route_after_review()（选择分支）` -> `revise()（修订草稿）` / `finalize()（生成最终结果）` -> `app.invoke(...)（运行图）`

关键名词：

- `State`：贯穿整个图的共享状态。
- `Node`：图里的一个处理步骤。
- `Edge`：节点之间的固定连线。
- `Conditional Edge`：根据状态决定下一步走向。
- `Loop`：`revise()` 和 `review()` 之间的循环。

理解要点：

- `classify_intent()` 先判断问题类型。
- `research()` 根据意图准备要点。
- `draft()` 把要点整理成草稿。
- `review()` 检查草稿是否够完整。
- `route_after_review()` 决定继续修订还是结束。
- `revise()` 形成一次回路修订。
- `finalize()` 汇总最终输出。

## 3. 高级 RAG 管线

文件：`advanced_rag_pipeline_demo/main.py`

调用流程：

`main()（程序入口）` -> `parse_args()（解析参数）` -> `load_documents()（加载文档）` -> `chunk_documents()（切分文档）` -> `retrieve()（初步检索）` -> `rerank()（二次重排）` -> `synthesize_answer()（合成答案）`

关键名词：

- `Document`：LangChain 文档对象。
- `Chunk`：切分后的文本片段。
- `rewrite query`：把问题改写成更适合检索的版本。
- `retrieve`：初步召回相关 chunk。
- `rerank`：对召回结果二次排序。
- `synthesize answer`：把结果组织成最终回答。

理解要点：

- `load_documents()` 读入原文。
- `chunk_documents()` 负责切块。
- `expand_terms()` 和 `rewrite_queries()` 负责扩展检索词。
- `score_chunk()` 负责打分。
- `retrieve()` 负责召回。
- `rerank()` 负责补分和重排。
- `synthesize_answer()` 负责输出带引用的答案。

## 4. 社内文件 + Wiki 混合检索

文件：`internal_hybrid_rag_demo/main.py`

调用流程：

`main()（程序入口）` -> `parse_args()（解析参数）` -> `load_documents()（加载文档）` -> `filter_by_role()（按角色过滤）` -> `retrieve()（初步检索）` -> `rerank()（二次重排）` -> `synthesize_answer()（合成答案）` -> `print_section()（打印分段标题）`

关键名词：

- `catalog`：文档清单。
- `ACL`：访问控制列表。
- `role`：当前用户角色。
- `server_docs` / `wiki_docs`：两类来源文档。
- `权限过滤`：先把不可见内容剔除，再做检索。

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

## 5. LlamaIndex 概念版索引

文件：`llamaindex_index_demo/main.py`

调用流程：

`main()（程序入口）` -> `parse_args()（解析参数）` -> `load_documents()（加载文档）` -> `split_into_nodes()（切分节点）` -> `build_inverted_index()（构建倒排索引）` -> `retrieve()（召回节点）` -> `synthesize_answer()（合成答案）`

关键名词：

- `Document`：原始文档。
- `Node`：切分后的节点。
- `Inverted Index`：倒排索引。
- `QueryEngine`：查询引擎思路。
- `QueryResult`：检索结果对象。

理解要点：

- `split_into_nodes()` 把长文拆成小节点。
- `build_inverted_index()` 建索引。
- `expand_query()` 让问题更容易命中相关词。
- `retrieve()` 先用索引召回，再做轻微加分。
- `synthesize_answer()` 用结果拼出带引用的回答。

## 6. 多 Agent 协作

文件：`multi_agent_team_demo/main.py`

调用流程：

`main()（程序入口）` -> `parse_args()（解析主题）` -> `supervisor()（总调度）` -> `planner_agent()（规划任务）` -> `researcher_agent()（调研资料）` -> `writer_agent()（生成草稿）` -> `critic_agent()（审校问题）` -> `writer_agent()（修订草稿）` -> `critic_agent()（再次审校）` -> 最终汇总

关键名词：

- `Supervisor`：总调度者。
- `Planner`：任务拆分者。
- `Researcher`：资料收集者。
- `Writer`：内容组织者。
- `Critic`：审核者。
- `TeamState`：共享状态容器。

理解要点：

- `planner_agent()` 把主题拆成任务。
- `expand_keywords()` 找知识库关键词。
- `researcher_agent()` 生成调研要点。
- `writer_agent()` 生成草稿。
- `critic_agent()` 找缺项。
- `supervisor()` 串起整个协作闭环。

## 7. 容器化服务

文件：`deployment/container_demo/app.py`

调用流程：

`main()（程序入口）` -> `HTTPServer(...)（启动 HTTP 服务）` -> `Handler.do_GET()（处理 GET 请求）` -> 返回 JSON

关键名词：

- `HTTPServer`：标准库 HTTP 服务。
- `Handler`：请求处理器。
- `Health Check`：健康检查接口。
- `Environment Variable`：环境变量配置。

理解要点：

- `do_GET()` 负责构造响应体。
- `log_message()` 被重写为静默输出。
- `main()` 负责启动服务。

## 8. RAG 评估脚本

文件：`eval/rag_eval_demo/eval_rag.py`

调用流程：

`main()（程序入口）` -> `load_samples()（加载样本）` -> `coverage()（计算覆盖率）` / `precision()（计算精确率）` -> 汇总输出

关键名词：

- `Sample`：评估样本。
- `gold_sources`：标准来源。
- `retrieved_sources`：检索结果来源。
- `coverage`：覆盖率。
- `precision`：精确率。

理解要点：

- `load_samples()` 读取样本数据。
- `coverage()` 看标准来源覆盖了多少。
- `precision()` 看召回结果有多少是对的。
- `main()` 逐条输出报表并计算平均值。

## 9. 快速记忆版

- “加载数据”的函数通常在前面：`load_*`
- “预处理”的函数通常负责切分、扩展、过滤：`chunk_*`、`split_*`、`filter_*`、`expand_*`
- “打分”的函数通常是：`score_*`
- “召回”的函数通常是：`retrieve()`
- “重排”的函数通常是：`rerank()`
- “生成答案”的函数通常是：`synthesize_answer()`
- “主流程”的函数通常是：`main()`
