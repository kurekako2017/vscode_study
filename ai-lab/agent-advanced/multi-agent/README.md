# multi-agent

这个目录放多 Agent 专题。

这里主要是概念和组织方式，对应的可运行代码在：

- [projects/multi_agent_team_demo](../projects/multi_agent_team_demo/README.md)

建议内容：

- 单 Agent 到多 Agent 的差异
- 监督者 / 执行者 / 规划者
- Agent 路由
- 工具共享
- 消息传递和状态共享
- 失败恢复和终止条件

## 业务场景说明

- 适用场景：一个任务需要多个角色分工协作，例如规划、调研、写作、审校各自负责一段。
- 如果不用这种方式：单个 agent 会承担过多职责，质量波动更大，也不容易定位问题。
- 解决的问题：先从概念上讲清楚多 agent 的角色和协作方式，再去看可运行 demo 会更容易理解。
