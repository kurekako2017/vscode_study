"""Agent 服务化过渡：SSE token/status/error/done 事件。"""
from __future__ import annotations

import asyncio
import json

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Streaming Agent API Demo")


class RunRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)


def event(name: str, data: dict) -> str:
    return f"event: {name}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


async def run_agent(message: str):
    yield event("status", {"stage": "planning"})
    await asyncio.sleep(0.02)
    if "error" in message.lower():
        yield event("error", {"code": "SIMULATED_FAILURE", "message": "模拟执行失败"})
        return
    for token in ["已", "处理", "：", message]:
        await asyncio.sleep(0)  # cancellation point
        yield event("token", {"text": token})
    yield event("done", {"finish_reason": "stop"})


@app.post("/runs/stream")
async def stream_run(request: RunRequest) -> StreamingResponse:
    return StreamingResponse(run_agent(request.message), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
