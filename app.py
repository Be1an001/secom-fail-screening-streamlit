"""Streamlit entry point for the SECOM fail-screening portfolio app."""

from __future__ import annotations

import streamlit as st

from app_utils.layout_utils import apply_portfolio_theme, render_sidebar_title
from app_pages import (
    page_1_project_data,
    page_2_model_benchmark,
    page_3_champion_tradeoff,
    page_4_explainability,
    page_5_mlops_ai_api,
)


PAGES = {
    "Overview": page_1_project_data.render,
    "Benchmark": page_2_model_benchmark.render,
    "Cost Trade-off": page_3_champion_tradeoff.render,
    "Explainability": page_4_explainability.render,
    "API & AI Summary": page_5_mlops_ai_api.render,
}


def main() -> None:
    """Render the app shell and route to the selected page."""

    st.set_page_config(
        page_title="SECOM Fail-Screening Portfolio",
        page_icon=":microscope:",
        layout="wide",
    )

    apply_portfolio_theme()
    render_sidebar_title(
        "SECOM Screening",
        "From noisy sensor data to screening trade-offs, model interpretation, "
        "and AI-assisted summaries.",
    )

    selected_page = st.sidebar.radio(
        "Navigation",
        list(PAGES.keys()),
        label_visibility="collapsed",
    )
    st.sidebar.markdown("---")
    st.sidebar.caption(
        "The app reads curated artifacts. It does not retrain models or make "
        "automatic pass/fail decisions."
    )

    PAGES[selected_page]()


if __name__ == "__main__":
    main()
