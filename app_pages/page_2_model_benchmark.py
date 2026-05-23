"""Model benchmark page."""

from __future__ import annotations

import streamlit as st

from app_utils.artifact_loader import (
    artifact_exists,
    filter_manifest_artifacts,
    load_artifact_manifest,
    load_csv_artifact,
)
from app_utils.layout_utils import (
    render_info_box,
    render_manifest_artifacts,
    render_page_intro,
)


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
        display_columns = [
            "experiment_name",
            "model_type",
            "threshold",
            "recall",
            "f2",
            "balanced_accuracy",
            "pr_auc",
            "review_rate",
        ]
        st.subheader("Current baseline validation metrics")
        st.dataframe(metrics[display_columns], use_container_width=True)
    else:
        st.warning(f"Missing metrics artifact: `{VALIDATION_METRICS}`")

    if artifact_exists("outputs/artifact_manifest.json"):
        manifest = load_artifact_manifest()
        render_manifest_artifacts(
            "Manifest artifacts for this page",
            filter_manifest_artifacts(manifest, page="Page 2 - Model Benchmark"),
        )

    st.subheader("Planned Page Direction")
    st.write(
        "Future phases will add literature-inspired and SOTA-inspired model "
        "comparisons under the same leakage-safe protocol. This page does not "
        "claim SOTA performance."
    )
