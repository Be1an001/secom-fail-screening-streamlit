"""Champion threshold trade-off page."""

from __future__ import annotations

import streamlit as st

from app_utils.artifact_loader import artifact_exists, load_csv_artifact
from app_utils.layout_utils import render_info_box, render_page_intro
from app_utils.metric_utils import format_count, format_metric, format_percent


FINAL_TEST_METRICS = "outputs/metrics/final_test_metrics.csv"
THRESHOLD_SWEEP = "outputs/metrics/threshold_sweep.csv"


def render() -> None:
    """Render the champion trade-off placeholder page."""

    render_page_intro(
        "Champion Trade-off",
        "This page summarizes the current validation-selected threshold and "
        "will later show a cost or review-capacity trade-off view.",
    )

    render_info_box(
        "The current threshold is a screening decision support setting. It is "
        "not an automatic pass/fail decision rule."
    )

    if artifact_exists(FINAL_TEST_METRICS):
        final_metrics = load_csv_artifact(FINAL_TEST_METRICS)
        row = final_metrics.iloc[0]

        st.subheader("Current holdout summary")
        columns = st.columns(4)
        columns[0].metric("Threshold", format_metric(row["threshold"], digits=3))
        columns[1].metric("Fail recall", format_percent(row["recall"]))
        columns[2].metric("F2-score", format_metric(row["f2"], digits=3))
        columns[3].metric("Flagged rate", format_percent(row["review_rate"]))

        st.write(
            f"At this threshold, the baseline workflow found "
            f"{format_count(row['tp'])} fail cases, missed "
            f"{format_count(row['fn'])} fail cases, and flagged "
            f"{format_count(row['fp'])} pass cases."
        )
    else:
        st.warning(f"Missing final metrics artifact: `{FINAL_TEST_METRICS}`")

    if artifact_exists(THRESHOLD_SWEEP):
        st.subheader("Current threshold sweep artifact")
        st.dataframe(load_csv_artifact(THRESHOLD_SWEEP), use_container_width=True)
    else:
        st.warning(f"Missing threshold sweep artifact: `{THRESHOLD_SWEEP}`")

    st.subheader("Planned Page Direction")
    st.write(
        "Later phases will add a simple cost trade-off and review-capacity "
        "view so reviewers can compare threshold choices."
    )
