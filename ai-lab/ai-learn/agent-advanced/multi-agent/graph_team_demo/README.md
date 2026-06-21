# 真实 Multi-Agent 图编排

LangGraph Supervisor 根据共享状态把任务 handoff 给 Planner、Researcher、Writer、Reviewer。所有 worker 回到 Supervisor；`budget` 与 `recursion_limit` 提供双重终止保护。

```bash
python3 main.py "设计日本 SES 案件匹配方案"
python3 main.py "预算终止演示" --budget 2
```

验收：正常预算产生计划、证据、草稿和 `pass`；低预算提前终止。该实现用确定性 worker 隔离编排逻辑，接入 LLM 时无需改变图结构。
