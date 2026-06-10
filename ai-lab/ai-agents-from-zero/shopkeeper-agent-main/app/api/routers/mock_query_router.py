"""
Mock 问数接口路由

用于在本地基础设施还没完全恢复时，先把前端和 SSE 链路跑起来。
这个模式不依赖 MySQL / Qdrant / Elasticsearch / TEI / LLM，适合做界面联调和流程演示。
"""

import asyncio
import json
from typing import AsyncGenerator

from fastapi import APIRouter
from starlette.responses import StreamingResponse

from app.api.schemas.query_schema import QuerySchema

mock_query_router = APIRouter()


async def _mock_stream(query: str) -> AsyncGenerator[str, None]:
    """按真实 SSE 形态模拟一个问数流程。"""

    steps = [
        "抽取关键词",
        "召回字段信息",
        "召回指标信息",
        "召回字段取值",
        "生成 SQL",
        "执行 SQL",
    ]

    for step in steps:
        payload = {"type": "progress", "step": step, "status": "running"}
        yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
        await asyncio.sleep(0.15)
        payload = {"type": "progress", "step": step, "status": "success"}
        yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"

    result = {
        "query": query,
        "sql": "SELECT region_name, SUM(order_amount) AS gmv FROM fact_order JOIN dim_region USING(region_id) GROUP BY region_name ORDER BY gmv DESC;",
        "rows": [
            {"region_name": "华东", "gmv": 15499.0},
            {"region_name": "华北", "gmv": 11398.0},
            {"region_name": "华南", "gmv": 8999.0},
        ],
        "note": "这是 mock 模式返回的示例结果，真实模式下会来自 NAS MySQL / Qdrant / ES / TEI 联动。",
    }
    yield f"data: {json.dumps({'type': 'result', 'data': result}, ensure_ascii=False)}\n\n"


@mock_query_router.post("/api/query")
async def mock_query_handler(query: QuerySchema):
    """返回一个可供前端消费的模拟 SSE 流。"""

    return StreamingResponse(_mock_stream(query.query), media_type="text/event-stream")
