# vector_db_demo

这是一个“向量数据库最小教学版” demo。

它不是在真实 Qdrant / Chroma 服务上跑，而是用纯 Python 先把向量数据库最核心的流程讲清楚：

- 文本切分
- 文本向量化
- 写入 collection
- 相似度检索
- 返回 top-k 结果

## 业务场景说明

- 谁会用：第一次学习向量、collection、metadata 和相似度搜索的开发人员。
- 现实中的问题：制度文档里写的是“差旅费用精算”，员工搜索的是“出差怎么报销”。只做完全相同的字符串匹配时，表达方式不同就可能找不到相关资料。
- 这个例子怎么解决：把样本文档转换成教学用向量，写入内存中的 collection，再把用户问题也转换成向量，通过余弦相似度返回最接近的 Top-K 文档。
- 现实例子：系统中保存了报销规定、远程办公制度和发布手册。员工询问“出差花的钱如何申请”，搜索结果应该优先返回报销规定，而不是只查找完全相同的文字。
- 初学者重点：这个项目用纯 Python 模拟 Qdrant、Chroma 和内存数据库的使用方式，方便观察原理；它没有连接真实数据库，向量算法也只是教学实现。

## 这个 demo 会演示什么

- `Qdrant` 风格：按 collection 存文档向量和 payload，再做相似度搜索
- `Chroma` 风格：按 collection 名称管理文档、向量和元数据，再做相似度搜索
- `Memory` 风格：不依赖数据库，只在内存里模拟向量检索

## 安装

这个 demo 只用 Python 标准库，不需要额外安装第三方包。

如果你想看整个工作区的统一依赖说明，可以参考：

- [项目依赖总表](../DEPENDENCIES.md)

## 运行方式

```bash
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/ai-learn/agent-advanced/projects/vector_db_demo/main.py "怎么申请出差报销？"
```

可选参数：

- `--backend qdrant`
- `--backend chroma`
- `--backend memory`
- `--top-k 3`

例如：

```bash
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/ai-learn/agent-advanced/projects/vector_db_demo/main.py "远程办公怎么申请？" --backend chroma --top-k 2
```

## 目录结构

```text
vector_db_demo/
├── assets/
│   ├── deployment_faq.md
│   ├── expense_policy.md
│   └── remote_work.md
├── main.py
└── README.md
```

## 你会学到什么

1. 向量数据库为什么比关键词检索更适合语义搜索
2. collection / 文档 / 向量 / metadata 的关系
3. 相似度搜索是怎么工作的
4. Qdrant 风格和 Chroma 风格的数据组织差别

## 常见报错

- 如果结果很乱，通常是样本太少，换一个更接近内容的 query。
- 如果输出为空，先确认你是在 demo 目录下运行，且 `assets/` 没被删。
- 如果你想改成真实 Qdrant / Chroma，下一步可以直接参考：
  - [真实 Qdrant 版骨架](../vector_db_qdrant_demo/README.md)
  - [真实 Chroma 版骨架](../vector_db_chroma_demo/README.md)

## 学习点

1. `load_documents()` 看样本文档怎么加载
2. `embed_text()` 看文本如何转成向量
3. `upsert()` 看文档如何写入 collection
4. `search()` 看相似度检索如何返回 top-k
