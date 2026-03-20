# Agent Lab

面向日本 IT 现场与派遣案件需求的 `Agent 开发` 进阶学习资料目录。

这条线不是主入口，而是建立在 `llm-lab/` 之后的进阶专题。

如果你的目标是日本现场和派遣案件，建议顺序是：

1. 先学 [llm-lab/README.md](D:/dev/source_code/vscode_study/llm-lab/README.md)
2. 再学 [agent-lab/README.md](D:/dev/source_code/vscode_study/agent-lab/README.md)

## 目标

这条学习线的目标是逐步建立：

- Tool Calling 能力
- Agent 工作流设计能力
- 评估与上线意识

这里默认你已经具备这些前置基础：

- 模型调用
- 结构化输出
- `RAG`
- Python 后端集成

## 建议学习顺序

1. [01-学习路线.md](D:/dev/source_code/vscode_study/agent-lab/01-%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)
2. [02-模型调用基础.md](D:/dev/source_code/vscode_study/agent-lab/02-%E6%A8%A1%E5%9E%8B%E8%B0%83%E7%94%A8%E5%9F%BA%E7%A1%80.md)
3. [04-RAG.md](D:/dev/source_code/vscode_study/agent-lab/04-RAG.md)
4. [03-Tool%20Calling.md](D:/dev/source_code/vscode_study/agent-lab/03-Tool%20Calling.md)
5. [05-Agent工作流.md](D:/dev/source_code/vscode_study/agent-lab/05-Agent%E5%B7%A5%E4%BD%9C%E6%B5%81.md)

## 推荐输出物

- `chat_cli`
- `structured_output_demo`
- `doc_qa_agent`
- `rag_api_demo`
- `tool_agent_demo`
- `workflow_agent`

## `agent-lab` 和 `llm-lab` 的区别

`agent-lab` 更聚焦让模型完成任务的系统，重点会放在：

- `Tool Calling`
- `RAG + tools`
- 工作流
- 单 Agent / 多 Agent
- 自动化执行

`llm-lab` 的范围会更宽，除了 Agent 之外，通常还会包含：

- 模型调用基础
- Prompt
- 结构化输出
- Embedding
- RAG
- Eval
- Fine-tuning
- Agent

所以当前这个目录命名成 `agent-lab` 是更合适的，因为这条线的目标是从“调用模型”一路走到“可执行任务的 Agent”。

如果后面内容继续扩展到更广的 LLM 主题，也可以再把 `agent-lab` 作为 `llm-lab` 里的一个子目录。

## 日本现场更常见的 LLM 应用形态

按目前日本企业的实际落地节奏看，最常见的并不是一开始就做强自治的通用 Agent，而是先从更稳、更容易落地的形态开始。

### 现在更常见的落地方向

- 社内问答
- 社内搜索
- `RAG` 知识库问答
- 会议纪要、摘要、翻译、邮件草拟
- 面向特定流程的业务助手

也就是说，日本现场更常见的是：

- 先做“会回答的助手”
- 再做“会查资料的助手”
- 再做“会调用工具的半自动 Agent”
- 最后才逐步走向更强的 Agent 化系统

### 为什么会这样

主要原因通常是：

- 企业更重视准确性和可控性
- 社内文档和规程是最容易先接入的资产
- `RAG` 比全自动 Agent 更容易控制风险
- 业务系统里很多流程仍然需要人工确认

## 日本派遣案件更常出现的关键词

如果是按案件和职位要求来学，当前更高频的关键词通常是：

- `Python`
- `TypeScript`
- `RAG`
- `LangChain`
- `LlamaIndex`
- `Azure OpenAI`
- `AWS Bedrock`
- `FastAPI`
- `社内検索`
- `生成AIアプリ`

相比之下，复杂的多 Agent 设计往往不是最先要求的核心能力。

## 学习顺序上的建议

如果你的目标是贴近日本企业现场和派遣案件，Agent 更适合作为下面这些能力之后的下一步：

1. 模型调用
2. 结构化输出
3. `RAG / 社内検索`
4. Python 后端整合
5. 再进入 `Tool Calling` 和 Agent

## 资料判断说明

这个判断主要基于近年的日本企业生成 AI 公开案例和案件趋势整理：

- 社内検索 / RAG 类应用明显更多
- Agent 型 AI 正在升温，但整体还在扩大阶段
- 大企业和 IT 厂商已经开始推进 Agent，但普及度还不如 RAG 与 Copilot 型场景
- 派遣 / 业委案件里，`Python + RAG + 云平台` 的组合更常见

可参考这些资料：

- ITmedia AI+: https://www.itmedia.co.jp/aiplus/articles/2510/07/news063.html
- SO Technologies: https://www.so-tech.co.jp/news/press-release/664
- MONOist: https://monoist.itmedia.co.jp/mn/articles/2501/09/news092.html
- マイナビ TECH+: https://news.mynavi.jp/techplus/article/20250912-3451630/
- ITmedia Enterprise: https://www.itmedia.co.jp/enterprise/articles/2509/18/news027.html
- CrowdWorks 案件: https://crowdworks.jp/public/jobs/12935631
- ベスキャリIT 案件: https://www.bscareer-it.jp/project/35438

## 目录结构

```text
agent-lab/
|-- README.md
|-- 01-学习路线.md
|-- 02-模型调用基础.md
|-- 03-Tool Calling.md
|-- 04-RAG.md
|-- 05-Agent工作流.md
`-- projects/
    |-- chat_cli/
    |   |-- README.md
    |   |-- main.py
    |   `-- requirements.txt
    |-- doc_qa_agent/
    |   |-- README.md
    |   |-- main.py
    |   `-- requirements.txt
    |-- rag_api_demo/
    |   |-- README.md
    |   |-- main.py
    |   `-- requirements.txt
    |-- structured_output_demo/
    |   |-- README.md
    |   |-- main.py
    |   `-- requirements.txt
    `-- tool_agent_demo/
        |-- README.md
        |-- main.py
        `-- requirements.txt
```

## 使用建议

- 每读完一篇，至少做一个最小 demo。
- 不要只看框架名，优先自己把最基本的流程写通。
- 每个阶段都保留代码、文档和问题记录。
- 如果你的目标是找日本现场案件，作品集优先做 `RAG + Python + 企业资料检索`，Agent 放在后续进阶展示。
