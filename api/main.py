"""Minimal read-only FastAPI artifact service."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from api.artifact_service import (
    ArtifactNotFoundError,
    get_csv_artifact_response,
    get_manifest,
    get_report_response,
)
from api.schemas import (
    ArtifactTableResponse,
    ControlledSummaryResponse,
    HealthResponse,
    PresetQuestionsResponse,
    ReportResponse,
)
from app_utils.ai_summary import generate_controlled_summary
from app_utils.rag_context import get_preset_questions


BENCHMARK_METRICS = "outputs/metrics/benchmark_model_comparison_prototype.csv"
COST_SELECTED_THRESHOLDS = "outputs/metrics/cost_selected_thresholds_prototype.csv"
TOP_SENSOR_SIGNALS = "outputs/metrics/top_sensor_signals_prototype.csv"
MODEL_CARD = "reports/model_card.md"
COST_REPORT = "reports/cost_threshold_prototype_report.md"
EXPLAINABILITY_REPORT = "reports/explainability_prototype_report.md"

app = FastAPI(
    title="SECOM Artifact Service",
    description=(
        "Minimal read-only artifact service for a portfolio-scale SECOM "
        "screening decision support project. This is not a production backend."
    ),
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Return service health without touching model code."""

    return HealthResponse(
        status="ok",
        service="secom-artifact-service",
        read_only=True,
        production_backend=False,
    )


@app.get("/manifest")
def manifest() -> dict[str, object]:
    """Return the committed artifact manifest."""

    try:
        return get_manifest()
    except ArtifactNotFoundError as exc:
        raise http_404(str(exc)) from exc


@app.get("/metrics/benchmark", response_model=ArtifactTableResponse)
def benchmark_metrics() -> dict[str, object]:
    """Return prototype benchmark metrics."""

    return csv_response(BENCHMARK_METRICS, "benchmark_model_comparison_prototype")


@app.get("/metrics/cost-selected-thresholds", response_model=ArtifactTableResponse)
def cost_selected_thresholds() -> dict[str, object]:
    """Return selected thresholds for illustrative cost scenarios."""

    return csv_response(COST_SELECTED_THRESHOLDS, "cost_selected_thresholds_prototype")


@app.get("/metrics/explainability/top-sensors", response_model=ArtifactTableResponse)
def explainability_top_sensors() -> dict[str, object]:
    """Return the prototype top sensor signal summary."""

    return csv_response(TOP_SENSOR_SIGNALS, "top_sensor_signals_prototype")


@app.get("/reports/model-card", response_model=ReportResponse)
def model_card() -> dict[str, str]:
    """Return the current model card report."""

    return report_response(MODEL_CARD, "model_card")


@app.get("/reports/cost-threshold", response_model=ReportResponse)
def cost_threshold_report() -> dict[str, str]:
    """Return the prototype cost threshold report."""

    return report_response(COST_REPORT, "cost_threshold_prototype_report")


@app.get("/reports/explainability", response_model=ReportResponse)
def explainability_report() -> dict[str, str]:
    """Return the prototype explainability report."""

    return report_response(EXPLAINABILITY_REPORT, "explainability_prototype_report")


@app.get("/summary/questions", response_model=PresetQuestionsResponse)
def summary_questions() -> PresetQuestionsResponse:
    """Return allowed controlled RAG-lite preset questions."""

    return PresetQuestionsResponse(questions=get_preset_questions())


@app.get("/summary/{question_key}", response_model=ControlledSummaryResponse)
def controlled_summary(question_key: str) -> ControlledSummaryResponse:
    """Return an artifact-grounded fallback summary for one preset question."""

    questions = get_preset_questions()
    if question_key not in questions:
        raise HTTPException(
            status_code=404,
            detail="Unknown preset question key.",
        )

    return ControlledSummaryResponse(
        question_key=question_key,
        question=questions[question_key],
        answer=generate_controlled_summary(question_key, use_openai=False),
        used_openai=False,
    )


def csv_response(relative_path: str, name: str) -> dict[str, object]:
    """Return a CSV response or a clear 404."""

    try:
        return get_csv_artifact_response(relative_path, name)
    except ArtifactNotFoundError as exc:
        raise http_404(str(exc)) from exc


def report_response(relative_path: str, name: str) -> dict[str, str]:
    """Return a report response or a clear 404."""

    try:
        return get_report_response(relative_path, name)
    except ArtifactNotFoundError as exc:
        raise http_404(str(exc)) from exc


def http_404(message: str) -> HTTPException:
    """Build a consistent artifact 404 error."""

    return HTTPException(status_code=404, detail=message)
