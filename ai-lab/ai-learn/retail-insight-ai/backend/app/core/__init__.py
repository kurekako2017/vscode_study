"""核心学习辅助模块入口。

这个包目前只放和教学、观察相关的旁路能力，避免把学习日志分散到各个业务模块里。
"""

from app.core.learning_trace import configure_learning_trace, trace_enter, trace_exit, trace_step

__all__ = [
    "configure_learning_trace",
    "trace_enter",
    "trace_exit",
    "trace_step",
]
