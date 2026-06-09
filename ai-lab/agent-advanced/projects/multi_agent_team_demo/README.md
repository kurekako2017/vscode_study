# multi_agent_team_demo

多 Agent 协作 demo。

这个 demo 模拟了几个典型角色：

- Supervisor
- Planner
- Researcher
- Writer
- Critic

## 业务场景说明

- 适用场景：复杂任务需要分工协作，比如规划、调研、写作和审校各自独立完成。
- 如果不用这种方式：单个 agent 容易同时背太多职责，结果波动更大，也不利于定位问题。
- 解决的问题：把职责拆给多个角色协同处理，让复杂任务更可控、可追踪，也更容易扩展。

## 安装

这个 demo 只用 Python 标准库，不需要额外安装第三方包。

如果你想统一查看各 demo 的依赖说明，可以看 [项目依赖总表](../DEPENDENCIES.md)。

## 运行

```bash
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/multi_agent_team_demo/main.py "如何学习 LangGraph 和高级 RAG"
```

## 常见报错

- 如果输出太短，通常是主题太窄，可以换一个更具体但更完整的问题。
- 如果没有看到二轮修订，说明 `critic_agent()` 没有发现明显问题，属于正常情况。

## 学习点

1. `planner_agent()` 看任务怎么拆
2. `researcher_agent()` 看知识怎么补
3. `writer_agent()` 看结果怎么组织
4. `critic_agent()` 看反馈怎么做
5. `supervisor()` 看总调度怎么收口
