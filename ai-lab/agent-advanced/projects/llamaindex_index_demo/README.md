# llamaindex_index_demo

这是一个 LlamaIndex 风格的概念 demo。

说明一下：这里没有依赖真实 `llama_index` 包，而是用纯 Python 先把 LlamaIndex 的核心概念跑通：

- Document
- Node
- Index
- QueryEngine
- ResponseSynthesizer

## 运行

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/llamaindex_index_demo
python3 main.py "LlamaIndex 和 LangChain 有什么区别？"
```

## 学习点

1. `split_into_nodes()` 看文档怎么拆成节点
2. `build_inverted_index()` 看索引怎么建
3. `retrieve()` 看查询怎么召回
4. `synthesize_answer()` 看答案怎么组织
