"""Agent 服务化过渡：SSE token/status/error/done 事件。"""
from __future__ import annotations

import asyncio
import json

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Streaming Agent API Demo")

# 当前服务只演示 SSE 事件格式，token 是本地列表，不是模型流式输出。
print("MODEL: provider=local model=none mode=sse-simulation")


class RunRequest(BaseModel):
    """客户端请求体；长度限制可以阻止意外提交超大文本。"""

    message: str = Field(min_length=1, max_length=1000)


def event(name: str, data: dict) -> str:
    """把事件名和字典编码成浏览器可识别的 SSE 文本格式。"""
    return f"event: {name}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


async def run_agent(message: str):
    """依次产生状态、文本、完成事件；包含 error 时走模拟失败分支。"""
    # status 先告诉客户端当前阶段，客户端可据此显示进度提示。
    yield event("status", {"stage": "planning"})
    await asyncio.sleep(0.02)
    if "error" in message.lower():
        yield event("error", {"code": "SIMULATED_FAILURE", "message": "模拟执行失败"})
        return
    for token in ["已", "处理", "：", message]:
        # sleep(0) 把控制权交回事件循环，使客户端断开时能够及时取消任务。
        await asyncio.sleep(0)
        yield event("token", {"text": token})
    yield event("done", {"finish_reason": "stop"})


@app.post("/runs/stream")
async def stream_run(request: RunRequest) -> StreamingResponse:
    """把异步生成器包装为 HTTP 流，并关闭代理缓冲。"""
    return StreamingResponse(
        run_agent(request.message),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
