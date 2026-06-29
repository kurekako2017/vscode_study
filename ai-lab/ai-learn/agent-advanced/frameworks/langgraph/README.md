# LangGraph

这个章节讲 LangGraph 的状态图、分支和循环。

## 业务场景说明

- 适用场景：任务需要显式状态和回路管理，比如审阅修订、条件分支、循环补充信息。
- 如果不用这种方式：普通链路难以表达复杂流程，后续想加重试或回路时会很别扭。
- 解决的问题：把流程建模成状态图，让复杂 Agent 行为可控、可视和可测试。
- 举例说明：例如把“审批请求 -> 检查条件 -> 进入不同分支 -> 输出结果”做成一个小图，验证 LangGraph 的状态流转是否清晰。

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

## 结构整理补充

### 1. 目录作用

本目录是 LangGraph 基础知识入口，负责 State、Node、Edge、条件路由和循环；进阶与企业示例分布在项目和专题目录中。

### 2. 适合学习内容

- Typed State 与节点输入输出。
- 条件边、循环终止、错误分支和重试。
- Checkpoint、Memory、Interrupt、人工审批和恢复。
- Supervisor 与 Multi-Agent 图编排。

### 3. 子目录与文件说明

当前没有下级子目录，学习入口由以下文件组成：

| 文件 | 用途 |
| --- | --- |
| [README.md](./README.md) | LangGraph 基础概念和学习目标 |
| [相关项目链接.md](./相关项目链接.md) | 基础、Multi-Agent、企业级和完整业务项目导航 |

### 4. 推荐学习顺序

1. 阅读本 README 并手画 State、Node、Edge。
2. 运行基础 `langgraph_workflow_demo`。
3. 学习 `graph_team_demo` 的共享状态和角色路由。
4. 学习企业能力、Deep Research 和完整业务项目。

### 5. 相关实战项目

统一查看 [LangGraph 相关项目链接](./相关项目链接.md)。

### 6. 注意事项

- 轻量多角色协作示例不一定使用真实 LangGraph，必须查看导入代码。
- 循环必须有明确终止条件；高影响节点应设置人工审批。
- 不移动企业项目、runtime 数据库、测试或前端目录。
