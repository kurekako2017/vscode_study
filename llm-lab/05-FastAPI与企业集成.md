# FastAPI 与企业集成

## 1. 为什么要学这一块

日本案件里常见的不是“只有一个本地脚本”，而是：

- `FastAPI` 后端
- 内部系统调用
- 前端或管理画面调用
- 企业资料目录接入

所以把 `LLM` 能力 API 化，是非常重要的一步。

很多企业现场真正需要的不是：

- 一个只能在本机跑的 demo

而是：

- 一个可以被别的系统调用的服务

这就是为什么在 `模型调用 -> 结构化输出 -> RAG` 之后，下一步通常就是：

- `FastAPI`
- API 设计
- 错误处理
- 服务化

## 2. 这一阶段要掌握什么

这一章至少要掌握这些：

- `FastAPI`
- 请求 / 返回模型
- 健康检查
- 配置管理
- 错误处理
- 文档重载

学完以后，你应该能做到：

- 把一个本地 `LLM / RAG` 能力包装成可调用接口

## 3. 这一章学完后，应该会什么

学完这一章，至少要能做到：

- 知道为什么 `CLI demo` 不等于后端服务
- 能写一个最小 `FastAPI` 服务
- 能定义请求和响应结构
- 能写 `GET /health`
- 能写 `POST /ask`
- 能处理最基本的服务错误
- 能解释“为什么企业现场更关心 API 化”

## 4. 教程：为什么 `FastAPI` 在这条线里重要

如果只会本地命令行脚本，很多场景没法直接接到：

- 前端页面
- 管理后台
- 内部业务系统
- 测试工具

而 `FastAPI` 的价值就在于：

- 很适合快速做 PoC
- 很适合定义清晰的请求 / 响应结构
- 很适合把 `Python + RAG` 能力包装成服务

所以对当前这条学习线来说，`FastAPI` 不是“顺手补一下”的内容，而是：

- 从 demo 走向可交付形态的关键一步

## 5. 教程：最小 API 化流程长什么样

最小 API 化，一般可以拆成 5 步：

1. 定义请求模型
2. 定义响应模型
3. 初始化服务
4. 写业务接口
5. 写健康检查接口

### 步骤 1：定义请求模型

例如：

```python
from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str
```

这一步的重点是：

- 先把前端或调用方要传什么说清楚

### 步骤 2：定义响应模型

例如：

```python
from pydantic import BaseModel


class AskResponse(BaseModel):
    answer: str
```

这一步的重点是：

- 把服务返回什么说清楚

### 步骤 3：初始化服务

```python
from fastapi import FastAPI


app = FastAPI()
```

这一步就是把脚本能力变成服务入口。

### 步骤 4：写业务接口

```python
@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    return AskResponse(answer=f"你问的是：{request.question}")
```

这一步相当于把原来的命令行处理逻辑，换成 HTTP 接口。

### 步骤 5：写健康检查接口

```python
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

健康检查虽然简单，但在企业系统里很常见。

因为别人接你这个服务时，通常首先会关心：

- 服务是不是活着
- 配置有没有加载
- 当前状态是否正常

## 6. 最小示例

下面给一个适合初学阶段理解的最小示例。

这个示例只做两件事：

- 暴露一个健康检查接口
- 暴露一个最小问答接口

```python
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    return AskResponse(answer=f"收到问题: {request.question}")
```

### 这个最小示例学的是什么

你要从这段代码里看懂 5 个点：

1. 服务入口是 `FastAPI()`
2. 请求和响应最好先定义清楚
3. `GET` 和 `POST` 的用途不同
4. API 不只是“能跑”，还要有清晰结构
5. 这是从脚本走向服务的第一步

## 7. 代码拆解

### 1. 为什么请求 / 返回模型很重要

因为企业系统接接口时，不希望靠猜。

更理想的状态是：

- 请求字段清楚
- 返回字段清楚
- 错误情况可预期

这也是为什么这一阶段一定要继续用：

- `Pydantic`

### 2. 为什么 `GET /health` 虽然简单却很重要

因为它会直接影响：

- 联调
- 部署确认
- 故障排查

也就是说，健康检查不是“附加项”，而是企业服务里很常见的基本项。

### 3. 为什么不能只停在本地 CLI

因为 CLI demo 更像：

- 开发者自己验证功能

而 API 服务更像：

- 给系统、前端、测试或其他模块调用

所以这一步本质上是在训练：

- 服务化思维

## 8. 进一小步：把 `RAG` 包装成 API

在这条学习线里，更有价值的不是只做一个“回声接口”，而是：

- 把前一章的 `RAG` 问答包装成 API

也就是：

1. 请求里传问题
2. 服务端做检索
3. 服务端调用模型回答
4. 返回答案和来源

这一步比单纯做一个聊天接口更贴近日本现场，因为很多实际需求是：

- 社内検索 API
- FAQ API
- 资料问答 API

## 9. 和当前工作区示例的对应关系

当前工作区里最适合这一章配套练的项目是：

- [agent-lab/projects/rag_api_demo/README.md](D:/dev/source_code/vscode_study/agent-lab/projects/rag_api_demo/README.md)

这个示例已经帮你做好了这些基础能力：

- `FastAPI` 服务入口
- 请求 / 响应模型
- `GET /health`
- `POST /ask`
- `POST /reload`
- `md / txt / pdf` 文档支持
- 把 `RAG` 逻辑服务化

如果你已经能读懂并改这个项目，就说明这一章已经基本过关。

## 10. 最小运行方式

先安装依赖：

```bash
pip install -r agent-lab/projects/rag_api_demo/requirements.txt
```

Windows PowerShell 设置环境变量：

```powershell
$env:OPENAI_API_KEY="your_api_key"
$env:RAG_API_DOCS_DIR="d:/dev/source_code/vscode_study/java-lab"
```

启动服务：

```bash
uvicorn agent-lab.projects.rag_api_demo.main:app --reload
```

如果你在 `agent-lab/projects/rag_api_demo` 目录内启动，也可以：

```bash
uvicorn main:app --reload
```

默认监听：

- `http://127.0.0.1:8000`

## 11. 请求示例

### `GET /health`

用于确认服务是否正常。

### `POST /ask`

请求体示例：

```json
{
  "question": "对日项目里的 RAG 和 Tool Calling 哪个优先学？",
  "model": "gpt-5"
}
```

返回内容会包括：

- `answer`
- `model`
- `docs_dir`
- `source_count`
- `sources`

### `POST /reload`

用于重新扫描本地文档并重建内存中的检索数据。

## 12. 常见错误与排查

### 1. 服务能启动，但接口设计很乱

表现通常是：

- 请求字段不稳定
- 返回结构经常改
- 调用方很难接

这时候要先做的事是：

- 先把请求 / 响应模型固定下来

### 2. 只会写接口，不会处理初始化

表现通常是：

- 服务虽然启动
- 但文档没加载
- 配置没检查

所以这一阶段不只是写路由，还要学会：

- 启动时初始化
- 配置检查
- 失败时明确报错

### 3. 只返回答案，不返回来源或元信息

表现通常是：

- 回答能出来
- 但不好排查和联调

更好的返回结构通常还会带：

- 使用的模型
- 文档目录
- 来源条数
- 来源标签

### 4. API 化了，但还是讲不清企业价值

这也是常见问题。

这一章真正要训练的是：

- 不只是把代码包成接口
- 还要能说清它怎么接前端、后台或内部系统

## 13. 练习题

下面这些练习题，建议按顺序做。

### 练习 1：给最小 API 增加 `model` 字段

让请求体支持：

- `question`
- `model`

目标：

- 理解接口字段应该可配置，而不是全写死

### 练习 2：增加来源字段

让响应里除了 `answer` 之外，再带：

- `sources`

目标：

- 训练“企业接口不只返回一句话”

### 练习 3：增加 `/reload`

加一个重新加载文档或配置的接口。

目标：

- 理解服务化后会出现“运行中重载”的需求

### 练习 4：支持 `pdf`

在现有能力上增加：

- `pdf` 文档读取

目标：

- 更贴近日企常见资料形态

### 练习 5：给错误信息做统一处理

当配置缺失或调用失败时，返回更明确的错误信息。

目标：

- 训练接口错误处理意识

### 练习 6：对照 `rag_api_demo` 改一版

要求：

- 读懂请求模型
- 读懂响应模型
- 读懂 `/health`、`/ask`、`/reload`
- 自己加一个字段或一个简单接口

目标：

- 从“看懂”进步到“能改”

## 14. 从图片里能借鉴的内容

你发的图片里有几个判断，对当前这章是有帮助的。

真正值得吸收的部分主要是：

- 日本 `AI Agent` 或生成 AI 系统，最后还是要落到工具和系统连接
- 只会 `LLM + Prompt` 不够，后面一定会遇到 API、工具调用、工作流
- `API` 集成能力非常关键，因为它决定了模型能力能不能接进真实系统

但也要注意学习顺序。

图片里提到的这些方向：

- `Memory`
- `Workflow`
- `Reflection`

都可以知道有这么回事，但当前主线不建议提前学得太深。

更适合当前阶段的优先顺序是：

1. `LLM`
2. `RAG`
3. `FastAPI`
4. API / 工具集成
5. 简单工作流
6. 再看 `Memory` 和 `Reflection`

也就是说，当前先把“能接系统”学会，比先研究复杂 Agent 机制更重要。

## 15. 企业集成里真正更优先的能力

如果按现实项目优先级来看，当前更该先补的是：

- API 设计
- 请求 / 响应结构
- 配置管理
- 文档重载
- 来源信息返回
- 基础日志和错误处理

后面再逐步补：

- 工具调用
- 简单工作流
- 认证
- 评估

而这些通常又比下面这些更早落地：

- 长期记忆
- 自我反思
- 多 Agent 协作

## 16. 这一章学到什么程度算过关

满足下面这些条件，就可以进入下一章：

- 能自己写一个最小 `FastAPI` 服务
- 能定义请求 / 响应模型
- 能写 `GET /health`
- 能写 `POST /ask`
- 能解释为什么企业现场需要 API 化
- 能读懂并修改 `rag_api_demo`

## 17. 下一步学什么

这一步完成后，最适合继续学的是：

- [06-评估与运维.md](D:/dev/source_code/vscode_study/llm-lab/06-%E8%AF%84%E4%BC%B0%E4%B8%8E%E8%BF%90%E7%BB%B4.md)

因为接下来要面对的问题会从：

- 怎么把能力做成服务

变成：

- 怎么判断这个服务到底好不好用、稳不稳定、值不值得上线

## 18. 企业集成常见方向

- 社内検索 API
- FAQ API
- 内部工具调用
- 管理后台调用
- 业务系统辅助接口

## 19. 日本现场高频关键词

- `FastAPI`
- `API連携`
- `バックエンド`
- `PoC`
- `社内利用`

## 20. 注意点

- 只会本地 CLI，不足以对应很多案件。
- 至少要会把能力包装成一个可调用 API。
- `API` 能接上系统，比界面花哨更重要。
- 当前阶段先把服务化打牢，再逐步进入更复杂的 Agent 工作流。
