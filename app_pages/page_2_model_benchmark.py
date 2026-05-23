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
from app_utils.model_display import (
    BASELINE_WARNING,
    MAIN_COMPARISON,
    SECONDARY_PROTOTYPE_COMPARISON,
    get_model_display,
)


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
        "All six models remain in the full benchmark table. The app highlights "
        "a smaller set of models for the main portfolio story. This display "
        "grouping is for readability; it does not remove models from the "
        "benchmark and does not create a final champion model."
    )
    render_info_box(
        "Random Forest reference currently has the strongest F2 in the "
        "prototype benchmark. XGBoost cost-sensitive provides a higher-recall "
        "option with higher review workload. Logistic + PCA remains useful "
        "as a classical baseline. This page makes no SOTA performance claim."
    )

    if artifact_exists(PROTOTYPE_MODEL_COMPARISON):
        comparison = _add_display_roles(load_csv_artifact(PROTOTYPE_MODEL_COMPARISON))
        _render_model_highlights(comparison)
        _render_role_section(
            comparison,
            MAIN_COMPARISON,
            "Main comparison",
            (
                "These models receive the most explanation in the portfolio "
                "story because they compare a classical baseline, the current "
                "Random Forest reference, and a cost-sensitive boosting option."
            ),
        )
        _render_role_section(
            comparison,
            BASELINE_WARNING,
            "Baseline warning",
            (
                "The dummy model is retained to show why accuracy alone is "
                "misleading in rare-fail screening."
            ),
        )
        _render_role_section(
            comparison,
            SECONDARY_PROTOTYPE_COMPARISON,
            "Secondary prototype comparison",
            (
                "These models stay visible as secondary prototype comparisons. "
                "They help document boosting-family and training-only "
                "resampling behavior without becoming the main story."
            ),
        )
        st.subheader("Full six-model benchmark table")
        st.dataframe(
            _format_leaderboard(comparison),
            use_container_width=True,
            hide_index=True,
        )
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


def _add_display_roles(comparison: object) -> object:
    enriched = comparison.copy()
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


def _render_role_section(
    comparison: object,
    display_role: str,
    title: str,
    summary: str,
) -> None:
    rows = comparison[comparison["display_role"] == display_role].copy()
    if rows.empty:
        return

    st.subheader(title)
    st.write(summary)
    st.dataframe(
        _format_role_table(rows),
        use_container_width=True,
        hide_index=True,
    )


def _format_role_table(rows: object) -> object:
    display = rows.loc[
        :,
        [
            "short_label",
            "threshold",
            "recall",
            "precision",
            "f2",
            "flagged_sample_rate",
            "main_message",
        ],
    ].copy()
    for column in ["threshold", "recall", "precision", "f2", "flagged_sample_rate"]:
        display[column] = display[column].map(
            lambda value: format_metric(value, digits=3)
        )
    return display


def _format_leaderboard(comparison: object) -> object:
    leaderboard = comparison.loc[:, LEADERBOARD_COLUMNS].copy()
    leaderboard.insert(
        0,
        "display_role",
        comparison["display_role"],
    )
    leaderboard.insert(
        0,
        "short_label",
        comparison["short_label"],
    )
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
