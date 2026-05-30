Doc QA Agent — 学习说明与快速上手

目的
- 本地文档问答（RAG PoC）：从本地目录读取文档、切分 chunk、基于关键词检索并构造上下文回答。

快速运行
1. Mock 模式（无需 API Key）:
   RAG_API_MOCK=1 python3 main.py --question "项目简介是什么"
2. Real 模式（需 `OPENAI_API_KEY`）:
   OPENAI_API_KEY=sk... python3 main.py --question "如何部署"

关键函数
- `build_chunks()`：从文件构建带来源的 chunk 列表。
- `retrieve()`：基于关键词重合度检索 top-k。
- `answer_question()`：将检索上下文发送给模型并返回答案（或 mock）。

学习建议
- 用小数据集尝试不同 `CHUNK_SIZE`，观察检索效果变化。
- 将关键词检索替换为 embeddings + 向量检索作为扩展练习。
