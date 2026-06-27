from __future__ import annotations

import io
import json
import logging
import unittest

from app.observability.logging import JsonLogFormatter, bind_request_id, log_event, reset_request_id


class StructuredLoggingTest(unittest.TestCase):
    """验证日志字段合同，避免后续修改破坏日志平台解析。"""

    def test_log_event_contains_required_fields(self) -> None:
        stream = io.StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(JsonLogFormatter("test-service"))
        logger = logging.Logger("structured-log-test", level=logging.INFO)
        logger.addHandler(handler)
        token = bind_request_id("request-123")

        try:
            log_event(
                logger,
                "info",
                "task_completed",
                "Task completed",
                task_id="task-456",
                status="completed",
                duration_ms=12.345,
            )
        finally:
            reset_request_id(token)

        payload = json.loads(stream.getvalue())
        self.assertEqual(payload["service"], "test-service")
        self.assertEqual(payload["request_id"], "request-123")
        self.assertEqual(payload["task_id"], "task-456")
        self.assertEqual(payload["event"], "task_completed")
        self.assertEqual(payload["message"], "Task completed")
        self.assertEqual(payload["status"], "completed")
        self.assertEqual(payload["duration_ms"], 12.35)
        self.assertIsNone(payload["error_code"])
        self.assertIn("timestamp", payload)
        self.assertEqual(payload["level"], "INFO")

    def test_missing_context_uses_reserved_placeholders(self) -> None:
        stream = io.StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(JsonLogFormatter("test-service"))
        logger = logging.Logger("structured-log-placeholder-test", level=logging.INFO)
        logger.addHandler(handler)

        log_event(logger, "info", "health_check", "Health check completed")

        payload = json.loads(stream.getvalue())
        self.assertEqual(payload["request_id"], "-")
        self.assertEqual(payload["task_id"], "-")
        self.assertIsNone(payload["duration_ms"])


if __name__ == "__main__":
    unittest.main()
