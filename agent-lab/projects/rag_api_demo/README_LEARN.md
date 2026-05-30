RAG API Demo — 学习说明与快速上手

目的
- 提供一个最小的 FastAPI 服务示例，实现本地 RAG（文档检索问答）PoC，包含 `/ask`、`/reload`、`/health`。

快速运行（mock）
1. 在项目目录运行：
   RAG_API_MOCK=1 uvicorn main:app --reload --port 8000
2. 测试：
   curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"question":"请总结文档"}'

关键函数与文件
- `load_state()`：扫描目录并缓存 chunks。
- `retrieve()`：基于关键词匹配做本地检索（PoC）。
- `answer_question()`：支持 mock 与 real 两种调用方式。
- `mock_test.py`：无依赖的 smoke test，适合受限环境。

学习建议
- 先在 mock 模式熟悉 API，然后在 CI 或有 API Key 的环境中切换为 real。
- 将检索替换为向量检索并引入 embeddings 服务作为进阶任务。
