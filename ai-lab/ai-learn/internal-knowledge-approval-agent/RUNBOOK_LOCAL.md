# RUNBOOK_LOCAL

## 1. 本地运行目标

本轮验证的是一条完整的本地调用链：

```text
React
→ FastAPI
→ QuestionService
→ Workflow
→ Retriever
→ RiskClassifier
→ AnswerGenerator
→ Approval
→ SSE
→ React
```

LOW 问题应自动完成；HIGH 问题应停在人工审批，Approve 后完成，Reject 后终止。

## 2. 前提条件

逐条查看版本：

```bash
python3 --version
pip --version
node -v
npm -v
docker --version
```

Python 3、Node.js、npm 和 curl 是本地运行所需工具。Docker 仅供以后容器化使用，是可选项；`docker --version` 失败不影响本项目当前运行。

## 3. 进入项目目录

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/internal-knowledge-approval-agent
pwd
```

`pwd` 预期以 `/ai-learn/internal-knowledge-approval-agent` 结尾。若你的路径不同，在 VS Code 左侧资源管理器找到该项目，右键目录复制路径，再执行 `cd '复制的路径'`。

## 4. 检查环境

```bash
chmod +x scripts/*.sh
./scripts/check_env.sh
```

预期 `python3`、`node`、`npm`、`curl` 均显示 `OK`，最后显示 `Environment OK`。该脚本不检查 Docker，因为 Docker 不是当前运行依赖。

## 5. 启动 Backend

```bash
./scripts/start_backend.sh
```

首次运行会创建 `backend/.venv` 并安装 `backend/requirements.txt`。成功时可看到 `Application startup complete` 和 `Uvicorn running on http://127.0.0.1:8000`。Backend 地址是 `http://127.0.0.1:8000`，按 `Ctrl+C` 停止。

若提示端口 8000 被占用：

```bash
ss -ltnp | grep ':8000'
```

先关闭已有 Backend 终端，或根据输出确认占用进程后正常停止它，再重新运行脚本。不要同时启动两个 Backend 共用同一个 SQLite 文件。

## 6. 启动 Frontend

新开一个终端：

```bash
cd ~/workspace/vscode_study/ai-lab/ai-learn/internal-knowledge-approval-agent
./scripts/start_frontend.sh
```

首次运行会执行 `npm install`。成功时可看到 `VITE ... ready` 和 `Local: http://127.0.0.1:5173/`。Frontend 地址是 `http://127.0.0.1:5173`，按 `Ctrl+C` 停止。

若端口 5173 被占用：

```bash
ss -ltnp | grep ':5173'
```

关闭已有 Vite 终端后重启。当前脚本和 CORS 配置以 5173 为准，不建议初学阶段临时改端口。

## 7. Health Check

```bash
curl -sS -i http://127.0.0.1:8000/health
```

当前响应正文示例：

```json
{"status":"ok","service":"internal-knowledge-approval-agent"}
```

- `status`：`ok` 表示 FastAPI 可处理请求。
- `service`：当前服务名。
- `provider`：当前接口没有返回该字段；本地固定文档 Provider 的边界见第 16 节。
- `request_id`：当前不在 Health JSON 正文中，而在响应头 `X-Request-ID`，所以这里使用 `-i` 查看响应头。

## 8. LOW 风险流程测试

```bash
curl -sS -X POST http://127.0.0.1:8000/api/questions \
  -H 'Content-Type: application/json' \
  -d '{"question":"休暇申請の手順を確認したい","department":"sales"}'
```

从 JSON 的 `data.question_id` 复制 UUID，以下用 `<question_id>` 表示。当前 Schema 只读取 `question`，示例中的 `department` 是兼容性输入，当前版本不会保存它。

查询状态：

```bash
curl -sS http://127.0.0.1:8000/api/questions/<question_id>
```

读取报告：

```bash
curl -sS http://127.0.0.1:8000/api/questions/<question_id>/report
```

LOW 预期：`risk_level` 为 `LOW`、`status` 为 `completed`、`approval_id` 为 `null`，报告可直接读取。

## 9. HIGH 风险流程测试

```bash
curl -sS -X POST http://127.0.0.1:8000/api/questions \
  -H 'Content-Type: application/json' \
  -d '{"question":"個人情報の取扱手順を確認したい","department":"sales"}'
```

复制新的 `data.question_id` 并查询：

```bash
curl -sS http://127.0.0.1:8000/api/questions/<question_id>
```

HIGH 预期：`risk_level` 为 `HIGH`，`status` 为 `approval_required`。原因是问题命中确定性风险策略。当前关键词包括：`契約`、`個人情報`、`セキュリティ`、`経費`、`法務`、`障害対応`、`退職`、`給与`，以及代码中的少量同义词。

## 10. Approve 测试

```bash
curl -sS -X POST http://127.0.0.1:8000/api/approvals/<question_id>/approve \
  -H 'Content-Type: application/json' \
  -d '{"approver":"manager01","comment":"確認済みです"}'
```

当前接口按 `question_id` 审批；请求体暂未建模，因此 `approver` 和 `comment` 不会持久化。Approve 后再次查询问题，预期 `status` 为 `completed`，报告可读取：

```bash
curl -sS http://127.0.0.1:8000/api/questions/<question_id>
curl -sS http://127.0.0.1:8000/api/questions/<question_id>/report
```

## 11. Reject 测试

先创建另一个 HIGH 问题；同一个问题只能审批一次。然后执行：

```bash
curl -sS -X POST http://127.0.0.1:8000/api/approvals/<question_id>/reject \
  -H 'Content-Type: application/json' \
  -d '{"approver":"manager01","reason":"法務確認が必要です"}'
```

Reject 后查询问题，预期 `status` 为 `rejected`：

```bash
curl -sS http://127.0.0.1:8000/api/questions/<question_id>
```

当前版本不保存 `approver` 或 `reason`，因此状态只能看到 `rejected`，不能看到拒绝理由；Rejected 问题没有正式报告，读取 report 会返回 `REPORT_NOT_READY`。这是当前实现边界，不是操作失败。

## 12. SSE 测试

建议在提交问题前或审批前新开终端订阅；已有事件也会从 SQLite 按顺序回放：

```bash
curl -sS -N http://127.0.0.1:8000/api/questions/<question_id>/events
```

事件含义：

- `received`：问题已接收并保存。
- `risk_checked`：风险关键词检查完成。
- `answer_generated`：固定模板回答已生成。
- `approval_required`：HIGH 问题等待人工决策。
- `approved`：审批通过，Workflow 恢复生成正式报告。
- `rejected`：审批拒绝，流程终止。
- `completed`：正式报告已保存，可读取 report。
- `error`：Workflow 执行失败，查看 `error_code` 和 Backend 日志。

LOW 常见顺序是 `received → risk_checked → answer_generated → completed`；HIGH Approve 是 `received → risk_checked → approval_required → approved → answer_generated → completed`；HIGH Reject 以 `rejected` 结束。

## 13. Frontend 操作测试

1. 打开 `http://127.0.0.1:5173`。
2. 输入 LOW 问题并点击提交。
3. 查看 SSE 状态时间线。
4. 确认最终回答显示。
5. 返回问题提交页，输入 HIGH 问题。
6. 确认页面进入审批列表并显示审批按钮。
7. 创建一个 HIGH 问题并点击 **Approve**，确认结果出现。
8. 再创建一个 HIGH 问题并点击 **Reject**，确认状态为 rejected。
9. 可停止 Backend 后再提交，确认错误提示区域正常显示。

Approve 和 Reject 必须使用两个不同问题，因为每个问题只允许一次审批决定。

## 14. 日志查看方法

日志直接输出在运行 `./scripts/start_backend.sh` 的终端中，每行是 JSON。重点字段：

- `request_id`：一次 HTTP 请求的关联 ID。
- `question_id`：同一个问题跨请求和 Workflow 的业务 ID。
- `event`：发生了什么，例如 `question_status_transition`。
- `status`：该时点状态。
- `error_code`：无错误时为 `null`。
- `duration_ms`：Workflow 耗时；不适用的日志可能为 `null`。

追踪方法：先从 POST 响应复制 `question_id`，再在 Backend 终端搜索同一 UUID。VS Code 终端可用 `Ctrl+F` 搜索；若把日志保存到文件，可执行：

```bash
grep '<question_id>' backend.log
```

按日志顺序即可看到 received、风险检查、审批和完成/拒绝的整条流程。`request_id` 会随每次 HTTP 请求改变，而 `question_id` 在同一业务流程中保持不变。

## 15. 常见错误排查

### ModuleNotFoundError

- 原因：不在项目目录启动、虚拟环境未创建，或依赖安装中断。
- 解决：回到项目根目录运行 `./scripts/start_backend.sh`；必要时确认 `backend/.venv/bin/python` 存在。
- 验证：`curl -sS http://127.0.0.1:8000/health` 返回 `status: ok`。

### uvicorn command not found

- 原因：直接执行了系统 `uvicorn`，但依赖安装在项目虚拟环境。
- 解决：使用 `./scripts/start_backend.sh`，不要直接运行 `uvicorn`。
- 验证：终端出现 `Uvicorn running on http://127.0.0.1:8000`。

### port 8000 already in use

- 原因：已有 Backend 或其他进程监听 8000。
- 解决：运行 `ss -ltnp | grep ':8000'`，关闭旧进程后重启。
- 验证：Health Check 返回 200。

### npm install 失败

- 原因：网络、npm registry、代理或 Node/npm 版本问题。
- 解决：先运行 `node -v`、`npm -v`、`npm config get registry`，修复网络/代理后在 `frontend` 目录运行 `npm install`。
- 验证：`cd frontend && npm test && npm run build` 全部通过。

### Vite 页面打不开

- 原因：Frontend 未启动、5173 被占用，或访问了错误地址。
- 解决：确认 Vite 终端仍运行，并检查 `ss -ltnp | grep ':5173'`。
- 验证：`curl -I http://127.0.0.1:5173` 返回 HTTP 200。

### CORS error

- 原因：Frontend 不是从 `localhost:5173` 或 `127.0.0.1:5173` 访问，或 Backend 未运行。
- 解决：使用文档规定地址启动两端，不要用随机 Vite 端口。
- 验证：浏览器 Network 中 `/api/questions` 不再被 CORS 拦截。

### question_id not found

- 原因：复制错误、使用了旧数据库之外的 ID，或误把 `approval_id` 当成 `question_id`。
- 解决：重新 POST 创建问题，复制 `data.question_id`。
- 验证：GET `/api/questions/<question_id>` 返回 `success: true`。

### approval_id 找不到

- 原因：公开 Approve/Reject URL 需要的是 `question_id`，不是响应中的 `approval_id`；LOW 问题也没有审批记录。
- 解决：使用 HIGH 问题的 `question_id` 调用 `/api/approvals/<question_id>/approve|reject`。
- 验证：响应 `data.status` 为 `approved` 或 `rejected`。

### SSE 没有输出

- 原因：ID 错误、Backend 未运行、未使用 `-N`，或事件流正等待 HIGH 审批。
- 解决：确认问题存在并使用 `curl -sS -N`；HIGH 流程在另一个终端执行 Approve/Reject。
- 验证：至少看到 `event: received` 和 `event: risk_checked`。

### report not found

- 原因：问题尚未 completed，HIGH 问题仍待审批，或已 rejected。
- 解决：先查询状态；approval_required 则审批，rejected 则重新创建问题。
- 验证：completed 后 report API 返回 `success: true`。

### Docker CLI not found

- 原因：本机未安装 Docker。
- 解决：当前本地流程无需处理；跳过 Docker 命令即可。只有未来需要容器运行时才安装 Docker。
- 验证：`./scripts/check_env.sh` 仍显示 `Environment OK`。

## 16. 当前实现边界

- 不接真实 LLM。
- 不接 OpenAI。
- 不接 PostgreSQL。
- 不接 Redis。
- 不接 RabbitMQ。
- 文档检索使用 `LocalStaticDocumentProvider` 这一角色的本地静态实现；当前代码对应 `backend/app/rag/documents.py` 和 `retrieve_documents()`，没有同名类。
- Repository 当前使用 SQLite 本地文件实现。
- `department`、`approver`、审批 comment/reason 当前不持久化。
- Health 当前只在正文返回 `status`、`service`，请求 ID 位于 `X-Request-ID` 响应头。
- 风险路由、审批状态转换、事件持久化、SSE 和报告读取是可实际运行的核心业务流程。
