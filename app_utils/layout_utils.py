"""Small Streamlit layout helpers."""

from __future__ import annotations

from collections.abc import Sequence

import streamlit as st


def render_page_intro(title: str, summary: str) -> None:
    """Render a consistent page heading and summary."""

    st.header(title)
    st.write(summary)


def render_info_box(message: str) -> None:
    """Render a simple informational note."""

    st.info(message)


def render_prototype_note() -> None:
    """Render the shared prototype artifact note."""

    st.info(
        "These are prototype artifacts for screening decision support. "
        "They are not final model-selection results."
    )


def render_illustrative_cost_note() -> None:
    """Render the shared illustrative-cost note."""

    st.info(
        "These cost scenarios are illustrative and are not validated "
        "manufacturing costs."
    )


def render_no_production_decision_note() -> None:
    """Render the shared non-production threshold note."""

    st.warning(
        "This analysis does not create a production decision rule and does "
        "not select a final champion model."
    )


def render_responsible_use_note() -> None:
    """Render the shared responsible-use note for baseline app pages."""

    st.info(
        "This app supports screening decision support with baseline artifacts. "
        "It does not make automatic pass/fail decisions."
    )


def render_artifact_tracking_note() -> None:
    """Render the shared artifact tracking note."""

    st.info(
        "This artifact-driven Streamlit app uses "
        "`outputs/artifact_manifest.json` as a lightweight artifact registry. "
        "Local MLflow tracking can support experiment review, but the public "
        "app uses exported artifacts instead of local MLflow databases."
    )


def render_scope_note(items: Sequence[str]) -> None:
    """Render a compact scope note."""

    st.subheader("Scope notes")
    st.write(
        "The following items are outside the current portfolio app scope or "
        "possible extensions:"
    )
    for item in items:
        st.write(f"- {item}")


def render_missing_artifact_warning(relative_path: str) -> None:
    """Render a consistent missing-artifact warning."""

    st.warning(f"Missing artifact: `{relative_path}`")


def render_artifact_list(title: str, artifacts: Sequence[str]) -> None:
    """Render a compact list of available artifacts."""

    st.subheader(title)
    if not artifacts:
        st.caption("No matching artifacts are available yet.")
        return

    for artifact in artifacts:
        st.write(f"- `{artifact}`")


def render_manifest_artifacts(title: str, artifacts: Sequence[dict[str, object]]) -> None:
    """Render a compact list of manifest artifact entries."""

    st.subheader(title)
    if not artifacts:
        st.caption("No manifest artifacts are listed for this page yet.")
        return

    for artifact in artifacts:
        name = artifact.get("name", "unnamed artifact")
        path = artifact.get("path", "missing path")
        description = artifact.get("description", "")
        st.write(f"- `{path}` - **{name}**")
        if description:
            st.caption(str(description))
