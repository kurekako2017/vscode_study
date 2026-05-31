# 00. Python 学习范围（面向 LLM 应用开发）

这篇只回答一个问题：

> 为了做 `LLM / RAG / FastAPI / Agent` 应用，Python 先学到什么范围就够用？

结论是：不要一开始把 Python 当成“全栈语言大百科”来学。当前最有效的路线是先掌握能马上落到项目里的能力。

```text
Python 基础 -> JSON / 文件处理 -> API 调用 -> Pydantic -> FastAPI -> RAG
```

## 1. 先说结论

当前阶段最优先学这些：

| 优先级 | 内容 | 用在什么地方 |
| --- | --- | --- |
| 必学 | 基础语法 | 读懂 demo、改函数、写流程 |
| 必学 | `dict / list / json` | 处理模型输入输出、API 请求响应 |
| 必学 | 文件与路径 | RAG 文档读取、配置、日志 |
| 必学 | 异常处理 | API Key、文件、模型调用失败时能定位问题 |
| 必学 | 类型标注 | 看懂现代 Python 项目 |
| 必学 | `Pydantic` | 结构化输出、请求体、响应校验 |
| 必学 | `FastAPI` | 把 LLM/RAG 能力封装成接口 |
| 后补 | `TypeScript` | 前端页面、Node.js、前后端联动 |

最核心的一句话：

```text
先把 Python + Pydantic + FastAPI + 文件处理 学到能改项目。
```

## 2. 为什么是这个范围

LLM 应用开发不是只写 prompt。实际项目里经常要处理：

- 读取本地文件或企业文档
- 把用户输入变成模型请求
- 把模型结果变成 JSON
- 校验字段是否稳定
- 封装成 HTTP API
- 记录错误、成本、延迟和评估结果

所以 Python 学习重点不是“语法多全面”，而是能不能支撑下面这些项目：

- `chat_cli`：命令行模型调用
- `structured_output_demo`：结构化输出
- `doc_qa_agent`：本地文档问答
- `rag_api_demo`：FastAPI 版 RAG 服务

## 3. Python 必学范围

### 3.1 基础语法

先学到能看懂和修改项目代码：

- 变量、字符串、数字、布尔值
- `list / dict / set`
- `if / for / while`
- 函数
- `import`
- 模块拆分

验收标准：

- 能读懂一个 `main.py`
- 能新增一个函数
- 能把重复逻辑拆成函数

### 3.2 JSON、字典和列表

LLM 应用里大量数据都是 JSON：

- 请求参数
- 模型响应
- 检索结果
- 结构化输出
- API 返回值

重点掌握：

- `dict.get()`
- 遍历列表
- 过滤和排序列表
- `json.loads()`
- `json.dumps(..., ensure_ascii=False, indent=2)`

验收标准：

- 能从 JSON 中取字段
- 能把 Python 对象保存成 JSON
- 能把模型结果整理成固定结构

### 3.3 文件和路径处理

RAG、日志、配置都离不开文件处理。

重点掌握：

- 读取文本文件
- 写入文本文件
- 读取 JSON 文件
- 遍历目录
- 判断文件和目录
- 使用 `pathlib.Path`

验收标准：

- 能读取一个资料目录中的 `.md` / `.txt`
- 能把结果写入 `json`
- 能看懂 `Path(__file__).parent`

### 3.4 异常处理

LLM 应用常见错误：

- 没有 `OPENAI_API_KEY`
- 文件不存在
- PDF 或文本解析失败
- 模型调用超时
- 返回结构不符合预期

重点掌握：

- `try / except`
- `raise`
- 自定义清楚的错误信息
- 什么时候让程序退出，什么时候返回错误响应

验收标准：

- 出错时能看懂原因
- 能给 CLI 或 API 返回清楚错误

### 3.5 类型标注

不用一开始学得很深，但必须能看懂这些：

- `str`
- `int`
- `bool`
- `list[str]`
- `dict[str, Any]`
- `Optional[str]`
- `Literal["low", "medium", "high"]`

验收标准：

- 能给函数参数和返回值补基础类型
- 能读懂 `Pydantic` model 的字段类型

## 4. LLM 应用必须补的 Python 生态

### 4.1 环境变量与配置

重点掌握：

- `os.getenv("OPENAI_API_KEY")`
- 模型名、资料路径、运行模式的配置
- mock 模式和 real 模式切换

验收标准：

- 没有 API Key 时能跑 mock
- 有 API Key 时能切到真实模型调用

### 4.2 Pydantic

`Pydantic` 是结构化输出和 FastAPI 的共同基础。

重点掌握：

- `BaseModel`
- `Field`
- `Literal`
- `model_dump()`
- `model_dump_json()`

用在：

- 定义模型输出 schema
- 校验 API 请求体
- 生成稳定 JSON

### 4.3 FastAPI

当前阶段不需要成为 Web 框架专家，先会写最小接口。

重点掌握：

- `GET /health`
- `POST /ask`
- 请求体模型
- JSON 响应
- 启动服务
- 基础错误处理

验收标准：

- 能把命令行 demo 改成 API
- 能用 curl 或浏览器调用接口

### 4.4 文档与文本处理

RAG 的前置基础：

- 文本切分
- 简单清洗
- 关键词匹配
- 简单评分
- 检索结果排序
- 引用来源

验收标准：

- 能读取本地资料
- 能返回相关片段
- 能说明答案来自哪个文件

## 5. 暂时不用优先学

下面这些不是没用，而是当前投入产出比不高：

- 复杂算法刷题
- 深度学习底层实现
- 爬虫进阶
- GUI 开发
- 游戏开发
- 科学计算全套
- 元类、装饰器、协程底层细节
- Django / Flask / Tornado 全家桶

当前策略：

```text
先做出 LLM 应用，再按项目需要补深水区。
```

## 6. 当前工作区怎么练

推荐按这个顺序跑：

| 顺序 | 项目 | 主要练什么 |
| --- | --- | --- |
| 1 | `../agent-lab/projects/chat_cli` | Python 基础、API 调用、环境变量 |
| 2 | `../agent-lab/projects/structured_output_demo` | Pydantic、结构化输出 |
| 3 | `../agent-lab/projects/doc_qa_agent` | 文件处理、文本切分、最小 RAG |
| 4 | `../agent-lab/projects/rag_api_demo` | FastAPI、RAG API 化 |
| 5 | `../agent-lab/projects/tool_agent_demo` | Tool Calling |
| 6 | `../agent-lab/projects/workflow_agent` | 工作流和多阶段处理 |

建议每个项目都完成 3 步：

1. 跑通原始 demo
2. 改一个小功能
3. 写下这个项目的输入、处理、输出

## 7. 学到什么程度算够用

满足下面条件，就可以进入 RAG 和 FastAPI 主线：

- 能读懂项目里的 `main.py`
- 能自己改 CLI 参数
- 能处理 JSON 和文件
- 能写基础异常处理
- 能看懂 `Pydantic` model
- 能写一个 `GET /health`
- 能写一个 `POST /ask`

不需要等到“Python 全学完”再继续。

## 8. TypeScript 什么时候补

`TypeScript` 后面值得补，但不是当前第一主线。

建议等下面几项稳定后再补：

- 能独立改 Python demo
- 能写最小 FastAPI 接口
- 能处理 JSON / 文件
- 能做一个最小 RAG

TypeScript 先补到这个范围即可：

- JavaScript 基础
- `Promise`
- `async / await`
- `type`
- `interface`
- `npm`
- 前端调用后端 API

## 9. 常见误区

| 误区 | 更好的做法 |
| --- | --- |
| 先把 Python 全学完 | 先围绕项目学最常用部分 |
| 只会调用模型就够了 | 还要会文件、JSON、API、校验 |
| 直接冲复杂 Agent | 先把 Pydantic、RAG、FastAPI 打稳 |
| 只看教程不改代码 | 每章都跑 demo 并改一版 |

## 10. 一句话概括

当前最推荐的学习组合：

```text
Python + Pydantic + FastAPI + 文件处理 + RAG
```

这套能力比单独学“聊天机器人”更贴近日本现场的生成 AI PoC 和企业集成案件。
