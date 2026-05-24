"""MLOps, API, and AI summary page."""

from __future__ import annotations

import streamlit as st

from app_utils.artifact_loader import (
    artifact_exists,
    filter_manifest_artifacts,
    load_artifact_manifest,
    load_csv_artifact,
    load_markdown_artifact,
    validate_manifest_paths,
)
from app_utils.ai_summary import (
    generate_controlled_summary,
    is_openai_available,
    is_openai_summary_enabled,
)
from app_utils.layout_utils import (
    render_artifact_list,
    render_artifact_tracking_note,
    render_future_work_note,
    render_info_box,
    render_manifest_artifacts,
    render_missing_artifact_warning,
    render_page_intro,
)
from app_utils.rag_context import get_preset_questions


REPORT_ARTIFACTS = [
    "reports/experiment_summary.md",
    "reports/model_card.md",
    "reports/benchmark_prototype_summary.md",
    "reports/cost_threshold_prototype_report.md",
    "reports/explainability_prototype_report.md",
    "reports/mlflow_artifact_tracking_summary.md",
    "outputs/README.md",
]
PROTOTYPE_ARTIFACT_PATHS = {
    "outputs/metrics/benchmark_model_comparison_prototype.csv",
    "outputs/metrics/benchmark_threshold_sweep_prototype.csv",
    "outputs/metrics/cost_selected_thresholds_prototype.csv",
    "outputs/metrics/cost_threshold_sweep_prototype.csv",
    "outputs/metrics/permutation_importance_prototype.csv",
    "outputs/metrics/feature_stability_prototype.csv",
    "outputs/metrics/top_sensor_signals_prototype.csv",
    "reports/benchmark_prototype_summary.md",
    "reports/cost_threshold_prototype_report.md",
    "reports/explainability_prototype_report.md",
}
MLFLOW_SUMMARY = "outputs/metrics/mlflow_runs_summary.csv"
ARTIFACT_TRACKING_REPORT = "reports/mlflow_artifact_tracking_summary.md"


def render() -> None:
    """Render the MLOps, API, and AI summary placeholder page."""

    render_page_intro(
        "MLOps, API, and AI Summary",
        "This artifact-driven page summarizes current MLOps-lite evidence, "
        "artifact tracking, and future API and AI summary work that remains "
        "planned.",
    )

    render_artifact_tracking_note()
    render_info_box(
        "The optional FastAPI artifact service is a local read-only portfolio "
        "demo. It is not a production backend."
    )
    render_info_box(
        "The app now includes full six-model prototype benchmark artifacts, "
        "display grouping for readability, threshold/cost trade-off artifacts, "
        "and prototype explainability artifacts."
    )
    render_info_box(
        "Local MLflow tracking files such as `mlflow.db`, `mlruns/`, and "
        "`mlartifacts/` are intentionally ignored. An exported MLflow summary "
        "may be shown here only when real local run data is available."
    )
    render_info_box(
        "The controlled RAG-lite summary can use an optional OpenAI summary "
        "path with preset questions and compact artifact-grounded context. It "
        "is not a general chatbot, and raw CSVs are not sent to an LLM."
    )

    available_reports = [path for path in REPORT_ARTIFACTS if artifact_exists(path)]
    render_artifact_list("Available report artifacts", available_reports)

    if artifact_exists("outputs/artifact_manifest.json"):
        manifest = load_artifact_manifest()
        validate_manifest_paths(manifest)
        st.subheader("Artifact manifest")
        prototype_count = sum(
            1
            for artifact in manifest["artifacts"]
            if artifact.get("current_status") == "prototype"
        )
        st.write(
            f"The artifact manifest lists {len(manifest['artifacts'])} "
            f"artifacts, including {prototype_count} prototype artifacts."
        )
        render_artifact_list(
            "Benchmark and cost trade-off artifacts",
            [
                path
                for path in sorted(PROTOTYPE_ARTIFACT_PATHS)
                if artifact_exists(path)
            ],
        )
        render_manifest_artifacts(
            "Manifest artifacts for this page",
            filter_manifest_artifacts(
                manifest,
                page="Page 5 - MLOps, API, and AI Summary",
            ),
        )
    else:
        render_missing_artifact_warning("outputs/artifact_manifest.json")

    st.subheader("Exported MLflow summary")
    if artifact_exists(MLFLOW_SUMMARY):
        st.dataframe(
            load_csv_artifact(MLFLOW_SUMMARY),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.caption(
            "No exported MLflow summary artifact is available yet. Run "
            "`python scripts/export_mlflow_runs_summary.py` after local MLflow "
            "tracking data exists to create one."
        )

    if artifact_exists(ARTIFACT_TRACKING_REPORT):
        with st.expander("MLflow and artifact tracking summary"):
            st.markdown(load_markdown_artifact(ARTIFACT_TRACKING_REPORT))

    if artifact_exists("reports/model_card.md"):
        with st.expander("Current model card artifact"):
            st.markdown(load_markdown_artifact("reports/model_card.md"))

    _render_api_and_summary_section()

    st.write(
        "These future workflow features are not implemented in this phase. "
        "This page does not implement a deployed MLflow tracking server, "
        "production backend, general chatbot, or agentic workflow automation."
    )
    render_future_work_note(
        [
            "review of exported MLflow summary if real local run data exists",
            "possible refinement of the local FastAPI artifact service",
            "optional OpenAI API use for controlled RAG-lite summaries",
            "future agentic workflow concept",
        ]
    )


def _render_api_and_summary_section() -> None:
    st.subheader("Local API and controlled summary")
    st.write("Run the read-only artifact service locally with:")
    st.code("uvicorn api.main:app --reload", language="bash")
    render_artifact_list(
        "Available local API endpoints",
        [
            "GET /health",
            "GET /manifest",
            "GET /metrics/benchmark",
            "GET /metrics/cost-selected-thresholds",
            "GET /metrics/explainability/top-sensors",
            "GET /reports/model-card",
            "GET /reports/cost-threshold",
            "GET /reports/explainability",
            "GET /summary/questions",
            "GET /summary/{question_key}",
        ],
    )

    st.write(
        "No API key is stored in the repo. OpenAI API use is optional, and the "
        "fallback summary works without secrets, OpenAI package access, or "
        "network access."
    )
    st.caption(
        "Optional OpenAI status: "
        f"{'enabled and configured' if is_openai_available() else 'fallback summary only'}."
    )

    questions = get_preset_questions()
    question_key = st.selectbox(
        "Controlled RAG-lite preset question",
        list(questions.keys()),
        format_func=lambda key: questions[key],
    )
    use_openai = st.checkbox(
        "Use OpenAI summary if configured",
        value=False,
        help=(
            "Requires OPENAI_SUMMARY_ENABLED=true, OPENAI_API_KEY, and "
            "OPENAI_SUMMARY_MODEL in Streamlit secrets or environment variables."
        ),
    )
    if use_openai and not is_openai_available():
        if not is_openai_summary_enabled():
            st.caption("OpenAI summary is disabled; showing fallback summary.")
        else:
            st.caption(
                "OpenAI summary is not fully configured or the package is "
                "unavailable; showing fallback summary."
            )

    st.write(generate_controlled_summary(question_key, use_openai=use_openai))
