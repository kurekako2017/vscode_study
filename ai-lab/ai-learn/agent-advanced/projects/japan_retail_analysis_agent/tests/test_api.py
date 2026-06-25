from __future__ import annotations

"""Application/API boundary tests.

教学要点：
- 这里不使用 TestClient 驱动后台任务，避免测试框架和 event loop 互相影响。
- 测试重点是 application service 使用的 repository/checkpoint/event 结果。
"""

import asyncio
import sys
import unittest
from pathlib import Path
from uuid import uuid4


PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from retail_agent.api.app import app, health  # noqa: E402
from retail_agent.orchestration.orchestrator import RetailAnalysisOrchestrator  # noqa: E402


class RetailAnalysisApiTest(unittest.TestCase):
    def test_health_endpoint(self) -> None:
        """Health endpoint should return a simple liveness status."""
        response = asyncio.run(health())
        self.assertEqual(response["status"], "ok")

    def test_task_runner_writes_checkpoint_and_events(self) -> None:
        """A completed task should persist report and execution events."""
        task_id = uuid4().hex
        question = "売上と在庫を確認し、市場トレンドと競合を含めて報告"

        def record(event_type: str, message: str, payload: dict) -> None:
            app.state.task_service.repository.save_event(
                task_id,
                {"type": event_type, "message": message, "payload": payload},
            )

        app.state.task_service.repository.create(task_id, question, "hybrid")
        app.state.task_service.repository.update_status(task_id, "running")
        state = RetailAnalysisOrchestrator(event_callback=record).run(question, "hybrid")
        app.state.task_service.repository.save_state(task_id, state, "completed")
        app.state.task_service.repository.save_event(
            task_id,
            {"type": "completed", "message": "Report completed", "payload": {}},
        )

        detail = app.state.task_service.repository.get(task_id)
        self.assertIsNotNone(detail)
        assert detail is not None
        self.assertEqual(detail["status"], "completed")
        self.assertIn("日本小売 経営分析レポート", detail["report_markdown"])
        event_types = [event["type"] for event in app.state.task_service.repository.events(task_id)]
        self.assertIn("workflow_completed", event_types)
        self.assertIn("research_completed", event_types)
        self.assertIn("completed", event_types)


if __name__ == "__main__":
    unittest.main()
