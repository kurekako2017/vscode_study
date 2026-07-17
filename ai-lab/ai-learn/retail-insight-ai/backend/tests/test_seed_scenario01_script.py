"""Scenario01 seed 脚本合同与安全边界。

覆盖：
- 脚本存在且可执行意图（bash shebang）
- 强制 PostgreSQL-only
- 禁止 Retrieval / AI / Approval / Provider
- 幂等关键词（reuse / Idempotency-Key / title 匹配）
- 不输出 Token / 密码 / Key 字段
- 使用 01-06 业务文档，不入库 07-10
"""

from __future__ import annotations

import os
import re
import stat
import unittest
from pathlib import Path


def _find_project_root() -> Path:
    """兼容 host（backend/tests）与 Compose 挂载（/project 或同目录 scripts）。"""

    candidates: list[Path] = []
    here = Path(__file__).resolve()
    candidates.extend(list(here.parents))
    candidates.append(Path("/project"))
    for parent in candidates:
        if (parent / "scripts" / "seed_scenario01.sh").is_file():
            return parent
        if (parent / "backend" / "app").is_dir() and (parent / "scripts").is_dir():
            return parent
    # Docker 镜像未打包 scripts 时，回退到 backend 上级（仅 host 结构）
    return here.parents[2]


class SeedScenario01ScriptContractTest(unittest.TestCase):
    def setUp(self) -> None:
        root = _find_project_root()
        self.script = root / "scripts" / "seed_scenario01.sh"
        self.sample_dir = (
            root / "docs" / "learning" / "sample-data" / "Scenario01_Sales_Decline"
        )
        if not self.script.is_file() or not self.sample_dir.is_dir():
            self.skipTest(
                "seed script/sample-data not available in this environment "
                "(mount project scripts/ and docs/ when running tests in container)"
            )

    def test_script_exists_and_is_executable_flag(self) -> None:
        self.assertTrue(self.script.is_file(), f"missing {self.script}")
        mode = self.script.stat().st_mode
        # 至少 owner 可执行（仓库内 chmod +x）
        self.assertTrue(mode & stat.S_IXUSR, "seed script should be executable")

    def test_script_contract_text(self) -> None:
        text = self.script.read_text(encoding="utf-8")
        self.assertIn("#!/usr/bin/env bash", text)
        self.assertIn('repository_backend', text)
        self.assertIn("postgres", text)
        self.assertIn("InMemory", text)
        # 只走文档三件套
        self.assertIn("/api/v1/documents", text)
        self.assertIn("/import", text)
        self.assertIn("/chunks", text)
        # 禁止业务主链副作用
        self.assertNotIn("document-retrieval", text)
        self.assertNotIn("ai-analysis", text)
        self.assertNotIn("executive-reports", text)
        self.assertNotIn("submit-approval", text)
        # 幂等
        self.assertIn("Idempotency-Key", text)
        self.assertIn("reuse", text)
        self.assertIn("provider_calls", text)
        # 安全：脚本不得 echo 密码或 token 值字段名到日志（允许变量名 PASSWORD 用于 login body）
        self.assertNotIn("echo.*TOKEN", text)
        self.assertNotIn("echo \"$TOKEN\"", text)
        self.assertNotIn("echo \"${TOKEN}\"", text)
        self.assertNotIn("echo $PASSWORD", text)
        self.assertNotIn("api_key", text.lower())
        # 仅 01-06
        self.assertIn("0{1,2,3,4,5,6}_", text)
        self.assertIn("provider_call_target=0", text)

    def test_scenario01_business_files_exist(self) -> None:
        files = sorted(self.sample_dir.glob("0[1-6]_*.md"))
        self.assertEqual(len(files), 6, files)
        # 07-10 是问题/输入例，不应被 seed 当语料强制要求上传
        extras = list(self.sample_dir.glob("0[7-9]_*.md")) + list(
            self.sample_dir.glob("10_*.md")
        )
        self.assertGreaterEqual(len(extras), 1)


@unittest.skipUnless(
    os.environ.get("RUN_SEED_LIVE") == "1",
    "opt-in live seed: RUN_SEED_LIVE=1 BASE_URL=... (PostgreSQL compose)",
)
class SeedScenario01LiveIdempotencyTest(unittest.TestCase):
    """连续执行两次 seed，第二次 created 应为 0（不新增重复）。"""

    def test_seed_twice_no_duplicate_create(self) -> None:
        import subprocess

        root = Path(__file__).resolve().parents[2]
        script = root / "scripts" / "seed_scenario01.sh"
        env = os.environ.copy()
        env.setdefault("BASE_URL", "http://127.0.0.1:8000")
        first = subprocess.run(
            ["bash", str(script)],
            cwd=str(root),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
        self.assertIn("provider_calls=0", first.stdout)
        second = subprocess.run(
            ["bash", str(script)],
            cwd=str(root),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(second.returncode, 0, second.stderr + second.stdout)
        self.assertIn("provider_calls=0", second.stdout)
        self.assertRegex(second.stdout, r"created=0")
        # 不泄漏
        combined = (first.stdout + second.stdout).lower()
        self.assertNotIn("sk-", combined)
        self.assertNotIn("bearer ", combined)
        self.assertNotIn("access_token", combined)


if __name__ == "__main__":
    unittest.main()
