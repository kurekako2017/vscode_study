# advanced_rag_pipeline_demo

这是一个“高级 RAG 流水线”的最小可运行 demo。

你会看到完整的链路：

1. 加载文档
2. 切分 chunk
3. query rewrite
4. 检索
5. rerank
6. 带引用的回答

## 运行

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/advanced_rag_pipeline_demo
python3 main.py "LangGraph 适合什么场景，RAG 怎么做引用和重排？"
```

## 学习点

- `load_documents()`：文档输入
- `chunk_documents()`：切分
- `rewrite_queries()`：查询改写
- `retrieve()`：召回
- `rerank()`：重排
- `synthesize_answer()`：引用型回答
