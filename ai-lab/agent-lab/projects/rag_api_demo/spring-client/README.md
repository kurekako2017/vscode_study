# rag_api_demo Spring Boot 客户端

这是一个最小的 Spring Boot 客户端应用，用来调用 `rag_api_demo` 的 FastAPI 接口。

它的定位是“Java 服务如何作为客户端去调用另一个 agent / RAG 服务”。

## 业务场景说明

- 适用场景：公司里已有 Spring Boot 或 Java 业务系统，需要复用 RAG 能力而不是单独再造一个入口。
- 如果不用这种方式：AI 能力和现有业务系统会割裂，Java 侧只能手工调用接口，集成成本高。
- 解决的问题：把 RAG 服务包装成 Java 客户端范式，方便接入企业现有后端和服务编排。
- 举例说明：例如用 Java 客户端发起一次“制度问答”请求，验证后端返回的检索结果能否被前端正常消费。

## 1. 它会调用哪些接口

- `GET /`
- `GET /health`
- `POST /ask`
- `POST /reload`

## 2. 本地运行

先启动后端服务:

```bash
cd ai-lab/agent-lab/projects/rag_api_demo
./run-dev.sh
```

再启动 Spring Boot 客户端:

```bash
cd ai-lab/agent-lab/projects/rag_api_demo/spring-client
mvn spring-boot:run
```

第一次运行如果本地还没有对应的 Maven 缓存，可能会先下载依赖，这属于正常情况。

如果你的后端不在 `http://127.0.0.1:8000`，可以这样改:

```bash
cd ai-lab/agent-lab/projects/rag_api_demo/spring-client
RAG_API_BASE_URL=http://127.0.0.1:8000 mvn spring-boot:run
```

## 3. 访问方式

客户端默认监听:

```text
http://127.0.0.1:8088
```

可用接口:

- `GET /client`
- `GET /client/root`
- `GET /client/health`
- `POST /client/ask`
- `POST /client/reload`

## 4. 示例请求

```bash
curl http://127.0.0.1:8088/client/health
```

```bash
curl -X POST http://127.0.0.1:8088/client/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"请总结文档重点","model":"gpt-5"}'
```

```bash
curl -X POST http://127.0.0.1:8088/client/reload
```

## 5. 这个客户端的定位

- 它是一个 Java / Spring Boot 版的 API 客户端
- 它不是替代后端，而是作为上游调用者
- 适合学习企业里常见的“Java 服务调 AI 服务”的方式
