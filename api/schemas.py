"""Pydantic response schemas for the read-only artifact API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    service: str
    read_only: bool
    production_backend: bool


class ArtifactTableResponse(BaseModel):
    """CSV artifact response as compact JSON records."""

    model_config = ConfigDict(protected_namespaces=())

    name: str
    path: str
    row_count: int
    columns: list[str]
    records: list[dict[str, Any]]


class ReportResponse(BaseModel):
    """Markdown report response."""

    name: str
    path: str
    content: str


class PresetQuestionsResponse(BaseModel):
    """Controlled RAG-lite preset question response."""

    questions: dict[str, str]


class ControlledSummaryResponse(BaseModel):
    """Controlled summary response for one preset question."""

    question_key: str
    question: str
    answer: str
    used_openai: bool
