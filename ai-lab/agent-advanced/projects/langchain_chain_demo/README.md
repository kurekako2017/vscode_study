# langchain_chain_demo

LangChain 风格最小链路示例。

这个 demo 重点练三件事：

1. `ChatPromptTemplate` 组织提示词
2. `RunnableLambda` / `|` 串起链路
3. 结构化输出解析

默认不需要 API Key，直接可以跑。

## 安装

```bash
/usr/bin/python3 -m pip install -r /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/requirements.txt
```

依赖说明见 [项目依赖总表](../DEPENDENCIES.md)。

## 运行

```bash
/usr/bin/python3 -m pip install -r requirements.txt
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/langchain_chain_demo/main.py "什么是 LangChain 的链式编排"
```

尝试真实模式：

```bash
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/langchain_chain_demo/main.py --real "什么是 LangChain 的链式编排"
```

## 常见报错

- 如果终端里的 `which python3` 还指向别的 `.venv`，就直接用 `/usr/bin/python3` 执行上面的命令。
- 如果 VS Code 里还是红线，通常是 Python 解释器没切到当前 WSL 的 `/usr/bin/python3`，重载窗口或重新选择解释器即可。
- `缺少 langchain-openai`：只在 `--real` 模式需要；如果只是练流程，直接用 `--mock` 即可。

## 学习顺序

1. 先看 `build_prompt()`
2. 再看 `mock_llm()`
3. 再看 `parse_response()`
4. 最后看 `build_chain()`
