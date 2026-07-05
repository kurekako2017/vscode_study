# AI Learn 术语速查表

## Python -> FastAPI -> OpenAPI -> 文档展示

```text
Python 代码
↓
FastAPI
↓
OpenAPI(JSON)
├── Swagger UI
└── ReDoc
```

说明：

- `FastAPI` 会根据 Python 代码自动生成 `OpenAPI(JSON)`。
- `Swagger UI` 和 `ReDoc` 都是 `OpenAPI` 的展示方式。
- `Swagger UI` 更适合调试和验证接口。
- `ReDoc` 更适合阅读接口文档。

## RAG 学习路径

```text
文档 / 资料
↓
Chunk 切分
↓
Retriever 检索
↓
Citation 引用
↓
回答生成
```

说明：

- `Chunk` 是检索的基本单位。
- `Retriever` 负责找证据，不负责直接编答案。
- `Citation` 用来说明答案依据。

## 企业学习提示

- 先确认接口和输入输出。
- 再看流程、日志和错误码。
- 最后看如何和前端或既存系统联调。
