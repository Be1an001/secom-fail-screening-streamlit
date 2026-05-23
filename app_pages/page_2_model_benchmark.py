"""Model benchmark page."""

from __future__ import annotations

import streamlit as st

from app_utils.artifact_loader import artifact_exists, load_csv_artifact
from app_utils.layout_utils import render_info_box, render_page_intro


VALIDATION_METRICS = "outputs/metrics/validation_metrics.csv"


def render() -> None:
    """Render the model benchmark placeholder page."""

    render_page_intro(
        "Model Benchmark",
        "This page will eventually show the six-model fail-screening benchmark. "
        "The current artifact is the baseline workflow comparison.",
    )

    render_info_box(
        "The current benchmark is not a completed six-model benchmark. Future "
        "phases may add planned literature-inspired upgrade methods and "
        "SOTA-inspired methods without claiming SOTA performance."
    )

    if artifact_exists(VALIDATION_METRICS):
        metrics = load_csv_artifact(VALIDATION_METRICS)
        st.subheader("Current validation metrics artifact")
        st.dataframe(metrics, use_container_width=True)
    else:
        st.warning(f"Missing metrics artifact: `{VALIDATION_METRICS}`")

    st.subheader("Planned Page Direction")
    st.write(
        "Later phases will add a reviewed six-model comparison, method notes, "
        "and clear links back to generated benchmark artifacts."
    )
