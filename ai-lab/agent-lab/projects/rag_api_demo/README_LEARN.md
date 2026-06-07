RAG API Demo - 学习说明与快速上手

目的
- 提供一个最小的 FastAPI 服务示例，实现本地 RAG（文档检索问答）PoC，包含 `/ask`、`/reload`、`/health`。

快速运行
1. 推荐直接使用项目自带脚本：
   ```bash
   cd ai-lab/agent-lab/projects/rag_api_demo
   ./run-dev.sh
   ```
2. 如果只想看 mock 输出，也可以直接跑：
   ```bash
   cd ai-lab/agent-lab/projects/rag_api_demo
   python3 mock_test.py
   ```
3. 手动启动 mock 服务：
   ```bash
   cd ai-lab/agent-lab/projects/rag_api_demo
   RAG_API_MOCK=1 uvicorn main:app --reload --port 8000 --host 127.0.0.1
   ```

关键函数与文件
- `load_state()`：扫描目录并缓存 chunks。
- `retrieve()`：基于关键词匹配做本地检索（PoC）。
- `answer_question()`：支持 mock 与 real 两种调用方式。
- `mock_test.py`：无依赖的 smoke test，适合受限环境。

学习建议
- 先在 mock 模式熟悉 API，然后在 CI 或有 API Key 的环境中切换为 real。
- 将检索替换为向量检索并引入 embeddings 服务作为进阶任务。

运行本地 smoke-test 并解析错误日志
--------------------------------

项目包含一个便捷的本地 smoke 测试脚本 `smoke_local.sh`，用于在 mock 模式下启动服务、等待 `/health`、调用 `/ask` 并做简单校验。使用步骤：

```bash
# 从仓库根或任意位置运行脚本（脚本会自动 cd 到项目目录）
./ai-lab/agent-lab/projects/rag_api_demo/smoke_local.sh
```

脚本会把服务日志写入 `ai-lab/agent-lab/projects/rag_api_demo/server.log`，并在退出前停止服务。

常见失败原因与排查方法：

- 超时未就绪（脚本在等待 `/health` 时超时，错误码 2）
  - 检查 `server.log`，查找导入错误（ImportError）、依赖缺失或启动异常（Traceback）。
  - 常见：`uvicorn` 未安装（"command not found"）或 Python 包缺失。
  - 解决：在项目目录创建虚拟环境并安装依赖，或者重新运行 `./run-dev.sh`。

- 端口被占用（server.log 包含 "Address already in use"）
  - 使用 `lsof -i :8000` 或 `ss -ltnp` 查找并释放端口，或修改脚本中 `PORT` 变量为其他端口。

- `/ask` 返回格式不符合预期（脚本报告缺少 `answer` 或 `source_count`）
  - 打开 `server.log` 与脚本输出，查看 `load_state()` 是否成功加载了文档目录（没有可读文档会导致服务抛出错误）。
  - 确认 `RAG_API_DOCS_DIR` 指向包含 `.md`/`.txt`/`.pdf` 的目录，或把示例文档放到当前目录下测试。
