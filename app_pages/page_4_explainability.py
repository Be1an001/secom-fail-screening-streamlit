"""Explainability page."""

from __future__ import annotations

import streamlit as st

from app_utils.artifact_loader import (
    artifact_exists,
    artifact_path,
    filter_manifest_artifacts,
    load_artifact_manifest,
    load_csv_artifact,
    load_markdown_artifact,
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
PERMUTATION_IMPORTANCE = "outputs/metrics/permutation_importance_prototype.csv"
FEATURE_STABILITY = "outputs/metrics/feature_stability_prototype.csv"
TOP_SENSOR_SIGNALS = "outputs/metrics/top_sensor_signals_prototype.csv"
PERMUTATION_IMPORTANCE_FIGURE = (
    "outputs/figures/permutation_importance_prototype.png"
)
FEATURE_STABILITY_FIGURE = "outputs/figures/feature_stability_prototype.png"
EXPLAINABILITY_REPORT = "reports/explainability_prototype_report.md"


def render() -> None:
    """Render the explainability placeholder page."""

    render_page_intro(
        "Explainability",
        "This page shows model-important sensor signals from the baseline "
        "workflow and prototype explainability artifacts.",
    )

    render_info_box(
        "Prototype explainability focuses on Random Forest Reference and "
        "XGBoost Cost-Sensitive. Feature importance is model behavior, not "
        "physical root-cause analysis and not causal proof."
    )

    _render_prototype_explainability()

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
            "reviewer feedback on sensor-signal explanation wording",
            "possible SHAP extension if it stays lightweight",
            "additional explainability artifacts with clear limits",
        ]
    )


def _render_prototype_explainability() -> None:
    st.subheader("Prototype explainability artifacts")

    if artifact_exists(PERMUTATION_IMPORTANCE_FIGURE):
        st.image(str(artifact_path(PERMUTATION_IMPORTANCE_FIGURE)))
    else:
        render_missing_artifact_warning(PERMUTATION_IMPORTANCE_FIGURE)

    if artifact_exists(FEATURE_STABILITY_FIGURE):
        st.image(str(artifact_path(FEATURE_STABILITY_FIGURE)))
    else:
        render_missing_artifact_warning(FEATURE_STABILITY_FIGURE)

    if artifact_exists(TOP_SENSOR_SIGNALS):
        st.write("Top model-important sensor signals across focus models")
        st.dataframe(
            load_csv_artifact(TOP_SENSOR_SIGNALS).head(20),
            use_container_width=True,
        )
    else:
        render_missing_artifact_warning(TOP_SENSOR_SIGNALS)

    with st.expander("Permutation importance and feature stability tables"):
        if artifact_exists(PERMUTATION_IMPORTANCE):
            st.write("Permutation importance")
            st.dataframe(
                load_csv_artifact(PERMUTATION_IMPORTANCE),
                use_container_width=True,
            )
        else:
            render_missing_artifact_warning(PERMUTATION_IMPORTANCE)

        if artifact_exists(FEATURE_STABILITY):
            st.write("Feature stability")
            st.dataframe(
                load_csv_artifact(FEATURE_STABILITY),
                use_container_width=True,
            )
        else:
            render_missing_artifact_warning(FEATURE_STABILITY)

    if artifact_exists(EXPLAINABILITY_REPORT):
        with st.expander("Prototype explainability report"):
            st.markdown(load_markdown_artifact(EXPLAINABILITY_REPORT))
    else:
        render_missing_artifact_warning(EXPLAINABILITY_REPORT)
