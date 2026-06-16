# Bug 日志使用说明

这次补的日志默认输出到后端控制台，格式是：

```text
2026-06-16 23:10:00,123 | INFO | app.api.server | {"event":"task_started","thread_id":"xxx",...}
```

特点：

- 统一结构化输出，方便 `grep event`
- 会自动带上 `thread_id`
- 在主智能体和工具层尽量补上 `session_dir`、文件名、表名、异常信息

## 1. 默认行为

直接启动后端即可看到日志：

```bash
python3 -m uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload
```

## 2. 打开更详细的 bug 日志

```bash
DEEPSEARCH_LOG_LEVEL=DEBUG python3 -m uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload
```

推荐在排查问题时使用 `DEBUG`，平时可以保留默认 `INFO`。

## 3. 同时写入日志文件

推荐目录：

- 临时排查：`/tmp/deepsearch-debug.log`
- 放在项目目录里长期保留：`/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/logs/deepsearch-debug.log`

如果你希望日志跟项目放在一起，建议先使用下面这个路径：

```text
/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/logs/deepsearch-debug.log
```

```bash
DEEPSEARCH_LOG_LEVEL=DEBUG \
DEEPSEARCH_LOG_FILE=/tmp/deepsearch-debug.log \
python3 -m uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload
```

这样日志会同时输出到：

- 当前终端
- `/tmp/deepsearch-debug.log`

如果你要写到项目目录，直接用：

```bash
DEEPSEARCH_LOG_LEVEL=DEBUG \
DEEPSEARCH_LOG_FILE=/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/logs/deepsearch-debug.log \
python3 -m uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload
```

这样日志会输出到：

- 当前终端
- `/home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/logs/deepsearch-debug.log`

## 4. 最值得看的事件

### 4.1 请求进入

- `task_start_requested`
- `task_started`
- `websocket_connect_requested`

### 4.2 主智能体执行

- `run_deep_agent_started`
- `main_agent_primary_provider_selected`
- `agent_stream_started`
- `agent_chunk_received`
- `subagent_dispatch_detected`
- `agent_final_result_generated`

### 4.3 分支直达任务

- `database_branch_selected`
- `local_kb_branch_selected`
- `upload_task_branch_selected`

### 4.4 工具层

- `db_list_tables_started`
- `db_get_table_data_started`
- `db_execute_sql_started`
- `file_read_started`
- `markdown_generate_started`
- `pdf_convert_started`

### 4.5 异常排查

- `run_deep_agent_failed`
- `main_agent_primary_provider_failed_no_fallback`
- `main_agent_fallback_failed`
- `database_branch_failed`
- `upload_task_branch_failed`
- `local_kb_branch_failed`
- `websocket_exception`

## 5. 推荐 grep 方法

按任务看：

```bash
grep 'thread_id":"你的thread_id' /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/logs/deepsearch-debug.log
```

按数据库问题看：

```bash
grep 'db_' /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/logs/deepsearch-debug.log
```

按文件生成问题看：

```bash
grep 'markdown_generate\|pdf_convert\|file_read_' /home/victorkure/workspace/vscode_study/ai-lab/ai-agents-from-zero/deepsearch-agents-main/logs/deepsearch-debug.log
```
