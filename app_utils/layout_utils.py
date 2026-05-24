"""Small Streamlit layout helpers for the portfolio app."""

from __future__ import annotations

import html
import time
from collections.abc import Mapping, Sequence

import streamlit as st

from app_utils.artifact_loader import artifact_github_url


def apply_portfolio_theme() -> None:
    """Apply a lightweight portfolio CSS layer."""

    st.markdown(
        """
        <style>
        :root {
          --portfolio-bg: #f6f8fb;
          --portfolio-card: #ffffff;
          --portfolio-text: #172033;
          --portfolio-muted: #5f6b7a;
          --portfolio-border: #dbe4ef;
          --portfolio-accent: #0f7c80;
          --portfolio-blue: #2563eb;
          --portfolio-soft: #eef6f7;
          --portfolio-shadow: 0 10px 30px rgba(23, 32, 51, 0.07);
        }
        .stApp {
          background: var(--portfolio-bg);
          color: var(--portfolio-text);
        }
        section[data-testid="stSidebar"] {
          background: #ffffff;
          border-right: 1px solid var(--portfolio-border);
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label {
          border: 1px solid transparent;
          border-radius: 12px;
          padding: 0.45rem 0.55rem;
          margin-bottom: 0.15rem;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
          background: #f1f6fb;
          border-color: var(--portfolio-border);
        }
        .portfolio-sidebar-title {
          font-size: 1.0rem;
          font-weight: 750;
          color: var(--portfolio-text);
          line-height: 1.2;
          margin-bottom: 0.25rem;
        }
        .portfolio-sidebar-caption {
          color: var(--portfolio-muted);
          font-size: 0.84rem;
          line-height: 1.35;
          margin-bottom: 1rem;
        }
        .portfolio-hero {
          background:
            linear-gradient(135deg, rgba(15,124,128,0.10), rgba(37,99,235,0.08)),
            #ffffff;
          border: 1px solid var(--portfolio-border);
          border-radius: 18px;
          padding: 2rem 2.1rem;
          box-shadow: var(--portfolio-shadow);
          margin-bottom: 1.3rem;
        }
        .portfolio-eyebrow {
          color: var(--portfolio-accent);
          font-weight: 700;
          font-size: 0.8rem;
          letter-spacing: 0.04em;
          text-transform: uppercase;
          margin-bottom: 0.45rem;
        }
        .portfolio-hero h1 {
          color: var(--portfolio-text);
          font-size: 2.25rem;
          line-height: 1.08;
          margin: 0 0 0.65rem 0;
          letter-spacing: 0;
        }
        .portfolio-hero p {
          color: var(--portfolio-muted);
          font-size: 1.05rem;
          line-height: 1.55;
          max-width: 860px;
          margin: 0;
        }
        .portfolio-section {
          margin: 1.45rem 0 0.75rem 0;
        }
        .portfolio-section h2 {
          color: var(--portfolio-text);
          font-size: 1.35rem;
          margin: 0 0 0.25rem 0;
          letter-spacing: 0;
        }
        .portfolio-section p {
          color: var(--portfolio-muted);
          margin: 0;
          line-height: 1.5;
        }
        .portfolio-card {
          background: var(--portfolio-card);
          border: 1px solid var(--portfolio-border);
          border-radius: 16px;
          padding: 1.05rem 1.1rem;
          box-shadow: var(--portfolio-shadow);
          min-height: 100%;
          margin-bottom: 0.95rem;
          transition: transform 140ms ease, box-shadow 140ms ease;
        }
        .portfolio-card:hover {
          transform: translateY(-1px);
          box-shadow: 0 14px 34px rgba(23, 32, 51, 0.09);
        }
        .portfolio-card h3 {
          color: var(--portfolio-text);
          font-size: 1.0rem;
          margin: 0 0 0.45rem 0;
          letter-spacing: 0;
        }
        .portfolio-card p {
          color: var(--portfolio-muted);
          margin: 0;
          line-height: 1.45;
          font-size: 0.92rem;
        }
        .kpi-value {
          color: var(--portfolio-text);
          font-size: 1.65rem;
          font-weight: 760;
          margin: 0.1rem 0;
        }
        .kpi-label {
          color: var(--portfolio-muted);
          font-size: 0.78rem;
          text-transform: uppercase;
          letter-spacing: 0.04em;
          font-weight: 700;
        }
        .portfolio-note {
          background: var(--portfolio-soft);
          border: 1px solid #c8e3e5;
          border-radius: 14px;
          padding: 0.8rem 0.95rem;
          color: #244b52;
          margin: 0.8rem 0 1rem 0;
        }
        .portfolio-note strong {
          color: #123f45;
        }
        .timeline-step {
          display: flex;
          gap: 0.8rem;
          align-items: flex-start;
          margin-bottom: 0.85rem;
          border-left: 4px solid rgba(15,124,128,0.18);
        }
        .timeline-index {
          background: var(--portfolio-accent);
          color: #ffffff;
          width: 1.8rem;
          height: 1.8rem;
          border-radius: 999px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          font-size: 0.82rem;
          font-weight: 760;
          flex: 0 0 auto;
        }
        div.stButton > button {
          border-radius: 999px;
          border: 1px solid var(--portfolio-accent);
          background: var(--portfolio-accent);
          color: white;
          font-weight: 700;
          padding: 0.55rem 1.2rem;
        }
        div.stButton > button:hover {
          border-color: #0c6468;
          background: #0c6468;
          color: white;
        }
        div[data-testid="stMetric"] {
          background: #ffffff;
          border: 1px solid var(--portfolio-border);
          border-radius: 14px;
          padding: 0.8rem 0.95rem;
          box-shadow: var(--portfolio-shadow);
        }
        .portfolio-row-gap {
          height: 0.45rem;
        }
        .portfolio-evidence-spacer {
          height: 1.35rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_title(title: str, caption: str) -> None:
    """Render a compact sidebar title block."""

    st.sidebar.markdown(
        f"""
        <div class="portfolio-sidebar-title">{_escape(title)}</div>
        <div class="portfolio-sidebar-caption">{_escape(caption)}</div>
        """,
        unsafe_allow_html=True,
    )


def render_page_intro(title: str, summary: str) -> None:
    """Render a consistent page heading and summary."""

    render_hero(title=title, subtitle=summary)


def render_hero(title: str, subtitle: str, eyebrow: str | None = None) -> None:
    """Render a polished page hero."""

    eyebrow_html = (
        f'<div class="portfolio-eyebrow">{_escape(eyebrow)}</div>' if eyebrow else ""
    )
    st.markdown(
        f"""
        <section class="portfolio-hero">
          {eyebrow_html}
          <h1>{_escape(title)}</h1>
          <p>{_escape(subtitle)}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str, subtitle: str | None = None) -> None:
    """Render a lightweight section heading."""

    subtitle_html = f"<p>{_escape(subtitle)}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class="portfolio-section">
          <h2>{_escape(title)}</h2>
          {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_cards(cards: Sequence[Mapping[str, object]], columns: int = 4) -> None:
    """Render compact KPI cards."""

    if not cards:
        return

    for start in range(0, len(cards), columns):
        row_cards = cards[start : start + columns]
        row = st.columns(len(row_cards))
        for column, card in zip(row, row_cards, strict=True):
            label = str(card.get("label", "Metric"))
            value = str(card.get("value", "n/a"))
            caption = str(card.get("caption", ""))
            with column:
                st.markdown(
                    f"""
                    <div class="portfolio-card">
                      <div class="kpi-label">{_escape(label)}</div>
                      <div class="kpi-value">{_escape(value)}</div>
                      <p>{_escape(caption)}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.markdown('<div class="portfolio-row-gap"></div>', unsafe_allow_html=True)


def render_summary_card(title: str, body: str) -> None:
    """Render a compact explanatory card."""

    st.markdown(
        f"""
        <div class="portfolio-card">
          <h3>{_escape(title)}</h3>
          <p>{_escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_card_grid(cards: Sequence[Mapping[str, str]], columns: int = 3) -> None:
    """Render a grid of text cards."""

    if not cards:
        return
    for start in range(0, len(cards), columns):
        row_cards = cards[start : start + columns]
        row = st.columns(len(row_cards))
        for column, card in zip(row, row_cards, strict=True):
            with column:
                render_summary_card(card["title"], card["body"])
        st.markdown('<div class="portfolio-row-gap"></div>', unsafe_allow_html=True)


def render_process_timeline(steps: Sequence[Mapping[str, str]]) -> None:
    """Render a simple process timeline."""

    for index, step in enumerate(steps, start=1):
        st.markdown(
            f"""
            <div class="portfolio-card timeline-step">
              <span class="timeline-index">{index}</span>
              <div>
                <h3>{_escape(step["title"])}</h3>
                <p>{_escape(step["body"])}</p>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_subtle_note(message: str, title: str = "Scope note") -> None:
    """Render a calm note instead of a large alert box."""

    st.markdown(
        f"""
        <div class="portfolio-note">
          <strong>{_escape(title)}:</strong> {_escape(message)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_info_box(message: str) -> None:
    """Render a subtle informational note."""

    render_subtle_note(message, title="Note")


def render_prototype_note() -> None:
    """Render the shared prototype artifact note."""

    render_subtle_note(
        "These are prototype artifacts for screening decision support. "
        "They are not final model-selection results.",
        title="Prototype note",
    )


def render_illustrative_cost_note() -> None:
    """Render the shared illustrative-cost note."""

    render_subtle_note(
        "These cost scenarios are illustrative and are not validated "
        "manufacturing costs.",
        title="Cost note",
    )


def render_no_production_decision_note() -> None:
    """Render the shared non-production threshold note."""

    render_subtle_note(
        "This analysis does not create a production decision rule and does "
        "not select a final champion model.",
        title="Decision boundary",
    )


def render_responsible_use_note() -> None:
    """Render the shared responsible-use note for app pages."""

    render_subtle_note(
        "This app supports screening decision support. It does not make "
        "automatic pass/fail decisions.",
        title="Responsible use",
    )


def render_artifact_tracking_note() -> None:
    """Render the shared artifact tracking note."""

    render_subtle_note(
        "This artifact-driven Streamlit app uses outputs/artifact_manifest.json "
        "as a lightweight artifact registry. Local MLflow tracking can support "
        "experiment review, while the public app uses exported artifacts.",
        title="Artifact tracking",
    )


def render_scope_note(items: Sequence[str]) -> None:
    """Render a compact scope note."""

    if not items:
        return
    render_section_header("Additional context")
    for item in items:
        st.caption(f"- {item}")


def render_missing_artifact_warning(relative_path: str) -> None:
    """Render a consistent missing-artifact error."""

    st.error(f"Missing artifact: `{relative_path}`")


def render_artifact_list(title: str, artifacts: Sequence[str]) -> None:
    """Render a compact list of available artifacts."""

    render_section_header(title)
    if not artifacts:
        st.caption("No matching artifacts are available.")
        return

    for artifact in artifacts:
        st.markdown(f"- [{artifact}]({artifact_github_url(artifact)})")


def render_manifest_artifacts(title: str, artifacts: Sequence[dict[str, object]]) -> None:
    """Render a compact list of manifest artifact entries."""

    render_evidence_expander(artifacts, title=title)


def render_evidence_expander(
    artifacts: Sequence[str | Mapping[str, object]],
    *,
    title: str = "Evidence and source artifacts",
) -> None:
    """Render secondary evidence links in a collapsed expander."""

    if not artifacts:
        return

    st.markdown('<div class="portfolio-evidence-spacer"></div>', unsafe_allow_html=True)
    with st.expander(title, expanded=False):
        for artifact in artifacts:
            if isinstance(artifact, str):
                path = artifact
                label = artifact
                description = ""
            else:
                path = str(artifact.get("path", ""))
                label = str(artifact.get("name", path or "artifact"))
                description = str(artifact.get("description", ""))
            if not path:
                continue
            st.markdown(f"- [{_escape(label)}]({artifact_github_url(path)})")
            if description:
                st.caption(description)


def typewriter_text(text: str, delay: float = 0.006) -> None:
    """Render generated text with a lightweight typewriter-style reveal."""

    placeholder = st.empty()
    words = text.split()
    if not words:
        placeholder.markdown("")
        return

    rendered: list[str] = []
    for word in words:
        rendered.append(word)
        placeholder.markdown(" ".join(rendered))
        time.sleep(delay)


def _escape(value: object) -> str:
    return html.escape(str(value), quote=True)
