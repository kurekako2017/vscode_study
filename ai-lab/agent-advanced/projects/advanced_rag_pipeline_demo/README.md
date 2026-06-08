# advanced_rag_pipeline_demo

这是一个“高级 RAG 流水线”的最小可运行 demo。

你会看到完整的链路：

1. 加载文档
2. 切分 chunk
3. query rewrite
4. 检索
5. rerank
6. 带引用的回答

## 安装

```bash
/usr/bin/python3 -m pip install -r /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/requirements.txt
```

依赖说明见 [项目依赖总表](../DEPENDENCIES.md)。

## 运行

```bash
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/advanced_rag_pipeline_demo/main.py "LangGraph 适合什么场景，RAG 怎么做引用和重排？"
```

默认只打印检索结果和最终回答。如果你想看更多调试信息，可以加上 `--show-stats` 或 `--show-excerpt`：

```bash
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/advanced_rag_pipeline_demo/main.py "LangGraph 适合什么场景，RAG 怎么做引用和重排？" --show-stats --show-excerpt
```

## 常见报错

- `ModuleNotFoundError: No module named 'langchain_core'`：安装统一依赖后再跑。
- `ModuleNotFoundError: No module named 'langchain_text_splitters'`：同样属于依赖未装齐，优先用统一安装命令。

## 学习点

- `load_documents()`：文档输入
- `chunk_documents()`：切分
- `rewrite_queries()`：查询改写
- `retrieve()`：召回
- `rerank()`：重排
- `synthesize_answer()`：引用型回答
