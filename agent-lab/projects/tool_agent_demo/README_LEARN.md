Tool Agent Demo — 学习说明与快速上手

目的
- 展示工具调用型 agent：定义本地工具（list/read/search），并演示如何通过函数式工具扩展 agent 能力。

快速运行
1. Mock 模式：
   RAG_API_MOCK=1 python3 main.py --task "查找关键字"

关键函数
- `tools` 列表：定义可被 agent 调用的工具函数与签名。
- `run_agent()`：主循环，示例了如何在模型与工具间交互并处理函数调用。

学习建议
- 尝试增加自定义工具（如 web_fetch）并扩展 `run_agent()` 来处理更复杂的工具交互。
