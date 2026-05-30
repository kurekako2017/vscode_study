Chat CLI — 学习说明与快速上手

目的
- 一个最小的 OpenAI Responses API 命令行示例，支持一次性提问与交互式对话。

快速运行
1. Mock 模式（无需 API Key）:
   ```bash
   RAG_API_MOCK=1 python3 main.py "你好"
   ```
2. 实际调用（需设置 `OPENAI_API_KEY`）:
   ```bash
   OPENAI_API_KEY=sk... python3 main.py --real "请总结文档"
   ```

关键函数
- `parse_args()`：解析 CLI 参数（--mock/--real/--max-chars）。
- `resolve_mode()`：决定 mock 或 real 模式。
- `ask_once()`：一次性提问并格式化输出。
- `run_interactive()`：交互式对话循环。

学习建议
- 阅读 `format_output()` 的实现，理解如何做输出截断与格式化。
- 在无网络环境中用 `--mock` 验证行为，再在真实环境测试 `--real`。

练习题
- 为 `--max-chars` 添加单元测试，验证截断逻辑。
