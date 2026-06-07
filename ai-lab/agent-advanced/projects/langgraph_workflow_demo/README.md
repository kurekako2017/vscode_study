# langgraph_workflow_demo

LangGraph 风格最小状态图示例。

重点练习：

1. `StateGraph`
2. `State`
3. `Node`
4. `conditional edges`
5. `loop / revision`

## 运行

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/langgraph_workflow_demo
python3 main.py "LangGraph 适合什么场景"
```

## 学习点

- `classify_intent()` 看输入如何影响路由
- `research()` 看节点如何补充状态
- `review()` 和 `revise()` 看循环如何形成
- `finalize()` 看最终答案如何落地
