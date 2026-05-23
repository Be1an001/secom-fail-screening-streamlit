"""MLOps, API, and AI summary page."""

from __future__ import annotations

import streamlit as st

from app_utils.artifact_loader import artifact_exists, load_markdown_artifact
from app_utils.layout_utils import render_artifact_list, render_info_box, render_page_intro


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

    if artifact_exists("reports/model_card.md"):
        with st.expander("Current model card artifact"):
            st.markdown(load_markdown_artifact("reports/model_card.md"))

    st.subheader("Planned Page Direction")
    st.write(
        "Later phases may add an artifact manifest, a minimal FastAPI artifact "
        "service, a future controlled RAG-lite summary, and a future agentic "
        "workflow concept. These are not implemented in this phase."
    )
