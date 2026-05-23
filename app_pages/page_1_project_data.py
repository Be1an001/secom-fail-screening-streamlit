"""Project and data problem page."""

from __future__ import annotations

import streamlit as st

from app_utils.artifact_loader import (
    artifact_exists,
    list_existing_artifacts,
    load_artifact_manifest,
    validate_manifest_paths,
)
from app_utils.layout_utils import (
    render_artifact_list,
    render_future_work_note,
    render_missing_artifact_warning,
    render_page_intro,
    render_responsible_use_note,
)
from app_utils.metric_utils import format_count, format_percent


DATA_ARTIFACTS = [
    "data/secom.data",
    "data/secom_labels.data",
    "data/secom.names",
    "data/README.md",
]


def render() -> None:
    """Render the project and data problem placeholder page."""

    render_page_intro(
        "Project & Data Problem",
        "This page introduces the UCI SECOM fail-screening benchmark and the "
        "class imbalance that makes raw accuracy misleading.",
    )

    render_responsible_use_note()

    st.subheader("Current Baseline Dataset")
    st.write(
        "The baseline workflow loads public SECOM sensor data, maps raw labels "
        "into pass/fail classes, and keeps preprocessing leakage-safe."
    )

    columns = st.columns(5)
    columns[0].metric("Rows", format_count(1567))
    columns[1].metric("Sensor features", format_count(590))
    columns[2].metric("Pass samples", format_count(1463))
    columns[3].metric("Fail samples", format_count(104))
    columns[4].metric("Fail rate", format_percent(0.0664, digits=2))

    st.write(
        "The positive class is fail. Because fail samples are rare, accuracy "
        "alone can hide poor fail-class recall."
    )

    existing = list_existing_artifacts(DATA_ARTIFACTS)
    render_artifact_list("Available data artifacts", existing)

    if not artifact_exists("data/secom.data"):
        render_missing_artifact_warning("data/secom.data")

    if artifact_exists("outputs/artifact_manifest.json"):
        manifest = load_artifact_manifest()
        try:
            validate_manifest_paths(manifest)
            st.caption(
                f"Artifact manifest loaded with {len(manifest['artifacts'])} "
                "baseline artifacts."
            )
        except FileNotFoundError as exc:
            st.warning(str(exc))

    render_future_work_note(
        [
            "clearer class balance visuals",
            "missingness summaries",
            "artifact manifest links for data evidence",
        ]
    )
