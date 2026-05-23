"""Explainability page."""

from __future__ import annotations

import streamlit as st

from app_utils.artifact_loader import artifact_exists, artifact_path, load_csv_artifact
from app_utils.layout_utils import render_info_box, render_page_intro


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
    else:
        st.warning(f"Missing figure artifact: `{FEATURE_IMPORTANCE_FIGURE}`")

    if artifact_exists(FEATURE_IMPORTANCE_CSV):
        st.subheader("Current feature importance table")
        st.dataframe(load_csv_artifact(FEATURE_IMPORTANCE_CSV), use_container_width=True)
    else:
        st.warning(f"Missing metrics artifact: `{FEATURE_IMPORTANCE_CSV}`")

    st.subheader("Planned Page Direction")
    st.write(
        "Later phases may add stability checks, permutation importance, or "
        "other explainability artifacts if they remain clearly documented."
    )
