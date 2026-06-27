from __future__ import annotations

import inspect
import unittest

from app.repositories.implementations.in_memory.report_repository import InMemoryReportRepository
from app.repositories.implementations.in_memory.task_repository import InMemoryTaskRepository
from app.repositories.interfaces.report_repository import ReportRepository
from app.repositories.interfaces.task_repository import TaskRepository
from app.services.task_service import TaskService


class RepositoryBoundaryTest(unittest.TestCase):
    """保护 Service 依赖接口、组合根选择实现的架构边界。"""

    def test_in_memory_repositories_implement_protocols(self) -> None:
        self.assertIsInstance(InMemoryTaskRepository(), TaskRepository)
        self.assertIsInstance(InMemoryReportRepository(), ReportRepository)

    def test_task_service_does_not_import_repository_implementation(self) -> None:
        source = inspect.getsource(inspect.getmodule(TaskService))
        self.assertNotIn("repositories.implementations", source)
        self.assertIn("repositories.interfaces.task_repository", source)
        self.assertIn("repositories.interfaces.report_repository", source)


if __name__ == "__main__":
    unittest.main()
