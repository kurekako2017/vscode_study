Workflow Agent Demo — 学习说明与快速上手

目的
- 演示一个三阶段（分析→计划→最终化）的简易工作流 agent，使用 Pydantic 验证计划结构并展示阶段化设计。

快速运行
1. Mock 模式：
   RAG_API_MOCK=1 python3 main.py --input "请制定发布计划"

关键点
- `analyze()`、`plan()`、`finalize()`：分阶段拆解任务，便于测试与维护。
- `WorkflowPlan`：Pydantic 模型，定义计划输出结构并进行验证。

学习建议
- 将阶段拆分为更细的子任务并为每个阶段增加回滚或错误处理逻辑。
