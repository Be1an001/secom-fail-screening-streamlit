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
    render_evidence_expander,
    render_missing_artifact_warning,
    render_page_intro,
    render_section_header,
    render_subtle_note,
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
    """Render the explainability page."""

    render_page_intro(
        "Explainability",
        "Review model-important sensor signals for the Random Forest Reference "
        "and XGBoost Cost-Sensitive models. These artifacts describe model "
        "behavior, not physical root-cause analysis.",
    )
    render_subtle_note(
        "Permutation importance and feature stability can support process "
        "investigation. They are not causal proof and not production "
        "diagnostics.",
        title="Interpretation boundary",
    )

    _render_prototype_figures()
    _render_top_sensor_table()
    _render_baseline_feature_importance()
    _render_table_details()
    _render_evidence_links()


def _render_prototype_figures() -> None:
    render_section_header(
        "Prototype explainability evidence",
        "Figures are shown directly so the page reads like evidence, not script output.",
    )
    if artifact_exists(PERMUTATION_IMPORTANCE_FIGURE):
        st.image(
            str(artifact_path(PERMUTATION_IMPORTANCE_FIGURE)),
            width="stretch",
        )
        st.caption(
            "Permutation importance compares model-important sensor signals "
            "for the focus models."
        )
    else:
        render_missing_artifact_warning(PERMUTATION_IMPORTANCE_FIGURE)

    if artifact_exists(FEATURE_STABILITY_FIGURE):
        st.image(str(artifact_path(FEATURE_STABILITY_FIGURE)), width="stretch")
        st.caption(
            "Feature stability shows whether top signals recur across multiple "
            "training seeds."
        )
    else:
        render_missing_artifact_warning(FEATURE_STABILITY_FIGURE)


def _render_top_sensor_table() -> None:
    render_section_header(
        "Top model-important sensor signals",
        "Anonymous sensor IDs are ranked from model behavior only.",
    )
    if artifact_exists(TOP_SENSOR_SIGNALS):
        st.dataframe(
            load_csv_artifact(TOP_SENSOR_SIGNALS).head(20),
            width="stretch",
            hide_index=True,
        )
    else:
        render_missing_artifact_warning(TOP_SENSOR_SIGNALS)


def _render_baseline_feature_importance() -> None:
    render_section_header(
        "Baseline feature importance",
        "The original Random Forest baseline figure remains useful as context.",
    )
    if artifact_exists(FEATURE_IMPORTANCE_FIGURE):
        st.image(str(artifact_path(FEATURE_IMPORTANCE_FIGURE)), width="stretch")
        st.caption(
            "Final feature importance is model-driven and not root-cause evidence."
        )
    else:
        render_missing_artifact_warning(FEATURE_IMPORTANCE_FIGURE)


def _render_table_details() -> None:
    with st.expander("CSV details", expanded=False):
        if artifact_exists(PERMUTATION_IMPORTANCE):
            st.write("Permutation importance")
            st.dataframe(
                load_csv_artifact(PERMUTATION_IMPORTANCE),
                width="stretch",
                hide_index=True,
            )
        else:
            render_missing_artifact_warning(PERMUTATION_IMPORTANCE)

        if artifact_exists(FEATURE_STABILITY):
            st.write("Feature stability")
            st.dataframe(
                load_csv_artifact(FEATURE_STABILITY),
                width="stretch",
                hide_index=True,
            )
        else:
            render_missing_artifact_warning(FEATURE_STABILITY)

        if artifact_exists(FEATURE_IMPORTANCE_CSV):
            st.write("Baseline final feature importance")
            st.dataframe(
                load_csv_artifact(FEATURE_IMPORTANCE_CSV),
                width="stretch",
                hide_index=True,
            )
        else:
            render_missing_artifact_warning(FEATURE_IMPORTANCE_CSV)

    if artifact_exists(EXPLAINABILITY_REPORT):
        with st.expander("Prototype explainability report", expanded=False):
            st.markdown(load_markdown_artifact(EXPLAINABILITY_REPORT))
    else:
        render_missing_artifact_warning(EXPLAINABILITY_REPORT)


def _render_evidence_links() -> None:
    artifacts: list[str | dict[str, object]] = [
        PERMUTATION_IMPORTANCE,
        FEATURE_STABILITY,
        TOP_SENSOR_SIGNALS,
        PERMUTATION_IMPORTANCE_FIGURE,
        FEATURE_STABILITY_FIGURE,
        FEATURE_IMPORTANCE_FIGURE,
        EXPLAINABILITY_REPORT,
    ]
    if artifact_exists("outputs/artifact_manifest.json"):
        manifest = load_artifact_manifest()
        artifacts.extend(
            filter_manifest_artifacts(manifest, page="Page 4 - Explainability")
        )
    render_evidence_expander(artifacts)
