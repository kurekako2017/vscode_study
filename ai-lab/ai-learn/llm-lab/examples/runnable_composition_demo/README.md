# Runnable 组合模式

用真实 LCEL 演示 `RunnablePassthrough.assign`、`RunnableParallel`、`RunnableBranch`、`batch` 和 `stream`。示例无模型调用，不需要 API Key。

```bash
python3 main.py
python3 main.py "RAG 如何重排" --stream
```

验收：默认一次批处理两个问题并进入不同分支；`--stream` 能逐块输出。依赖：`langchain-core>=1.2,<2`。
