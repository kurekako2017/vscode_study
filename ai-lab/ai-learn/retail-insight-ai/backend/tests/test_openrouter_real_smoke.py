"""可选 OpenRouter 真实 smoke（默认永不执行，避免付费与外网）。

启用条件（全部满足）：
- LLM_PROVIDER_MODE=openrouter
- RUN_REAL_LLM_SMOKE=1
- OPENROUTER_API_KEY 已设置
- OPENROUTER_LOW_COST_MODEL / OPENROUTER_HIGH_QUALITY_MODEL 完整

警告：每个 tier 最多一次极小请求，会产生 API 用量。
不要把完整模型回答写入日志；不要在默认 CI/unittest discover 中依赖本文件通过。
"""

from __future__ import annotations

import os
import unittest
from decimal import Decimal

from pydantic import SecretStr

from app.config.settings import Settings
from app.models.ai_analysis import AIEvidence, LLMAnalysisInput, LLMReportInput
from app.providers.openrouter_llm_provider import OpenRouterLLMProvider


def _smoke_enabled() -> bool:
    if os.environ.get("RUN_REAL_LLM_SMOKE", "").strip() not in {"1", "true", "TRUE", "yes"}:
        return False
    mode = os.environ.get("LLM_PROVIDER_MODE", "stub").strip().lower()
    if mode != "openrouter":
        return False
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    low = os.environ.get("OPENROUTER_LOW_COST_MODEL", "").strip()
    high = os.environ.get("OPENROUTER_HIGH_QUALITY_MODEL", "").strip()
    return bool(key and low and high)


@unittest.skipUnless(
    _smoke_enabled(),
    "Real OpenRouter smoke disabled (set LLM_PROVIDER_MODE=openrouter RUN_REAL_LLM_SMOKE=1 and models/key)",
)
class OpenRouterRealSmokeTest(unittest.TestCase):
    """每个 route tier 一次最小真实请求；默认 suite 跳过。"""

    def setUp(self) -> None:
        self.settings = Settings(
            llm_provider_mode="openrouter",
            openrouter_api_key=SecretStr(os.environ["OPENROUTER_API_KEY"].strip()),
            openrouter_low_cost_model=os.environ["OPENROUTER_LOW_COST_MODEL"].strip(),
            openrouter_high_quality_model=os.environ["OPENROUTER_HIGH_QUALITY_MODEL"].strip(),
            openrouter_base_url=os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            real_llm_timeout_seconds=float(os.environ.get("REAL_LLM_TIMEOUT_SECONDS", "30")),
            real_llm_max_retries=0,
            run_real_llm_smoke=True,
            _env_file=None,
        )
        self.evidence = (
            AIEvidence(
                "doc-smoke",
                "chk-smoke",
                Decimal("1.0"),
                "Non-sensitive synthetic evidence: beverage sales declined in region A.",
            ),
        )

    def test_low_cost_analyze_once(self) -> None:
        provider = OpenRouterLLMProvider(
            provider_name="openrouter-low-cost",
            model_name=self.settings.llm_low_cost_model_name,
            api_key=self.settings.openrouter_api_key,  # type: ignore[arg-type]
            base_url=self.settings.openrouter_base_url,
            timeout_seconds=self.settings.real_llm_timeout_seconds,
            max_retries=0,
            http_referer=self.settings.openrouter_http_referer,
            app_title=self.settings.openrouter_app_title or "ERIP Smoke",
        )
        try:
            result = provider.analyze(
                LLMAnalysisInput(
                    question="One-sentence summary of the evidence.",
                    evidence=self.evidence,
                    max_output_tokens=48,
                    request_id="smoke-low-cost",
                    timeout_seconds=self.settings.real_llm_timeout_seconds,
                )
            )
        finally:
            provider.close()
        self.assertGreater(result.input_tokens + result.output_tokens, 0)
        self.assertTrue(result.provider_request_id)
        # 不打印完整回答。
        self.assertGreater(len(result.answer or ""), 0)

    def test_high_quality_report_once(self) -> None:
        provider = OpenRouterLLMProvider(
            provider_name="openrouter-high-quality",
            model_name=self.settings.llm_high_quality_model_name,
            api_key=self.settings.openrouter_api_key,  # type: ignore[arg-type]
            base_url=self.settings.openrouter_base_url,
            timeout_seconds=self.settings.real_llm_timeout_seconds,
            max_retries=0,
            http_referer=self.settings.openrouter_http_referer,
            app_title=self.settings.openrouter_app_title or "ERIP Smoke",
        )
        try:
            result = provider.generate_report(
                LLMReportInput(
                    title="Smoke Board Report",
                    analysis_answer="Evidence indicates regional sales decline.",
                    evidence=self.evidence,
                    max_output_tokens=96,
                    request_id="smoke-high-quality",
                    timeout_seconds=self.settings.real_llm_timeout_seconds,
                )
            )
        finally:
            provider.close()
        self.assertGreater(result.input_tokens + result.output_tokens, 0)
        self.assertTrue(result.executive_summary)
        self.assertTrue(result.markdown)


if __name__ == "__main__":
    print(
        "WARNING: This may incur OpenRouter API charges. "
        "Only run with explicit env flags and a configured budget."
    )
    unittest.main()
