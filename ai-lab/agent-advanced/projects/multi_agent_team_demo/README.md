# multi_agent_team_demo

多 Agent 协作 demo。

这个 demo 模拟了几个典型角色：

- Supervisor
- Planner
- Researcher
- Writer
- Critic

## 运行

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/multi_agent_team_demo
python3 main.py "如何学习 LangGraph 和高级 RAG"
```

## 学习点

1. `planner_agent()` 看任务怎么拆
2. `researcher_agent()` 看知识怎么补
3. `writer_agent()` 看结果怎么组织
4. `critic_agent()` 看反馈怎么做
5. `supervisor()` 看总调度怎么收口
