Chat CLI — 学习说明与快速上手

目的
- 一个最小的 OpenAI Responses API 命令行示例，支持一次性提问与交互式对话。

业务场景说明
- 适用场景：需要一个轻量入口来验证提示词、模型切换和交互循环，常用于开发自测或教学演示。
- 如果不用这种方式：只能通过更重的前端或服务来验证，排查问题会更慢，也不方便做快速回归。
- 解决的问题：把对话能力先做成最小闭环，帮助确认 CLI 参数、输出格式和 mock / real 行为都正常。
- 举例说明：例如先用“你好”这种最小问题验证 mock 输出，再切到真实 API 看模式切换是否正常。

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
