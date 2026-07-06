# 启动与排错指南

这份文档用于本地启动 Retail Insight AI，并区分 Swagger、ReDoc、OpenAPI JSON、unittest、前后端联调各自的作用。

## 三个文档入口不是同一个用途

- Swagger 是 API 调试与验证工具。
- ReDoc 是 API 阅读文档。
- OpenAPI JSON 是机器可读接口定义。
- 三者不是同一个用途。
- UI 完成后 Swagger 仍然可用于后端验证。
- Swagger 和 React 调用的是同一套 FastAPI API。

## 企业项目验证体系

Swagger（FastAPI 自动生成的 API 调试与验证工具）

项目验证体系分四层：

| 层级 | 工具 | 目的 |
|---|---|---|
| 单元测试（Unit Test） | python -m unittest | 验证单个模块或类的逻辑是否正确 |
| 接口验证（API Verification） | Swagger UI (/docs) | 手工验证 API 请求、响应和业务流程 |
| 前后端集成测试（Integration Test） | React + FastAPI | 验证完整用户操作流程 |
| 端到端测试（E2E Test） | Playwright / Cypress | 模拟真实用户完成整个业务流程 |

补充说明：

- Swagger 不是测试环境。
- Swagger 不是正式 UI。
- Swagger 是 API 调试与验证工具。
- 当前阶段主要用 Swagger 验证后端骨架。
- UI 完成后再做前后端 Integration Test。
- 发布前再考虑 E2E Test。

## 推荐启动顺序

1. 在项目根目录执行 `./scripts/check_env.sh`。
2. 在项目根目录执行 `./scripts/start_backend.sh`。
3. 打开 `http://127.0.0.1:8000/docs` 看 Swagger。
4. 打开 `http://127.0.0.1:8000/redoc` 看 ReDoc。
5. 打开 `http://127.0.0.1:8000/openapi.json` 看 OpenAPI JSON。
6. 如需前端联调，再执行 `./scripts/start_frontend.sh`。

## 如果要直接看后端原始输出

```bash
cd backend
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

这样做适合观察最原始的 FastAPI 启动日志和异常堆栈。

## Swagger / ReDoc / OpenAPI JSON 的使用方式

### Swagger

用途：手工执行接口，验证请求、响应和业务流程。

推荐先点：

1. `GET /health`
2. `POST /api/tasks`
3. `GET /api/tasks/{task_id}`
4. `GET /api/tasks/{task_id}/report`

### ReDoc

用途：阅读字段结构和响应模型，不适合高频点击调试。

### OpenAPI JSON

用途：确认接口定义是否真的注册，适合做合同检查和工具接入。

## unittest 执行规则

测试命令必须在 `backend` 目录执行：

```bash
cd backend
python3 -m unittest discover -s tests -v
```

单文件执行方式：

```bash
cd backend
python3 -m unittest tests.test_api -v
```

不要在项目根目录直接执行：

```bash
python3 -m unittest tests.test_api -v
```

如果出现 `ModuleNotFoundError: No module named tests`，说明执行目录错了，不要先怀疑测试代码本身。

## 常见问题

### Swagger 打不开

先确认后端是否真的启动，再确认访问的是 `127.0.0.1:8000/docs`。

### ReDoc 打不开

说明后端可能没起来，或者路由未正常注册。先回头验证 `/health`。

### openapi.json 打不开

优先怀疑后端启动失败、接口注册失败或访问地址错误。

### unittest 找不到 tests

大概率是因为你不在 `backend/` 目录里执行。

### 审批或安全接口是空的

先确认你不是在空白进程里刚启动后立即读取；再看 `docs/LEARNING_API_WALKTHROUGH.md` 的推荐执行顺序。

## 推荐验证顺序

```text
Swagger
→ 主链路 API
→ 文档链路 API
→ 审批 / 安全 / 审计 API
→ backend unittest
→ React + FastAPI 联调
```

# Appendix A: 初学者本地启动顺序

这一章专门给第一次跑 `retail-insight-ai` 的同学看，目标是先把后端稳定启动起来，再逐步检查文档、前端和测试。

## 1. 进入项目根目录

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai
```

为什么这样做：

- 所有相对路径命令都以项目根目录为基准。
- `backend/requirements.txt`、`docs/learning/RUNBOOK_LOCAL.md`、`scripts/` 都是在根目录下组织的。

## 2. 创建 `.venv`

```bash
python3 -m venv .venv
```

为什么这样做：

- 把项目依赖和系统 Python 隔离开。
- 新手最常见的问题就是“装过依赖，但不是装到当前解释器里”。

## 3. 激活 `.venv`

```bash
source .venv/bin/activate
```

激活成功后，命令行一般会出现 `(.venv)` 前缀。

## 4. 升级 `pip`

```bash
python -m pip install --upgrade pip
```

为什么这样做：

- 新版 `pip` 更容易正确安装 `fastapi`、`uvicorn`、`python-multipart` 这类依赖。
- 遇到奇怪安装失败时，先升级 `pip` 往往最省时间。

## 5. 安装依赖

```bash
cd backend
python -m pip install -r requirements.txt
```

为什么这样做：

- 后端依赖集中写在 `backend/requirements.txt`。
- 这一步会把 `python-multipart`、`fastapi`、`uvicorn` 等后端启动所需包装进当前 `.venv`。

## 6. 检查关键依赖

```bash
python -m pip show fastapi uvicorn python-multipart
python -c "import fastapi, uvicorn, multipart; print('dependency check ok')"
```

为什么这样做：

- `pip show` 可以确认包是否真的装进当前环境。
- `import multipart` 可以直接验证 `python-multipart` 是否可被当前 Python 解释器找到。

## 7. 检查 `.env`

```bash
cd ..
test -f .env && echo ".env exists" || echo ".env missing, copy from .env.example if needed"
```

如果需要初始化：

```bash
cp .env.example .env
```

为什么这样做：

- 后端启动时会读取环境配置。
- 即使当前阶段很多功能是本地静态实现，保留 `.env` 习惯也能避免后续扩展时踩坑。

## 8. 启动 Backend

```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

为什么这样做：

- 这是当前项目约定的本地启动方式。
- 从 `backend/` 目录执行，可以确保 `app.main:app` 的导入路径正确。

## 9. 验证 `/health`

```bash
curl -s http://127.0.0.1:8000/health
```

预期：

- 返回 200。
- 返回体里能看到健康状态信息。

## 10. 打开 Swagger / ReDoc / OpenAPI

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
http://127.0.0.1:8000/openapi.json
```

为什么这样做：

- Swagger 用于交互调试。
- ReDoc 用于阅读接口结构。
- OpenAPI JSON 用于检查接口合同是否正确注册。

## 11. 可选：启动 Frontend

```bash
cd ../frontend
npm install
npm run dev
```

为什么这样做：

- 当前阶段前端是可选的，本地学习可以先把后端跑通。
- 先验证后端，再联调前端，更容易判断问题出在哪一层。

## 12. 可选：运行 `unittest`

```bash
cd ../backend
python -m unittest discover -s tests -v
```

为什么这样做：

- 单元测试是后端最稳定的回归保护。
- 如果启动成功但测试失败，就说明是业务逻辑或接口行为问题，不是纯启动问题。

# Appendix B: 常见启动错误与修复

## 1. `python-multipart` 未安装

现象：

- 启动时出现 `RuntimeError: Form data requires "python-multipart" to be installed.`
- 访问上传接口相关路由时直接报错。

原因：

- `FastAPI` 处理 `UploadFile`、`Form(...)` 时需要 `python-multipart`。
- 依赖没有装进当前 `.venv`，或者 `requirements.txt` 没有声明这个包。

检查命令：

```bash
cd backend
python -m pip show python-multipart
python -c "import multipart; print('ok')"
```

修复命令：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai
source .venv/bin/activate
cd backend
python -m pip install -r requirements.txt
```

## 2. `ModuleNotFoundError`

现象：

- 启动时提示 `ModuleNotFoundError: No module named 'app'`。
- 或者提示找不到某个后端模块。

原因：

- 你可能在错误目录执行命令。
- 也可能没有激活 `.venv`，导致解释器环境不对。

检查命令：

```bash
pwd
python -c "import sys; print(sys.executable)"
```

修复命令：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai/backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

# Appendix C: Quick Start（1 Minute Quick Start）

第一次 Clone 项目后，先直接照着执行下面这组命令。

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

启动后立刻做最小健康检查：

```bash
curl http://127.0.0.1:8000/health
```

再打开 Swagger：

```text
http://127.0.0.1:8000/docs
```

# Appendix D: Startup Flow

```text
Project Root
↓
Create .venv
↓
Activate .venv
↓
Install Requirements
↓
Check .env
↓
Start Backend
↓
GET /health
↓
Swagger /docs
↓
Run Tests
↓
Frontend (Optional)
```

# Appendix E: Startup Checklist

第一次运行时，可以逐项勾选。

- [ ] Python 已安装
- [ ] 项目根目录已进入
- [ ] `.venv` 已创建
- [ ] `.venv` 已激活
- [ ] `requirements.txt` 已安装
- [ ] `.env` 已存在
- [ ] Backend 已启动
- [ ] `GET /health` 返回 200
- [ ] Swagger 可打开
- [ ] ReDoc 可打开
- [ ] `openapi.json` 可打开
- [ ] `python -m unittest discover -s tests -v` 通过
- [ ] 前端已按需启动

# Appendix F: WSL + VSCode 使用建议

- 本项目建议优先使用 WSL Ubuntu 里的 Python，而不是 Windows 系统 Python。
- 不要混用 Windows Python 和 WSL Python，否则 `.venv`、`pip`、`uvicorn`、`python -m unittest` 可能指向不同环境。
- 检查当前 Python：

```bash
which python
python -V
python -c "import sys; print(sys.executable)"
```

- 检查当前 pip：

```bash
which pip
python -m pip -V
```

- 确认 VSCode 使用的是 `.venv`：

```bash
which python
python -m pip -V
```

如果输出路径在项目 `.venv` 下，通常就是对的。

- VSCode Terminal 建议从项目根目录打开，再执行 `source .venv/bin/activate`。
- 如果 Terminal 里看到的 Python 路径不是项目 `.venv`，先切换解释器，再重新打开 Terminal。

# Appendix G: VSCode Debug & Run

第一次接触 VSCode 时，可以按下面顺序做。

1. 打开 VSCode。
2. 打开项目根目录。
3. 打开 Terminal。
4. 选择 Python Interpreter，指向项目 `.venv`。
5. 在 Terminal 里执行：

```bash
source .venv/bin/activate
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

6. 看 Terminal Log 是否出现 `Application startup complete`。
7. 如果要调试，把运行方式换成 VSCode 的 Python Debugger，再启动 `app.main:app`。
8. 调试时优先看 Terminal 输出，不要只看浏览器页面。

# Appendix H: Interview Demo Startup

面试演示建议按这个顺序。

```text
Backend
↓
Health
↓
Swagger
↓
Create Task
↓
Task Status
↓
SSE
↓
Report
↓
结束
```

为什么按这个顺序演示：

- 先证明服务活着，再证明接口可读。
- 再证明能创建任务、能观察任务状态、能看到实时进度。
- 最后展示报告，说明这是一个完整闭环，不是单点接口。

# Appendix I: Startup Decision Tree

```text
Backend 启动失败？
↓
ImportError？
↓
YES → 安装 requirements → 再启动
↓
NO
↓
Port 被占用？
↓
YES → kill 进程 → 再启动
↓
NO
↓
检查 .env
↓
检查 .venv
↓
检查 Python
↓
仍然失败 → 回看 Appendix B
```

如果更细一点，也可以按下面思路排：

- 先看是不是导入错误。
- 再看是不是端口占用。
- 再看是不是环境变量缺失。
- 再看是不是 `.venv` 没激活。
- 再看是不是 Python / pip 指到了别的环境。

# Appendix J: Beginner Tips

## 为什么必须进入 backend 再启动？

因为 `app.main:app` 是后端入口，很多相对路径和依赖默认都以 `backend/` 为基准。如果在项目根目录直接启动，容易出现导入路径或测试发现路径不一致的问题。新手最稳妥的做法就是先 `cd backend`，再运行后端命令。

## 为什么使用 `python -m uvicorn`？

这样会让 `python` 和 `uvicorn` 来自同一个解释器环境，减少“命令找得到，但依赖找不到”的问题。对新手来说，这比直接敲 `uvicorn` 更稳，也更容易排查问题。这个写法同样适合调试和文档复制执行。

## 为什么使用 `python -m pip`？

因为它明确表示“用当前 Python 对应的 pip”。如果直接用 `pip`，很容易装到系统环境或别的虚拟环境里。新手第一优先级是让安装和运行使用同一个解释器。

## 为什么不要 `sudo pip install`？

`sudo pip install` 很容易把依赖装到系统环境，后面会污染别的项目。它也会掩盖 `.venv` 没激活的问题。这个项目更推荐把所有安装都放进 `.venv`。

## 为什么使用 `.venv`？

`.venv` 可以把项目依赖和系统环境隔离开。这样你升级、删除或重装依赖时，不会影响别的项目。对初学者来说，这也是最容易复现和排错的方式。

## 为什么先跑 Health，再看 Swagger？

`/health` 是最轻量的启动验证点，能最快确认服务已经活着。只有服务真正启动后，再打开 Swagger 才有意义。这个顺序可以帮助你快速判断问题是在“服务没起来”还是“接口文档没注册”。

## 3. `uvicorn` 找不到

现象：

- 执行 `uvicorn ...` 时提示 `command not found`。

原因：

- `uvicorn` 没装进当前环境。
- 或者 `.venv` 没激活，系统 PATH 里没有这个命令。

检查命令：

```bash
which uvicorn
python -m pip show uvicorn
```

修复命令：

```bash
source .venv/bin/activate
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## 4. `8000` 端口被占用

现象：

- 启动时报 `Address already in use`。
- 或者 `port 8000 is already in use`。

原因：

- 另一个后端进程已经在监听 8000。

检查命令：

```bash
ss -ltnp | grep 8000
```

修复命令：

```bash
kill <PID>
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## 5. `.venv` 没有激活

现象：

- `python -V` 不是项目里的解释器。
- `pip install` 后依赖还是找不到。

原因：

- 你执行命令时使用了系统 Python，而不是项目虚拟环境。

检查命令：

```bash
which python
python -m pip -V
```

修复命令：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai
source .venv/bin/activate
which python
python -m pip -V
```

## 6. `requirements` 没装完整

现象：

- 后端部分模块能导入，部分模块导入失败。
- 上传、文档解析、Swagger 相关页面启动不完整。

原因：

- 依赖只装了一部分。
- 或者中途安装失败，但你没有注意到报错。

检查命令：

```bash
cd backend
python -m pip check
python -m pip freeze | sed -n '1,120p'
```

修复命令：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai/backend
python -m pip install -r requirements.txt
python -m pip check
```

## 7. 在错误目录执行命令

现象：

- `python -m unittest discover -s tests -v` 找不到测试。
- `python -m uvicorn app.main:app` 报导入错误。

原因：

- `backend/` 下的命令被放到了项目根目录执行。
- 或者根目录命令被放到了 `backend/` 里执行。

检查命令：

```bash
pwd
```

修复命令：

```bash
cd /home/victorkure/workspace/vscode_study/ai-lab/ai-learn/retail-insight-ai/backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
