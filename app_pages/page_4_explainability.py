"""Explainability page."""

from __future__ import annotations

import streamlit as st

from app_utils.artifact_loader import (
    artifact_exists,
    artifact_path,
    filter_manifest_artifacts,
    load_artifact_manifest,
    load_csv_artifact,
)
from app_utils.layout_utils import (
    render_future_work_note,
    render_info_box,
    render_manifest_artifacts,
    render_missing_artifact_warning,
    render_page_intro,
)


FEATURE_IMPORTANCE_CSV = "outputs/metrics/final_feature_importance.csv"
FEATURE_IMPORTANCE_FIGURE = "outputs/figures/final_feature_importance.png"


def render() -> None:
    """Render the explainability placeholder page."""

    render_page_intro(
        "Explainability",
        "This page shows current model-important sensor signals from the "
        "baseline workflow and outlines future explainability artifacts.",
    )

    render_info_box(
        "Feature importance is model-driven signal ranking. It is not a "
        "physical root cause or causal sensor explanation."
    )

    if artifact_exists(FEATURE_IMPORTANCE_FIGURE):
        st.subheader("Current feature importance figure")
        st.image(str(artifact_path(FEATURE_IMPORTANCE_FIGURE)))
        st.caption("This figure ranks model-important sensor signals.")
    else:
        render_missing_artifact_warning(FEATURE_IMPORTANCE_FIGURE)

    if artifact_exists(FEATURE_IMPORTANCE_CSV):
        st.subheader("Current model-important sensor signals")
        st.dataframe(load_csv_artifact(FEATURE_IMPORTANCE_CSV), use_container_width=True)
    else:
        render_missing_artifact_warning(FEATURE_IMPORTANCE_CSV)

    if artifact_exists("outputs/artifact_manifest.json"):
        manifest = load_artifact_manifest()
        render_manifest_artifacts(
            "Manifest artifacts for this page",
            filter_manifest_artifacts(manifest, page="Page 4 - Explainability"),
        )

    render_future_work_note(
        [
            "stability checks for sensor-signal ranking",
            "permutation importance if added later",
            "additional explainability artifacts with clear limits",
        ]
    )
