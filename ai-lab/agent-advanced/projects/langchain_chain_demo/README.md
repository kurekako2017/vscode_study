# langchain_chain_demo

LangChain 风格最小链路示例。

这个 demo 重点练三件事：

1. `ChatPromptTemplate` 组织提示词
2. `RunnableLambda` / `|` 串起链路
3. 结构化输出解析

默认不需要 API Key，直接可以跑。

## 运行

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/langchain_chain_demo
pip3 install -r requirements.txt
python3 main.py "什么是 LangChain 的链式编排"
```

尝试真实模式：

```bash
python3 main.py --real "什么是 LangChain 的链式编排"
```

## 学习顺序

1. 先看 `build_prompt()`
2. 再看 `mock_llm()`
3. 再看 `parse_response()`
4. 最后看 `build_chain()`
