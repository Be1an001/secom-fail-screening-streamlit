"""Controlled artifact-grounded context for RAG-lite summaries."""

from __future__ import annotations

from typing import Any

import pandas as pd

from app_utils.artifact_loader import (
    artifact_exists,
    filter_manifest_artifacts,
    load_artifact_manifest,
    load_csv_artifact,
)
from app_utils.model_display import MODEL_DISPLAY_ROLES


BENCHMARK_METRICS = "outputs/metrics/benchmark_model_comparison_prototype.csv"
COST_SELECTED_THRESHOLDS = "outputs/metrics/cost_selected_thresholds_prototype.csv"
TOP_SENSOR_SIGNALS = "outputs/metrics/top_sensor_signals_prototype.csv"
MODEL_IMPORTANT_LIMIT = 8


def get_preset_questions() -> dict[str, str]:
    """Return allowed controlled RAG-lite question keys."""

    return {
        "project_overview": "What does this SECOM portfolio project show?",
        "benchmark_summary": "What does the prototype benchmark show?",
        "threshold_tradeoff": "How should threshold and cost trade-offs be read?",
        "explainability_summary": "What do the explainability artifacts show?",
        "mlops_artifact_tracking": "How does artifact tracking work here?",
        "limitations": "What are the main limitations and non-goals?",
    }


def build_summary_context() -> dict[str, Any]:
    """Build compact artifact-grounded context without raw data files."""

    manifest = load_artifact_manifest()
    context: dict[str, Any] = {
        "project_summary": {
            "name": "SECOM fail-screening portfolio",
            "purpose": "screening decision support",
            "app_type": "artifact-driven Streamlit app",
            "dataset_rows": 1567,
            "sensor_features": 590,
            "fail_samples": 104,
            "fail_rate": 0.0664,
        },
        "model_display_grouping": MODEL_DISPLAY_ROLES,
        "benchmark_metric_snapshot": load_benchmark_snapshot(),
        "cost_scenario_summary": load_cost_snapshot(),
        "explainability_top_sensor_snapshot": load_top_sensor_snapshot(),
        "responsible_use_limits": [
            "not a production backend",
            "not a production decision rule",
            "not automatic pass/fail decision-making",
            "not physical root-cause analysis",
            "not causal proof",
            "not SOTA performance",
            "not a general chatbot",
        ],
        "available_reports": [
            artifact["path"]
            for artifact in filter_manifest_artifacts(manifest, artifact_type="report")
        ],
    }
    return context


def answer_without_llm(question_key: str, context: dict[str, Any]) -> str:
    """Return a controlled fallback answer for a preset question."""

    questions = get_preset_questions()
    if question_key not in questions:
        raise ValueError("Unknown preset question key.")

    if question_key == "project_overview":
        project = context["project_summary"]
        return (
            "This project presents the UCI SECOM fail-screening benchmark as "
            "screening decision support. The app is artifact-driven: it reads "
            f"curated metrics and reports for {project['dataset_rows']} rows, "
            f"{project['sensor_features']} anonymous sensor features, and a "
            f"fail rate of about {project['fail_rate'] * 100:.2f}%."
        )

    if question_key == "benchmark_summary":
        rows = context["benchmark_metric_snapshot"]
        rf = find_record(rows, "random_forest_reference")
        xgb = find_record(rows, "xgboost_cost_sensitive")
        return (
            "The prototype benchmark keeps all six models in the artifacts. "
            f"Random Forest Reference has prototype F2 {rf.get('f2', 'n/a')}, "
            "while XGBoost Cost-Sensitive is presented as a higher-recall "
            f"option with recall {xgb.get('recall', 'n/a')} and flagged rate "
            f"{xgb.get('flagged_sample_rate', 'n/a')}."
        )

    if question_key == "threshold_tradeoff":
        scenarios = sorted(
            {str(row["scenario"]) for row in context["cost_scenario_summary"]}
        )
        return (
            "Threshold is a decision lever. Lower thresholds may catch more "
            "missed fail cases but can increase review workload. The current "
            "illustrative cost scenarios are: " + ", ".join(scenarios) + "."
        )

    if question_key == "explainability_summary":
        sensors = context["explainability_top_sensor_snapshot"][:5]
        features = ", ".join(str(row["feature"]) for row in sensors)
        return (
            "Prototype explainability summarizes model-important sensor "
            "signals for Random Forest Reference and XGBoost Cost-Sensitive. "
            f"Top shared anonymous sensor signals include {features}. These "
            "rankings are not physical root-cause analysis and not causal proof."
        )

    if question_key == "mlops_artifact_tracking":
        return (
            "The app uses outputs/artifact_manifest.json as a lightweight "
            "artifact registry. Local MLflow tracking can support review, but "
            "local MLflow databases and run folders are ignored. Public views "
            "use committed exported artifacts."
        )

    limits = "; ".join(context["responsible_use_limits"])
    return (
        "The main limits are: " + limits + ". The project stays "
        "portfolio-scale and does not claim production readiness."
    )


def load_benchmark_snapshot() -> list[dict[str, Any]]:
    """Load a compact benchmark snapshot from the prototype artifact."""

    if not artifact_exists(BENCHMARK_METRICS):
        return []
    columns = [
        "model_name",
        "status",
        "threshold",
        "recall",
        "precision",
        "f2",
        "pr_auc",
        "roc_auc",
        "flagged_sample_rate",
    ]
    return select_columns(load_csv_artifact(BENCHMARK_METRICS), columns)


def load_cost_snapshot() -> list[dict[str, Any]]:
    """Load a compact selected-threshold snapshot."""

    if not artifact_exists(COST_SELECTED_THRESHOLDS):
        return []
    columns = [
        "model_name",
        "scenario",
        "selected_threshold",
        "total_cost",
        "recall",
        "precision",
        "f2",
        "flagged_sample_rate",
    ]
    return select_columns(load_csv_artifact(COST_SELECTED_THRESHOLDS), columns)


def load_top_sensor_snapshot() -> list[dict[str, Any]]:
    """Load a compact top sensor signal snapshot."""

    if not artifact_exists(TOP_SENSOR_SIGNALS):
        return []
    columns = ["feature", "models_where_top", "model_count", "best_rank", "mean_rank"]
    return select_columns(
        load_csv_artifact(TOP_SENSOR_SIGNALS).head(MODEL_IMPORTANT_LIMIT),
        columns,
    )


def select_columns(frame: pd.DataFrame, columns: list[str]) -> list[dict[str, Any]]:
    """Return selected columns as JSON-safe records."""

    existing_columns = [column for column in columns if column in frame.columns]
    selected = frame.loc[:, existing_columns].copy()
    return selected.where(selected.notna(), None).to_dict(orient="records")


def find_record(records: list[dict[str, Any]], model_name: str) -> dict[str, Any]:
    """Find one model record in a compact snapshot."""

    for record in records:
        if record.get("model_name") == model_name:
            return record
    return {}
