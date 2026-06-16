# DeepSearch 代码学习路线

这份文档不是启动指南，而是“按调用链学代码”的阅读顺序。

适合你现在这种目标：

- 想知道一个请求从前端到后端是怎么跑的
- 想知道哪个函数是真入口，哪个函数只是工具层
- 想结合日志边跑边看代码

建议配合这几份资料一起看：

- [deepsearch-call-flow.md](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/deepsearch-call-flow.md:1)
- [BUG_LOG_GUIDE.md](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/BUG_LOG_GUIDE.md:1)
- [BUG_REPRO_TASKS.md](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/BUG_REPRO_TASKS.md:1)

## 1. 第一轮先只看主线

如果你第一次进项目，不要一上来就看所有工具。

先只抓这一条主线：

```text
前端输入任务
  -> useDeepAgentSession()
  -> POST /api/task
  -> run_deep_agent()
  -> monitor 推送事件
  -> 前端展示结果
```

按这个顺序读：

1. [frontend/src/App.tsx](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/frontend/src/App.tsx:43)
   先看 `App()` 和 `handleSubmit()`
2. [frontend/src/hooks/useDeepAgentSession.ts](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/frontend/src/hooks/useDeepAgentSession.ts:23)
   重点看 `useDeepAgentSession()`、`connect()`、`submitTask()`
3. [frontend/src/lib/api.ts](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/frontend/src/lib/api.ts:32)
   重点看 `startTask()`
4. [app/api/server.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/api/server.py:132)
   重点看 `run_task()`
5. [app/agent/main_agent.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/agent/main_agent.py:468)
   重点看 `run_deep_agent()`
6. [app/api/monitor.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/api/monitor.py:38)
   重点看 `_emit()`、`report_task_result()`、`send_to_thread()`

这一轮看完，你应该能回答三个问题：

- 前端是怎么把任务发给后端的
- 后端是怎么异步执行任务的
- 结果和过程事件是怎么回到前端的

## 2. 第二轮看“任务为什么会走不同分支”

这个项目有一个很适合初学者的点：

- 不是所有任务都必须走完整多智能体链路
- 有些任务会先被关键词判断，直接走特定分支

重点读 [app/agent/main_agent.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/agent/main_agent.py:123) 里的这些函数：

- `_is_upload_file_task()`
- `_is_local_kb_task()`
- `_is_database_task()`
- `run_deep_agent()`
- `_answer_database_task_sync()`
- `_analyze_uploaded_files_sync()`
- `_answer_local_kb_sync()`

你要特别留意 `run_deep_agent()` 里的判断顺序，因为这决定了：

- 用户这句话是先走数据库直达
- 还是先走本地知识库直达
- 还是进入完整主智能体调度

建议你直接拿下面 3 句话分别测试：

1. `先列出当前数据库有哪些表，再挑一张表预览前 5 行数据。`
2. `请根据本地知识库总结 3 个核心趋势。`
3. `请读取我上传的文件，提炼核心观点和风险点。`

然后对照日志看：

- `database_branch_selected`
- `local_kb_branch_selected`
- `upload_task_branch_selected`

## 3. 第三轮看“完整主智能体是怎么调子助手的”

当任务没有命中直达分支时，就会进入真正的多智能体主链路。

按这个顺序读：

1. [app/agent/main_agent.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/agent/main_agent.py:54)
   看 `build_main_agent()`
2. [app/agent/prompts.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/agent/prompts.py:14)
   看 `load_yaml()`
3. [app/prompt/prompts.yml](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/prompt/prompts.yml:1)
   看主提示词到底怎么描述各助手职责
4. [app/agent/main_agent.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/agent/main_agent.py:382)
   看 `_stream_agent_sync()`

这一轮最关键的是 `_stream_agent_sync()`。

你重点盯住这几个点：

- `agent.stream(...)` 是怎么不断产出 chunk 的
- `node_name` 是怎么被记录和上报的
- `tool_calls` 里什么时候会出现 `task`
- `monitor.report_assistant()` 是在哪里触发的
- `monitor.report_task_result()` 是在哪里触发的

配合日志看最有感觉：

- `agent_stream_started`
- `agent_chunk_received`
- `subagent_dispatch_detected`
- `agent_final_result_generated`

## 4. 第四轮按子助手拆开学

主智能体学完后，再拆看每个子助手。

### 4.1 网络搜索助手

先看：

- [app/agent/subagents/network_search_agent.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/agent/subagents/network_search_agent.py:1)
- [app/tools/tavily_tool.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/tools/tavily_tool.py:38)

你会学到：

- 子助手是怎么绑定自己专属工具的
- 网络搜索结果是怎么回到主智能体的

### 4.2 数据库查询助手

先看：

- [app/agent/subagents/database_query_agent.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/agent/subagents/database_query_agent.py:1)
- [app/tools/db_tools.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/tools/db_tools.py:61)

重点函数：

- `list_sql_tables()`
- `get_table_data()`
- `execute_sql_query()`

你会学到：

- 数据库工具怎样把真实表数据转给模型
- 为什么日志里经常先看到列表，再看到预览，再看到 SQL

### 4.3 本地知识库助手

先看：

- [app/agent/subagents/knowledge_base_agent.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/agent/subagents/knowledge_base_agent.py:1)
- [app/tools/local_kb_tools.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/tools/local_kb_tools.py:19)
- [app/knowledge_base/local_index.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/knowledge_base/local_index.py:113)

重点函数：

- `get_assistant_list()`
- `create_ask_delete()`
- `load_knowledge_docs()`
- `search_knowledge_base()`

你会学到：

- 本地文档是怎么被加载成知识库的
- 问题是怎么在本地资料里做检索的

## 5. 第五轮学文件读写产物链

这个项目有一个很实用的学习点：

- 输入文件和输出文件是分开的
- 上传附件先进 `updated/`
- 真正任务工作区在 `output/`

按这个顺序读：

1. [app/api/server.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/api/server.py:185)
   看 `upload_files()`
2. [app/agent/main_agent.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/agent/main_agent.py:522)
   看上传文件复制到 `output/session_xxx` 的部分
3. [app/tools/upload_file_read_tool.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/tools/upload_file_read_tool.py:36)
   看 `read_file_content()`
4. [app/tools/markdown_tools.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/tools/markdown_tools.py:22)
   看 `generate_markdown()`
5. [app/tools/pdf_tools.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/tools/pdf_tools.py:25)
   看 `convert_md_to_pdf()`
6. [app/api/server.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/api/server.py:243)
   看 `list_files()` 和 `download_file()`

配合前端一起看：

- [frontend/src/components/FileDock.tsx](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/frontend/src/components/FileDock.tsx:1)

这一轮看完，你就能知道：

- 为什么有时上传成功了但任务还没开始
- 为什么产物文件要去 `output/session_xxx`
- 为什么文件列表是轮询，不是 WebSocket 直接推完整文件内容

## 6. 第六轮专门学日志与排错

如果你是按“上线后怎么靠日志排 bug”这个思路学项目，这一轮很重要。

先看：

- [app/utils/logging_utils.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/utils/logging_utils.py:1)
- [BUG_LOG_GUIDE.md](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/BUG_LOG_GUIDE.md:1)
- [BUG_REPRO_TASKS.md](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/BUG_REPRO_TASKS.md:1)

重点理解三件事：

1. 日志为什么统一打成 `event + 结构化字段`
2. `thread_id` 为什么几乎每条关键日志都要带
3. 为什么 monitor 事件和后端日志最好一起看

推荐日志文件目录：

- 项目内长期保留：
  [logs/deepsearch-debug.log](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/logs/deepsearch-debug.log)
- 临时排查：
  `/tmp/deepsearch-debug.log`

## 7. 最推荐的实战学习顺序

如果你只想要一条最省力的学习路线，就按下面跑。

1. 启动前后端，打开页面，先只观察 WebSocket 建连
2. 发一个数据库任务，看 `run_task()` -> `run_deep_agent()` -> `_answer_database_task_sync()`
3. 发一个知识库任务，看 `run_deep_agent()` -> `_answer_local_kb_sync()`
4. 上传一个文件，再发文件读取任务，看 `upload_files()` -> `read_file_content()` -> `_analyze_uploaded_files_sync()`
5. 发一个开放式调研任务，看 `build_main_agent()` -> `_stream_agent_sync()` -> 子助手工具调用
6. 一边跑，一边按 `thread_id` grep 日志

## 8. 读代码时的一个小技巧

每次只回答下面 4 个问题，不要试图一次全懂：

1. 这个函数是谁调用的
2. 这个函数往下又调用了谁
3. 它输入的关键数据是什么
4. 它出了错会打什么日志

你如果愿意，我下一步可以继续把这份 [CODE_READING_ROUTE.md](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/CODE_READING_ROUTE.md:1) 再补成“按数据库链 / 知识库链 / 文件链分别拆开的阅读版”。 
