"""Threshold / cost trade-off page."""

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
    render_evidence_expander,
    render_illustrative_cost_note,
    render_kpi_cards,
    render_method_reference_note,
    render_missing_artifact_warning,
    render_no_production_decision_note,
    render_page_intro,
    render_section_header,
    render_subtle_note,
)
from app_utils.metric_utils import (
    format_cost,
    format_count,
    format_metric,
    format_percent,
    format_threshold,
)
from app_utils.model_display import get_model_display


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
        "thresholds may catch more fail cases, but they can also increase "
        "review workload.",
    )
    render_illustrative_cost_note()
    render_no_production_decision_note()
    render_method_reference_note()

    if artifact_exists(COST_SELECTED_THRESHOLDS):
        selected = load_csv_artifact(COST_SELECTED_THRESHOLDS)
        _render_cost_controls(selected)
    else:
        render_missing_artifact_warning(COST_SELECTED_THRESHOLDS)

    with st.expander("Baseline holdout and threshold context", expanded=False):
        _render_baseline_threshold_context()

    if artifact_exists(COST_REPORT):
        with st.expander("Cost trade-off report", expanded=False):
            st.markdown(load_markdown_artifact(COST_REPORT))
    else:
        render_missing_artifact_warning(COST_REPORT)

    render_subtle_note(
        "Rows can be read as best under this illustrative scenario. This page "
        "does not create a production decision rule or select a final champion "
        "model.",
        title="How to read this page",
    )
    _render_evidence_links()


def _render_cost_controls(selected: object) -> None:
    selected = _add_display_roles(selected)
    scenario_options = sorted(selected["scenario"].dropna().unique().tolist())
    scenario = st.selectbox("Illustrative cost scenario", scenario_options)
    scenario_rows = selected[selected["scenario"] == scenario].copy()

    model_options = sorted(scenario_rows["model_name"].dropna().unique().tolist())
    model_name = st.selectbox(
        "Model",
        model_options,
        format_func=_format_model_option,
    )
    selected_row = scenario_rows[scenario_rows["model_name"] == model_name].iloc[0]

    render_section_header(
        "Selected threshold",
        "Cost assumptions can change which operating point looks most useful.",
    )
    st.caption(
        f"{selected_row['short_label']} - {selected_row['display_role']}. "
        f"{selected_row['main_message']}"
    )

    render_section_header("Decision and workload")
    render_kpi_cards(
        [
            {
                "label": "Threshold",
                "value": format_threshold(selected_row["selected_threshold"]),
                "caption": "Selected under this scenario",
            },
            {
                "label": "Flagged rate",
                "value": format_percent(selected_row["flagged_sample_rate"]),
                "caption": "Estimated review workload",
            },
        ],
        columns=2,
    )

    render_section_header("Performance")
    render_kpi_cards(
        [
            {
                "label": "Recall",
                "value": format_percent(selected_row["recall"]),
                "caption": "Share of fail cases caught",
            },
            {
                "label": "Precision",
                "value": format_percent(selected_row["precision"]),
                "caption": "Share of flags that are fail cases",
            },
            {
                "label": "F2-score",
                "value": format_metric(selected_row["f2"], digits=3),
                "caption": "Recall-weighted metric",
            },
        ],
        columns=3,
    )

    render_section_header("Cost and confusion matrix")
    render_kpi_cards(
        [
            {
                "label": "Total cost",
                "value": format_cost(selected_row["total_cost"]),
                "caption": "Illustrative cost units",
            },
            {
                "label": "Cost per sample",
                "value": format_cost(selected_row["cost_per_sample"]),
                "caption": "Cost normalized by validation samples",
            },
            {
                "label": "Reviewed counts",
                "value": (
                    f"TP {format_count(selected_row['tp'])} / "
                    f"FP {format_count(selected_row['fp'])}"
                ),
                "caption": (
                    f"FN {format_count(selected_row['fn'])} / "
                    f"TN {format_count(selected_row['tn'])}"
                ),
            },
        ],
        columns=3,
    )

    render_section_header("Selected thresholds for this scenario")
    st.dataframe(
        _format_cost_table(scenario_rows),
        width="stretch",
        hide_index=True,
    )


def _format_cost_table(rows: object) -> object:
    display = rows.loc[:, ["short_label", "display_role", *COST_DISPLAY_COLUMNS]].copy()
    display["selected_threshold"] = display["selected_threshold"].map(
        format_threshold
    )
    display["total_cost"] = display["total_cost"].map(format_cost)
    for column in ["recall", "precision", "flagged_sample_rate"]:
        display[column] = display[column].map(format_percent)
    display["f2"] = display["f2"].map(lambda value: format_metric(value, digits=3))
    return display


def _add_display_roles(rows: object) -> object:
    enriched = rows.copy()
    enriched["display_role"] = enriched["model_name"].map(
        lambda name: get_model_display(str(name))["display_role"]
    )
    enriched["short_label"] = enriched["model_name"].map(
        lambda name: get_model_display(str(name))["short_label"]
    )
    enriched["main_message"] = enriched["model_name"].map(
        lambda name: get_model_display(str(name))["main_message"]
    )
    return enriched


def _format_model_option(model_name: str) -> str:
    metadata = get_model_display(model_name)
    return f"{metadata['short_label']} ({metadata['display_role']})"


def _render_baseline_threshold_context() -> None:
    if artifact_exists(FINAL_TEST_METRICS):
        final_metrics = load_csv_artifact(FINAL_TEST_METRICS)
        row = final_metrics.iloc[0]

        render_section_header("Baseline holdout summary")
        render_kpi_cards(
            [
                {
                    "label": "Threshold",
                    "value": format_threshold(row["threshold"]),
                    "caption": "Baseline operating point",
                },
                {
                    "label": "Fail recall",
                    "value": format_percent(row["recall"]),
                    "caption": "Holdout fail recall",
                },
                {
                    "label": "F2-score",
                    "value": format_metric(row["f2"], digits=3),
                    "caption": "Recall-weighted metric",
                },
                {
                    "label": "Flagged rate",
                    "value": format_percent(row["review_rate"]),
                    "caption": "Baseline review workload",
                },
            ],
            columns=4,
        )
    else:
        render_missing_artifact_warning(FINAL_TEST_METRICS)

    if artifact_exists(THRESHOLD_SWEEP):
        sweep = load_csv_artifact(THRESHOLD_SWEEP)
        st.caption(
            f"The baseline threshold sweep artifact contains "
            f"{format_count(len(sweep))} candidate operating-point rows."
        )
    else:
        render_missing_artifact_warning(THRESHOLD_SWEEP)


def _render_evidence_links() -> None:
    artifacts: list[str | dict[str, object]] = [
        COST_SELECTED_THRESHOLDS,
        COST_THRESHOLD_SWEEP,
        COST_REPORT,
        FINAL_TEST_METRICS,
        THRESHOLD_SWEEP,
    ]

    if artifact_exists("outputs/artifact_manifest.json"):
        manifest = load_artifact_manifest()
        artifacts.extend(
            filter_manifest_artifacts(manifest, page="Page 3 - Champion Trade-off")
        )

    render_evidence_expander(artifacts)

    if artifact_exists(COST_THRESHOLD_SWEEP):
        cost_sweep = load_csv_artifact(COST_THRESHOLD_SWEEP)
        st.caption(
            "Full cost threshold sweep rows available: "
            f"{format_count(len(cost_sweep))}."
        )
