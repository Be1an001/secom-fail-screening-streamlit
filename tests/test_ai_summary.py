"""Tests for optional OpenAI controlled summaries."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app_utils import ai_summary


def test_generate_controlled_summary_respects_fallback_request(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_SUMMARY_ENABLED", "true")
    monkeypatch.setenv("OPENAI_API_KEY", "test-secret-value")
    monkeypatch.setenv("OPENAI_SUMMARY_MODEL", "gpt-5.4-mini")
    monkeypatch.setattr(
        ai_summary,
        "import_optional_openai",
        lambda: pytest.fail("OpenAI should not be imported for fallback."),
    )

    answer = ai_summary.generate_controlled_summary(
        "project_overview",
        use_openai=False,
    )

    assert "screening decision support" in answer
    assert "test-secret-value" not in answer


def test_openai_path_requires_enabled_flag(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_SUMMARY_ENABLED", "false")
    monkeypatch.setenv("OPENAI_API_KEY", "test-secret-value")
    monkeypatch.setenv("OPENAI_SUMMARY_MODEL", "gpt-5.4-mini")
    monkeypatch.setattr(
        ai_summary,
        "import_optional_openai",
        lambda: pytest.fail("OpenAI should not be imported when disabled."),
    )

    answer = ai_summary.generate_controlled_summary(
        "benchmark_summary",
        use_openai=True,
    )

    assert "prototype benchmark" in answer
    assert "test-secret-value" not in answer


def test_openai_success_path_uses_compact_context(monkeypatch) -> None:
    calls: list[dict[str, object]] = []

    class FakeResponses:
        def create(self, **kwargs):
            calls.append(kwargs)
            return SimpleNamespace(output_text="Controlled OpenAI summary.")

    class FakeClient:
        responses = FakeResponses()

    class FakeOpenAI:
        @staticmethod
        def OpenAI(api_key: str):
            assert api_key == "test-secret-value"
            return FakeClient()

    monkeypatch.setenv("OPENAI_SUMMARY_ENABLED", "true")
    monkeypatch.setenv("OPENAI_API_KEY", "test-secret-value")
    monkeypatch.setenv("OPENAI_SUMMARY_MODEL", "gpt-5.4-mini")
    monkeypatch.setattr(
        ai_summary.importlib.util,
        "find_spec",
        lambda name: object() if name == "openai" else None,
    )
    monkeypatch.setattr(ai_summary, "import_optional_openai", lambda: FakeOpenAI)

    answer = ai_summary.generate_controlled_summary(
        "explainability_summary",
        use_openai=True,
    )

    assert answer == "Controlled OpenAI summary."
    assert calls
    prompt_text = str(calls[0])
    assert "data/secom.data" not in prompt_text
    assert "data/secom_labels.data" not in prompt_text
    assert "test-secret-value" not in prompt_text
    assert "Use only the provided project context" in prompt_text


def test_openai_failure_returns_fallback_without_secret(monkeypatch) -> None:
    class BrokenResponses:
        def create(self, **_kwargs):
            raise RuntimeError("network unavailable")

    class BrokenClient:
        responses = BrokenResponses()

    class BrokenOpenAI:
        @staticmethod
        def OpenAI(api_key: str):
            assert api_key == "test-secret-value"
            return BrokenClient()

    monkeypatch.setenv("OPENAI_SUMMARY_ENABLED", "true")
    monkeypatch.setenv("OPENAI_API_KEY", "test-secret-value")
    monkeypatch.setenv("OPENAI_SUMMARY_MODEL", "gpt-5.4-mini")
    monkeypatch.setattr(
        ai_summary.importlib.util,
        "find_spec",
        lambda name: object() if name == "openai" else None,
    )
    monkeypatch.setattr(ai_summary, "import_optional_openai", lambda: BrokenOpenAI)

    answer = ai_summary.generate_controlled_summary(
        "limitations",
        use_openai=True,
    )

    assert "AI summary was unavailable" in answer
    assert "not a production backend" in answer
    assert "test-secret-value" not in answer


def test_unknown_question_key_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown preset question key"):
        ai_summary.generate_controlled_summary("free_form_prompt")
