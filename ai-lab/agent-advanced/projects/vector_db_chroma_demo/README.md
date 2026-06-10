# vector_db_chroma_demo

这是一个“真实 Chroma 版骨架” demo。

它和 Qdrant 版的区别是：这里更偏本地持久化和快速原型，适合先把 embedding + collection + query 这条链路跑通。

## 业务场景说明

- 适用场景：你想先在本地快速搭一个可持久化的向量检索 demo，不想一开始就依赖远端服务。
- 如果不用这种方式：每次重启后数据都没了，或者你为了验证一点逻辑就要重新部署整套服务。
- 解决的问题：把向量入库、元数据管理、相似度查询和本地持久化放在一个最小骨架里，适合原型验证。
- 举例说明：例如把报销制度、远程办公和发布 FAQ 存到本地 Chroma，问“远程办公怎么申请”，就能直接查到相关文档。

## 这个 demo 会演示什么

- 真实 Chroma Client 的接入方式
- collection 的创建
- 文档 embedding 写入
- 元数据 metadata 的保存
- query 检索和 top-k 召回

## 前置条件

- 本机能安装 `chromadb`
- 如果你想要真实向量效果，建议安装 `sentence-transformers`
- 如果你暂时只想看流程，也可以先跑 mock 模式

## 安装

```bash
/usr/bin/python3 -m pip install -r /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/vector_db_chroma_demo/requirements.txt
```

## 运行方式

### 先看 mock

```bash
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/vector_db_chroma_demo/main.py "怎么申请出差报销？" --mode mock
```

### 真实 Chroma

```bash
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/vector_db_chroma_demo/main.py "远程办公怎么申请？" --mode real --persist-dir ./chroma_data
```

如果你想换 embedding 方案，也可以加：

```bash
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/vector_db_chroma_demo/main.py "发布前要检查什么？" --mode real --embedding sentence-transformers
```

## 目录结构

```text
vector_db_chroma_demo/
├── assets/
│   ├── deployment_faq.md
│   ├── expense_policy.md
│   └── remote_work.md
├── main.py
├── README.md
└── requirements.txt
```

## 你会学到什么

1. Chroma 的 collection 怎么创建
2. metadata 和 document 为什么要一起存
3. query 返回结果是怎么组织的
4. 本地持久化和远端向量库的差别

## 常见报错

- `ModuleNotFoundError: chromadb`：先安装 `requirements.txt`
- `SQLite / persistence` 相关报错：通常是目录权限问题，换一个你有写权限的 `--persist-dir`
- `embedding size mismatch`：说明旧 collection 和新 embedding 维度不一致，建议先删掉持久化目录重来
- 如果结果不准，先换更短、更明确的 query

## 学习顺序

1. 先看 `build_embedder()`，理解文本如何转向量
2. 再看 `run_mock()`，理解入库和查询流程
3. 再看 `run_real()`，理解真实 Chroma 的接口
4. 最后对比 `vector_db_demo/` 和 `vector_db_qdrant_demo/`

