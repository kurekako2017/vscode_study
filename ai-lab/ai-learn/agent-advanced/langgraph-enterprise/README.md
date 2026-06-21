# LangGraph 企业能力主线

`demos/enterprise_graph.py` 在一张真实状态图中覆盖：

- `InMemorySaver` + `thread_id`：Checkpoint 与线程恢复
- `InMemoryStore`：跨线程的客户长期 Memory
- `interrupt` + `Command(resume=...)`：HITL 审批与恢复
- 编译后的准备子图：Subgraph
- `stream(..., stream_mode="updates")`：节点级 Streaming
- reducer：并行/嵌套节点安全追加事件

```bash
cd ai-learn/agent-advanced/langgraph-enterprise
python3 demos/enterprise_graph.py "发送三万日元以上报价" --decision yes
python3 demos/enterprise_graph.py "删除客户记录" --decision no --thread reject-1
```

验收：首次运行停在 `approval` checkpoint，恢复后进入执行或拒绝分支；终端持续打印节点更新。内存实现适合教学，生产应换 SQLite/Postgres checkpointer 和持久化 Store，并为 `thread_id` 增加租户隔离。

## 概念边界

Checkpoint 保存“某个线程运行到哪里”；短期 Memory 是该线程状态；Store 保存可跨线程读取的长期事实。HITL 必须在有 checkpointer 的图上使用，否则进程恢复后无法可靠续跑。
