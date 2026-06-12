# langchain_chain_demo

LangChain 风格最小链路示例。

如果你想先把 LangChain 的知识补齐，再来跑这个 demo，可以先看：

- [frameworks/langchain/LangChain 学习笔记](../../frameworks/langchain/LangChain学习笔记.md)

这个 demo 重点练三件事：

1. `ChatPromptTemplate` 组织提示词
2. `RunnableLambda` / `|` 串起链路
3. 结构化输出解析

默认会先尝试真实模型；如果没配 API Key，会自动回退到 mock。

## 业务场景说明

- 适用场景：需要把提示词、模型调用和输出解析串成固定链路，给后续业务步骤复用。
- 如果不用这种方式：相关逻辑会散落在各处，后面改一个字段或一段提示词就容易牵一发而动全身。
- 解决的问题：用链式编排把流程标准化，既方便复用，也方便替换其中某一段实现。
- 举例说明：例如先做一个“问题 -> 检索 -> 总结”的链式流程，确认每一步的输入输出都能单独检查。

## 安装

```bash
/usr/bin/python3 -m pip install -r /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/requirements.txt
```

依赖说明见 [项目依赖总表](../DEPENDENCIES.md)。

## 运行

```bash
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/langchain_chain_demo/main.py "什么是 LangChain 的链式编排"
```

强制 mock：

```bash
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/langchain_chain_demo/main.py "什么是 LangChain 的链式编排" --mock
```

如果你已经配置了 API Key，直接不加 `--mock` 就会优先尝试真实模式。

如果你想同时看“模型原始输出”和“解析后的结果”，再加上 `--show-raw`。

```bash
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/langchain_chain_demo/main.py "什么是 LangChain 的链式编排" --show-raw
```

输出里会先看到 `=== 原始结果 ===`，再看到 `=== 解析后结果 ===`。

## 常见报错

- 如果终端里的 `which python3` 还指向别的 `.venv`，就直接用 `/usr/bin/python3` 执行上面的命令。
- 如果 VS Code 里还是红线，通常是 Python 解释器没切到当前 WSL 的 `/usr/bin/python3`，重载窗口或重新选择解释器即可。
- `缺少 langchain-openai`：只在真实模式需要；如果只是练流程，直接用 `--mock` 即可。

## 学习顺序

1. 先看 `build_prompt()`
2. 再看 `mock_llm()`
3. 再看 `parse_response()`
4. 最后看 `build_chain()`
5. 如果想继续往后学，再看 `Tool Calling`、`Memory`、`Retriever`、`RAG`、`Agent`

如果想理解“上面那段是原始模型输出，下面那段是重新组装后的结构化结果”，再补看一次 `--show-raw` 的输出：

- `raw_message.content` 是模型直接吐出来的原始内容
- `parse_response()` 是把原始内容重新解析成字典
- `print(json.dumps(...))` 打印的是解析后的最终结果
