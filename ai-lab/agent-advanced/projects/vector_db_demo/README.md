# vector_db_demo

这是一个“向量数据库最小教学版” demo。

它不是在真实 Qdrant / Chroma 服务上跑，而是用纯 Python 先把向量数据库最核心的流程讲清楚：

- 文本切分
- 文本向量化
- 写入 collection
- 相似度检索
- 返回 top-k 结果

## 业务场景说明

- 适用场景：文档很多、问题需要语义匹配、不能只靠关键词检索时。
- 如果不用这种方式：你只能做字符串包含匹配，问题换个说法就搜不到，召回质量会很差。
- 解决的问题：把文本转成向量后做相似度检索，让“意思接近”的内容也能被召回。
- 举例说明：例如把“报销流程”“出差申请”“远程办公”分别写入 collection，再问“我怎么申请出差费用”，看能否召回和报销相关的内容。

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
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/vector_db_demo/main.py "怎么申请出差报销？"
```

可选参数：

- `--backend qdrant`
- `--backend chroma`
- `--backend memory`
- `--top-k 3`

例如：

```bash
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/vector_db_demo/main.py "远程办公怎么申请？" --backend chroma --top-k 2
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
- 如果你想改成真实 Qdrant / Chroma，下一步就是把 `MemoryVectorDB` 替换成真实客户端。

## 学习点

1. `load_documents()` 看样本文档怎么加载
2. `embed_text()` 看文本如何转成向量
3. `upsert()` 看文档如何写入 collection
4. `search()` 看相似度检索如何返回 top-k
