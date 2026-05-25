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
from app_utils.ai_summary import generate_controlled_summary
from app_utils.layout_utils import (
    render_artifact_tracking_note,
    render_card_grid,
    render_evidence_expander,
    render_kpi_cards,
    render_missing_artifact_warning,
    render_page_intro,
    render_process_timeline,
    render_section_header,
    render_summary_card,
    typewriter_text,
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
SUMMARY_TEXT_KEY = "controlled_summary_text"
SUMMARY_ANIMATE_KEY = "controlled_summary_animate"


def render() -> None:
    """Render the MLOps, API, and AI summary page."""

    render_page_intro(
        "API & AI Summary",
        "Explore the artifact-driven registry, local/demo FastAPI artifact "
        "service, and AI Summary feature that answers preset questions from "
        "compact project evidence.",
    )

    render_artifact_tracking_note()
    render_card_grid(
        [
            {
                "title": "Lightweight artifact registry",
                "body": "outputs/artifact_manifest.json connects metrics, figures, and reports to the app.",
            },
            {
                "title": "Local/demo API service",
                "body": "FastAPI endpoints serve existing artifacts only; they do not train models.",
            },
            {
                "title": "Controlled RAG-lite summary",
                "body": "Preset questions use compact artifact-grounded context. Raw CSVs are not sent.",
            },
        ],
        columns=3,
    )
    render_summary_card(
        "Portfolio boundary",
        "The API is not a production backend. AI Summary is not a general chatbot. "
        "Both features are included for portfolio review.",
    )

    _render_artifact_manifest_summary()
    _render_mlflow_summary()
    _render_api_overview()
    _render_controlled_summary_panel()
    _render_agentic_workflow_concept()
    _render_evidence_links()


def _render_artifact_manifest_summary() -> None:
    render_section_header(
        "Artifact tracking",
        "The public app reads committed artifacts instead of live experiment stores.",
    )
    if not artifact_exists("outputs/artifact_manifest.json"):
        render_missing_artifact_warning("outputs/artifact_manifest.json")
        return

    manifest = load_artifact_manifest()
    validate_manifest_paths(manifest)
    prototype_count = sum(
        1
        for artifact in manifest["artifacts"]
        if artifact.get("current_status") == "prototype"
    )
    available_reports = [path for path in REPORT_ARTIFACTS if artifact_exists(path)]
    available_prototype = [
        path for path in sorted(PROTOTYPE_ARTIFACT_PATHS) if artifact_exists(path)
    ]

    render_kpi_cards(
        [
            {
                "label": "Manifest artifacts",
                "value": str(len(manifest["artifacts"])),
                "caption": "Tracked evidence entries",
            },
            {
                "label": "Prototype artifacts",
                "value": str(prototype_count),
                "caption": "Benchmark, cost, and explainability outputs",
            },
            {
                "label": "Reports",
                "value": str(len(available_reports)),
                "caption": "Markdown evidence files",
            },
            {
                "label": "Key prototype files",
                "value": str(len(available_prototype)),
                "caption": "Metrics and reports used by the app",
            },
        ],
        columns=4,
    )


def _render_mlflow_summary() -> None:
    render_section_header(
        "MLOps-lite evidence",
        "Local MLflow tracking can support experiment review; committed views use exported artifacts.",
    )
    if artifact_exists(MLFLOW_SUMMARY):
        st.dataframe(
            load_csv_artifact(MLFLOW_SUMMARY),
            width="stretch",
            hide_index=True,
        )
    else:
        render_summary_card(
            "Exported MLflow summary",
            "No exported MLflow run summary is available in the public artifacts. "
            "The export script can create one when local run data exists.",
        )

    if artifact_exists(ARTIFACT_TRACKING_REPORT):
        with st.expander("MLflow and artifact tracking report", expanded=False):
            st.markdown(load_markdown_artifact(ARTIFACT_TRACKING_REPORT))


def _render_api_overview() -> None:
    render_section_header(
        "Read-only artifact service",
        "The local FastAPI service exposes selected project artifacts, metrics, reports, and summary endpoints for review or integration testing.",
    )
    render_summary_card(
        "FastAPI artifact service",
        "It does not train models or regenerate files. It simply reads the "
        "same committed artifacts that power the app.",
    )
    with st.expander("Run the local artifact service", expanded=False):
        st.code("python -m uvicorn api.main:app --reload", language="bash")
        st.markdown("API docs: <http://127.0.0.1:8000/docs>")
        st.markdown(
            "- `GET /health`\n"
            "- `GET /manifest`\n"
            "- `GET /metrics/benchmark`\n"
            "- `GET /metrics/cost-selected-thresholds`\n"
            "- `GET /metrics/explainability/top-sensors`\n"
            "- `GET /reports/model-card`\n"
            "- `GET /reports/cost-threshold`\n"
            "- `GET /reports/explainability`\n"
            "- `GET /summary/questions`\n"
            "- `GET /summary/{question_key}`"
        )


def _render_controlled_summary_panel() -> None:
    render_section_header(
        "AI Summary",
        "Generate a concise, artifact-grounded summary from preset project questions.",
    )
    st.caption(
        "This summary uses a controlled RAG-lite pattern: preset questions over "
        "compact project artifacts, not free-form chat. Raw CSVs are not sent."
    )

    questions = get_preset_questions()
    question_key = st.selectbox(
        "Preset question",
        list(questions.keys()),
        format_func=lambda key: questions[key],
    )

    if st.button("Generate summary", type="primary"):
        with st.spinner("Generating summary from curated artifacts..."):
            st.session_state[SUMMARY_TEXT_KEY] = generate_controlled_summary(
                question_key,
                use_openai=True,
            )
            st.session_state[SUMMARY_ANIMATE_KEY] = True

    summary = st.session_state.get(SUMMARY_TEXT_KEY)
    if summary:
        render_section_header("Generated summary")
        if st.session_state.get(SUMMARY_ANIMATE_KEY):
            typewriter_text(str(summary))
            st.session_state[SUMMARY_ANIMATE_KEY] = False
        else:
            st.markdown(str(summary))
    else:
        render_summary_card(
            "Ready when you are",
            "Choose a question and generate a concise project summary.",
        )


def _render_agentic_workflow_concept() -> None:
    render_section_header(
        "Extension Concept: Agentic Analytics Workflow",
        "The current app separates artifacts, metrics, reports, and summaries. "
        "An orchestration layer could review those steps while keeping human "
        "approval before any decision.",
    )
    render_process_timeline(
        [
            {
                "title": "Artifact monitor",
                "body": "Check whether expected metrics, figures, and reports exist.",
            },
            {
                "title": "Benchmark reviewer",
                "body": "Compare model outputs against the evaluation benchmark.",
            },
            {
                "title": "Cost trade-off analyst",
                "body": "Summarize threshold choices under illustrative review scenarios.",
            },
            {
                "title": "Explainability reviewer",
                "body": "Inspect model-important sensor signals and wording boundaries.",
            },
            {
                "title": "Summary generator",
                "body": "Create preset artifact-grounded summaries for review.",
            },
            {
                "title": "Human approval",
                "body": "Keep a person responsible for interpretation before any decision.",
            },
        ]
    )
    render_summary_card(
        "Architecture extension concept",
        "A tool framework such as LangGraph could orchestrate this review flow. "
        "LangGraph is not implemented here, and this app does not perform "
        "autonomous decision-making.",
    )


def _render_evidence_links() -> None:
    artifacts: list[str | dict[str, object]] = [
        "outputs/artifact_manifest.json",
        *sorted(PROTOTYPE_ARTIFACT_PATHS),
        *REPORT_ARTIFACTS,
    ]
    if artifact_exists("outputs/artifact_manifest.json"):
        manifest = load_artifact_manifest()
        artifacts.extend(
            filter_manifest_artifacts(
                manifest,
                page="Page 5 - MLOps, API, and AI Summary",
            )
        )
    render_evidence_expander(artifacts)
