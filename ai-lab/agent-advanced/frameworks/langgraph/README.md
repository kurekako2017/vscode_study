# LangGraph

这个章节讲 LangGraph 的状态图、分支和循环。

## 业务场景说明

- 适用场景：任务需要显式状态和回路管理，比如审阅修订、条件分支、循环补充信息。
- 如果不用这种方式：普通链路难以表达复杂流程，后续想加重试或回路时会很别扭。
- 解决的问题：把流程建模成状态图，让复杂 Agent 行为可控、可视和可测试。

## 先看什么

1. State 是什么
2. Node 是什么
3. Edge / conditional edge 怎么控制流程

## 对应代码

- [projects/langgraph_workflow_demo](../../projects/langgraph_workflow_demo/README.md)

## 学习目标

- 看懂状态驱动的工作流
- 看懂条件分支和回路
- 理解 LangGraph 适合做什么类型的 Agent
