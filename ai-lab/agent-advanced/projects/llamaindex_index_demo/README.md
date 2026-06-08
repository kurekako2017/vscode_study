# llamaindex_index_demo

这是一个 LlamaIndex 风格的概念 demo。

说明一下：这里没有依赖真实 `llama_index` 包，而是用纯 Python 先把 LlamaIndex 的核心概念跑通：

- Document
- Node
- Index
- QueryEngine
- ResponseSynthesizer

## 安装

这个 demo 只用 Python 标准库，不需要额外安装第三方包。

如需统一查看环境要求，可参考 [项目依赖总表](../DEPENDENCIES.md)。

## 运行

```bash
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/llamaindex_index_demo/main.py "LlamaIndex 和 LangChain 有什么区别？"
```

## 常见报错

- 如果文档目录里没有 `.md` 文件，先确认 `assets/` 下的示例文档是否还在。
- 如果输出为空，通常是查询词没命中文档内容，可以换一个更接近示例主题的问题。

## 学习点

1. `split_into_nodes()` 看文档怎么拆成节点
2. `build_inverted_index()` 看索引怎么建
3. `retrieve()` 看查询怎么召回
4. `synthesize_answer()` 看答案怎么组织
