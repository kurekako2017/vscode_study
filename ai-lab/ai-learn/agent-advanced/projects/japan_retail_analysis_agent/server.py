from __future__ import annotations

"""Uvicorn entrypoint.

教学要点：
- 开发时可以 `python3 server.py` 启动。
- Dockerfile 也复用这个入口。
- 实际生产可改用 `uvicorn retail_agent.api.app:app --workers N`。
"""

import uvicorn

from retail_agent.core.config import get_settings


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "retail_agent.api.app:app",
        host=settings.host,
        port=settings.port,
        reload=False,
    )
