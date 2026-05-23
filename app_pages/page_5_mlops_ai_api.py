"""MLOps, API, and AI summary page."""

from __future__ import annotations

import streamlit as st

from app_utils.artifact_loader import (
    artifact_exists,
    filter_manifest_artifacts,
    load_artifact_manifest,
    load_markdown_artifact,
    validate_manifest_paths,
)
from app_utils.layout_utils import (
    render_artifact_list,
    render_future_work_note,
    render_info_box,
    render_manifest_artifacts,
    render_missing_artifact_warning,
    render_page_intro,
)


REPORT_ARTIFACTS = [
    "reports/experiment_summary.md",
    "reports/model_card.md",
    "outputs/README.md",
]


def render() -> None:
    """Render the MLOps, API, and AI summary placeholder page."""

    render_page_intro(
        "MLOps, API, and AI Summary",
        "This page summarizes current MLOps-lite evidence and marks future API "
        "and AI summary work as planned, not complete.",
    )

    render_info_box(
        "No FastAPI service, OpenAI call, or future controlled RAG-lite summary "
        "runs in this app skeleton."
    )

    available_reports = [path for path in REPORT_ARTIFACTS if artifact_exists(path)]
    render_artifact_list("Available report artifacts", available_reports)

    if artifact_exists("outputs/artifact_manifest.json"):
        manifest = load_artifact_manifest()
        validate_manifest_paths(manifest)
        st.subheader("Artifact manifest")
        st.write(
            f"The baseline manifest lists {len(manifest['artifacts'])} existing "
            "baseline artifacts."
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

    if artifact_exists("reports/model_card.md"):
        with st.expander("Current model card artifact"):
            st.markdown(load_markdown_artifact("reports/model_card.md"))

    render_future_work_note(
        [
            "MLflow summary export",
            "minimal FastAPI artifact service",
            "future controlled RAG-lite summary",
            "future agentic workflow concept",
        ]
    )
