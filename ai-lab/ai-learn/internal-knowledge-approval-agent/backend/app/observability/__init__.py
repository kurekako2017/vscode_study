"""可观测性导出边界。

当前只复用 ``app.config.logging`` 的 JSON Log；生产可在此接 OpenTelemetry trace/metric，
但不得记录密钥、完整问题或文档正文。日本现场面试应明确 Trace、Metric 和 SLO 仍是缺口。
"""

from app.config.logging import get_logger, log_event

__all__ = ["get_logger", "log_event"]
