# LLM Lab

面向日本 IT 现场与派遣案件需求的 `LLM 应用开发` 学习资料目录。

这条线的重点不是先学复杂 Agent，而是先建立更常见、更容易落地、也更容易对应岗位要求的能力：

- 模型调用
- 结构化输出
- `RAG / 社内検索`
- `FastAPI` 后端整合
- 评估与运维
- 企业环境与岗位对照

`agent-lab/` 保留为进阶专题，重点放在：

- Tool Calling
- 单 Agent
- 多 Agent
- 工作流

如果你的目标是：

- 学 `Python + RAG + FastAPI`
- 贴近日本现场和派遣案件
- 先做可交付 PoC，再学 Agent

那么先走 `llm-lab/` 这条主线更合适。

## 快速入口

如果你现在只想知道“应该先点哪几个文件”，直接按这个顺序：

1. [LLM应用框架系统知识.md](./LLM应用框架系统知识.md)
2. [00-Python学习范围（面向LLM应用开发）.md](./00-Python学习范围（面向LLM应用开发）.md)
3. [01-学习路线.md](./01-学习路线.md)
4. [02-模型调用基础.md](./02-模型调用基础.md)
5. [03-结构化输出.md](./03-结构化输出.md)
6. [04-RAG.md](./04-RAG.md)

## 先理解的系统知识

如果你觉得“模型、RAG、角色、Prompt、Embedding、结构化输出、评估”这些词有点散，先看：

- [LLM应用框架系统知识.md](./LLM应用框架系统知识.md)
- [术语速查表.md](./术语速查表.md)

这份文档补充了：

- LLM 应用的系统分层
- 每个角色是什么、作用是什么
- 常见术语的概念性解释
- 最小 LLM 应用数据流
- RAG 应用数据流
- 各教程在系统中的位置

## 这套资料怎么用

这套资料不是按“技术百科”写的，而是按“学习主线”组织的。

建议按下面这个方式使用：

1. 先看一篇教程文档
2. 再跑对应 demo
3. 再自己改一版
4. 再进入下一篇

也就是说，正确用法不是：

- 把所有文档从头读到尾

而是：

- 文档和示例交替学习

## 主线结论

如果只记一条主线，记这个就够了：

- `Python -> 模型调用 -> 结构化输出 -> RAG -> FastAPI -> 评估 -> 日本现场对照 -> Agent`

对应的学习原则是：

- 先做日本现场更常见的应用
- 先做 `RAG + FastAPI`
- 先会把能力服务化
- 先会评估
- 再进入 Agent 进阶

## 推荐学习顺序

1. [LLM应用框架系统知识.md](./LLM应用框架系统知识.md)
2. [00-Python学习范围（面向LLM应用开发）.md](D:/dev/source_code/vscode_study/llm-lab/00-Python%E5%AD%A6%E4%B9%A0%E8%8C%83%E5%9B%B4%EF%BC%88%E9%9D%A2%E5%90%91LLM%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91%EF%BC%89.md)
3. [01-学习路线.md](D:/dev/source_code/vscode_study/llm-lab/01-%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)
4. [02-模型调用基础.md](D:/dev/source_code/vscode_study/llm-lab/02-%E6%A8%A1%E5%9E%8B%E8%B0%83%E7%94%A8%E5%9F%BA%E7%A1%80.md)
5. [03-结构化输出.md](D:/dev/source_code/vscode_study/llm-lab/03-%E7%BB%93%E6%9E%84%E5%8C%96%E8%BE%93%E5%87%BA.md)
6. [04-RAG.md](D:/dev/source_code/vscode_study/llm-lab/04-RAG.md)
6. [05-FastAPI与企业集成.md](D:/dev/source_code/vscode_study/llm-lab/05-FastAPI%E4%B8%8E%E4%BC%81%E4%B8%9A%E9%9B%86%E6%88%90.md)
7. [06-评估与运维.md](D:/dev/source_code/vscode_study/llm-lab/06-%E8%AF%84%E4%BC%B0%E4%B8%8E%E8%BF%90%E7%BB%B4.md)
8. [07-日本现场应用与案件关键词.md](D:/dev/source_code/vscode_study/llm-lab/07-%E6%97%A5%E6%9C%AC%E7%8E%B0%E5%9C%BA%E5%BA%94%E7%94%A8%E4%B8%8E%E6%A1%88%E4%BB%B6%E5%85%B3%E9%94%AE%E8%AF%8D.md)
9. [08-云平台与企业环境.md](D:/dev/source_code/vscode_study/llm-lab/08-%E4%BA%91%E5%B9%B3%E5%8F%B0%E4%B8%8E%E4%BC%81%E4%B8%9A%E7%8E%AF%E5%A2%83.md)
10. [09-岗位与技能要求对照.md](D:/dev/source_code/vscode_study/llm-lab/09-%E5%B2%97%E4%BD%8D%E4%B8%8E%E6%8A%80%E8%83%BD%E8%A6%81%E6%B1%82%E5%AF%B9%E7%85%A7.md)
11. [10-作品集与面试准备.md](D:/dev/source_code/vscode_study/llm-lab/10-%E4%BD%9C%E5%93%81%E9%9B%86%E4%B8%8E%E9%9D%A2%E8%AF%95%E5%87%86%E5%A4%87.md)

## 每一篇是干什么的

### 起步阶段

- [00-Python学习范围（面向LLM应用开发）.md](D:/dev/source_code/vscode_study/llm-lab/00-Python%E5%AD%A6%E4%B9%A0%E8%8C%83%E5%9B%B4%EF%BC%88%E9%9D%A2%E5%90%91LLM%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91%EF%BC%89.md)
  - 解决“先学什么、暂时不用学什么、为什么先学 Python 后补 TypeScript”
- [01-学习路线.md](D:/dev/source_code/vscode_study/llm-lab/01-%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)
  - 给出 `8 周执行路线` 和整个主线顺序

### 技术主线

- [02-模型调用基础.md](D:/dev/source_code/vscode_study/llm-lab/02-%E6%A8%A1%E5%9E%8B%E8%B0%83%E7%94%A8%E5%9F%BA%E7%A1%80.md)
  - 学最小模型调用、命令行运行、异常处理
- [03-结构化输出.md](D:/dev/source_code/vscode_study/llm-lab/03-%E7%BB%93%E6%9E%84%E5%8C%96%E8%BE%93%E5%87%BA.md)
  - 学 `Pydantic`、schema、稳定 JSON 输出
- [04-RAG.md](D:/dev/source_code/vscode_study/llm-lab/04-RAG.md)
  - 学文档读取、切分、检索、来源返回
- [05-FastAPI与企业集成.md](D:/dev/source_code/vscode_study/llm-lab/05-FastAPI%E4%B8%8E%E4%BC%81%E4%B8%9A%E9%9B%86%E6%88%90.md)
  - 学 API 化、请求响应结构、服务化
- [06-评估与运维.md](D:/dev/source_code/vscode_study/llm-lab/06-%E8%AF%84%E4%BC%B0%E4%B8%8E%E8%BF%90%E7%BB%B4.md)
  - 学评估表、失败案例、测试观点、成本和延迟意识

### 现场与求职主线

- [07-日本现场应用与案件关键词.md](D:/dev/source_code/vscode_study/llm-lab/07-%E6%97%A5%E6%9C%AC%E7%8E%B0%E5%9C%BA%E5%BA%94%E7%94%A8%E4%B8%8E%E6%A1%88%E4%BB%B6%E5%85%B3%E9%94%AE%E8%AF%8D.md)
  - 学日本现场更常见的应用形态和 `Agent` 的真实位置
- [08-云平台与企业环境.md](D:/dev/source_code/vscode_study/llm-lab/08-%E4%BA%91%E5%B9%B3%E5%8F%B0%E4%B8%8E%E4%BC%81%E4%B8%9A%E7%8E%AF%E5%A2%83.md)
  - 学企业环境里常见的云平台、权限、网络、成本意识
- [09-岗位与技能要求对照.md](D:/dev/source_code/vscode_study/llm-lab/09-%E5%B2%97%E4%BD%8D%E4%B8%8E%E6%8A%80%E8%83%BD%E8%A6%81%E6%B1%82%E5%AF%B9%E7%85%A7.md)
  - 学岗位关键词、学习内容和作品表达怎么对上
- [10-作品集与面试准备.md](D:/dev/source_code/vscode_study/llm-lab/10-%E4%BD%9C%E5%93%81%E9%9B%86%E4%B8%8E%E9%9D%A2%E8%AF%95%E5%87%86%E5%A4%87.md)
  - 学如何把 demo 讲成作品集和 PoC 输出物

## 文档和 demo 的对应关系

| 学习主题 | 教程文档 | 对应 demo / 资料 |
|---|---|---|
| 模型调用 | [02-模型调用基础.md](D:/dev/source_code/vscode_study/llm-lab/02-%E6%A8%A1%E5%9E%8B%E8%B0%83%E7%94%A8%E5%9F%BA%E7%A1%80.md) | [chat_cli](D:/dev/source_code/vscode_study/agent-lab/projects/chat_cli/README.md) |
| 结构化输出 | [03-结构化输出.md](D:/dev/source_code/vscode_study/llm-lab/03-%E7%BB%93%E6%9E%84%E5%8C%96%E8%BE%93%E5%87%BA.md) | [structured_output_demo](D:/dev/source_code/vscode_study/agent-lab/projects/structured_output_demo/README.md) |
| `RAG` | [04-RAG.md](D:/dev/source_code/vscode_study/llm-lab/04-RAG.md) | [doc_qa_agent](D:/dev/source_code/vscode_study/agent-lab/projects/doc_qa_agent/README.md) |
| `FastAPI + RAG API` | [05-FastAPI与企业集成.md](D:/dev/source_code/vscode_study/llm-lab/05-FastAPI%E4%B8%8E%E4%BC%81%E4%B8%9A%E9%9B%86%E6%88%90.md) | [rag_api_demo](D:/dev/source_code/vscode_study/agent-lab/projects/rag_api_demo/README.md) |
| 评估与运维 | [06-评估与运维.md](D:/dev/source_code/vscode_study/llm-lab/06-%E8%AF%84%E4%BC%B0%E4%B8%8E%E8%BF%90%E7%BB%B4.md) | [rag_eval_notes.md](D:/dev/source_code/vscode_study/llm-lab/projects/rag_eval_notes.md) |

## 推荐输出物

如果按日本现场和作品集准备来做，最值得优先产出的输出物是：

- `chat_cli`
- `structured_output_demo`
- `doc_qa_agent`
- `rag_api_demo`
- `rag_eval_notes`

其中最值得优先打磨的是：

- `doc_qa_agent`
- `rag_api_demo`

因为这两个最贴：

- `RAG`
- `社内検索`
- `FastAPI`
- `API連携`
- 生成 AI 后端 `PoC`

## 如果你现在刚开始

如果你现在是第一次进入这套资料，推荐直接这样开始：

1. 先看 [00-Python学习范围（面向LLM应用开发）.md](D:/dev/source_code/vscode_study/llm-lab/00-Python%E5%AD%A6%E4%B9%A0%E8%8C%83%E5%9B%B4%EF%BC%88%E9%9D%A2%E5%90%91LLM%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91%EF%BC%89.md)
2. 再看 [01-学习路线.md](D:/dev/source_code/vscode_study/llm-lab/01-%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)
3. 跑 [chat_cli](D:/dev/source_code/vscode_study/agent-lab/projects/chat_cli/README.md)
4. 再进入 [02-模型调用基础.md](D:/dev/source_code/vscode_study/llm-lab/02-%E6%A8%A1%E5%9E%8B%E8%B0%83%E7%94%A8%E5%9F%BA%E7%A1%80.md)

如果你已经会基础模型调用，建议直接从这里继续：

1. [03-结构化输出.md](D:/dev/source_code/vscode_study/llm-lab/03-%E7%BB%93%E6%9E%84%E5%8C%96%E8%BE%93%E5%87%BA.md)
2. [04-RAG.md](D:/dev/source_code/vscode_study/llm-lab/04-RAG.md)
3. [05-FastAPI与企业集成.md](D:/dev/source_code/vscode_study/llm-lab/05-FastAPI%E4%B8%8E%E4%BC%81%E4%B8%9A%E9%9B%86%E6%88%90.md)

## 适合人群

- 想按日本现场需求学习生成 AI 的工程师
- 想找 `Python + RAG + FastAPI` 相关案件的人
- 已经会一点大模型调用，但不会做实际应用的人
- 想从 `LLM 应用开发` 进阶到 `Agent 开发` 的学习者

## 和 `agent-lab` 的关系

- `llm-lab`
  - 主线，偏实际落地
- `agent-lab`
  - 进阶，偏自动化执行与工作流

如果你的目标是日本现场和派遣案件，建议先学 `llm-lab`，再学 `agent-lab`。

更具体一点说：

- 先把 `模型调用 + 结构化输出 + RAG + FastAPI + 评估` 打牢
- 再进入 Tool Calling、Workflow、Agent

## 目录结构

```text
llm-lab/
|-- README.md
|-- 00-Python学习范围（面向LLM应用开发）.md
|-- 01-学习路线.md
|-- 02-模型调用基础.md
|-- 03-结构化输出.md
|-- 04-RAG.md
|-- 05-FastAPI与企业集成.md
|-- 06-评估与运维.md
|-- 07-日本现场应用与案件关键词.md

## 示例代码位置与快速运行

- 说明：本仓库的可运行 demo 全部放在 `agent-lab/projects/`，`llm-lab` 只保留主线文档和评估资料以减少重复维护。

- 主要 demo 路径（工作区相对路径）：
  - [agent-lab/projects/chat_cli/README.md](agent-lab/projects/chat_cli/README.md)
  - [agent-lab/projects/structured_output_demo/README.md](agent-lab/projects/structured_output_demo/README.md)
  - [agent-lab/projects/doc_qa_agent/README.md](agent-lab/projects/doc_qa_agent/README.md)
  - [agent-lab/projects/rag_api_demo/README.md](agent-lab/projects/rag_api_demo/README.md)

- 快速运行（示例以 `chat_cli` 为例）：

PowerShell:
```
cd d:\dev\source_code\vscode_study\agent-lab\projects\chat_cli
pip install -r requirements.txt
$env:OPENAI_API_KEY="your_api_key"
python main.py "用一句话解释什么是 agent"
```

macOS / Linux:
```
cd llm-lab/projects/chat_cli  # 或到 agent-lab/projects/chat_cli
pip install -r requirements.txt
export OPENAI_API_KEY="your_api_key"
python main.py "用一句话解释什么是 agent"
```

- 如果你希望把某个 demo 的副本放到 `llm-lab/projects`（便于修改或离线修改），可以复制整个目录：

PowerShell:
```
mkdir llm-lab\projects\chat_cli
Copy-Item -Path agent-lab\projects\chat_cli\* -Destination llm-lab\projects\chat_cli -Recurse
```

macOS / Linux:
```
mkdir -p llm-lab/projects/chat_cli
cp -r agent-lab/projects/chat_cli/* llm-lab/projects/chat_cli/
```

（复制后请在 `llm-lab/projects/chat_cli` 下按 README 运行示例）
|-- 08-云平台与企业环境.md
|-- 09-岗位与技能要求对照.md
|-- 10-作品集与面试准备.md
`-- projects/
    |-- README.md
    `-- rag_eval_notes.md
```
