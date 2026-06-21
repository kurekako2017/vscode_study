"""无厂商锁定的 JSONL tracing、耗时、成本与失败记录。"""
from __future__ import annotations

import argparse
import json
import time
import uuid
from contextlib import contextmanager
from pathlib import Path


class Tracer:
    """把一次运行中的 span 追加写入 JSONL 文件。"""

    def __init__(self, output: Path) -> None:
        # 同一次程序运行共用 trace_id，每个步骤再分配独立 span_id。
        self.output = output
        self.trace_id = uuid.uuid4().hex

    def emit(self, event: dict) -> None:
        """追加一行 JSON；JSONL 便于逐行采集，不必一次加载整个文件。"""
        self.output.parent.mkdir(parents=True, exist_ok=True)
        with self.output.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event, ensure_ascii=False) + "\n")

    @contextmanager
    def span(self, name: str, **attributes):
        """记录代码块耗时；成功和异常都会落盘，异常仍继续向上抛出。"""
        started = time.perf_counter()
        span_id = uuid.uuid4().hex[:12]
        try:
            # yield 前是进入 span，yield 后是离开 span。
            yield span_id
        except Exception as exc:
            self.emit({"trace_id": self.trace_id, "span_id": span_id, "name": name, "status": "error", "error": str(exc), "duration_ms": round((time.perf_counter() - started) * 1000, 2), **attributes})
            raise
        else:
            self.emit({"trace_id": self.trace_id, "span_id": span_id, "name": name, "status": "ok", "duration_ms": round((time.perf_counter() - started) * 1000, 2), **attributes})


def main() -> None:
    """模拟 Agent、检索器和工具三个嵌套步骤，并输出 trace 文件位置。"""
    print("MODEL: provider=local model=mock mode=mock-trace")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("traces/run.jsonl"))
    parser.add_argument("--fail", action="store_true")
    args = parser.parse_args()
    tracer = Tracer(args.output)
    # attributes 会原样进入 trace，生产环境中可放模型、token 和成本等信息。
    with tracer.span("agent.run", model="mock", input_tokens=120, output_tokens=40, estimated_cost_usd=0.0):
        with tracer.span("retriever.search", top_k=3):
            time.sleep(0.01)
        with tracer.span("tool.execute", tool="crm_lookup"):
            if args.fail:
                raise RuntimeError("模拟工具超时")
    print(f"trace_id={tracer.trace_id} output={args.output}")


if __name__ == "__main__":
    main()
