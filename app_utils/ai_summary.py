"""Controlled summary helper for preset artifact-grounded questions."""

from __future__ import annotations

import importlib.util
import json
import os
from typing import Any

from app_utils.rag_context import (
    answer_without_llm,
    build_summary_context,
    get_preset_questions,
)


def generate_controlled_summary(
    question_key: str,
    context: dict[str, Any] | None = None,
    *,
    use_openai: bool = False,
) -> str:
    """Generate a controlled summary for one preset question key.

    The default path is fallback-only. Optional OpenAI use is future-ready and
    requires an installed package, an API key, and an explicit model name in the
    environment. Tests do not require OpenAI or network access.
    """

    questions = get_preset_questions()
    if question_key not in questions:
        raise ValueError("Unknown preset question key.")

    summary_context = context or build_summary_context()
    if use_openai and is_openai_available():
        return generate_openai_summary(question_key, summary_context)
    return answer_without_llm(question_key, summary_context)


def is_openai_available() -> bool:
    """Return whether optional OpenAI summary generation can be used."""

    return (
        importlib.util.find_spec("openai") is not None
        and bool(get_openai_api_key())
        and bool(os.getenv("OPENAI_SUMMARY_MODEL"))
    )


def generate_openai_summary(question_key: str, context: dict[str, Any]) -> str:
    """Generate an optional OpenAI summary from compact artifact context."""

    api_key = get_openai_api_key()
    model = os.getenv("OPENAI_SUMMARY_MODEL")
    if not api_key or not model:
        return answer_without_llm(question_key, context)

    openai_module = import_optional_openai()
    if openai_module is None:
        return answer_without_llm(question_key, context)

    client = openai_module.OpenAI(api_key=api_key)
    questions = get_preset_questions()
    prompt = {
        "instruction": (
            "Answer only the selected preset question using the compact "
            "artifact-grounded context. Do not claim production readiness, "
            "automatic decision-making, root cause, causal proof, or SOTA "
            "performance."
        ),
        "question": questions[question_key],
        "context": context,
    }
    response = client.responses.create(
        model=model,
        input=json.dumps(prompt, ensure_ascii=True),
    )
    text = getattr(response, "output_text", "")
    return str(text).strip() or answer_without_llm(question_key, context)


def get_openai_api_key() -> str | None:
    """Read an optional OpenAI API key without requiring Streamlit."""

    if os.getenv("OPENAI_API_KEY"):
        return os.getenv("OPENAI_API_KEY")

    try:
        import streamlit as st
    except ImportError:
        return None

    try:
        value = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        return None
    return str(value) if value else None


def import_optional_openai():
    """Import OpenAI only when optional use is explicitly available."""

    try:
        import openai
    except ImportError:
        return None
    return openai
