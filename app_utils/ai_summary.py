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


OPENAI_SUMMARY_ENABLED = "OPENAI_SUMMARY_ENABLED"
OPENAI_API_KEY = "OPENAI_API_KEY"
OPENAI_SUMMARY_MODEL = "OPENAI_SUMMARY_MODEL"
TRUE_VALUES = {"1", "true", "yes", "on"}
SYSTEM_INSTRUCTION = (
    "Use only the provided project context. Do not invent metrics, artifacts, "
    "deployment status, production readiness, root-cause claims, causal proof, "
    "or SOTA performance. If the context is insufficient, say so briefly. "
    "Answer in 4 to 8 concise sentences."
)


def generate_controlled_summary(
    question_key: str,
    context: dict[str, Any] | None = None,
    *,
    use_openai: bool | None = None,
) -> str:
    """Generate a controlled summary for one preset question key.

    OpenAI use is optional. It requires the feature flag, an API key, a model,
    the package, and either a caller request or default-enabled configuration.
    Tests do not require OpenAI, a key, or network access.
    """

    questions = get_preset_questions()
    if question_key not in questions:
        raise ValueError("Unknown preset question key.")

    summary_context = context or build_summary_context()
    fallback = answer_without_llm(question_key, summary_context)
    if should_use_openai_summary(use_openai):
        return generate_openai_summary(question_key, summary_context, fallback)
    return fallback


def is_openai_available() -> bool:
    """Return whether optional OpenAI summary generation can be used."""

    return (
        is_openai_summary_enabled()
        and importlib.util.find_spec("openai") is not None
        and bool(get_openai_api_key())
        and bool(get_openai_summary_model())
    )


def should_use_openai_summary(use_openai: bool | None) -> bool:
    """Return whether this request should try the OpenAI path."""

    if use_openai is False:
        return False
    return is_openai_available()


def is_openai_summary_enabled() -> bool:
    """Return whether OpenAI summaries are enabled by config."""

    value = get_config_value(OPENAI_SUMMARY_ENABLED)
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in TRUE_VALUES


def generate_openai_summary(
    question_key: str,
    context: dict[str, Any],
    fallback: str,
) -> str:
    """Generate an optional OpenAI summary from compact artifact context."""

    api_key = get_openai_api_key()
    model = get_openai_summary_model()
    if not api_key or not model:
        return fallback

    openai_module = import_optional_openai()
    if openai_module is None:
        return fallback

    try:
        client = openai_module.OpenAI(api_key=api_key)
        text = call_openai_client(client, model, question_key, context)
    except Exception:
        return (
            "AI summary was unavailable, so this fallback summary is shown. "
            + fallback
        )
    return text or fallback


def call_openai_client(
    client: Any,
    model: str,
    question_key: str,
    context: dict[str, Any],
) -> str:
    """Call an OpenAI client with compact context only."""

    questions = get_preset_questions()
    payload = {
        "preset_question_key": question_key,
        "preset_question": questions[question_key],
        "artifact_grounded_context": context,
    }
    if hasattr(client, "responses"):
        response = client.responses.create(
            model=model,
            instructions=SYSTEM_INSTRUCTION,
            input=json.dumps(payload, ensure_ascii=True),
            max_output_tokens=450,
        )
        return str(getattr(response, "output_text", "")).strip()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {
                "role": "user",
                "content": json.dumps(payload, ensure_ascii=True),
            },
        ],
        max_tokens=450,
    )
    return str(response.choices[0].message.content).strip()


def get_openai_api_key() -> str | None:
    """Read an optional OpenAI API key without requiring Streamlit."""

    value = get_config_value(OPENAI_API_KEY)
    return str(value) if value else None


def get_openai_summary_model() -> str | None:
    """Read the optional OpenAI summary model name."""

    value = get_config_value(OPENAI_SUMMARY_MODEL)
    return str(value) if value else None


def get_config_value(name: str) -> object | None:
    """Read config from Streamlit secrets first, then environment variables."""

    try:
        import streamlit as st
    except ImportError:
        return os.environ.get(name)

    try:
        value = st.secrets.get(name)
    except Exception:
        value = None
    if value not in (None, ""):
        return value
    return os.environ.get(name)


def import_optional_openai():
    """Import OpenAI only when optional use is explicitly available."""

    try:
        import openai
    except ImportError:
        return None
    return openai
