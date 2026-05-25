"""Small navigation helpers for the Streamlit app."""

from __future__ import annotations

from collections.abc import Sequence

import streamlit as st


CURRENT_PAGE_KEY = "current_page"
PENDING_PAGE_KEY = "pending_page"


def apply_pending_navigation(valid_pages: Sequence[str], default_page: str) -> None:
    """Apply any queued page navigation before the sidebar radio is rendered."""

    pending_page = st.session_state.pop(PENDING_PAGE_KEY, None)
    if pending_page in valid_pages:
        st.session_state[CURRENT_PAGE_KEY] = pending_page
    elif st.session_state.get(CURRENT_PAGE_KEY) not in valid_pages:
        st.session_state[CURRENT_PAGE_KEY] = default_page


def queue_page_navigation(page_key: str) -> None:
    """Queue in-app navigation and rerun the Streamlit app."""

    st.session_state[PENDING_PAGE_KEY] = page_key
    st.rerun()
