# rag

这个目录放高级 RAG 专题。

这里主要是方法论和拆解文档，对应的可运行代码在：

- [projects/advanced_rag_pipeline_demo](../projects/advanced_rag_pipeline_demo/README.md)
- [projects/internal_hybrid_rag_demo](../projects/internal_hybrid_rag_demo/README.md)

建议拆成这些部分：

- 文档切分
- 索引构建
- 检索策略
- rerank
- query rewrite
- multi-query
- 引用来源展示
- 评估与调优
- 社内文件与 Wiki 混合检索

## 业务场景说明

- 适用场景：知识库很大、资料来源多、且回答需要引用和可追溯性时。
- 如果不用这种方式：简单检索容易答偏，资料更新后也更难控制答案质量。
- 解决的问题：把 RAG 的方法论拆成切分、检索、重排、引用、评估等部分，便于在真实项目里逐步落地。
