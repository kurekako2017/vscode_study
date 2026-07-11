# FastAPI 项目启动过程（Retail Insight AI）

## 启动命令

```bash
cd backend

uvicorn app.main:app --host 127.0.0.1 --port 8000
```

---

## 启动过程（项目真实流程）

```text
执行：

uvicorn app.main:app

        │
        ▼

启动 Uvicorn（Web Server）

        │
        ▼

读取：

backend/app/main.py

        │
        ▼

找到：

app = FastAPI(...)

        │
        ▼

执行：

create_app()

        │
        ▼

注册所有 Router
(include_router)

        │
        ▼

启动 HTTP Server

        │
        ▼

监听：

127.0.0.1:8000

        │
        ▼

等待浏览器请求

        │
        ▼

浏览器访问：

http://127.0.0.1:8000/docs

        │
        ▼

Swagger UI

        │
        ▼

点击 Execute

        │
        ▼

进入 Router

        │
        ▼

Service

        │
        ▼

Repository

        │
        ▼

HTTP Response
```

---

## 为什么 Learning Trace 要从 main.py 开始？

真正的入口并不是 `health()` 或 `create_task()`。

程序首先由 **Uvicorn** 启动，然后加载 `backend/app/main.py`， 创建
`FastAPI` 实例，注册所有 Router，最后才会进入具体接口。

因此学习源码时，建议按照下面的顺序阅读：

```text
Uvicorn
    ↓
backend/app/main.py
    ↓
create_app()
    ↓
include_router()
    ↓
api/health.py 或 api/tasks.py
    ↓
Service
    ↓
Repository
    ↓
Response
```

---

## Java 对照理解

  Java                    FastAPI

---

  Tomcat                  Uvicorn
  SpringBootApplication   main.py
  DispatcherServlet       FastAPI Router
  Controller              api/\*.py
  Service                 services/\*.py
  Repository              repositories/\*.py

> 可以把 **Uvicorn** 理解为 Python 世界中负责运行 FastAPI 应用的 Web
> Server。
