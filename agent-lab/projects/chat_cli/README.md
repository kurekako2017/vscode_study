# chat_cli

最小可运行的大模型命令行对话示例。

这个样例只做一件事：

- 从命令行读取用户输入
- 调用模型
- 把回答打印到终端

它故意保持简单，目的是给后面的：

- 结构化输出
- Tool Calling
- RAG
- Agent 工作流

做基础。

如果按日本现场和派遣案件来看，这个样例对应的是最基础的“会调模型 API”能力，本身还不构成项目交付物，但它是后面做 `RAG` 和业务接口整合的起点。

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

直接传入一句话：

```bash
python main.py "用一句话解释什么是 agent"
```

进入交互模式：

```bash
python main.py
```

指定模型：

```bash
python main.py --model gpt-5 "给我一个三步学习计划"
```

## 5. 代码说明

- 使用官方 `openai` Python SDK
- 使用官方推荐的 `Responses API`
- 默认从 `OPENAI_API_KEY` 读取密钥
- 默认模型为 `gpt-5`

## 6. 下一步建议

这个样例跑通后，下一步最适合继续做：

1. 增加 JSON 结构化输出
2. 做需求整理或摘要输出
3. 再进入 `RAG` 或本地资料问答
