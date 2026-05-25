"""Literature reference and wording guardrails."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LITERATURE_REFERENCES = PROJECT_ROOT / "docs" / "literature_references.md"
README = PROJECT_ROOT / "README.md"
DOCS_README = PROJECT_ROOT / "docs" / "README.md"
METHODOLOGY = PROJECT_ROOT / "docs" / "methodology_summary.md"
BENCHMARK_REPORT = PROJECT_ROOT / "reports" / "benchmark_prototype_summary.md"
COST_REPORT = PROJECT_ROOT / "reports" / "cost_threshold_prototype_report.md"
EXPLAINABILITY_REPORT = PROJECT_ROOT / "reports" / "explainability_prototype_report.md"
NOTEBOOK = PROJECT_ROOT / "notebooks" / "SECOM_Fail_Screening_Portfolio_Summary.ipynb"
BENCHMARK_CONFIG = PROJECT_ROOT / "configs" / "model_benchmark_prototype.yaml"
BENCHMARK_COMPARISON = (
    PROJECT_ROOT / "outputs" / "metrics" / "benchmark_model_comparison_prototype.csv"
)
BENCHMARK_SWEEP = (
    PROJECT_ROOT / "outputs" / "metrics" / "benchmark_threshold_sweep_prototype.csv"
)
COST_SWEEP = PROJECT_ROOT / "outputs" / "metrics" / "cost_threshold_sweep_prototype.csv"


def test_literature_reference_document_exists_with_core_references() -> None:
    text = LITERATURE_REFERENCES.read_text(encoding="utf-8")

    expected_terms = [
        "Chen",
        "Guestrin",
        "XGBoost",
        "Ke",
        "LightGBM",
        "Chawla",
        "SMOTE",
        "Elkan",
        "Saito",
        "Rehmsmeier",
        "Fisher",
        "Rudin",
    ]

    for term in expected_terms:
        assert term in text

    assert "## Baseline Group" in text
    assert "## Upgrade Method References" in text
    assert "These models came from the original coursework baseline" in text
    assert text.count("Project application:") >= 6
    assert "No paper reproduction." in text
    assert "No research-leading performance claim." in text
    assert "No physical root-cause claim." in text


def test_literature_reference_document_scopes_formal_references_to_upgrades() -> None:
    text = LITERATURE_REFERENCES.read_text(encoding="utf-8")

    forbidden_sections = [
        "### Random Forest",
        "### Logistic Regression + PCA",
        "### PCA",
    ]

    for section in forbidden_sections:
        assert section not in text

    assert "https://link.springer.com/article/10.1023/A:1010933404324" not in text
    assert "https://link.springer.com/book/10.1007/b98835" not in text
    assert "scikit-learn" not in text.lower()


def test_stale_upgrade_group_label_is_removed() -> None:
    acronym = "so" + "ta"
    old_label = f"literature_{acronym}_inspired_prototype"
    expected_label = "literature_informed_upgrade"
    checked_files = [
        BENCHMARK_CONFIG,
        BENCHMARK_COMPARISON,
        BENCHMARK_SWEEP,
        COST_SWEEP,
        NOTEBOOK,
    ]

    for path in checked_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        assert old_label not in text

    assert expected_label in BENCHMARK_CONFIG.read_text(encoding="utf-8")
    assert expected_label in BENCHMARK_COMPARISON.read_text(encoding="utf-8")


def test_literature_reference_document_uses_verified_upgrade_links() -> None:
    text = LITERATURE_REFERENCES.read_text(encoding="utf-8")

    expected_links = [
        "https://www.kdd.org/kdd2016/papers/files/rfp0697-chenAemb.pdf",
        "https://doi.org/10.1145/2939672.2939785",
        "https://papers.nips.cc/paper_files/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html",
        "https://www.jair.org/index.php/jair/article/view/10302",
        "https://dl.acm.org/doi/10.5555/1642194.1642224",
        "https://cseweb.ucsd.edu/~elkan/rescale.pdf",
        "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0118432",
        "https://jmlr.org/papers/v20/18-760.html",
    ]

    for link in expected_links:
        assert link in text


def test_public_docs_link_to_literature_references() -> None:
    linked_files = [
        README,
        DOCS_README,
        METHODOLOGY,
        BENCHMARK_REPORT,
        COST_REPORT,
        EXPLAINABILITY_REPORT,
    ]

    for path in linked_files:
        text = path.read_text(encoding="utf-8")
        assert "literature_references.md" in text


def test_notebook_markdown_links_to_literature_references() -> None:
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    markdown_text = "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell.get("cell_type") == "markdown"
    )

    assert "../docs/literature_references.md" in markdown_text


def test_public_text_avoids_unqualified_literature_overclaims() -> None:
    public_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore").lower()
        for path in _public_text_files()
    )
    acronym = "so" + "ta"
    state_of_the_art = "state-of-the" + "-art"

    forbidden_claims = [
        f"{acronym} performance achieved",
        f"achieves {acronym} performance",
        f"{state_of_the_art} performance achieved",
        f"literature_{acronym}_inspired_prototype",
        "reproduces the xgboost paper",
        "reproduces the lightgbm paper",
        "reproduces cited papers",
        "paper reproduction is claimed",
        "baseline models are paper reproductions",
        "baseline group has formal paper references",
        "physical root-cause analysis proves",
        "causal proof of sensor",
        "causal sensor driver",
    ]

    for claim in forbidden_claims:
        assert claim not in public_text


def test_streamlit_pages_use_compact_method_reference_links() -> None:
    page_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (PROJECT_ROOT / "app_pages").glob("page_*.py")
    )

    assert "render_method_reference_note" in page_text
    assert "Upgrade method references are summarized" in (
        PROJECT_ROOT / "app_utils" / "layout_utils.py"
    ).read_text(encoding="utf-8")
    assert "docs/literature_references.md" in (
        PROJECT_ROOT / "app_utils" / "layout_utils.py"
    ).read_text(encoding="utf-8")
    assert "Breiman" not in page_text
    assert "Chen and Guestrin" not in page_text


def _public_text_files() -> list[Path]:
    roots = [
        PROJECT_ROOT / "README.md",
        PROJECT_ROOT / "AGENTS.md",
        PROJECT_ROOT / ".github",
        PROJECT_ROOT / "app_pages",
        PROJECT_ROOT / "app_utils",
        PROJECT_ROOT / "api",
        PROJECT_ROOT / "configs",
        PROJECT_ROOT / "data",
        PROJECT_ROOT / "docs",
        PROJECT_ROOT / "outputs" / "README.md",
        PROJECT_ROOT / "reports",
        PROJECT_ROOT / "scripts",
    ]
    suffixes = {".md", ".txt", ".py", ".yml", ".yaml"}
    files: list[Path] = []

    for root in roots:
        if root.is_file():
            files.append(root)
        elif root.is_dir():
            files.extend(
                path
                for path in root.rglob("*")
                if path.is_file() and path.suffix.lower() in suffixes
            )

    return files
