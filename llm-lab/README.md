# LLM Lab

面向日本 IT 现场与派遣案件需求的 `LLM 应用开发` 学习资料目录。

这条线的重点不是先学复杂 Agent，而是先建立更常见、更容易落地、也更容易对应岗位要求的能力：

- 模型调用
- Prompt
- 结构化输出
- `RAG / 社内検索`
- `FastAPI` 后端整合
- 云平台对接
- 评估与运维

`agent-lab/` 保留为进阶专题，重点放在：

- Tool Calling
- 单 Agent
- 多 Agent
- 工作流

## 建议学习顺序

1. [00-Python学习范围（面向LLM应用开发）.md](D:/dev/source_code/vscode_study/llm-lab/00-Python%E5%AD%A6%E4%B9%A0%E8%8C%83%E5%9B%B4%EF%BC%88%E9%9D%A2%E5%90%91LLM%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91%EF%BC%89.md)
2. [01-学习路线.md](D:/dev/source_code/vscode_study/llm-lab/01-%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)
3. [02-模型调用基础.md](D:/dev/source_code/vscode_study/llm-lab/02-%E6%A8%A1%E5%9E%8B%E8%B0%83%E7%94%A8%E5%9F%BA%E7%A1%80.md)
4. [03-结构化输出.md](D:/dev/source_code/vscode_study/llm-lab/03-%E7%BB%93%E6%9E%84%E5%8C%96%E8%BE%93%E5%87%BA.md)
5. [04-RAG.md](D:/dev/source_code/vscode_study/llm-lab/04-RAG.md)
6. [05-FastAPI与企业集成.md](D:/dev/source_code/vscode_study/llm-lab/05-FastAPI%E4%B8%8E%E4%BC%81%E4%B8%9A%E9%9B%86%E6%88%90.md)
7. [06-评估与运维.md](D:/dev/source_code/vscode_study/llm-lab/06-%E8%AF%84%E4%BC%B0%E4%B8%8E%E8%BF%90%E7%BB%B4.md)
8. [07-日本现场应用与案件关键词.md](D:/dev/source_code/vscode_study/llm-lab/07-%E6%97%A5%E6%9C%AC%E7%8E%B0%E5%9C%BA%E5%BA%94%E7%94%A8%E4%B8%8E%E6%A1%88%E4%BB%B6%E5%85%B3%E9%94%AE%E8%AF%8D.md)
9. [08-云平台与企业环境.md](D:/dev/source_code/vscode_study/llm-lab/08-%E4%BA%91%E5%B9%B3%E5%8F%B0%E4%B8%8E%E4%BC%81%E4%B8%9A%E7%8E%AF%E5%A2%83.md)
10. [09-岗位与技能要求对照.md](D:/dev/source_code/vscode_study/llm-lab/09-%E5%B2%97%E4%BD%8D%E4%B8%8E%E6%8A%80%E8%83%BD%E8%A6%81%E6%B1%82%E5%AF%B9%E7%85%A7.md)
11. [10-作品集与面试准备.md](D:/dev/source_code/vscode_study/llm-lab/10-%E4%BD%9C%E5%93%81%E9%9B%86%E4%B8%8E%E9%9D%A2%E8%AF%95%E5%87%86%E5%A4%87.md)

## 推荐输出物

- `chat_cli`
- `structured_output_demo`
- `doc_qa_agent`
- `rag_api_demo`
- `rag_eval_notes`
- `enterprise_integration_notes`

## 适合人群

- 想按日本现场需求学习生成 AI 的工程师
- 想找 `Python + RAG + FastAPI` 相关案件的人
- 已经会一点大模型调用，但不会做实际应用的人
- 想从 `LLM 应用开发` 进阶到 `Agent 开发` 的学习者

## 和 `agent-lab` 的关系

- `llm-lab`：主线，偏实际落地
- `agent-lab`：进阶，偏自动化执行与工作流

如果你的目标是日本现场和派遣案件，建议先学 `llm-lab`，再学 `agent-lab`。

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
|-- 08-云平台与企业环境.md
|-- 09-岗位与技能要求对照.md
|-- 10-作品集与面试准备.md
`-- projects/
    `-- README.md
```
