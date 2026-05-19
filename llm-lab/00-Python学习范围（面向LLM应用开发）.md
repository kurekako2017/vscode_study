# 00. Python 学习范围（面向 LLM 应用开发）

如果目标是：

- 学 `LLM` 应用开发
- 学 `RAG`
- 学 `FastAPI`
- 学 `Agent` 的前置基础
- 贴近日本 IT 现场和派遣案件

那么 `Python` 不需要一开始学得很“全”，而应该先学最实用、最常用、最容易马上落到项目里的部分。

这一篇的重点是整理：

- 该学什么
- 暂时不用学什么
- 建议学习顺序

## 0.1 先说结论

对 `LLM` 应用开发来说，最值得先学好的 `Python` 内容是：

- 基础语法
- JSON 和字典处理
- 文件处理
- 异常处理
- 类型标注
- `Pydantic`
- `FastAPI`
- 环境变量和配置读取

如果把范围再压缩成最核心的一句，就是：

- `Python + Pydantic + FastAPI + 文件处理`

这套组合比一开始去学复杂算法、爬虫、桌面开发、深度框架实现更实用。

## 0.2 为什么 Python 很重要

虽然 `LLM` 和 `Agent` 开发不只限于 `Python`，但当前最常见、最实用的还是 `Python`。

原因主要是：

- 大模型 SDK 支持成熟
- `RAG` 相关生态丰富
- 文档处理和数据处理库很多
- `FastAPI` 很适合做 PoC 和后端接口
- 日本现场很多生成 AI PoC 也常见 `Python`

所以更现实的策略是：

- 主线先学 `Python`
- 后面需要时再补 `TypeScript`

## 0.3 必须优先学的内容

### 1. 基础语法

先学这些最常用的基础：

- 变量
- 字符串
- 数字
- 布尔值
- 列表
- 字典
- 集合
- `if`
- `for`
- `while`
- 函数
- `import`

这里的目标不是背语法，而是能写出这种代码：

- 遍历文档
- 处理 JSON
- 调函数
- 组合结果

### 2. 字典、列表、JSON 处理

这块很重要，因为 `LLM` 开发里大量数据都是：

- JSON 请求
- JSON 响应
- schema 数据
- 检索结果列表

要重点掌握：

- `dict.get()`
- 列表遍历
- 列表过滤
- 排序
- `json.dumps()`
- `json.loads()`

### 3. 文件处理

这对 `RAG`、日志、配置、文档问答非常重要。

要重点学：

- 读取文本文件
- 写入文本文件
- 读取 `json`
- 遍历目录
- 判断文件和目录
- 拼接路径

推荐重点掌握：

- `pathlib`

因为它比传统字符串拼路径更稳定、更适合项目代码。

### 4. 异常处理

在 `LLM` 应用里，出错很常见：

- API Key 没配
- 文件不存在
- PDF 读失败
- 请求超时
- 模型调用失败

所以要掌握：

- `try / except`
- `raise`
- 怎么输出清楚的错误信息

### 5. 函数与模块拆分

你至少要会把逻辑拆成函数，比如：

- `build_client()`
- `load_docs()`
- `search_chunks()`
- `ask_question()`

然后逐步学会拆成多个文件和模块。

### 6. 类型标注

现在的 `Python` 项目里，尤其是 `LLM / FastAPI / Pydantic` 相关代码，经常会写：

- `str`
- `list[str]`
- `dict[str, Any]`
- `Optional[str]`
- `Literal["low", "medium", "high"]`

所以不用一开始学特别深，但至少要能看懂并能自己写基础类型标注。

## 0.4 面向 LLM 应用必须补的内容

### 1. 环境变量与配置

要会：

- 读取 `OPENAI_API_KEY`
- 读取路径配置
- 读取模型名
- 管理不同环境参数

最常见的就是：

- `os.getenv()`

### 2. `Pydantic`

这是 `LLM` 应用里很实用的一块。

主要用来做：

- 结构化输出 schema
- 请求参数定义
- 响应结果校验
- API 数据模型

要掌握这些：

- `BaseModel`
- `Field`
- `model_dump()`
- `model_dump_json()`

### 3. `FastAPI`

如果想贴近案件要求，这块几乎一定要学。

要掌握：

- 路由定义
- `GET`
- `POST`
- 请求体模型
- 响应 JSON
- 启动服务

重点不是把 `FastAPI` 学成框架专家，而是要能做这种最小后端：

- `GET /health`
- `POST /ask`
- `POST /reload`

### 4. 文档与文本处理

这对 `RAG` 很重要。

要掌握：

- 文本切分
- 基础清洗
- 关键词匹配
- 简单评分
- 结果排序

如果处理文档，还要逐步补：

- `md`
- `txt`
- `pdf`

## 0.5 暂时不用优先学的内容

如果目标是尽快进入 `LLM` 应用开发，下面这些不是最优先：

- 复杂算法与数据结构刷题
- 深度学习底层实现
- `Python` Web 全家桶
- 爬虫进阶
- GUI 开发
- 游戏开发
- 科学计算全套
- 装饰器、元类、协程底层细节学得过深

不是说这些没用，而是：

- 现在先学这些，投入产出比不高

## 0.6 建议学习顺序

推荐顺序如下：

1. `Python` 基础语法
2. 列表 / 字典 / JSON 处理
3. 文件和路径处理
4. 异常处理
5. 环境变量与配置
6. `OpenAI API` 调用
7. 类型标注
8. `Pydantic`
9. `FastAPI`
10. 文档处理与最小 `RAG`
11. Tool Calling
12. Workflow / Agent

如果再压缩成适合你当前路线的版本，就是：

1. `Python` 基础
2. JSON / 文件处理
3. 模型调用
4. `Pydantic`
5. `FastAPI`
6. `RAG`
7. Tool Calling
8. Agent

## 0.7 对应到当前工作区怎么学

你现在这个工作区里，其实已经有很合适的练习顺序：

1. `chat_cli`
2. `structured_output_demo`
3. `doc_qa_agent`
4. `rag_api_demo`
5. `tool_agent_demo`
6. `workflow_agent`

可以这样对应：

- `chat_cli`
  - 练 `Python` 基础 + API 调用
- `structured_output_demo`
  - 练 `Pydantic` + 结构化输出
- `doc_qa_agent`
  - 练文件处理 + 文本切分 + 最小 `RAG`
- `rag_api_demo`
  - 练 `FastAPI` + `PDF` + API 化
- `tool_agent_demo`
  - 练 Tool Calling
- `workflow_agent`
  - 练工作流状态和多阶段处理

## 0.8 学到什么程度算够用

对当前阶段来说，不需要把 `Python` 学成高级语言专家。

够用的标准是：

- 能读懂项目代码
- 能自己改 demo
- 能自己写最小 API
- 能处理文件和 JSON
- 能写基础异常处理
- 能看懂 `Pydantic` model
- 能写简单 `FastAPI`

如果能做到这些，就已经足够支撑你继续学：

- `RAG`
- 企业 PoC
- Tool Calling
- Workflow Agent

## 0.9 常见误区

### 误区 1：要先把 Python 学得非常全

不需要。

更好的做法是：

- 先学会项目里会用到的部分
- 再边做边补

### 误区 2：先直接冲 Agent

如果 `Python` 基础、文件处理、`Pydantic`、`FastAPI` 都没稳，直接做 Agent 往往会很空。

### 误区 3：只会调用模型就够了

不够。

现场真正需要的是：

- 数据处理
- 文件处理
- API 化
- 结构化输出

## 0.10 当前最推荐的学习组合

如果只记一套组合，建议记这个：

- `Python`
- `Pydantic`
- `FastAPI`
- 文件处理
- `RAG`

这套能力比单独学“聊天机器人”更贴近日本现场实际。

## 0.11 成本与注意点

- 不要一开始把学习面铺得太宽。
- 先把 `Python + Pydantic + FastAPI + 文件处理` 打牢，再继续往 `RAG` 和 Agent 走。
- 代码练习比纯看概念更重要。
- 模型调用会产生 API 成本，可以先多做本地文本处理和接口结构练习，再增加真实调用次数。

## 0.12 为什么后面还要补 TypeScript

`TypeScript` 不是当前主线，但后面很值得补。

原因主要是：

- 很多 `Web UI` 和前后端联动项目会用到它
- `Node.js` 生态里大量工程都默认使用 `TypeScript`
- 一些 Agent SDK、自动化工具、前端集成方案会优先提供 `TypeScript` 示例
- 如果以后要做完整产品，而不只是后端 PoC，`TypeScript` 很常见

所以更合适的顺序不是：

- 一开始同时硬学 `Python + TypeScript`

而是：

1. 先把 `Python` 学到能独立做小项目
2. 再补 `JavaScript / TypeScript`
3. 再做 `Python + TypeScript` 联动项目

## 0.13 TypeScript 要补到什么范围

如果目标是配合 `LLM` 应用开发使用，不需要一开始就学很深。

先补这些最实用的内容：

### 1. 先补 JavaScript 基础

- 变量
- 字符串
- 数组
- 对象
- 条件判断
- 循环
- 函数
- 模块导入导出

## 附：一句话概括

- **RAG**：检索增强生成，把外部文档检索结果与生成式模型结合，提升答案准确性并增强可解释性。
- **FastAPI**：高性能的 Python Web 框架，用于快速构建异步 RESTful API 并自动生成 OpenAPI 文档。
- **POC**：概念验证，通过最小化原型快速验证技术或想法的可行性与价值。
- `Promise`
- `async / await`

### 2. 再补 TypeScript 类型系统

- `type`
- `interface`
- 基础类型标注
- 可选字段
- 联合类型
- 泛型
- 函数参数和返回值类型

目标不是先把类型系统学得很理论，而是能看懂并改这种代码：

- API 请求参数
- API 响应类型
- 前端表单数据
- SDK 调用结果

### 3. 再补 Node.js 基础

- `npm`
- 包管理
- 项目脚本
- 环境变量
- 读取文件
- 调 HTTP API
- 启动最小服务

### 4. 如果要做界面，再补前端框架

后面如果要做网页界面，再补：

- `React`
- `Next.js`
- 表单处理
- 调后端接口
- 基础状态管理

## 0.14 教程和示例要怎么补

这块建议不要只看教程，也不要只抄项目。

更有效的方式是：

- 教程负责补概念和语法
- 示例负责把知识点变成可运行代码
- 每学完一块就自己改一版

可以按这个节奏补：

### 阶段 1：Python 主线

教程重点：

- 语法基础
- JSON / 文件处理
- 环境变量
- `Pydantic`
- `FastAPI`

示例重点：

- 读写 `json`
- 读取目录中的文档
- 调模型 API
- 写最小 `/ask` 接口

### 阶段 2：Python AI 小项目

教程重点：

- 结构化输出
- `RAG`
- 文本切分
- 错误处理

示例重点：

- 命令行聊天
- 结构化结果提取
- 本地文档问答
- `FastAPI` 版问答接口

### 阶段 3：TypeScript 补课

教程重点：

- `JavaScript` 基础
- `TypeScript` 类型
- `Node.js`
- `async / await`

示例重点：

- 读取本地文件
- 调 LLM API
- 返回结构化 JSON
- 写一个最小后端接口

### 阶段 4：前后端联动

教程重点：

- 前端调用后端
- 表单提交
- 错误提示
- 环境变量区分

示例重点：

- 一个聊天页面
- 一个文档问答页面
- 一个调用 `Python FastAPI` 后端的前端页面

## 0.15 最推荐的补法

如果要尽量贴近你当前路线，建议这样分配：

- `Python` 学习和项目：`70%`
- `LLM / RAG / FastAPI` 实战：`20%`
- `TypeScript` 起步补课：`10%`

等你已经能独立做出 2 到 3 个 `Python` 小项目后，再把 `TypeScript` 比重提高。

也就是说，现阶段不用焦虑“是不是两门都要同时学”。

更现实的答案是：

- 是，后面最好补 `TypeScript`
- 但现在先把 `Python` 学扎实更重要

## 0.16 对应到当前工作区怎么补教程和示例

可以直接按现在这个工作区的内容来练：

### 先练 Python 主线

- `agent-lab/projects/chat_cli`
  - 练 API 调用、命令行交互、基础异常处理
- `agent-lab/projects/structured_output_demo`
  - 练结构化输出、数据模型、结果解析
- `agent-lab/projects/doc_qa_agent`
  - 练文件处理、文本切分、最小 `RAG`
- `agent-lab/projects/rag_api_demo`
  - 练 `FastAPI`、接口化、文档问答

### 再补 Web / TypeScript 方向

- `web-projects`
  - 用来熟悉前端项目结构、`TypeScript`、页面与接口联动

所以你的学习文档可以先按这个理解：

1. 主线先学 `Python`
2. 主线项目先做 `LLM + RAG + FastAPI`
3. 后面再补 `TypeScript`
4. 最后做前后端一体的 AI 应用
