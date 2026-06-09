Doc QA Agent — 学习说明与快速上手

目的
- 本地文档问答（RAG PoC）：从本地目录读取文档、切分 chunk、基于关键词检索并构造上下文回答。

业务场景说明
- 适用场景：本地知识库、项目文档、制度手册、FAQ 等需要“基于资料回答”的场景。
- 如果不用这种方式：模型会缺少上下文，只能猜测答案，面对内部资料时很容易失真。
- 解决的问题：把文档检索和模型回答连起来，并用来源约束答案范围，方便做 PoC 和小范围落地。
- 举例说明：例如先用一份很短的制度文档测试“检索 -> 摘要 -> 引用来源”的最小链路。

快速运行
1. Mock 模式（无需 API Key）:
   ```bash
   RAG_API_MOCK=1 python3 main.py --question "项目简介是什么"
   ```
2. Real 模式（需 `OPENAI_API_KEY`）:
   ```bash
   OPENAI_API_KEY=sk... python3 main.py --question "如何部署"
   ```

关键函数
- `build_chunks()`：从文件构建带来源的 chunk 列表。
- `retrieve()`：基于关键词重合度检索 top-k。
- `answer_question()`：将检索上下文发送给模型并返回答案（或 mock）。

学习建议
- 用小数据集尝试不同 `CHUNK_SIZE`，观察检索效果变化。
- 将关键词检索替换为 embeddings + 向量检索作为扩展练习。
