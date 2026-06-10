# 测试方案与测试骨架规划

> 这份文档不是现成的测试结果，而是给当前 `deepsearch-agents-main` 项目准备的一份测试规划说明。  
> 它回答三个问题：
> 1. 这个项目应该怎么测；
> 2. 哪些地方适合写测试类；
> 3. 后续如果补测试骨架，建议怎么组织目录。

## 1. 先说结论

这个项目不是一个纯函数库，而是一个“单体应用 + 外部服务 + 多智能体 + WebSocket + 文件系统”的组合体。

所以它的测试方式不能只靠单元测试，也不能只靠人工点按钮。比较合理的做法是：

1. 用单元测试覆盖纯逻辑
2. 用集成测试覆盖接口和内部调用链
3. 用端到端测试覆盖前端到后端的完整闭环
4. 用 smoke test 和验收清单做部署后回归

换句话说：

- `pytest` 适合测“函数本身”
- `FastAPI TestClient` 适合测“接口是否可用”
- `WebSocket` / 前端联调适合测“完整链路是否连通”
- 文档清单适合测“上线后是否稳定”

## 2. 这个项目适合测什么

### 2.1 纯逻辑层

适合写单元测试的地方：

- 路径解析
- 文件名处理
- Markdown 到 PDF 的转换入口参数
- 环境变量读取逻辑
- 健康检查返回字段
- SQL 结果格式化
- 结果文件命名规则

这些地方通常输入明确、输出明确，适合写测试类。

### 2.2 业务工具层

适合做集成测试的地方：

- `generate_markdown`
- `convert_md_to_pdf`
- `read_file_content`
- `tavily_tool`
- `db_tools`
- `ragflow_tools`

这些工具往往会接外部依赖，所以更适合做“准备输入 -> 调用工具 -> 看输出是否合理”的测试。

### 2.3 API 层

适合测的接口：

- `GET /api/health`
- `POST /api/task`
- `POST /api/task/{thread_id}/cancel`
- `POST /api/upload`
- `GET /api/files`
- `GET /api/download`
- WebSocket 连接接口

这一层最适合写接口测试和集成测试。

### 2.4 端到端链路

适合测的完整场景：

- 输入数据库问题，返回结果并生成 Markdown
- 上传附件后让智能体读取并总结
- 触发网络搜索后返回摘要
- 触发 RAGFlow 后返回知识库结果
- 任务执行过程能通过 WebSocket 推送给前端

这一层通常不是写很多细碎断言，而是写“场景级”测试。

## 3. 如果要写测试类，建议怎么分

如果后面要补 `tests/` 目录，建议按下面的层级来分：

```text
tests/
├── unit/
│   ├── test_path_utils.py
│   ├── test_word_converter.py
│   ├── test_markdown_tools.py
│   └── test_health_schema.py
├── integration/
│   ├── test_api_health.py
│   ├── test_api_task.py
│   ├── test_api_upload.py
│   └── test_db_tools.py
├── e2e/
│   ├── test_db_question_flow.py
│   ├── test_file_upload_flow.py
│   └── test_websocket_monitor_flow.py
└── fixtures/
    ├── sample_md/
    ├── sample_docx/
    └── sample_xlsx/
```

### 3.1 `unit/`

适合放纯逻辑测试。

### 3.2 `integration/`

适合放依赖 FastAPI、数据库、文件系统的测试。

### 3.3 `e2e/`

适合放“真实运行一条链路”的测试。

### 3.4 `fixtures/`

适合放测试样本文件。

## 4. 推荐的测试骨架

如果后面要真正补测试骨架，我建议至少具备下面这些基础文件：

```text
tests/
├── conftest.py
├── unit/
│   ├── test_path_utils.py
│   ├── test_word_converter.py
│   └── test_markdown_tools.py
├── integration/
│   ├── test_api_health.py
│   └── test_api_task_smoke.py
└── e2e/
    └── test_db_query_flow.py
```

### 建议的骨架职责

- `conftest.py`
  - 放测试客户端、临时目录、环境变量替身、公共 fixture
- `unit/`
  - 放可重复、无外部依赖的测试
- `integration/`
  - 放接口和工具层联通测试
- `e2e/`
  - 放端到端验收场景

## 5. 这个项目里哪些地方现在更适合用日志

目前代码里已经有少量 `print` 和 `logging`，这说明它现在是“开发调试优先”的状态。

更推荐的策略是：

- `monitor` 负责业务事件流
- `logging` 负责系统日志
- `print` 只保留给 demo、脚本和极少量调试场景

### 5.1 适合保留 `print` 的地方

- 示例脚本
- 本地工具自测入口
- 教程演示代码

### 5.2 适合改成 `logging` 的地方

- API 入口和异常处理
- 工具失败
- 文件转换失败
- WebSocket 断开和异常
- 数据库查询失败
- 外部服务调用失败

### 5.3 适合继续用 `monitor` 的地方

- 工具开始执行
- 子智能体开始调用
- 任务结果输出
- 会话目录创建
- 任务取消

## 6. 部署后怎么验

部署后的验证建议按下面顺序：

1. 先看健康检查
2. 再看前端页面
3. 再跑数据库查询任务
4. 再看事件流
5. 再看输出文件
6. 最后看日志

### 6.1 第一层：健康检查

确认：

- 后端进程在
- LLM 配置在
- MySQL 配置在
- 可选服务按实际情况显示

### 6.2 第二层：接口联通

确认：

- `/api/task` 能启动任务
- `/api/upload` 能上传文件
- `/api/files` 能列文件
- `/api/download` 能下载结果

### 6.3 第三层：任务链路

确认：

- 主智能体能调用子智能体
- 事件流能推送到前端
- Markdown / PDF 能落盘

### 6.4 第四层：问题定位

如果出问题，按这个顺序查：

1. 环境变量
2. 健康检查
3. WebSocket
4. 外部服务
5. 文件目录
6. 日志

## 7. 后续可以直接补的内容

如果以后要把这份规划真正落地，建议补这几类文件：

- `tests/conftest.py`
- `tests/unit/`
- `tests/integration/`
- `tests/e2e/`
- `app/utils/` 下的纯逻辑单测
- `app/tools/` 下的工具测试
- `app/api/` 下的接口测试

## 8. 这份规划适合谁

- 想把项目从“能跑”变成“可验证”的人
- 想补测试骨架，但不想一开始就写太重的人
- 想先定测试层级，再开始落测试代码的人

## 8.1 相关说明页

如果你想继续往下看目录怎么拆，可以接着看：

- [测试目录树说明页](testing-skeleton-directory-guide.md)

## 9. 如果现在就开始落地，建议先做哪一批

如果你要把这份规划真正变成代码，建议先从“最稳、最容易写、收益最高”的部分开始。

### 第一批：纯逻辑单测

优先顺序：

1. `app/utils/path_utils.py`
2. `app/utils/word_converter.py`
3. `app/tools/markdown_tools.py`
4. `app/api/server.py` 里的健康检查返回结构

原因：

- 不依赖真实外部服务
- 容易 mock
- 回归收益高
- 最容易形成稳定的测试骨架

### 第二批：接口烟雾测试

优先顺序：

1. `/api/health`
2. `/api/upload`
3. `/api/task`
4. `/api/files`

原因：

- 能快速判断服务是否能起
- 能验证最核心的后端入口
- 对部署后的排错最有帮助

### 第三批：工具集成测试

优先顺序：

1. 文件生成工具
2. 文件读取工具
3. PDF 转换工具
4. 数据库查询工具

原因：

- 是项目能力的关键组成部分
- 一旦坏了，用户最容易感知

### 第四批：完整链路测试

优先顺序：

1. 数据库查询到结果文件生成
2. 上传附件到总结回答
3. 事件流推送到前端

原因：

- 这些是项目的“主卖点”
- 最能代表系统是否真正可用

## 10. 测试骨架命名建议

为了让未来的测试文件好维护，建议统一按下面规则命名：

- 单元测试文件：`test_*.py`
- 测试函数：`test_*`
- fixture：按作用命名，不要太抽象
- 场景测试：文件名里尽量带上业务场景，例如 `test_db_query_flow.py`

### 推荐命名风格

```text
tests/
├── unit/
│   ├── test_path_utils.py
│   ├── test_word_converter.py
│   └── test_markdown_tools.py
├── integration/
│   ├── test_api_health.py
│   └── test_api_task_smoke.py
└── e2e/
    └── test_db_query_flow.py
```

### 不太建议的命名

- `test1.py`
- `aaa.py`
- `temp_test.py`
- `final_final_test.py`

这类名字后面会很难维护，也不利于自动化筛选。

## 11. 骨架落地时的注意事项

1. 先把纯逻辑单测跑起来，再补外部依赖测试
2. 外部服务相关测试尽量做成可跳过
3. 对真实 MySQL / RAGFlow / Tavily 的测试，要准备独立环境变量
4. 前端联调不要和单元测试混在一起
5. 真实任务链路的测试，建议保留最少几个固定场景

## 12. 更具体的目录蓝图

如果后面真的要落测试代码，建议把目录再细分成“公共能力、单元、集成、端到端、样本”五层。

```text
tests/
├── conftest.py
├── helpers/
│   ├── __init__.py
│   ├── api_client.py
│   ├── env.py
│   └── sample_data.py
├── unit/
│   ├── test_path_utils.py
│   ├── test_word_converter.py
│   ├── test_markdown_tools.py
│   ├── test_pdf_tools.py
│   └── test_health_payload.py
├── integration/
│   ├── test_api_health.py
│   ├── test_api_upload.py
│   ├── test_api_task_smoke.py
│   ├── test_db_tools.py
│   └── test_ragflow_tools.py
├── e2e/
│   ├── test_db_query_flow.py
│   ├── test_file_upload_flow.py
│   └── test_websocket_monitor_flow.py
└── fixtures/
    ├── md/
    ├── docx/
    ├── xlsx/
    └── pdf/
```

### 12.1 `helpers/`

建议放公共测试辅助函数，不要直接把它当业务代码。

适合放：

- 创建 `TestClient`
- 读取测试 `.env`
- 构造假数据
- 创建临时文件
- 包装 WebSocket 连接

### 12.2 `unit/`

建议只测“本地纯逻辑”。

典型目标：

- `resolve_path`
- Markdown / PDF 处理的输入输出结构
- 返回值 schema
- 健康检查 payload 结构

### 12.3 `integration/`

建议只测“一个模块 + 它的依赖”。

典型目标：

- API 是否能跑通
- 工具是否能和外部服务交互
- 上传文件后是否能落盘
- 任务接口是否能触发后台协程

### 12.4 `e2e/`

建议只测“用户任务场景”。

典型目标：

- 生成数据库分析报告
- 上传附件并总结
- 任务执行过程推送事件

### 12.5 `fixtures/`

建议放固定样本文件，不要和测试逻辑混在一起。

典型内容：

- 小型 Markdown
- 小型 Word
- 小型 Excel
- 小型 PDF

## 13. 第一版骨架建议保留哪些最小文件

如果只想先做“最小可用测试骨架”，建议保留下面 8 个文件：

```text
tests/
├── conftest.py
├── helpers/
│   └── api_client.py
├── unit/
│   ├── test_path_utils.py
│   └── test_health_payload.py
├── integration/
│   ├── test_api_health.py
│   └── test_api_upload.py
└── e2e/
    └── test_db_query_flow.py
```

### 13.1 为什么先保留这几个

- `conftest.py` 是所有测试共享入口
- `api_client.py` 方便统一构造测试客户端
- `test_path_utils.py` 是最稳的纯逻辑测试
- `test_health_payload.py` 是最容易做的结构校验
- `test_api_health.py` 能最快判断服务是否活着
- `test_api_upload.py` 能验证文件链路
- `test_db_query_flow.py` 能覆盖最关键的业务主链路

## 14. 建议的落地节奏

如果后面真的开始写测试代码，建议按这个节奏：

1. 先把 `unit/` 做起来
2. 再补 `integration/`
3. 然后加一两个 `e2e/`
4. 最后再把不稳定的外部依赖测试补齐

这样可以避免一开始就把测试写得太重，导致后面难以维护。
