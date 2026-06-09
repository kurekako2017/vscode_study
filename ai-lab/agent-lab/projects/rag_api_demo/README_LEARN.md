# rag_api_demo 学习笔记

这份文档不是重复运行说明，而是把 `rag_api_demo` 的核心逻辑拆开讲清楚，方便你从“会跑”进到“看懂”。

业务场景说明
- 适用场景：把本地文档问答做成一个可以被浏览器、命令行或其他服务调用的 API。
- 如果不用这种方式：RAG 只能作为单机脚本使用，难以接入前端、Java 服务或自动化流程。
- 解决的问题：用接口化的方式把“检索 + 生成 + 来源”标准化，方便扩展、部署和联调。
- 举例说明：例如先拿一份报销制度或项目说明书做测试，看看答案里能不能带出引用来源。

## 1. 先记住一句话

这个例子本质上是:

`HTTP 客户端` 通过 `FastAPI` 调用一个 `RAG 后端`，后端再去读本地文档、做检索、调用模型，最后把答案和来源返回给客户端。

## 2. 角色分工

| 角色 | 对应对象 | 作用 |
|---|---|---|
| 客户端 | `curl`、浏览器、前端页面、测试脚本 | 发请求、收 JSON |
| 程序入口 | `main.py` | 启动服务、定义接口、串起业务流程 |
| 服务端 | `main.py` 启动的 `FastAPI` 应用 | 提供 `/`、`/health`、`/ask`、`/reload` |
| 文档数据 | 当前目录或 `RAG_API_DOCS_DIR` 指向的目录 | 提供 `.md`、`.txt`、`.pdf` |
| 模型 | Mock 或 OpenAI | 生成回答 |

在真实项目里，客户端不一定是人，也可能是别的系统。

## 3. 处理流程

### 3.1 启动时发生什么

现在这个项目是懒加载，不是“启动即预热”。

也就是说:

- 启动 `uvicorn` 时，只是把服务拉起来
- 还没有立刻扫描所有文档
- 第一次访问 `/health`、`/ask` 或 `/reload` 时，才会执行 `load_state()`

### 3.2 第一次请求 `/health`

流程:

1. 客户端请求 `/health`
2. 进入 `health()`
3. 调用 `ensure_state_loaded()`
4. 如果状态没准备好，就执行 `load_state()`
5. 扫描目录、读取文件、切块、缓存到 `app.state`
6. 返回 `status`、`docs_dir`、`chunk_count`

### 3.3 请求 `/ask`

流程:

1. 客户端提交 `question`
2. `ask()` 调用 `ensure_state_loaded()`
3. 从 `app.state.chunks` 里检索相关片段
4. 用检索结果构造上下文
5. 调用 `answer_question()`
6. 返回答案、来源、模型名和文档目录

### 3.4 请求 `/reload`

流程:

1. 客户端调用 `/reload`
2. 服务直接重新执行 `load_state()`
3. 文档重新扫描
4. `app.state` 里的缓存被更新
5. 返回新的 `chunk_count`

### 3.5 前后端完整链路

如果把这个 demo 当成“前端 + 后端”的完整小系统，可以这样理解:

前端链路:

1. 用户在 React 页面或 Spring Boot 客户端输入问题
2. 客户端把问题发到 `/ask`
3. 前端收到 `answer`、`sources`、`source_count`
4. 页面把回答和来源展示给用户

后端链路:

1. `ask()` 收到请求
2. `ensure_state_loaded()` 确认索引已准备好
3. `retrieve()` 在内存 chunk 中找相关片段
4. `build_context()` 把片段拼成上下文
5. `answer_question()` 生成回答
6. `AskResponse` 返回给前端

### 3.6 文档整理流程

当你新增或修改文档时，建议按下面的顺序整理:

1. 把资料放进 `docs` 目录，或者放到 `RAG_API_DOCS_DIR` 指向的目录
2. 调用 `/reload` 重新扫描文件并重建 chunk
3. 调用 `/health` 检查 `docs_dir` 和 `chunk_count`
4. 再调用 `/ask` 看答案和来源是否更新
5. 前端页面同步刷新结果展示，确认前后端看到的是同一份资料

## 4. 关键函数

### `load_state()`

负责:

- 找到文档目录
- 扫描可读文件
- 读取内容
- 切分成 chunk
- 准备客户端对象
- 写入 `app.state`

你可以把它理解成“把静态资料变成服务可以即时使用的内存状态”。

### `ensure_state_loaded()`

负责:

- 检查 `app.state` 有没有缓存
- 没有就调用 `load_state()`

它的意义是:

- 把“启动时加载”改成“请求时加载”
- 避免 VS Code 打开工作区时就把服务和索引一起拉起来

### `retrieve()`

负责:

- 根据问题找相关片段
- 给片段打分
- 选出最相关的一批内容

它不是向量检索，只是教学版关键词重叠检索。

### `build_context()`

负责:

- 把检索结果拼成模型上下文
- 让模型知道它应该依据哪些资料回答

### `answer_question()`

负责:

- Mock 模式下返回模拟答案
- Real 模式下调用 OpenAI

## Python 里为什么没有 `main()`

如果你熟 Java，会习惯性去找 `public static void main(String[] args)`。
但 Python 不是这么启动 Web 服务的。

在这个 demo 里：

- `main.py` 只是模块文件，不是必须包含 `main()` 函数
- `uvicorn main:app` 才是真正的启动命令
- `main:app` 的意思是“导入 `main.py`，读取里面的 `app` 对象”

具体流程是：

1. `uvicorn` 导入 `main.py`
2. Python 执行这个文件里的顶层代码
3. `app = FastAPI(...)` 被创建出来
4. `uvicorn` 把这个 `app` 当成服务入口运行

这也是为什么你会看到：

- `root()`、`health()`、`ask()`、`reload_docs()` 这些函数是直接定义在文件里的
- 它们没有被手动调用
- 是 FastAPI 根据装饰器 `@app.get(...)`、`@app.post(...)` 自动注册的

所以在 Python + FastAPI 里，入口通常不是 `main()`，而是：

`模块名 + app 对象 + ASGI 服务器`

如果你想把这个部分再学透一点，可以继续看：

- [Python 入门补充](/home/victorkure/workspace/vscode_study/ai-lab/agent-lab/projects/rag_api_demo/Python入门补充.md)

## FastAPI、Flask、Django 怎么理解

你截图里的对比可以直接记成下面这张表:

| 框架 | 特点 | 关键词 |
|---|---|---|
| Flask | 老牌、轻量 | 自由度高、适合小而清晰的服务 |
| Django | 很重、全家桶 | 自带后台、ORM、认证、模板等 |
| FastAPI | 现代、快、AI 项目最常见 | 类型提示、自动文档、API 开发体验好 |

放到这个例子里，FastAPI 的优势很明显:

- 这个项目的核心是“提供接口”，不是做页面
- `/health`、`/ask`、`/reload` 这种接口特别适合 FastAPI
- 它能比较自然地把请求模型、响应模型、接口文档组织起来
- 对学习 `RAG API` 来说，结构比传统 Web 框架更直接

## 5. 接口怎么理解

### `GET /`

这是“服务活着吗”的最简单检查。

适合浏览器直接打开。

### `GET /health`

这是“服务状态怎么样”的接口。

它比 `/` 更适合自动化检查，因为会告诉你:

- 读到了哪个目录
- 目前有多少 chunk

### `POST /ask`

这是核心问答接口。

它适合:

- 前端页面调用
- 自动化测试调用
- 其他系统集成调用

### `POST /reload`

这是“文档更新后，重新加载”的接口。

适合:

- 你新增了文档
- 你修改了文档
- 你想验证重载后结果是否变化

## 三种学习方式

你现在可以用同一个后端，配三种客户端来学：

### 方式 A: `curl` 直连

适合先搞懂接口本身。

```bash
cd ai-lab/agent-lab/projects/rag_api_demo
./run-dev.sh
```

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"question":"请总结文档重点"}'
```

### 方式 B: React Web 客户端

适合看最常见的浏览器前端怎么调用 agent。

```bash
cd ai-lab/agent-lab/projects/rag_api_demo
./run-dev.sh
cd react-client
npm install
npm run dev
```

这里的 `react-client` 就是原来文档里说的 `client`，只是我把目录名改得更清楚了。

### 方式 C: Spring Boot 客户端

适合学习 Java 服务如何作为上游客户端调用 agent。

```bash
cd ai-lab/agent-lab/projects/rag_api_demo
./run-dev.sh
cd spring-client
mvn spring-boot:run
```

## 6. 部署方式

### 6.1 本地开发

最推荐:

```bash
cd ai-lab/agent-lab/projects/rag_api_demo
./run-dev.sh
```

这个脚本会:

- 创建虚拟环境
- 安装依赖
- 设置 Mock 模式
- 启动服务

### 6.2 手工运行

```bash
cd ai-lab/agent-lab/projects/rag_api_demo
RAG_API_MOCK=1 uvicorn main:app --reload --port 8000 --host 127.0.0.1
```

### 6.3 Docker

```bash
cd ai-lab/agent-lab/projects/rag_api_demo
docker build -t rag_api_demo:dev .
docker run -p 8000:8000 rag_api_demo:dev
```

## 7. 访问方式

### 7.1 浏览器

打开:

```text
http://127.0.0.1:8000/
```

### 7.2 命令行

健康检查:

```bash
curl http://127.0.0.1:8000/health
```

问答:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"请总结文档重点"}'
```

重载:

```bash
curl -X POST http://127.0.0.1:8000/reload
```

## 8. 为什么会有 Mock 和 Real

### Mock

用途:

- 不依赖 OpenAI
- 没有 API Key 也能跑
- 适合学习和测试流程

### Real

用途:

- 真正调用模型
- 观察真实的问答结果
- 验证你配置的 API 是否可用

切换规则:

- 设置 `RAG_API_MOCK=1` 就是 Mock
- 没有 Mock 时，如果有 `OPENAI_API_KEY` 就走 Real

## 9. 一个请求的完整链路

你可以把 `/ask` 想成一条流水线:

```text
客户端
  -> HTTP POST /ask
  -> FastAPI 路由
  -> ensure_state_loaded()
  -> load_state() 仅在首次请求或 reload 后执行
  -> retrieve()
  -> build_context()
  -> answer_question()
  -> JSON 响应
```

这里最关键的是:

- `load_state()` 负责把“文档变成可用状态”
- `retrieve()` 负责找资料
- `answer_question()` 负责生成答案

## 10. 你最容易混淆的点

- `health` 不是“模型健康”，而是“服务健康”
- `reload` 不是“重启程序”，而是“重扫文档”
- 客户端不是固定一个人，终端、浏览器、前端、别的系统都可以是客户端
- `FastAPI` 是服务端，不是客户端
- `OpenAI` 只是在 Real 模式下才是上游服务

## 11. 推荐练习顺序

1. 先跑 `python3 mock_test.py`
2. 再跑 `./run-dev.sh`
3. 打开 `/`
4. 请求 `/health`
5. 请求 `/ask`
6. 修改一份文档后请求 `/reload`
7. 再请求 `/health` 和 `/ask` 看变化

## 12. 阅读源码时的顺序

如果你想继续看代码，建议按下面顺序:

1. `main.py` 顶部的请求/响应模型
2. `load_state()` 和 `ensure_state_loaded()`
3. `retrieve()` 和 `build_context()`
4. `answer_question()`
5. 最后看四个路由函数

这样更容易把“功能”和“接口”对应起来。
