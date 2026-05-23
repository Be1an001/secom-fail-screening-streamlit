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
