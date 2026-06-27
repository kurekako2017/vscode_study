from pydantic import BaseModel


class HealthResponse(BaseModel):
    """定义健康检查的稳定响应字段。"""

    status: str
    service: str
    provider: str
