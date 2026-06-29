# Internal Knowledge Approval Agent 学习计划 Day1～Day5

每天先进入项目目录：

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/internal-knowledge-approval-agent
```

## Day1：项目运行

### 目标

- 启动 Backend。
- 启动 Frontend。
- 跑通 LOW / HIGH。
- 看懂日志。

### 任务

1. 执行 `./scripts/check_env.sh`。
2. 执行 `./scripts/start_backend.sh`。
3. 新终端执行 `./scripts/start_frontend.sh`。
4. 提交 LOW 问题并读取 report。
5. 提交 HIGH 问题并确认 approval_required。
6. 用两个 HIGH 问题分别测试 Approve / Reject。

### 完成标准

能用自己的话解释 LOW 为什么直接 completed，HIGH 为什么需要审批；能从日志中找到 `question_id`。

## Day2：后端入口

### 学习

- `backend/app/main.py`
- `backend/app/api/routes/questions.py`
- `backend/app/api/routes/approvals.py`

按一次请求顺序寻找：FastAPI 如何匹配 Route、Schema 如何校验、依赖注入如何取得 Service、异常如何变成统一响应。

### 完成标准

能解释 API 如何进入 Service，并能说出创建、查询、审批和 report 的 URL 分别由哪个 Route 处理。

## Day3：业务层与 Workflow

### 学习

- `backend/app/services/question_service.py`
- `backend/app/services/approval_service.py`
- `backend/app/workflow/graph.py`
- `backend/app/workflow/nodes.py`

画出 LOW、HIGH Approve、HIGH Reject 三条状态线，重点区分 Graph state、SQLite state 和 SSE event。

### 完成标准

能解释状态如何从 received 流转到 completed/approval_required/rejected，以及审批后为什么能恢复 Workflow。

## Day4：RAG 与审批

### 学习

- `backend/app/rag/retriever.py`
- `backend/app/rag/documents.py`
- `backend/app/approval/policy.py`
- `backend/app/agents/answer_generator.py`

确认 Retriever 返回哪些固定文档、关键词如何判断 HIGH、报告如何组合风险与审批说明。

### 完成标准

能解释为什么高风险问题不能直接回答，并明确当前 Retriever 和 AnswerGenerator 都是确定性本地实现，不调用 LLM。

## Day5：前端与 SSE

### 学习

- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- SSE 时间线
- Approve / Reject UI

跟踪 `submit()`、`watch()`、`decide()`，观察 EventSource 收到不同 event 后怎样更新 view、status、events、report 和 error。

### 完成标准

能解释前端如何接收状态并展示结果；能指出 completed、approval_required、rejected、error 各自触发什么 UI 行为。

## Day6 以后

建议按一次只改一个点的方式继续：

- 新增一个高风险关键词，并补测试。
- 新增一个社内文档，并确认报告引用。
- 新增一个错误路径测试。
- 修改报告模板，并验证 LOW 与 approved HIGH。
- 准备 3 分钟面试说明：业务问题、调用链、风险审批、当前边界、下一步改进。
