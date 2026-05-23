"""Tests for controlled artifact-grounded RAG-lite context."""

from __future__ import annotations

import pytest

from app_utils.ai_summary import generate_controlled_summary, is_openai_available
from app_utils.rag_context import (
    answer_without_llm,
    build_summary_context,
    get_preset_questions,
)


def test_preset_questions_are_fixed_and_named() -> None:
    questions = get_preset_questions()

    assert set(questions) == {
        "project_overview",
        "benchmark_summary",
        "threshold_tradeoff",
        "explainability_summary",
        "mlops_artifact_tracking",
        "limitations",
    }


def test_summary_context_is_compact_and_artifact_grounded() -> None:
    context = build_summary_context()
    text = str(context).lower()

    assert "project_summary" in context
    assert "benchmark_metric_snapshot" in context
    assert "cost_scenario_summary" in context
    assert "explainability_top_sensor_snapshot" in context
    assert "responsible_use_limits" in context
    assert "data/secom.data" not in text
    assert "data/secom_labels.data" not in text


def test_fallback_answers_work_without_openai() -> None:
    context = build_summary_context()
    answer = answer_without_llm("threshold_tradeoff", context)

    assert "Threshold is a decision lever" in answer
    assert "review workload" in answer


def test_unknown_preset_question_is_rejected() -> None:
    context = build_summary_context()

    with pytest.raises(ValueError, match="Unknown preset question key"):
        answer_without_llm("tell_me_anything", context)

    with pytest.raises(ValueError, match="Unknown preset question key"):
        generate_controlled_summary("tell_me_anything", context)


def test_generate_controlled_summary_uses_fallback_by_default() -> None:
    answer = generate_controlled_summary("limitations")

    assert "not a production backend" in answer
    assert "production readiness" in answer


def test_openai_is_not_required_for_tests() -> None:
    assert isinstance(is_openai_available(), bool)
