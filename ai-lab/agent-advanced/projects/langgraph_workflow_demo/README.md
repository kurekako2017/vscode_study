# langgraph_workflow_demo

LangGraph 风格最小状态图示例。

重点练习：

1. `StateGraph`
2. `State`
3. `Node`
4. `conditional edges`
5. `loop / revision`

## 业务场景说明

- 适用场景：任务需要状态、条件分支和循环，比如审阅-修订、分类-路由、或者多轮补全。
- 如果不用这种方式：普通链路很难表达回路和状态变化，后续扩展流程时也不容易维护。
- 解决的问题：把复杂流程显式建模成状态图，让分支、重试和修订都可见、可控、可测试。

## 安装

```bash
/usr/bin/python3 -m pip install -r /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/requirements.txt
```

依赖说明见 [项目依赖总表](../DEPENDENCIES.md)。

## 运行

```bash
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/langgraph_workflow_demo/main.py "LangGraph 适合什么场景"
```

默认只打印简洁结果。如果你想看完整 Mermaid 图，加上 `--show-graph`：

```bash
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/langgraph_workflow_demo/main.py "LangGraph 适合什么场景" --show-graph
```

## 常见报错

- `ModuleNotFoundError: No module named 'langgraph'`：先安装统一依赖，并确认当前终端和 VS Code 解释器一致；如果 `python3` 被别的虚拟环境劫持，直接改用 `/usr/bin/python3`。
- 如果运行时还是红线，通常是解释器选错了，不是代码本身坏了。

## 学习点

- `classify_intent()` 看输入如何影响路由
- `research()` 看节点如何补充状态
- `review()` 和 `revise()` 看循环如何形成
- `finalize()` 看最终答案如何落地
