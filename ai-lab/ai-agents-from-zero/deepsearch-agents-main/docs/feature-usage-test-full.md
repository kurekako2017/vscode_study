# 功能使用与测试完整版

> 这份文档适合你真的要做功能验收、演示或排错时使用。  
> 每个功能都固定写成：功能说明、测试命令、推荐截图、预期结果、排错点。

## 0. 可直接复用的示例截图

你可以先把这几张现成图片当作参考：

- 前端首页示例图：[deepsearch-agent-home.jpg](images/deepsearch-agent-home.jpg)
- 数据库结果示例图：[deepsearch-database-report-result.jpg](images/deepsearch-database-report-result.jpg)
- 网络搜索结果示例图：[deepsearch-network-search-result.jpg](images/deepsearch-network-search-result.jpg)
- 系统架构图：[deepsearch-system-architecture.svg](images/deepsearch-system-architecture.svg)

如果你后面补自己的截图，建议命名成：

- `health-check-result.png`
- `frontend-home.png`
- `db-query-result.png`
- `network-search-result.png`
- `ragflow-result.png`
- `file-upload-result.png`

## 0.1 截图编号建议

如果你要把这份文档做成“验收版”，建议按下面编号补图：

- 截图 1：后端健康检查
- 截图 2：前端健康面板
- 截图 3：数据库查询结果
- 截图 4：网络搜索结果
- 截图 5：RAGFlow 结果
- 截图 6：文件上传与读取
- 截图 7：结果文件生成
- 截图 8：完整联调流程

## 1. 后端健康检查

### 1.1 功能说明

- 检查 FastAPI 后端是否存活。
- 同时返回模型、MySQL、Tavily、RAGFlow 的配置状态。

### 1.2 测试命令

```bash
curl http://127.0.0.1:8000/api/health
```

### 1.3 推荐截图

- 浏览器打开 `http://127.0.0.1:8000/api/health` 的响应页面
- 或者终端中 `curl` 返回的 JSON 输出

### 1.4 预期结果

- 返回 `status=ok`
- `backend=alive`
- `llm.configured=true`
- `mysql.configured=true`
- `services.tavily` 和 `services.ragflow` 按实际配置显示

### 1.5 验收看点

- 能不能正常返回 JSON
- 配置状态能不能正确反映 `.env`

### 1.6 排错点

- 后端是否真的启动
- `.env` 是否已加载
- OpenRouter key 是否有效
- NAS MySQL 是否可达

## 2. 前端健康面板

### 2.1 功能说明

- 展示系统状态、任务输入区、事件流和结果区。

### 2.2 测试命令

```bash
cd ai-lab/ai-agents-from-zero/deepsearch-agents-main/frontend
npm install
npm run dev
```

### 2.3 推荐截图

- 前端首页健康面板
- 推荐参考图：[deepsearch-agent-home.jpg](images/deepsearch-agent-home.jpg)

### 2.4 预期结果

- 页面可以正常打开
- 能看到健康状态
- 能看到任务输入框
- 能看到事件流和结果区域

### 2.5 验收看点

- 页面是否白屏
- 健康状态是否正常显示
- 是否能看见与后端联动的数据

### 2.6 排错点

- 前端是否启动成功
- 后端 `/api/health` 是否可访问
- 前端是否指向正确的后端地址

## 3. 数据库查询助手

### 3.1 功能说明

- 通过 NAS MySQL 查询结构化业务数据。
- 适合药品、库存、销售、分类统计等场景。

### 3.2 测试命令

```text
请直接查询 drugs 表中 therapeutic_area 为 心血管 的药品，并用 Markdown 表格输出名称、品牌、规格、厂家和简介，直接给出结果，不要向我提问。
```

### 3.3 推荐截图

- 前端事件流里出现数据库工具调用的截图
- 最终回答表格截图
- 结果文件预览截图
- 推荐参考图：[deepsearch-database-report-result.jpg](images/deepsearch-database-report-result.jpg)

### 3.4 预期结果

- 返回与数据库一致的数据
- 结果通常是 Markdown 表格
- 输出目录下生成结果文件

### 3.5 验收看点

- 事件流里是否出现数据库相关工具调用
- 表格内容是否和数据库一致
- 是否生成了结果文件

### 3.6 排错点

- `MYSQL_HOST=192.168.10.2`
- `MYSQL_PORT=3306`
- `MYSQL_USER=root`
- `MYSQL_PASSWORD=123456`
- `MYSQL_DATABASE=ecommjava`

## 4. 网络搜索助手

### 4.1 功能说明

- 用来搜索公开互联网资料。
- 适合新闻、行业趋势、政策和网页内容。

### 4.2 测试命令

```text
搜索 2026 年 AI 在电商行业的应用趋势，并总结 3 个重点。
```

### 4.3 推荐截图

- 前端事件流里出现搜索工具调用的截图
- 搜索结果摘要截图
- 推荐参考图：[deepsearch-network-search-result.jpg](images/deepsearch-network-search-result.jpg)

### 4.4 预期结果

- 有 key 时返回搜索结果
- 最终回答会总结重点
- 搜索结果里能看到来源或摘要

### 4.5 验收看点

- 是否真的调用了网络搜索
- 结果是否包含外部来源
- 总结是否和搜索结果一致

### 4.6 排错点

- `TAVILY_API_KEY` 是否存在
- 账号额度是否可用
- 网络是否通

## 5. RAGFlow 助手

### 5.1 功能说明

- 查询内部知识库或私有文档。
- 适合制度、文档、研报、内部说明。

### 5.2 测试命令

```text
请根据内部知识库总结电商行业 AI 应用的 3 个核心趋势。
```

### 5.3 推荐截图

- 前端事件流里出现 RAGFlow 调用的截图
- 最终回答截图
- 如果你后面接上真实知识库，可以补一张“知识库返回结果”的截图

### 5.4 预期结果

- 配置正常时返回知识库问答结果
- 未配置时返回友好提示
- 不影响主流程继续执行

### 5.5 验收看点

- 是否真的走到 RAGFlow 工具
- 未配置时是否优雅降级

### 5.6 排错点

- RAGFlow 服务是否在线
- API URL 是否正确
- API key 是否可用

## 6. 文件上传与读取

### 6.1 功能说明

- 上传用户文件并在任务中读取内容。
- 适合 PDF、Word、Excel、Markdown、文本文件。

### 6.2 测试命令

1. 先上传一个文件
2. 再输入：

```text
请先读取我上传的文件，然后总结主要内容。
```

### 6.3 推荐截图

- 文件上传控件截图
- 上传成功后的附件列表截图
- 智能体引用文件内容的回答截图

### 6.4 预期结果

- 文件被保存到会话目录
- 智能体能读到文件内容
- 最终回答和附件内容一致

### 6.5 验收看点

- 上传后文件是否可见
- 回答是否明显引用了附件内容
- 附件是否进入当前会话目录

### 6.6 排错点

- 上传接口是否正常
- 文件格式是否支持
- 会话目录是否创建成功

## 7. 结果文件生成

### 7.1 功能说明

- 将任务结果保存成 Markdown 或其他文件。

### 7.2 测试命令

```text
请整理一份心血管药品报告，并保存为 Markdown 文件。
```

### 7.3 推荐截图

- 生成完成后的文件列表截图
- 输出目录 `app/output/session_{thread_id}` 的截图
- 文件内容预览截图

### 7.4 预期结果

- 在 `app/output/session_{thread_id}` 下出现 `.md` 文件
- 文件内容和任务主题一致

### 7.5 验收看点

- 是否真的执行到了文件生成步骤
- 结果文件内容是否可读
- 文件名是否能看出任务主题

### 7.6 排错点

- 输出目录权限是否正常
- 任务有没有提前异常结束
- 文件生成逻辑是否有报错

## 8. 一次完整联调怎么测

如果你想一次把主链路跑通，推荐按这个顺序测：

1. `/api/health`
2. 前端页面
3. 数据库查询助手
4. 文件上传与读取
5. 结果文件生成

如果这 5 个都通过，说明：

- 后端活着
- 前端能连后端
- MySQL 能查
- 文件能处理
- 结果能落盘

## 9. 常见失败点

### 9.1 健康检查报错

- 优先看 `.env`
- 再看后端是否重启
- 再看 OpenRouter key

### 9.2 数据库查询失败

- 优先看 NAS MySQL 是否能连
- 再看表名和字段名是否写对

### 9.3 前端页面空白

- 优先看前端是否启动
- 再看后端接口是否可访问

### 9.4 文件不生成

- 优先看任务有没有正常结束
- 再看输出目录是否存在

## 10. 你后面怎么继续补

如果你以后还要新增功能，继续按这个结构写就行：

1. 功能说明
2. 测试命令
3. 推荐截图
4. 预期结果
5. 验收看点
6. 排错点
