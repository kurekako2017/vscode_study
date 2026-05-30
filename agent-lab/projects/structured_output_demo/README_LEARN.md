Structured Output Demo — 学习说明与快速上手

目的
- 演示如何用模型生成受结构化约束的输出，并用 Pydantic 做解析与验证。

快速运行
1. Mock 模式：
   ```bash
   RAG_API_MOCK=1 python3 main.py --prompt "请生成计划"
   ```

关键点
- `AgentPlan`：Pydantic 模型，定义输出结构。
- `client.responses.parse()`：演示如何解析模型输出为结构化对象（real 模式）。

学习建议
- 修改 Pydantic 模型以匹配不同任务（如任务列表、时间线），并验证解析失败的处理逻辑。
