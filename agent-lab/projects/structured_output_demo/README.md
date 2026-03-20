# structured_output_demo

最小可运行的结构化输出示例。

这个样例解决的问题是：

- 输入一句自然语言需求
- 调用模型
- 稳定输出结构化 JSON

它适合作为 `chat_cli` 之后的第二个样例，因为这一阶段要重点学会：

- 让模型按固定结构返回结果
- 用代码校验结果
- 为后面的 Tool Calling 和 Agent 工作流打基础

如果按日本现场和案件要求来看，这个样例也很关键，因为很多企业应用真正需要的不是“聊天”，而是：

- 稳定 JSON 输出
- 稳定分类结果
- 稳定任务清单
- 能接后端 API 的结构化数据

## 1. 前置条件

- Python 3.10+
- 已安装依赖
- 已配置 `OPENAI_API_KEY`

## 2. 安装依赖

```bash
pip install -r requirements.txt
```

## 3. 配置环境变量

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your_api_key"
```

Windows CMD:

```cmd
set OPENAI_API_KEY=your_api_key
```

macOS / Linux:

```bash
export OPENAI_API_KEY="your_api_key"
```

## 4. 运行方式

```bash
python main.py "做一个读取本地 Markdown 并输出摘要的 agent"
```

指定模型：

```bash
python main.py --model gpt-4o "帮我做一个带搜索功能的知识库 agent"
```

## 5. 输出内容

程序会输出两部分：

1. pretty JSON
2. 原始 JSON 字符串

结构包括：

- `goal`
- `user_type`
- `core_capabilities`
- `tools`
- `deliverables`
- `risks`

## 6. 代码说明

- 使用官方 `openai` Python SDK
- 使用 `Responses API`
- 使用 `responses.parse`
- 使用 `Pydantic` 做结构定义和结果校验

## 7. 下一步建议

这个样例跑通后，下一步最适合继续做：

1. 把输出结果写入文件
2. 把输出结果接到 `RAG` 或 API
3. 再把结构化结果接到 Tool Calling
