"""Champion threshold trade-off page."""

from __future__ import annotations

import streamlit as st

from app_utils.artifact_loader import (
    artifact_exists,
    filter_manifest_artifacts,
    load_artifact_manifest,
    load_csv_artifact,
    load_markdown_artifact,
)
from app_utils.layout_utils import (
    render_future_work_note,
    render_illustrative_cost_note,
    render_manifest_artifacts,
    render_missing_artifact_warning,
    render_no_production_decision_note,
    render_page_intro,
    render_prototype_note,
)
from app_utils.metric_utils import (
    format_cost,
    format_count,
    format_metric,
    format_percent,
    format_threshold,
)


FINAL_TEST_METRICS = "outputs/metrics/final_test_metrics.csv"
THRESHOLD_SWEEP = "outputs/metrics/threshold_sweep.csv"
COST_SELECTED_THRESHOLDS = (
    "outputs/metrics/cost_selected_thresholds_prototype.csv"
)
COST_THRESHOLD_SWEEP = "outputs/metrics/cost_threshold_sweep_prototype.csv"
COST_REPORT = "reports/cost_threshold_prototype_report.md"
COST_DISPLAY_COLUMNS = [
    "model_name",
    "selected_threshold",
    "total_cost",
    "recall",
    "precision",
    "f2",
    "flagged_sample_rate",
]


def render() -> None:
    """Render the threshold / cost trade-off page."""

    render_page_intro(
        "Threshold and Cost Trade-off",
        "Threshold is a decision lever for screening decision support. Lower "
        "thresholds may catch more fail cases but can increase review workload.",
    )
    render_prototype_note()
    render_illustrative_cost_note()
    render_no_production_decision_note()

    if artifact_exists(COST_SELECTED_THRESHOLDS):
        selected = load_csv_artifact(COST_SELECTED_THRESHOLDS)
        _render_cost_controls(selected)
    else:
        render_missing_artifact_warning(COST_SELECTED_THRESHOLDS)

    with st.expander("Baseline holdout and threshold artifacts"):
        _render_baseline_threshold_context()

    if artifact_exists(COST_THRESHOLD_SWEEP):
        cost_sweep = load_csv_artifact(COST_THRESHOLD_SWEEP)
        st.caption(
            f"The prototype cost threshold sweep artifact contains "
            f"{format_count(len(cost_sweep))} model-threshold-scenario rows."
        )
    else:
        render_missing_artifact_warning(COST_THRESHOLD_SWEEP)

    if artifact_exists(COST_REPORT):
        with st.expander("Cost trade-off report"):
            st.markdown(load_markdown_artifact(COST_REPORT))
    else:
        render_missing_artifact_warning(COST_REPORT)

    if artifact_exists("outputs/artifact_manifest.json"):
        manifest = load_artifact_manifest()
        render_manifest_artifacts(
            "Manifest artifacts for this page",
            filter_manifest_artifacts(manifest, page="Page 3 - Champion Trade-off"),
        )

    st.write(
        "Rows in this page can be described as best under this illustrative "
        "scenario. This page does not select a final champion model and does "
        "not create a production decision rule."
    )
    render_future_work_note(
        [
            "reviewer-approved cost assumptions",
            "clearer threshold decision support visuals",
            "app integration with final benchmark review",
        ]
    )


def _render_cost_controls(selected: object) -> None:
    scenario_options = sorted(selected["scenario"].dropna().unique().tolist())
    scenario = st.selectbox("Illustrative cost scenario", scenario_options)
    scenario_rows = selected[selected["scenario"] == scenario].copy()

    model_options = sorted(scenario_rows["model_name"].dropna().unique().tolist())
    model_name = st.selectbox("Model", model_options)
    selected_row = scenario_rows[scenario_rows["model_name"] == model_name].iloc[0]

    st.subheader("Selected threshold for this model and scenario")
    cols = st.columns(4)
    cols[0].metric(
        "Threshold",
        format_threshold(selected_row["selected_threshold"]),
    )
    cols[1].metric("Total cost", format_cost(selected_row["total_cost"]))
    cols[2].metric("Cost per sample", format_cost(selected_row["cost_per_sample"]))
    cols[3].metric("Flagged rate", format_percent(selected_row["flagged_sample_rate"]))

    cols = st.columns(4)
    cols[0].metric("Recall", format_percent(selected_row["recall"]))
    cols[1].metric("Precision", format_percent(selected_row["precision"]))
    cols[2].metric("F2-score", format_metric(selected_row["f2"], digits=3))
    cols[3].metric(
        "Confusion counts",
        (
            f"TP {format_count(selected_row['tp'])} / "
            f"FP {format_count(selected_row['fp'])} / "
            f"FN {format_count(selected_row['fn'])} / "
            f"TN {format_count(selected_row['tn'])}"
        ),
    )

    st.caption(str(selected_row.get("notes", "")))
    st.subheader("All selected thresholds for this scenario")
    st.dataframe(
        _format_cost_table(scenario_rows),
        use_container_width=True,
        hide_index=True,
    )


def _format_cost_table(rows: object) -> object:
    display = rows.loc[:, COST_DISPLAY_COLUMNS].copy()
    display["selected_threshold"] = display["selected_threshold"].map(
        format_threshold
    )
    display["total_cost"] = display["total_cost"].map(format_cost)
    for column in ["recall", "precision", "flagged_sample_rate"]:
        display[column] = display[column].map(format_percent)
    display["f2"] = display["f2"].map(lambda value: format_metric(value, digits=3))
    return display


def _render_baseline_threshold_context() -> None:
    if artifact_exists(FINAL_TEST_METRICS):
        final_metrics = load_csv_artifact(FINAL_TEST_METRICS)
        row = final_metrics.iloc[0]

        st.subheader("Baseline holdout summary")
        columns = st.columns(4)
        columns[0].metric("Threshold", format_threshold(row["threshold"]))
        columns[1].metric("Fail recall", format_percent(row["recall"]))
        columns[2].metric("F2-score", format_metric(row["f2"], digits=3))
        columns[3].metric("Flagged rate", format_percent(row["review_rate"]))
    else:
        render_missing_artifact_warning(FINAL_TEST_METRICS)

    if artifact_exists(THRESHOLD_SWEEP):
        sweep = load_csv_artifact(THRESHOLD_SWEEP)
        st.write(
            f"The baseline threshold sweep artifact contains "
            f"{format_count(len(sweep))} candidate operating-point rows."
        )
    else:
        render_missing_artifact_warning(THRESHOLD_SWEEP)
