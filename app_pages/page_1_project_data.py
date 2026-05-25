"""Project overview and data storytelling page."""

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
    render_hero,
    render_kpi_cards,
    render_method_reference_note,
    render_missing_artifact_warning,
    render_process_timeline,
    render_responsible_use_note,
    render_section_header,
    render_subtle_note,
    render_summary_card,
)
from app_utils.metric_utils import format_count, format_metric, format_percent
from app_utils.navigation import queue_page_navigation


DATA_ARTIFACTS = [
    "data/secom.data",
    "data/secom_labels.data",
    "data/secom.names",
    "data/README.md",
]
BENCHMARK_COMPARISON = "outputs/metrics/benchmark_model_comparison_prototype.csv"
COST_SELECTED_THRESHOLDS = "outputs/metrics/cost_selected_thresholds_prototype.csv"
TOP_SENSOR_SIGNALS = "outputs/metrics/top_sensor_signals_prototype.csv"


def render() -> None:
    """Render the project overview page."""

    render_hero(
        title="SECOM Fail-Screening Decision Support",
        subtitle=(
            "A portfolio data product that turns a rare-fail semiconductor "
            "dataset into a leakage-safe benchmark, threshold trade-off "
            "analysis, and model interpretation workflow."
        ),
        eyebrow="Project overview",
    )

    render_kpi_cards(
        [
            {"label": "Rows", "value": format_count(1567), "caption": "SECOM samples"},
            {
                "label": "Sensor features",
                "value": format_count(590),
                "caption": "Anonymous process signals",
            },
            {
                "label": "Fail samples",
                "value": format_count(104),
                "caption": "Positive screening class",
            },
            {
                "label": "Fail rate",
                "value": format_percent(0.0664, digits=2),
                "caption": "Rare-class imbalance",
            },
            {
                "label": "Benchmark models",
                "value": format_count(6),
                "caption": "Baseline and prototype comparison",
            },
            {
                "label": "App pages",
                "value": format_count(5),
                "caption": "Overview through API and AI summary",
            },
        ],
        columns=3,
    )

    render_responsible_use_note()

    render_section_header(
        "Guided workflow story",
        "A reviewer can read the project from raw data problem to finished data product.",
    )
    render_process_timeline(
        [
            {
                "title": "Start with a rare-fail problem",
                "body": "The dataset has many sensor columns, but only a small share of fail cases.",
            },
            {
                "title": "Split before learning from the data",
                "body": "The workflow separates training and validation data before preprocessing to reduce leakage risk.",
            },
            {
                "title": "Clean and prepare sensor features",
                "body": "Missing-value handling and feature filtering are fit on training data only.",
            },
            {
                "title": "Build baseline references",
                "body": "Dummy, Logistic + PCA, and Random Forest models define the starting comparison.",
            },
            {
                "title": "Add upgrade candidates",
                "body": "XGBoost, LightGBM, and training-only SMOTE variants test reference-supported imbalance methods.",
            },
            {
                "title": "Compare model trade-offs",
                "body": "Metrics focus on recall, precision, F2, PR-AUC, and review workload instead of accuracy alone.",
            },
            {
                "title": "Choose thresholds by cost scenario",
                "body": "Thresholds are treated as decision levers for different review and missed-fail assumptions.",
            },
            {
                "title": "Explain model-important signals",
                "body": "Permutation importance and stability checks show which anonymous sensors matter to model behavior.",
            },
            {
                "title": "Package the work as a data product",
                "body": "Streamlit, artifact tracking, FastAPI, and AI summaries make the workflow easier to review.",
            },
        ]
    )
    render_method_reference_note()

    _render_result_snapshot()

    _render_next_steps_navigation()

    _render_data_evidence()


def _render_result_snapshot() -> None:
    render_section_header(
        "Main result snapshot",
        "A compact reading of the current prototype evidence.",
    )
    cards = [
        {
            "title": "Random Forest Reference",
            "body": "Currently has the strongest prototype F2 in the benchmark artifacts.",
        },
        {
            "title": "XGBoost Cost-Sensitive",
            "body": "Provides a higher-recall option with higher review workload.",
        },
        {
            "title": "Threshold choice",
            "body": "Changes the balance between missed fail cases and review workload.",
        },
        {
            "title": "Sensor signals",
            "body": "Model-important sensor signals support investigation, not root-cause proof.",
        },
    ]

    if artifact_exists(BENCHMARK_COMPARISON):
        comparison = load_csv_artifact(BENCHMARK_COMPARISON)
        rf = comparison[comparison["model_name"] == "random_forest_reference"]
        xgb = comparison[comparison["model_name"] == "xgboost_cost_sensitive"]
        if not rf.empty:
            cards[0]["body"] = (
                "Random Forest Reference has the strongest prototype F2 "
                f"({format_metric(rf.iloc[0]['f2'])})."
            )
        if not xgb.empty:
            cards[1]["body"] = (
                "XGBoost Cost-Sensitive reaches recall "
                f"{format_percent(xgb.iloc[0]['recall'])} with flagged rate "
                f"{format_percent(xgb.iloc[0]['flagged_sample_rate'])}."
            )

    render_card_grid(cards, columns=2)
    render_subtle_note(
        "These results support portfolio review and screening decision support. "
        "They do not select a final champion model.",
        title="Interpretation",
    )


def _render_next_steps_navigation() -> None:
    render_section_header(
        "What to explore next",
        "Use these cards to move through the app story.",
    )
    cards = [
        {
            "page": "Benchmark",
            "title": "Benchmark",
            "button": "Open Benchmark",
            "body": "Compare the full six-model benchmark and the display grouping used for the portfolio story.",
        },
        {
            "page": "Cost Trade-off",
            "title": "Cost Trade-off",
            "button": "Open Cost Trade-off",
            "body": "Change the illustrative scenario and inspect how threshold choices affect review workload.",
        },
        {
            "page": "Explainability",
            "title": "Explainability",
            "button": "Open Explainability",
            "body": "Review permutation importance, stability, and model-important sensor signals.",
        },
        {
            "page": "API & AI Summary",
            "title": "API & AI Summary",
            "button": "Open API & AI Summary",
            "body": "Inspect artifact tracking, local API endpoints, and preset controlled summaries.",
        },
    ]

    for start in range(0, len(cards), 2):
        row_cards = cards[start : start + 2]
        columns = st.columns(len(row_cards))
        for column, card in zip(columns, row_cards, strict=True):
            with column:
                render_summary_card(card["title"], card["body"])
                if st.button(card["button"], key=f"overview_nav_{card['page']}"):
                    queue_page_navigation(card["page"])


def _render_data_evidence() -> None:
    artifacts: list[str | dict[str, object]] = [
        artifact for artifact in DATA_ARTIFACTS if artifact_exists(artifact)
    ]
    artifacts.extend(
        [
            BENCHMARK_COMPARISON,
            COST_SELECTED_THRESHOLDS,
            TOP_SENSOR_SIGNALS,
        ]
    )

    if artifact_exists("outputs/artifact_manifest.json"):
        manifest = load_artifact_manifest()
        artifacts.extend(
            filter_manifest_artifacts(manifest, page="Page 1 - Project & Data Problem")
        )

    render_evidence_expander(artifacts)

    if not artifact_exists("data/secom.data"):
        render_missing_artifact_warning("data/secom.data")
