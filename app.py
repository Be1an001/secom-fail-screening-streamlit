"""Streamlit entry point for the SECOM fail-screening portfolio app."""

from __future__ import annotations

import streamlit as st

from app_pages import (
    page_1_project_data,
    page_2_model_benchmark,
    page_3_champion_tradeoff,
    page_4_explainability,
    page_5_mlops_ai_api,
)


PAGES = {
    "Project & Data Problem": page_1_project_data.render,
    "Model Benchmark": page_2_model_benchmark.render,
    "Champion Trade-off": page_3_champion_tradeoff.render,
    "Explainability": page_4_explainability.render,
    "MLOps, API, and AI Summary": page_5_mlops_ai_api.render,
}


def main() -> None:
    """Render the app shell and route to the selected page."""

    st.set_page_config(
        page_title="SECOM Fail-Screening Portfolio",
        page_icon=":microscope:",
        layout="wide",
    )

    st.title("SECOM Fail-Screening Portfolio")
    st.caption(
        "A baseline workflow being upgraded toward an artifact-driven Streamlit "
        "app for screening decision support."
    )

    selected_page = st.sidebar.radio("Pages", list(PAGES.keys()))
    st.sidebar.markdown("---")
    st.sidebar.caption(
        "This app skeleton reads pre-generated artifacts. It does not retrain "
        "models or make automatic pass/fail decisions."
    )

    PAGES[selected_page]()


if __name__ == "__main__":
    main()
