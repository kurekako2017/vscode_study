"""Backend 存活检查接口。

文件职责：返回服务是否已成功启动；监控、脚本和容器探针会调用它。
输入：注入的 AppContainer；输出：最小健康状态，不包含敏感配置。
初学者重点：Health Route 不执行知识检索或数据库写入。
日本现场面试：当前是 liveness 基线；企业级应拆分 readiness 并检查必要依赖。
"""

from fastapi import APIRouter, Depends

from app.api.routes.dependencies import get_container
from app.config.container import AppContainer


router = APIRouter()


@router.get("/health")
async def health(container: AppContainer = Depends(get_container)) -> dict[str, str]:
    return {"status": "ok", "service": container.settings.service_name}
