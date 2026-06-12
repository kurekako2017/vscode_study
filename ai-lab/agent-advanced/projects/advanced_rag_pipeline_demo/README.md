# advanced_rag_pipeline_demo

这是一个“高级 RAG 流水线”的最小可运行 demo。

你会看到完整的链路：

1. 加载文档
2. 切分 chunk
3. query rewrite
4. 检索
5. rerank
6. 带引用的回答

## 业务场景说明

- 谁会用：已经理解基础 RAG，准备继续学习查询改写、结果重排和来源引用的开发人员。
- 现实中的问题：员工询问“系统发布失败后怎么恢复”，文档里可能写的是“部署异常”“回滚步骤”或“故障恢复”。只按原问题检索，可能漏掉意思相关但用词不同的内容。
- 这个例子怎么解决：先加载并切分文档，再用 `rewrite_queries()` 生成多种查询表达，`retrieve()` 找候选片段，`rerank()` 调整排序，最后 `synthesize_answer()` 根据靠前片段生成带来源的回答。
- 现实例子：运维人员询问“上线后服务起不来怎么办”，程序会同时考虑“部署失败”“启动异常”“回滚”等相关表达，重新排列搜索结果，并指出建议来自哪份操作文档。
- 初学者重点：这个项目用本地样本文档和可观察的评分逻辑讲解高级 RAG 流程，重点是看清每一步如何影响结果，不等同于生产环境的向量库和专业 rerank 模型。

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
