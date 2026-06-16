"""
FastAPI 接口层与项目闭环入口

负责承接前端的任务提交、任务取消、文件上传/下载、输出文件列表查询和
WebSocket 长连接。HTTP 接口只做轻量调度，真正的 DeepAgents 执行放到后台
任务中；执行进度、工具调用和最终结果由 monitor 按 thread_id 推送给前端。
"""

import asyncio
import os
import shutil
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import List

import uvicorn
from fastapi import (
    FastAPI,
    File,
    Form,
    HTTPException,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.agent.main_agent import run_deep_agent
from app.api.monitor import manager
from app.runtime_config import resolve_llm_config
from app.knowledge_base.local_index import has_local_knowledge_base
from app.utils.logging_utils import get_logger, log_event

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    服务生命周期入口。

    启动时绑定当前事件循环到 WebSocket 管理器，确保后台 Agent 任务可以把
    monitor 事件投递回 FastAPI 所在的 loop。
    """
    loop = asyncio.get_running_loop()
    manager.set_loop(loop)
    log_event(logger, 20, "server_lifespan_started", loop_id=id(loop))
    yield


# 当前文件位于 app/api/server.py，运行时目录统一收敛到 app 目录
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent

app = FastAPI(title="DeepAgents API", lifespan=lifespan)

# 保存 thread_id -> 后台 Agent 任务，用于同一会话任务替换和主动取消
active_tasks: dict[str, asyncio.Task] = {}

# output 保存每个会话最终工作区，前端只允许从这里浏览和下载生成文件
output_dir = project_root / "output"
output_dir.mkdir(exist_ok=True)

# updated 暂存用户上传文件，run_deep_agent 启动时会复制到对应 output/session_xxx
updated_dir = project_root / "updated"
updated_dir.mkdir(exist_ok=True)

# 教学项目通常前后端分别本地启动，这里放开跨域以便 Vite 页面直接调用 API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskRequest(BaseModel):
    """前端启动任务时提交的请求体。"""

    query: str
    thread_id: str = None


def _forget_task(thread_id: str, task: asyncio.Task) -> None:
    """
    清理已结束任务的登记关系。

    done_callback 触发时，active_tasks 中可能已经被新任务替换；只有仍是同一个
    task 时才删除，避免误清理同 thread_id 下刚启动的新任务。
    """
    if active_tasks.get(thread_id) is task:
        active_tasks.pop(thread_id, None)


@app.get("/api/health")
async def health_check():
    """
    最轻量的健康检查接口。

    这个接口的设计目标不是“验证所有依赖都完全可用”，而是先回答两个最基础问题：
    1. FastAPI 进程本身是否活着
    2. 当前读取到了哪些运行配置

    所以前端加载页面时，可以先打这个接口，快速判断是“后端没起来”，
    还是“后端起来了，但外部能力还没配置完整”。
    """
    llm_config = resolve_llm_config()
    log_event(
        logger,
        10,
        "health_check_requested",
        llm_provider=llm_config["provider"],
        mysql_host=os.getenv("MYSQL_HOST", ""),
    )

    return {
        "status": "ok",
        "backend": "alive",
        "llm": {
            "configured": bool(llm_config["configured"]),
            "source": str(llm_config["source"]),
            "provider": str(llm_config["provider"]),
            "model": str(llm_config["model"]),
        },
        "mysql": {
            "host": os.getenv("MYSQL_HOST", ""),
            "port": os.getenv("MYSQL_PORT", ""),
            "configured": bool(os.getenv("MYSQL_HOST") and os.getenv("MYSQL_PORT") and os.getenv("MYSQL_USER") and os.getenv("MYSQL_PASSWORD") and os.getenv("MYSQL_DATABASE")),
        },
        "services": {
            "tavily": bool(os.getenv("TAVILY_API_KEY")),
            "local_knowledge_base": has_local_knowledge_base(),
        },
    }


@app.post("/api/task")
async def run_task(request: TaskRequest):
    """
    启动一次 DeepAgents 后台任务。

    HTTP 请求只负责创建后台协程并立即返回，后续执行轨迹、子智能体调用和最终
    答案都会由 monitor 通过 `/ws/{thread_id}` 推送给同一会话的前端。
    """
    thread_id = request.thread_id or str(uuid.uuid4())
    log_event(
        logger,
        20,
        "task_start_requested",
        thread_id=thread_id,
        query=request.query,
        query_length=len(request.query or ""),
    )

    # 同一个 thread_id 只保留一个活跃任务，新任务会先取消旧任务，避免并发写同一会话目录
    old_task = active_tasks.get(thread_id)
    if old_task and not old_task.done():
        log_event(logger, 30, "task_replaced_existing_active_task", thread_id=thread_id)
        old_task.cancel()

    # create_task 把长耗时 Agent 执行交给事件循环，接口本身不用等待最终结果
    task = asyncio.create_task(run_deep_agent(request.query, thread_id))
    active_tasks[thread_id] = task
    task.add_done_callback(lambda finished_task: _forget_task(thread_id, finished_task))
    log_event(logger, 20, "task_started", thread_id=thread_id, active_task_count=len(active_tasks))

    return {"status": "started", "thread_id": thread_id}


@app.post("/api/task/{thread_id}/cancel")
async def cancel_task(thread_id: str):
    """
    取消指定 thread_id 对应的后台 Agent 任务。

    注意：取消会向 asyncio.Task 注入 CancelledError。若底层第三方工具正在执行不可中断
    的同步阻塞调用，任务可能需要等该调用返回后才会真正结束。
    """
    task = active_tasks.get(thread_id)
    log_event(logger, 20, "task_cancel_requested", thread_id=thread_id, task_found=bool(task))
    if not task or task.done():
        active_tasks.pop(thread_id, None)
        log_event(logger, 30, "task_cancel_missing_or_finished", thread_id=thread_id)
        raise HTTPException(status_code=404, detail="任务不存在或已结束")

    # 先发出取消信号，再短暂等待协程响应；若底层阻塞中，则返回 cancelling 给前端继续展示状态
    task.cancel()
    try:
        await asyncio.wait_for(task, timeout=1.0)
    except asyncio.CancelledError:
        _forget_task(thread_id, task)
        log_event(logger, 20, "task_cancelled", thread_id=thread_id)
        return {"status": "cancelled", "thread_id": thread_id}
    except asyncio.TimeoutError:
        log_event(logger, 30, "task_cancellation_pending", thread_id=thread_id)
        return {"status": "cancelling", "thread_id": thread_id}
    except Exception as e:
        _forget_task(thread_id, task)
        log_event(logger, 40, "task_cancellation_exception", thread_id=thread_id, error=str(e))
        return {"status": "cancelled", "thread_id": thread_id, "message": str(e)}

    _forget_task(thread_id, task)
    log_event(logger, 20, "task_cancelled_after_wait", thread_id=thread_id)
    return {"status": "cancelled", "thread_id": thread_id}


@app.post("/api/upload")
async def upload_files(files: List[UploadFile] = File(...), thread_id: str = Form(...)):
    """
    文件上传接口 (File Upload)。

    目标：
    1. 接收用户上传的一个或多个文件。
    2. 保存到 `updated/session_{thread_id}` 目录。
    3. 供 Agent 在后续任务中读取和分析。

    Args:
        files (List[UploadFile]): 文件对象列表。
        thread_id (str): 关联的任务会话 ID。
    """
    # 上传文件先按会话隔离保存，避免不同任务读取到彼此的附件
    # 注意这里先写到 updated/session_xxx，而不是直接写到 output/session_xxx。
    # 这样做的好处是：
    # 1. 用户可能先上传文件，稍后再发任务
    # 2. 真正执行任务时，再由 run_deep_agent 统一复制到工作目录
    # 3. output 目录就只放“本次任务真正使用过的工作区”
    target_dir = updated_dir / f"session_{thread_id}"
    target_dir.mkdir(parents=True, exist_ok=True)
    log_event(
        logger,
        20,
        "upload_started",
        thread_id=thread_id,
        file_count=len(files),
        target_dir=str(target_dir),
    )

    saved_files = []
    for file in files:
        file_path = target_dir / file.filename
        # 直接复制文件流，避免大文件一次性读入内存
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file.filename)
        log_event(
            logger,
            20,
            "upload_saved_file",
            thread_id=thread_id,
            filename=file.filename,
            path=str(file_path),
        )

    return {"status": "uploaded", "files": saved_files}


@app.get("/api/download")
async def download_file(path: str):
    """
    文件下载接口 (File Download)。

    目标：
    1. 根据绝对路径下载文件。
    2. 严格的安全检查，防止越权访问。

    Args:
        path (str): 文件的绝对路径 (通常从 list_files 接口获取)。
    """
    try:
        # resolve 后再做 is_relative_to，防止 `../` 之类的路径穿越到 output 之外
        abs_path = Path(path).resolve()
        output_abs = output_dir.resolve()

        # 下载接口只允许访问 output 目录，是为了避免把服务器任意文件暴露给前端。
        if not abs_path.is_relative_to(output_abs):
            log_event(logger, 40, "download_rejected_outside_output_dir", path=path, resolved_path=str(abs_path))
            return {"error": "拒绝访问: 只能下载输出目录下的文件"}
    except Exception:
        log_event(logger, 40, "download_invalid_path", path=path)
        return {"error": "无效的路径参数"}

    if not abs_path.exists():
        log_event(logger, 30, "download_missing_file", path=path, resolved_path=str(abs_path))
        return {"error": "文件不存在"}

    log_event(logger, 20, "download_started", path=path, resolved_path=str(abs_path))
    # FileResponse 会以流式响应返回文件内容，并让浏览器使用原文件名下载
    return FileResponse(abs_path, filename=abs_path.name)


@app.get("/api/files")
async def list_files(path: str):
    """
    文件列表查询接口 (File Explorer)。

    目标：
    1. 列出指定目录下的所有生成文件。
    2. 提供文件元数据（大小、修改时间、下载所需路径）。
    3. 严格的安全检查，防止路径遍历攻击。

    Args:
        path (str): 目标目录的绝对路径 (必须在 output 目录下)。
    """
    log_event(logger, 10, "list_files_requested", path=path)

    try:
        # 和下载接口保持同一条安全边界：前端只能查看 output 目录内部内容
        abs_path = Path(path).resolve()
        output_abs = output_dir.resolve()

        if not abs_path.is_relative_to(output_abs):
            log_event(logger, 40, "list_files_rejected_outside_output_dir", path=path, resolved_path=str(abs_path))
            return {"error": "拒绝访问: 只能访问输出目录下的文件"}

    except Exception as e:
        log_event(logger, 40, "list_files_path_parse_failed", path=path, error=str(e))
        return {"error": f"路径无效: {e}"}

    if not abs_path.exists():
        log_event(logger, 30, "list_files_directory_missing", path=path, resolved_path=str(abs_path))
        return {"error": "目录不存在"}

    # 返回给前端的不是树形目录，而是一个扁平文件列表。
    # 这样页面实现更简单，用户也更容易快速看到最终产物。
    files = []
    try:
        # 递归返回文件元数据，前端据此渲染文件列表并发起下载请求
        for file_path in abs_path.rglob("*"):
            if file_path.is_file():
                stat = file_path.stat()
                files.append(
                    {
                        "name": file_path.name,
                        "type": "file",
                        "path": str(file_path),
                        "size": stat.st_size,
                        "mtime": stat.st_mtime,
                    }
                )

    except Exception as e:
        log_event(logger, 40, "list_files_walk_failed", path=path, error=str(e))
        return {"error": str(e)}

    # 最新生成的文件排在前面，方便用户优先看到本次任务产物
    files.sort(key=lambda x: x.get("mtime", 0), reverse=True)
    log_event(logger, 20, "list_files_completed", path=path, file_count=len(files))
    return {"files": files}


@app.websocket("/ws/{thread_id}")
async def websocket_endpoint(websocket: WebSocket, thread_id: str):
    """
    WebSocket 实时通讯核心接口 (Real-time Communication)。

    连接建立后，ConnectionManager 会用 thread_id 保存 WebSocket。monitor 后续
    发送事件时只需要按 thread_id 查找连接，就能把进度推给对应页面。循环中的
    receive_text 用于接收前端心跳，避免连接空闲断开。
    """
    log_event(logger, 20, "websocket_connect_requested", thread_id=thread_id, client=str(websocket.client))

    # 连接建立后立即按 thread_id 注册，monitor 后续才能把事件定向推给当前页面
    await manager.connect(websocket, thread_id)

    try:
        while True:
            # 前端通常发送 ping 心跳；服务端回复 pong，顺便维持连接活跃
            # 当前项目里前端主要发送 ping 心跳，不走复杂指令协议。
            # 如果你后续想扩展“前端主动订阅更多事件”，这里就是协议入口。
            data = await websocket.receive_text()
            log_event(logger, 10, "websocket_message_received", thread_id=thread_id, message=data)
            await websocket.send_json(
                {"type": "pong", "message": f"服务端已收到: {data}"}
            )

    except WebSocketDisconnect:
        # 只移除当前 WebSocket 实例，避免旧连接断开时误删同 thread_id 的新连接
        manager.disconnect(websocket, thread_id)
        log_event(logger, 20, "websocket_disconnected", thread_id=thread_id)

    except Exception as e:
        log_event(logger, 40, "websocket_exception", thread_id=thread_id, error=str(e))
        manager.disconnect(websocket, thread_id)


if __name__ == "__main__":
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=True)
