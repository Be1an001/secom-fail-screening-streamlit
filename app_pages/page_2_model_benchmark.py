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
    render_card_grid,
    render_evidence_expander,
    render_kpi_cards,
    render_method_reference_note,
    render_missing_artifact_warning,
    render_page_intro,
    render_prototype_note,
    render_section_header,
    render_subtle_note,
)
from app_utils.metric_utils import format_metric, format_percent, format_threshold
from app_utils.model_display import (
    BASELINE_WARNING,
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
BENCHMARK_REPORT = "reports/benchmark_prototype_summary.md"
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
MAIN_MODEL_ORDER = [
    "logistic_regression_pca_baseline",
    "random_forest_reference",
    "xgboost_cost_sensitive",
]


def render() -> None:
    """Render the model benchmark page."""

    render_page_intro(
        "Model Benchmark",
        "Compare the original baseline group with later reference-supported "
        "upgrade methods. The display grouping helps the portfolio story, "
        "while the full six-model benchmark remains visible. These results "
        "are not final model-selection results.",
    )
    render_prototype_note()
    render_subtle_note(
        "All six models remain in the full benchmark table. This display "
        "grouping is for readability; it does not remove models from the "
        "benchmark and does not create a final champion model.",
        title="Display grouping",
    )
    render_method_reference_note()

    if artifact_exists(PROTOTYPE_MODEL_COMPARISON):
        comparison = _add_display_roles(load_csv_artifact(PROTOTYPE_MODEL_COMPARISON))
        _render_model_highlights(comparison)
        _render_main_model_cards(comparison)
        _render_role_section(
            comparison,
            BASELINE_WARNING,
            "Accuracy warning baseline",
            (
                "Dummy Majority stays in the benchmark to show why accuracy "
                "alone is misleading when fail samples are rare."
            ),
        )
        _render_role_section(
            comparison,
            SECONDARY_PROTOTYPE_COMPARISON,
            "Secondary prototype comparisons",
            (
                "LightGBM and XGBoost + Training-only SMOTE remain visible as "
                "secondary comparisons for boosting-family and leakage-safe "
                "resampling behavior."
            ),
        )
        render_section_header(
            "Full six-model benchmark table",
            "The table keeps every prototype model and does not claim research-leading performance.",
        )
        st.dataframe(
            _format_leaderboard(comparison),
            width="stretch",
            hide_index=True,
        )
    else:
        render_missing_artifact_warning(PROTOTYPE_MODEL_COMPARISON)

    with st.expander("Baseline validation metrics", expanded=False):
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
            st.dataframe(metrics[display_columns], width="stretch", hide_index=True)
        else:
            render_missing_artifact_warning(VALIDATION_METRICS)

    _render_evidence_links()


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

    render_section_header(
        "Prototype highlights",
        "A quick reading of the current benchmark artifacts.",
    )
    render_kpi_cards(
        [
            {
                "label": "Strongest prototype F2",
                "value": get_model_display(str(best_f2["model_name"]))["short_label"],
                "caption": (
                    f"F2 {format_metric(best_f2['f2'])} at threshold "
                    f"{format_threshold(best_f2['threshold'])}"
                ),
            },
            {
                "label": "Higher-recall option",
                "value": get_model_display(str(high_recall["model_name"]))[
                    "short_label"
                ],
                "caption": (
                    f"Recall {format_percent(high_recall['recall'])}; flagged "
                    f"rate {format_percent(high_recall['flagged_sample_rate'])}"
                ),
            },
        ],
        columns=2,
    )
    render_subtle_note(
        "Random Forest Reference currently has the strongest prototype F2. "
        "XGBoost Cost-Sensitive provides a higher-recall option with higher "
        "review workload. This page makes no research-leading performance claim.",
        title="Benchmark reading",
    )


def _render_main_model_cards(comparison: object) -> None:
    render_section_header(
        "Main comparison models",
        "The portfolio story emphasizes a classical baseline, the Random Forest reference, and the cost-sensitive boosting option.",
    )
    cards = []
    for model_name in MAIN_MODEL_ORDER:
        rows = comparison[comparison["model_name"] == model_name]
        if rows.empty:
            continue
        row = rows.iloc[0]
        metadata = get_model_display(model_name)
        cards.append(
            {
                "title": metadata["short_label"],
                "body": (
                    f"{metadata['main_message']} F2 {format_metric(row['f2'])}, "
                    f"recall {format_percent(row['recall'])}, precision "
                    f"{format_percent(row['precision'])}, flagged rate "
                    f"{format_percent(row['flagged_sample_rate'])}."
                ),
            }
        )
    render_card_grid(cards, columns=3)


def _render_role_section(
    comparison: object,
    display_role: str,
    title: str,
    summary: str,
) -> None:
    rows = comparison[comparison["display_role"] == display_role].copy()
    if rows.empty:
        return

    render_section_header(title, summary)
    st.dataframe(
        _format_role_table(rows),
        width="stretch",
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
    leaderboard.insert(0, "display_role", comparison["display_role"])
    leaderboard.insert(0, "short_label", comparison["short_label"])
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


def _render_evidence_links() -> None:
    artifacts: list[str | dict[str, object]] = [
        PROTOTYPE_MODEL_COMPARISON,
        PROTOTYPE_THRESHOLD_SWEEP,
        VALIDATION_METRICS,
        BENCHMARK_REPORT,
    ]
    if artifact_exists("outputs/artifact_manifest.json"):
        manifest = load_artifact_manifest()
        artifacts.extend(
            filter_manifest_artifacts(manifest, page="Page 2 - Model Benchmark")
        )
    render_evidence_expander(artifacts)
