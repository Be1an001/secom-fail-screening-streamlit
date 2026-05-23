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
    render_future_work_note,
    render_info_box,
    render_manifest_artifacts,
    render_missing_artifact_warning,
    render_page_intro,
    render_prototype_note,
)
from app_utils.metric_utils import format_metric, format_percent, format_threshold


VALIDATION_METRICS = "outputs/metrics/validation_metrics.csv"
PROTOTYPE_MODEL_COMPARISON = (
    "outputs/metrics/benchmark_model_comparison_prototype.csv"
)
PROTOTYPE_THRESHOLD_SWEEP = (
    "outputs/metrics/benchmark_threshold_sweep_prototype.csv"
)
LEADERBOARD_COLUMNS = [
    "model_name",
    "model_group",
    "status",
    "threshold",
    "recall",
    "precision",
    "f2",
    "pr_auc",
    "roc_auc",
    "flagged_sample_rate",
]


def render() -> None:
    """Render the model benchmark page."""

    render_page_intro(
        "Model Benchmark",
        "This page compares the current baseline workflow with a prototype "
        "literature-inspired benchmark. These results are prototype artifacts, "
        "not final model-selection results.",
    )
    render_prototype_note()
    render_info_box(
        "Random Forest reference currently has the strongest F2 in the "
        "prototype benchmark. XGBoost cost-sensitive provides a higher-recall "
        "option, but with a higher flagged sample rate. This page makes no "
        "SOTA performance claim."
    )

    if artifact_exists(PROTOTYPE_MODEL_COMPARISON):
        comparison = load_csv_artifact(PROTOTYPE_MODEL_COMPARISON)
        st.subheader("Prototype benchmark leaderboard")
        st.dataframe(
            _format_leaderboard(comparison),
            use_container_width=True,
            hide_index=True,
        )
        _render_model_highlights(comparison)
    else:
        render_missing_artifact_warning(PROTOTYPE_MODEL_COMPARISON)

    if artifact_exists(PROTOTYPE_THRESHOLD_SWEEP):
        sweep = load_csv_artifact(PROTOTYPE_THRESHOLD_SWEEP)
        st.caption(
            f"The prototype threshold sweep artifact is available with "
            f"{len(sweep):,} threshold rows."
        )
    else:
        render_missing_artifact_warning(PROTOTYPE_THRESHOLD_SWEEP)

    with st.expander("Baseline validation metrics"):
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
            st.dataframe(metrics[display_columns], use_container_width=True)
        else:
            render_missing_artifact_warning(VALIDATION_METRICS)

    if artifact_exists("outputs/artifact_manifest.json"):
        manifest = load_artifact_manifest()
        render_manifest_artifacts(
            "Manifest artifacts for this page",
            filter_manifest_artifacts(manifest, page="Page 2 - Model Benchmark"),
        )

    render_future_work_note(
        [
            "formal literature review notes for selected methods",
            "final benchmark refinement after reviewer feedback",
            "explainability artifacts for model-important sensor signals",
        ]
    )


def _format_leaderboard(comparison: object) -> object:
    leaderboard = comparison.loc[:, LEADERBOARD_COLUMNS].copy()
    numeric_columns = [
        "threshold",
        "recall",
        "precision",
        "f2",
        "pr_auc",
        "roc_auc",
        "flagged_sample_rate",
    ]
    for column in numeric_columns:
        leaderboard[column] = leaderboard[column].map(
            lambda value: format_metric(value, digits=3)
        )
    return leaderboard


def _render_model_highlights(comparison: object) -> None:
    completed = comparison[comparison["status"] == "completed"].copy()
    if completed.empty:
        return

    best_f2 = completed.sort_values(
        by=["f2", "model_name"],
        ascending=[False, True],
    ).iloc[0]
    high_recall = completed.sort_values(
        by=["recall", "flagged_sample_rate", "model_name"],
        ascending=[False, True, True],
    ).iloc[0]

    st.subheader("Prototype highlights")
    cols = st.columns(2)
    cols[0].metric(
        "Strongest prototype F2",
        str(best_f2["model_name"]),
        help=(
            f"F2 {format_metric(best_f2['f2'])} at threshold "
            f"{format_threshold(best_f2['threshold'])}."
        ),
    )
    cols[1].metric(
        "Highest prototype recall",
        str(high_recall["model_name"]),
        help=(
            f"Recall {format_percent(high_recall['recall'])}; flagged rate "
            f"{format_percent(high_recall['flagged_sample_rate'])}."
        ),
    )
