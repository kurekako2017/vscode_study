from __future__ import annotations

"""Health and metrics endpoints."""

from fastapi import APIRouter, Depends

from ..dependencies import get_metrics


router = APIRouter(tags=["health"])


@router.get("/api/health")
async def health() -> dict[str, str]:
    """Liveness endpoint used by smoke tests and containers."""
    return {"status": "ok"}


@router.get("/api/metrics")
async def metrics(metrics=Depends(get_metrics)) -> dict:
    """Teaching metrics endpoint; production should expose Prometheus format."""
    return metrics.snapshot()
