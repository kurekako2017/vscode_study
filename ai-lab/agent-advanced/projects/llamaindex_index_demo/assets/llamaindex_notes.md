# LlamaIndex-style Notes

LlamaIndex 的核心思路是：

1. 把文档切成 node
2. 给 node 建索引
3. 用 query engine 查询
4. 用 response synthesizer 组织答案

## 适合的场景

- 文档型知识库
- 有明确 source 的回答
- 需要把“数据接入层”和“查询层”拆开

## 和 LangChain 的差别

- LangChain 更偏“编排”和“工具链”
- LlamaIndex 更偏“索引”和“查询”
