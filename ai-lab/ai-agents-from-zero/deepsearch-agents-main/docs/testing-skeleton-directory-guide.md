# 测试目录树说明页

> 这份文档专门解释“测试骨架应该怎么摆目录、每个目录放什么、哪些地方先 mock、哪些地方保留真实依赖”。
> 它是 [测试方案与测试骨架规划](testing-strategy-and-skeleton.md) 的下一层细化说明。

## 1. 先看结论

如果后面要开始补测试代码，建议按下面这个结构起步：

```text
tests/
├── conftest.py
├── helpers/
├── unit/
├── integration/
├── e2e/
└── fixtures/
```

这个结构的目标很简单：

1. 先把纯逻辑测住
2. 再把接口和工具链测住
3. 最后把完整任务链路测住

## 2. 为什么要这样分

这个项目不是单纯的函数库，它包含：

- FastAPI 接口
- WebSocket 推送
- 多智能体调度
- MySQL 查询
- 本地知识库查询
- 文件上传和文件生成

如果把所有测试都塞在一个目录里，后面会很难维护。

所以要按“测试层级”来分：

- `unit/` 负责纯逻辑
- `integration/` 负责模块联通
- `e2e/` 负责完整场景
- `fixtures/` 负责样本文件
- `helpers/` 负责公共辅助代码

## 3. 目录树总览

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
│   └── test_local_kb_tools.py
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

## 4. 每个目录放什么

### 4.1 `conftest.py`

`conftest.py` 是整个测试体系的公共入口。

建议放：

- `TestClient`
- 临时目录 fixture
- 假环境变量 fixture
- 会话 ID fixture
- 样本文件准备函数

不要把业务逻辑写进来。

### 4.2 `helpers/`

`helpers/` 是测试辅助工具，不是业务代码。

建议放：

- 构造 API 请求的 helper
- 构造 WebSocket 连接的 helper
- 构造临时文件的 helper
- 构造假返回值的 helper
- 测试环境变量的 helper

### 4.3 `unit/`

`unit/` 只测本地纯逻辑，不碰真实外部服务。

适合测试：

- 路径解析
- 返回值 schema
- Markdown / PDF 输入输出格式
- 健康检查 JSON 结构
- 文件命名规则

### 4.4 `integration/`

`integration/` 测的是“模块 + 依赖”的组合。

适合测试：

- FastAPI 接口是否能启动
- 上传接口是否能保存文件
- 任务接口是否能触发后台流程
- MySQL 工具是否能连通
- 本地知识库工具是否能返回结果

### 4.5 `e2e/`

`e2e/` 是最接近真实用户场景的测试层。

适合测试：

- 输入数据库问题，输出报告文件
- 上传附件后让智能体总结
- 任务执行过程通过 WebSocket 推送

### 4.6 `fixtures/`

`fixtures/` 放固定样本，不要把它当测试逻辑。

建议样本：

- 小 Markdown
- 小 Word
- 小 Excel
- 小 PDF

## 5. 第一批建议先写哪些

如果是第一次补测试骨架，建议先写最小的一批：

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

### 为什么先写这几个

- `test_path_utils.py`
  - 最容易稳定
  - 最适合先验证纯逻辑
- `test_health_payload.py`
  - 适合先把返回结构校验做起来
- `test_api_health.py`
  - 一眼就能看出服务活没活
- `test_api_upload.py`
  - 能验证文件链路
- `test_db_query_flow.py`
  - 能覆盖最关键的业务链路

## 6. 哪些地方先 mock，哪些地方保留真实依赖

### 6.1 先 mock 的地方

先 mock 的意思是：先不连真实外部服务，只验证本地逻辑。

建议先 mock：

- LLM 调用
- MySQL 连接
- 本地知识库调用
- Tavily 搜索
- 文件转换外部依赖

### 6.2 保留真实依赖的地方

保留真实依赖的意思是：这些地方最终要做一次真实联通验证。

建议保留真实验证：

- `/api/health`
- `/api/upload`
- `/api/task`
- `db_tools`
- `read_file_content`
- `generate_markdown`

### 6.3 推荐策略

最稳的做法是：

1. 单元测试尽量 mock
2. 集成测试只连少量真实依赖
3. E2E 测试保留关键真实链路

## 7. 以后可以怎么扩展

如果后面测试越来越多，可以继续加这些目录：

```text
tests/
├── unit/
├── integration/
├── e2e/
├── smoke/
├── contract/
└── performance/
```

### 7.1 `smoke/`

放最小烟雾测试，比如启动后先确认服务没挂。

### 7.2 `contract/`

放前后端接口契约测试，避免接口字段改坏。

### 7.3 `performance/`

放简单的性能基线，比如任务响应时间、文件生成时间。

## 8. 目录设计的原则

1. 先保证容易读
2. 再保证容易维护
3. 再保证容易扩展
4. 不要一开始就把测试写得太复杂

## 9. 和现有文档的关系

- [文档总目录](docs-index.md)
- [当前工作区运行指南](workspace-run-guide.md)
- [功能使用与测试最短版](feature-usage-test-template.md)
- [功能使用与测试完整版](feature-usage-test-full.md)
- [测试方案与测试骨架规划](testing-strategy-and-skeleton.md)
