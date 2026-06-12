# LangChain

LangChain 可以简单理解成：

**把大模型 API 变成“能调用工具、能记忆、能查资料、能多步骤执行”的 Python 框架。**

普通调用模型是这样：

```text
你问一句 -> 模型回答一句
```

LangChain 是这样：

```text
用户问题
↓
模型判断要不要调用工具
↓
调用 Python 函数 / 搜索 / 数据库 / 文件
↓
把结果交给模型
↓
模型继续回答
```

所以它主要用来做：

| 用途 | 例子 |
| --- | --- |
| Tool Calling | 让模型调用天气、计算器、文件读取函数 |
| RAG | 让模型查询你的 PDF / 文档后回答 |
| Agent | 让模型自己决定下一步做什么 |
| Memory | 让模型记住前面对话 |
| Workflow | 多步骤任务自动执行 |

最小例子：

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="nvidia/nemotron-3-ultra-550b-a55b",
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1",
)

res = llm.invoke("请用简单中文解释什么是 Agent")
print(res.content)
```

你真正要练的 4 个小项目：

1. **计算器 Agent**：模型自动调用加减乘除函数。
2. **文件助手 Agent**：读取本地 txt/md 文件并总结。
3. **RAG 问答 Agent**：把 PDF/Markdown 放进向量库后问答。
4. **代码助手 Agent**：读取一个 Python 文件，解释 bug，并建议修改。

一句话：

**LangChain 是“工具箱”，LangGraph 是“流程控制器”。**

你先学 LangChain 的工具调用，再学 LangGraph，会顺很多。
