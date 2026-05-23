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
