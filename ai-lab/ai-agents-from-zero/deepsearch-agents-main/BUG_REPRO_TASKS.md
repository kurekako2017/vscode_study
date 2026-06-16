# 故障复现任务清单

这份清单是配合 [BUG_LOG_GUIDE.md](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/BUG_LOG_GUIDE.md:1) 使用的。

目的不是做产品验收，而是：

- 快速复现常见问题
- 对照关键日志学习代码调用链
- 知道一个任务到底走了哪条分支

建议启动方式：

```bash
DEEPSEARCH_LOG_LEVEL=DEBUG \
DEEPSEARCH_LOG_FILE=/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/logs/deepsearch-debug.log \
python3 -m uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload
```

上面这条命令会把日志写到：

```text
/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/logs/deepsearch-debug.log
```

---

## 1. 通用观察方法

每次测试都建议先看这几类日志：

- 请求进入：`task_start_requested`、`task_started`
- WebSocket：`websocket_connect_requested`、`websocket_message_received`
- 主入口：`run_deep_agent_started`
- 分支判断：`database_branch_selected`、`local_kb_branch_selected`、`upload_task_branch_selected`
- 结果结束：`agent_final_result_generated`、`monitor_event_emitted`
- 异常结束：`run_deep_agent_failed`

按当前任务过滤：

```bash
grep 'thread_id":"你的thread_id' /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/logs/deepsearch-debug.log
```

---

## 2. 健康检查链路

### 测试动作

```bash
curl -s http://127.0.0.1:8000/api/health
```

### 预期现象

- 能返回 JSON
- 前端健康区也应能显示 Backend / LLM / MySQL / Services

### 关键日志

- `health_check_requested`

### 适合学习的代码入口

- [app/api/server.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/api/server.py:96)

---

## 3. WebSocket 建连链路

### 测试动作

打开前端页面，不发任务，只观察页面初始化。

### 预期现象

- 左侧 `WebSocket` 显示 `已连接`
- 不需要先发任务就能建立连接

### 关键日志

- `websocket_connect_requested`
- `connection_manager_client_connected`
- `websocket_message_received`

### 出问题时常见表现

- 页面一直 `连接中`
- 页面反复 `重连中`

### 适合学习的代码入口

- [useDeepAgentSession.ts](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/frontend/src/hooks/useDeepAgentSession.ts:79)
- [app/api/server.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/api/server.py:295)
- [app/api/monitor.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/api/monitor.py:160)

---

## 4. 数据库直达分支

### 测试输入

```text
先列出当前数据库有哪些表，再挑一张表预览前 5 行数据。
```

### 预期现象

- 直接走数据库分支
- 最终结果区应该是可读中文，不应该是原始 JSON
- 能看到表名，或明确提示空库/异常

### 关键日志

- `task_start_requested`
- `run_deep_agent_started`
- `database_branch_selected`
- `database_direct_answer_started`
- `db_list_tables_started`
- `db_list_tables_completed` 或 `db_list_tables_failed`
- `db_get_table_data_started`
- `db_get_table_data_completed` 或 `db_get_table_data_failed`
- `database_direct_answer_context_ready`
- `monitor_event_emitted`

### 出问题时怎么判断

- 没看到 `database_branch_selected`
  说明任务问法没有命中数据库分支关键词
- 只看到 `db_list_tables_started`，没看到 completed
  说明卡在数据库连接或查询阶段
- 结果区是原始 JSON
  优先看 `agent_final_result_generated` 和 `monitor_event_emitted`

### 适合学习的代码入口

- [app/agent/main_agent.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/agent/main_agent.py:594)
- [app/tools/db_tools.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/tools/db_tools.py:61)

---

## 5. 数据库复杂查询链路

### 测试输入

```text
请基于真实表名执行一个最容易命中的查询，并用 Markdown 表格输出。若没有数据，请明确告诉我当前表是空的还是表名不匹配。
```

### 预期现象

- 如果有数据，看到表格或结构化结果
- 如果没有数据，看到明确错误原因

### 关键日志

- `database_branch_selected`
- `db_list_tables_started`
- `db_get_table_data_started`
- `db_execute_sql_started`
- `db_execute_sql_completed` 或 `db_execute_sql_failed`

### 出问题时怎么判断

- 看到了 `db_execute_sql_failed`
  优先排 SQL、表名、字段名
- 只看到 `db_get_table_data_completed`
  说明还没走到执行 SQL

### 适合学习的代码入口

- [app/tools/db_tools.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/tools/db_tools.py:173)

---

## 6. 本地知识库直达分支

### 测试输入

```text
请根据内部知识库总结电商行业 AI 应用的 3 个核心趋势。
```

### 预期现象

- 直接走本地知识库分支
- 不依赖外部 RAGFlow 服务
- 能返回资料摘要、建议，或者明确提示没命中

### 关键日志

- `local_kb_branch_selected`
- `local_kb_direct_answer_started`
- `local_kb_get_assistant_list_started`
- `local_kb_assistant_list_completed` 或 `local_kb_empty`
- `local_kb_query_started`
- `local_kb_query_completed` 或 `local_kb_query_no_results`

### 出问题时怎么判断

- 如果直接看到 `local_kb_empty`
  先检查 `docs/knowledge_base/`
- 如果看到 `local_kb_query_no_results`
  说明链路是通的，只是语义没召回

### 适合学习的代码入口

- [app/agent/main_agent.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/agent/main_agent.py:581)
- [app/tools/local_kb_tools.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/tools/local_kb_tools.py:19)
- [app/knowledge_base/local_index.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/knowledge_base/local_index.py:148)

---

## 7. 上传文件缺失错误分支

### 测试输入

```text
请读取我上传的文件，提炼核心观点和风险点。
```

前提：

- 不上传任何文件，直接发这句话

### 预期现象

- 页面应明确提示没有检测到上传文件
- 不应该进入真正的文件读取

### 关键日志

- `run_deep_agent_started`
- `upload_task_missing_uploaded_files`
- `monitor_event_emitted`

### 出问题时怎么判断

- 如果没看到 `upload_task_missing_uploaded_files`
  说明任务没有命中文件分支

### 适合学习的代码入口

- [app/agent/main_agent.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/agent/main_agent.py:556)

---

## 8. 上传文件分析直达分支

### 测试动作

先上传一个 `.md`、`.pdf` 或 `.xlsx` 文件，再发送：

```text
请读取我上传的文件，提炼核心观点、风险点、待补充信息和下一步分析计划。
```

### 预期现象

- 直接走上传文件分支
- 能看到读取文件和分析结果

### 关键日志

- `upload_started`
- `upload_saved_file`
- `run_deep_agent_started`
- `session_uploaded_files_found`
- `upload_task_branch_selected`
- `uploaded_files_analysis_started`
- `file_read_started`
- `file_read_text_completed` / `file_read_pdf_completed` / `file_read_excel_completed`

### 出问题时怎么判断

- 有 `upload_saved_file`，但没有 `session_uploaded_files_found`
  先检查 `thread_id` 是否一致
- 有 `file_read_started`，但没有 completed
  说明文件解析出错

### 适合学习的代码入口

- [app/api/server.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/api/server.py:180)
- [app/agent/main_agent.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/agent/main_agent.py:563)
- [app/tools/upload_file_read_tool.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/tools/upload_file_read_tool.py:36)

---

## 9. 常规多智能体任务链路

### 测试输入

```text
帮我简单介绍一下这个系统能做什么。
```

### 预期现象

- 不走数据库/知识库/上传文件直达分支
- 进入主智能体常规流式执行

### 关键日志

- `main_agent_primary_provider_selected`
- `agent_worker_thread_started`
- `agent_stream_started`
- `agent_chunk_received`
- `subagent_dispatch_detected` 或 `agent_final_result_generated`

### 出问题时怎么判断

- 没有 `agent_stream_started`
  说明还没进入主智能体执行
- 有 `agent_stream_started`，但没有 `agent_final_result_generated`
  说明流式执行中断、超时或模型没有给最终文本

### 适合学习的代码入口

- [app/agent/main_agent.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/agent/main_agent.py:400)

---

## 10. Markdown 生成链路

### 测试输入

```text
请生成一份 Markdown 报告，总结这个系统的主要能力，并保存到当前工作目录。
```

### 预期现象

- 最终会生成 `.md` 文件
- 文件列表里能看到产物

### 关键日志

- `text_tool_call_detected`
- `markdown_generate_started`
- `markdown_generate_path_resolved`
- `markdown_generate_parent_created`
- `markdown_generate_completed`
- `list_files_completed`

### 出问题时怎么判断

- 有 `text_tool_call_detected`，但没有 `markdown_generate_started`
  说明文本工具调用兼容没接上
- 有 started 没有 completed
  看 `markdown_generate_failed`

### 适合学习的代码入口

- [app/agent/main_agent.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/agent/main_agent.py:182)
- [app/tools/markdown_tools.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/tools/markdown_tools.py:22)

---

## 11. PDF 生成链路

### 测试输入

```text
请生成一份 PDF 报告，总结这个系统的主要能力，并保存到当前工作目录。
```

### 预期现象

- 会先生成 Markdown，再转 PDF
- 文件列表里最终能看到 `.pdf`

### 关键日志

- `text_tool_call_detected`
- `markdown_generate_started`
- `pdf_convert_started`
- `pdf_convert_md_path_resolved`
- `pdf_convert_output_path_ready`
- `pdf_convert_completed`

### 出问题时怎么判断

- 有 Markdown 生成，没有 PDF 完成
  优先看 `pdf_convert_failed`
- `pdf_convert_missing_markdown`
  说明前一步 Markdown 没生成成功

### 适合学习的代码入口

- [app/tools/pdf_tools.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/tools/pdf_tools.py:25)
- [app/utils/word_converter.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/utils/word_converter.py:1)

---

## 12. 网络搜索链路

### 测试输入

```text
请使用网络搜索工具，搜索 2026 年 AI 在电商行业的应用趋势，并总结 3 个重点。
```

### 预期现象

- 常规多智能体链路里调起网络搜索助手
- 如果没配 Tavily，会给明确提示

### 关键日志

- `agent_stream_started`
- `subagent_dispatch_detected`
- `internet_search_started`
- `internet_search_completed` 或 `internet_search_missing_api_key`

### 出问题时怎么判断

- 如果看不到 `internet_search_started`
  说明没有真正调用到工具
- 如果是 `internet_search_missing_api_key`
  说明链路正常，只是环境没配

### 适合学习的代码入口

- [app/agent/subagents/network_search_agent.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/agent/subagents/network_search_agent.py:1)
- [app/tools/tavily_tool.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/tools/tavily_tool.py:38)

---

## 13. 超时与模型 fallback 链路

### 测试方法

这个场景通常不是靠固定 prompt 触发，而是在模型慢、网络差、额度异常时出现。

### 关键日志

- `main_agent_primary_provider_selected`
- `agent_worker_timeout`
- `main_agent_primary_provider_failed_no_fallback`
- `main_agent_fallback_to_nvidia`
- `main_agent_fallback_failed`
- `run_deep_agent_failed`

### 适合学习的代码入口

- [app/agent/main_agent.py](/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/app/agent/main_agent.py:624)

---

## 14. 最推荐的学习顺序

如果你想边复现边学调用链，推荐按这个顺序跑：

1. 健康检查链路
2. WebSocket 建连链路
3. 数据库直达分支
4. 本地知识库直达分支
5. 上传文件直达分支
6. 常规多智能体任务链路
7. Markdown / PDF 生成链路
8. 网络搜索链路

这样你会从“最短路径”逐步走到“最长路径”，不容易乱。
