# vector_db_qdrant_demo

这是一个“真实 Qdrant 版骨架” demo。

它保留了教学版的核心步骤，但把存储层换成了真实 Qdrant Client，方便你后面直接接：

- 本机 Docker Qdrant
- 远端 Qdrant 服务
- 企业知识库检索
- FAQ / 工单 / 制度文档检索

## 业务场景说明

- 适用场景：你已经有真实向量库，想把“文档入库、向量检索、top-k 召回”这条链路真正接上。
- 如果不用这种方式：你只能停留在“内存里演示一下”的层面，后面接真实知识库时还要重写很多接口。
- 解决的问题：把 collection、payload、upsert、search 这些真实 Qdrant 概念提前放进项目结构里，后面接服务时只需要替换连接信息。
- 举例说明：例如把报销制度、远程办公和发布 FAQ 入库，用户问“出差报销需要哪些材料”，就能直接从 Qdrant 里搜到对应条目。

## 这个 demo 会演示什么

- 真实 Qdrant Client 的接入方式
- collection 的创建与重建
- 文档向量写入
- 相似度检索和 top-k 召回
- `mock` / `real` 两种运行模式

## 前置条件

- 本机已经能访问 Qdrant
- 如果你要跑真实模式，需要安装依赖
- 如果你暂时没有服务，可以先用 `--mode mock` 看骨架和流程

## 安装

```bash
/usr/bin/python3 -m pip install -r /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/vector_db_qdrant_demo/requirements.txt
```

## 运行方式

### 先看 mock

```bash
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/vector_db_qdrant_demo/main.py "怎么申请出差报销？" --mode mock
```

### 真实 Qdrant

```bash
QDRANT_URL=http://localhost:6333 \
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/vector_db_qdrant_demo/main.py "怎么申请出差报销？" --mode real --recreate
```

如果你的 Qdrant 需要 API key，也可以再加：

```bash
QDRANT_URL=http://localhost:6333 QDRANT_API_KEY=xxx \
/usr/bin/python3 /home/victorkure/workspace/vscode_study/ai-lab/agent-advanced/projects/vector_db_qdrant_demo/main.py "远程办公怎么申请？" --mode real
```

## 目录结构

```text
vector_db_qdrant_demo/
├── assets/
│   ├── deployment_faq.md
│   ├── expense_policy.md
│   └── remote_work.md
├── main.py
├── README.md
└── requirements.txt
```

## 你会学到什么

1. 真实向量库里 collection 是怎么建的
2. payload 为什么要和向量一起存
3. upsert 和 search 的真实写法
4. Qdrant 的接入点和教学版的差别

## 常见报错

- `Connection refused`：通常是 Qdrant 没起或者 `QDRANT_URL` 写错。
- `Collection already exists`：先加 `--recreate`，或者删掉旧 collection 再跑。
- `ModuleNotFoundError: qdrant_client`：先安装 `requirements.txt`。
- `embedding size mismatch`：说明你换了 embedding 维度，但旧 collection 还是老维度，建议 `--recreate`。

## 学习顺序

1. 先看 `build_embedder()`，理解文本怎么变成向量
2. 再看 `run_mock()`，理解入库和检索流程
3. 再看 `run_real()`，理解真实 Qdrant Client 的接口
4. 最后对比 `vector_db_demo/`，看教学版和真实版的差别

