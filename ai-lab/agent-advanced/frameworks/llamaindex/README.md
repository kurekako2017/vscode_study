# LlamaIndex

这个章节讲 LlamaIndex 的索引和查询引擎思路。

## 业务场景说明

- 适用场景：文档较多、需要先建索引再查询的知识库、文档检索和问答系统。
- 如果不用这种方式：每次都全量扫文档会慢，而且数据一多就不利于扩展和复用。
- 解决的问题：用索引和查询引擎把文档处理流程标准化，方便组织检索和回答。
- 举例说明：例如先用一批项目文档建索引，再问“报销流程在哪一页提到过”，看看检索和引用效果是否稳定。

## 先看什么

1. Document 如何变成 Node
2. Node 如何进入 Index
3. QueryEngine 如何把检索和回答组织起来

## 对应代码

- [projects/llamaindex_index_demo](../../projects/llamaindex_index_demo/README.md)

## 学习目标

- 看懂索引和节点的关系
- 看懂查询引擎的职责
- 理解 LlamaIndex 在知识库检索里的位置
