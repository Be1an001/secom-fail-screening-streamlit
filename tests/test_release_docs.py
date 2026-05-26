"""Release documentation guardrails.

These tests keep final portfolio docs aligned without checking brittle prose.
"""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
README = PROJECT_ROOT / "README.md"
DOCS_README = PROJECT_ROOT / "docs" / "README.md"
FINAL_CHECKLIST = PROJECT_ROOT / "docs" / "final_release_checklist.md"
API_RAG_DOC = PROJECT_ROOT / "docs" / "api_and_rag_lite.md"
USER_GUIDE = PROJECT_ROOT / "docs" / "user_guide.md"
OUTPUTS_README = PROJECT_ROOT / "outputs" / "README.md"
PAGE_5 = PROJECT_ROOT / "app_pages" / "page_5_mlops_ai_api.py"
PR_TEMPLATE = PROJECT_ROOT / ".github" / "pull_request_template.md"
DOCKERFILE = PROJECT_ROOT / "Dockerfile"
DOCKERIGNORE = PROJECT_ROOT / ".dockerignore"
DOCKER_DOC = PROJECT_ROOT / "docs" / "docker_usage.md"
NOTEBOOK = PROJECT_ROOT / "notebooks" / "SECOM_Fail_Screening_Portfolio_Summary.ipynb"
RENAMED_DOCS = [
    PROJECT_ROOT / "docs" / "product_requirements_document_prd.md",
    PROJECT_ROOT / "docs" / "technical_design_document_tdd.md",
    PROJECT_ROOT / "docs" / "user_guide.md",
    PROJECT_ROOT / "docs" / "project_summary.md",
    PROJECT_ROOT / "docs" / "development_history.md",
    PROJECT_ROOT / "docs" / "docker_usage.md",
]
OLD_DOCS = [
    PROJECT_ROOT / "docs" / ("pr" + "d.md"),
    PROJECT_ROOT / "docs" / ("td" + "d.md"),
    PROJECT_ROOT / "docs" / ("streamlit_app_" + "walkthrough.md"),
    PROJECT_ROOT / "docs" / ("portfolio_project_" + "summary.md"),
    PROJECT_ROOT / "docs" / ("phase_" + "log.md"),
    PROJECT_ROOT / "docs" / ("decision_" + "log.md"),
    PROJECT_ROOT / "docs" / ("product_requirements" + ".md"),
    PROJECT_ROOT / "docs" / ("technical_design" + ".md"),
]
FOLDER_READMES = [
    PROJECT_ROOT / "outputs" / "README.md",
    PROJECT_ROOT / "reports" / "README.md",
    PROJECT_ROOT / "scripts" / "README.md",
    PROJECT_ROOT / "configs" / "README.md",
]


def test_readme_has_final_portfolio_sections() -> None:
    readme = README.read_text(encoding="utf-8")

    expected_sections = [
        "## Short Summary",
        "## Project Type / Status / Tools",
        "## Business Problem",
        "## Project Objective",
        "## Dataset and Scope",
        "## My Role / Contribution",
        "## Methodology",
        "## Model Benchmark and Evaluation",
        "## Threshold and Cost Trade-off",
        "## Explainability",
        "## Streamlit App",
        "## API and AI Summary Boundaries",
        "## MLOps-lite Notes",
        "## Repository Structure",
        "## Local Run",
        "## How to Review This Project",
        "## Optional OpenAI Summary Setup",
        "## Reproducibility Notes",
        "## Limitations",
        "## Future Improvements",
        "## Related Files",
    ]

    for section in expected_sections:
        assert section in readme

    assert "https://secom-fail-screening.streamlit.app/" in readme
    assert "[Documentation guide](docs/README.md)" in readme
    assert "[User guide](docs/user_guide.md)" in readme
    assert "[Technical Design Document](docs/technical_design_document_tdd.md)" in readme
    assert "[Literature references](docs/literature_references.md)" in readme
    assert "[Docker usage](docs/docker_usage.md)" in readme
    assert readme.rstrip().endswith("[CI workflow](.github/workflows/ci.yml)")


def test_docs_navigation_and_professional_names_exist() -> None:
    docs_readme = DOCS_README.read_text(encoding="utf-8")

    for path in RENAMED_DOCS:
        assert path.is_file()

    for path in OLD_DOCS:
        assert not path.exists()

    for path in FOLDER_READMES:
        assert path.is_file()

    assert "[Project Summary](project_summary.md)" in docs_readme
    assert "[User Guide](user_guide.md)" in docs_readme
    assert "[Product Requirements Document](product_requirements_document_prd.md)" in docs_readme
    assert "[Technical Design Document](technical_design_document_tdd.md)" in docs_readme
    assert "[Literature References](literature_references.md)" in docs_readme
    assert "[Development History](development_history.md)" in docs_readme
    assert "[Docker Usage](docker_usage.md)" in docs_readme


def test_final_release_checklist_exists_with_expected_sections() -> None:
    checklist = FINAL_CHECKLIST.read_text(encoding="utf-8")

    expected_sections = [
        "## App QA",
        "## Artifact QA",
        "## API QA",
        "## OpenAI Summary QA",
        "## Optional Docker QA",
        "## Responsible Wording QA",
        "## GitHub / CI QA",
    ]

    for section in expected_sections:
        assert section in checklist


def test_docs_describe_secret_handling_and_no_raw_csv_transfer() -> None:
    combined_docs = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in [README, API_RAG_DOC, USER_GUIDE]
    )

    assert "streamlit secrets" in combined_docs
    assert "openai_api_key" in combined_docs
    assert "raw csvs are not sent" in combined_docs
    assert "no free-form chatbot" in combined_docs or "not a general chatbot" in combined_docs
    assert ".streamlit/secrets.toml" in combined_docs


def test_docs_include_copy_ready_validation_and_runtime_commands() -> None:
    combined_docs = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in [README, USER_GUIDE, FINAL_CHECKLIST, DOCKER_DOC]
    )

    expected_commands = [
        "python -m pip install -r requirements.txt",
        "python -m pytest",
        "python -m ruff check .",
        "python -m compileall app.py app_pages app_utils api src scripts tests",
        "git diff --check",
        "python -m jupyter nbconvert --to notebook --execute notebooks/secom_fail_screening_portfolio_summary.ipynb --inplace",
        "streamlit run app.py",
        "python -m uvicorn api.main:app --reload",
        "docker build -t secom-fail-screening-streamlit:local .",
        "docker run --rm -p 8501:8501 secom-fail-screening-streamlit:local",
    ]

    for command in expected_commands:
        assert command in combined_docs

    assert "http://localhost:8501" in combined_docs
    assert "http://127.0.0.1:8000/docs" in combined_docs


def test_final_docs_avoid_unqualified_release_overclaims() -> None:
    combined_docs = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in [README, API_RAG_DOC, USER_GUIDE, PR_TEMPLATE]
    )
    stale_acronym = "so" + "ta"

    forbidden_unqualified_claims = [
        "research-leading performance achieved",
        stale_acronym,
        "final champion model selected",
        "production backend is deployed",
        "deployed api endpoint",
        "general chatbot is implemented",
        "automatic pass/fail decision system is deployed",
        "physical root-cause analysis proves",
    ]

    for claim in forbidden_unqualified_claims:
        assert claim not in combined_docs

    assert "c:\\users" not in combined_docs
    assert "/users/" not in combined_docs


def test_page_5_describes_current_local_api_and_controlled_summary() -> None:
    page_5 = PAGE_5.read_text(encoding="utf-8").lower()
    normalized_page_5 = " ".join(page_5.split())

    assert "fastapi artifact service" in normalized_page_5
    assert "controlled rag-lite summary" in normalized_page_5
    assert "ai summary" in normalized_page_5
    assert "raw csvs are not sent" in normalized_page_5
    assert "not a production backend" in normalized_page_5
    assert "not a general chatbot" in normalized_page_5
    assert "generate summary" in normalized_page_5
    assert "use_openai=True" in PAGE_5.read_text(encoding="utf-8")
    assert "extension concept: agentic analytics workflow" in normalized_page_5
    assert "langgraph is not implemented here" in normalized_page_5
    assert "scope note" not in normalized_page_5
    assert "use openai summary if configured" not in normalized_page_5
    assert "no api key is stored in the repo" not in normalized_page_5
    assert "future api and ai summary work that remains planned" not in page_5


def test_outputs_readme_embeds_expected_images() -> None:
    outputs_readme = OUTPUTS_README.read_text(encoding="utf-8")

    expected_images = [
        "![Final confusion matrix](figures/final_confusion_matrix.png)",
        "![Final precision-recall curve](figures/final_pr_curve.png)",
        "![Final ROC curve](figures/final_roc_curve.png)",
        "![Final feature importance](figures/final_feature_importance.png)",
        "![Permutation importance](figures/permutation_importance_prototype.png)",
        "![Feature stability](figures/feature_stability_prototype.png)",
    ]

    for image in expected_images:
        assert image in outputs_readme


def test_optional_docker_packaging_files_are_safe() -> None:
    dockerfile = DOCKERFILE.read_text(encoding="utf-8")
    dockerignore = DOCKERIGNORE.read_text(encoding="utf-8")
    docker_doc = DOCKER_DOC.read_text(encoding="utf-8").lower()
    normalized_docker_doc = " ".join(docker_doc.split())

    assert "FROM python:3.12-slim" in dockerfile
    assert "streamlit" in dockerfile
    assert ".streamlit/secrets.toml" in dockerignore
    assert ".env" in dockerignore
    assert "mlflow.db" in dockerignore
    assert "mlruns/" in dockerignore
    assert "mlartifacts/" in dockerignore
    assert "no production deployment claim" in docker_doc
    assert (
        "streamlit community cloud deployment does not require docker"
        in normalized_docker_doc
    )
    assert "your-key-here" in docker_doc


def test_notebook_is_positioned_as_portfolio_summary() -> None:
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    markdown_text = "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell.get("cell_type") == "markdown"
    ).lower()

    assert "secom fail-screening portfolio summary notebook" in markdown_text
    assert "https://secom-fail-screening.streamlit.app/" in markdown_text
    assert "docs/user_guide.md" in markdown_text
    assert "docs/product_requirements_document_prd.md" in markdown_text
    assert "docs/technical_design_document_tdd.md" in markdown_text
    assert "outputs/artifact_manifest.json" in markdown_text
    assert "future app" not in markdown_text
    assert "work in progress" not in markdown_text
    assert "not implemented in this phase" not in markdown_text


def test_public_text_avoids_private_process_wording_and_real_secrets() -> None:
    public_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore").lower()
        for path in _public_text_files()
    )

    forbidden_meta_phrases = [
        "chinese communication",
        "the user and reviewer",
        "codex",
        "chatgpt",
        "practice project",
        "still upgrading",
        "currently being upgraded",
        "future phase",
        "planned phase",
        "work in progress",
        "not implemented in this phase",
        "to be done",
        "tbd",
        "master's-graduate-level",
    ]

    for phrase in forbidden_meta_phrases:
        assert phrase not in public_text

    assert "sk-" not in public_text
    assert 'openai_api_key = "your-key-here"' in public_text


def test_streamlit_deprecated_width_parameter_is_not_used() -> None:
    app_text = "\n".join(
        path.read_text(encoding="utf-8")
        for root in [PROJECT_ROOT / "app_pages", PROJECT_ROOT / "app_utils"]
        for path in root.rglob("*.py")
    )

    assert "use_container_width" not in app_text
    assert 'width="stretch"' in app_text


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
        PROJECT_ROOT / "outputs",
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
