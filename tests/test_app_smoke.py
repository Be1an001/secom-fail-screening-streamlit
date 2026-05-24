"""Source-based smoke tests for the Streamlit app shell.

These tests avoid importing Streamlit so they can run in the minimal CI
environment.
"""

from __future__ import annotations

import ast
from pathlib import Path

from app_utils.artifact_loader import (
    artifact_github_url,
    load_artifact_manifest,
    validate_manifest_paths,
)
from app_utils.model_display import MODEL_DISPLAY_ROLES


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_PATH = PROJECT_ROOT / "app.py"
PAGE_DIR = PROJECT_ROOT / "app_pages"
PAGE_MODULES = [
    PAGE_DIR / "page_1_project_data.py",
    PAGE_DIR / "page_2_model_benchmark.py",
    PAGE_DIR / "page_3_champion_tradeoff.py",
    PAGE_DIR / "page_4_explainability.py",
    PAGE_DIR / "page_5_mlops_ai_api.py",
]
PROTOTYPE_BENCHMARK_ARTIFACT = (
    PROJECT_ROOT / "outputs" / "metrics" / "benchmark_model_comparison_prototype.csv"
)
COST_SELECTED_ARTIFACT = (
    PROJECT_ROOT / "outputs" / "metrics" / "cost_selected_thresholds_prototype.csv"
)
EXPLAINABILITY_ARTIFACT = (
    PROJECT_ROOT / "outputs" / "metrics" / "permutation_importance_prototype.csv"
)
EXPECTED_PAGE_TITLES = {
    "Overview",
    "Benchmark",
    "Cost Trade-off",
    "Explainability",
    "API & AI Summary",
}
FORBIDDEN_IMPORTS = {
    "docker",
    "fastapi",
    "imblearn",
    "lightgbm",
    "openai",
    "shap",
    "xgboost",
}
IMPLEMENTED_CLAIM_PHRASES = {
    "six-model benchmark is complete",
    "fastapi service is implemented",
    "openai integration is implemented",
    "rag-lite summary is implemented",
    "docker deployment is implemented",
    "sota performance achieved",
    "final champion model selected",
    "is a production decision rule",
}


def test_app_page_registry_contains_expected_pages() -> None:
    tree = _parse(APP_PATH)
    page_titles = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "PAGES" for target in node.targets):
                if isinstance(node.value, ast.Dict):
                    page_titles.update(
                        key.value
                        for key in node.value.keys
                        if isinstance(key, ast.Constant) and isinstance(key.value, str)
                    )

    assert page_titles == EXPECTED_PAGE_TITLES


def test_sidebar_labels_and_tagline_are_portfolio_friendly() -> None:
    app_text = APP_PATH.read_text(encoding="utf-8")
    normalized_app_text = _normalize_source(app_text)

    assert '"Overview"' in app_text
    assert '"01 Overview"' not in app_text
    assert '"02 Benchmark"' not in app_text
    assert "From noisy sensor data to screening trade-offs" in normalized_app_text
    assert "AI-assisted summaries" in normalized_app_text


def test_page_modules_define_render_function() -> None:
    for path in PAGE_MODULES:
        tree = _parse(path)
        function_names = {
            node.name for node in tree.body if isinstance(node, ast.FunctionDef)
        }

        assert "render" in function_names


def test_page_modules_do_not_import_future_optional_packages() -> None:
    for path in PAGE_MODULES:
        imported_roots = _imported_roots(_parse(path))

        assert not (imported_roots & FORBIDDEN_IMPORTS)


def test_app_text_keeps_future_features_future_facing() -> None:
    app_text = "\n".join(
        path.read_text(encoding="utf-8").lower() for path in PAGE_MODULES
    )
    normalized_app_text = _normalize_source(app_text)

    for phrase in IMPLEMENTED_CLAIM_PHRASES:
        assert phrase not in app_text

    assert "not final model-selection results" in normalized_app_text
    assert "illustrative cost scenario" in normalized_app_text
    assert "does not create a final champion model" in normalized_app_text
    assert "not create a production decision rule" in normalized_app_text
    assert "not physical root-cause analysis" in normalized_app_text
    assert "not a general chatbot" in normalized_app_text
    assert "sota performance achieved" not in app_text
    assert "does not" in app_text


def test_page_1_tells_portfolio_workflow_story() -> None:
    page_1_text = PAGE_MODULES[0].read_text(encoding="utf-8")

    expected_terms = [
        "SECOM Fail-Screening Decision Support",
        "Start with a rare-fail problem",
        "Split before learning from the data",
        "Clean and prepare sensor features",
        "Build baseline references",
        "Add literature-inspired candidates",
        "Compare model trade-offs",
        "Choose thresholds by cost scenario",
        "Explain model-important signals",
        "Package the work as a data product",
    ]

    for term in expected_terms:
        assert term in page_1_text


def test_app_references_prototype_benchmark_and_cost_artifacts() -> None:
    page_2_text = PAGE_MODULES[1].read_text(encoding="utf-8")
    page_3_text = PAGE_MODULES[2].read_text(encoding="utf-8")
    page_4_text = PAGE_MODULES[3].read_text(encoding="utf-8")

    assert PROTOTYPE_BENCHMARK_ARTIFACT.is_file()
    assert COST_SELECTED_ARTIFACT.is_file()
    assert EXPLAINABILITY_ARTIFACT.is_file()
    assert "benchmark_model_comparison_prototype.csv" in page_2_text
    assert "cost_selected_thresholds_prototype.csv" in page_3_text
    assert "permutation_importance_prototype.csv" in page_4_text
    assert "feature_stability_prototype.csv" in page_4_text
    assert "top_sensor_signals_prototype.csv" in page_4_text


def test_page_5_describes_artifact_tracking_without_overclaiming() -> None:
    page_5_text = PAGE_MODULES[4].read_text(encoding="utf-8").lower()
    normalized_page_5_text = _normalize_source(page_5_text)

    assert "outputs/artifact_manifest.json" in normalized_page_5_text
    assert "local mlflow tracking" in normalized_page_5_text
    assert "mlflow_runs_summary.csv" in normalized_page_5_text
    assert "fastapi artifact service" in normalized_page_5_text
    assert "controlled rag-lite summary" in normalized_page_5_text
    assert "raw csvs" in normalized_page_5_text
    assert "not a production backend" in normalized_page_5_text
    assert "not a general chatbot" in normalized_page_5_text
    assert "ai summary" in normalized_page_5_text
    assert "generate summary" in normalized_page_5_text
    assert "use_openai=True" in PAGE_MODULES[4].read_text(encoding="utf-8")
    assert "extension concept: agentic analytics workflow" in normalized_page_5_text
    assert "langgraph is not implemented here" in normalized_page_5_text
    assert "scope note" not in normalized_page_5_text
    assert "use openai summary if configured" not in normalized_page_5_text
    assert "no api key is stored in the repo" not in normalized_page_5_text
    assert "text_input" not in page_5_text
    assert "text_area" not in page_5_text
    assert "production mlops platform" not in page_5_text
    assert "fastapi service is implemented" not in page_5_text
    assert "rag-lite summary is implemented" not in page_5_text


def test_page_2_describes_model_display_grouping() -> None:
    page_2_text = PAGE_MODULES[1].read_text(encoding="utf-8")

    assert "Main comparison" in page_2_text
    assert "Accuracy warning baseline" in page_2_text
    assert "Secondary prototype comparisons" in page_2_text
    assert "Full six-model benchmark table" in page_2_text
    assert "does not remove models" in page_2_text
    assert "does not create a final champion model" in page_2_text


def test_page_sources_use_calm_notes_instead_of_alert_boxes() -> None:
    page_text = "\n".join(path.read_text(encoding="utf-8") for path in PAGE_MODULES)

    assert "st.info" not in page_text
    assert "st.warning" not in page_text
    assert "render_subtle_note" in page_text


def test_cost_page_groups_selected_threshold_cards() -> None:
    page_3_text = PAGE_MODULES[2].read_text(encoding="utf-8")

    assert "Decision and workload" in page_3_text
    assert "Performance" in page_3_text
    assert "Cost and confusion matrix" in page_3_text


def test_explainability_figures_are_not_side_by_side() -> None:
    page_4_text = PAGE_MODULES[3].read_text(encoding="utf-8")

    assert "st.columns(2)" not in page_4_text
    assert "PERMUTATION_IMPORTANCE_FIGURE" in page_4_text
    assert "FEATURE_STABILITY_FIGURE" in page_4_text


def test_artifact_github_link_helper_uses_main_blob_url() -> None:
    assert artifact_github_url("outputs/metrics/final_test_metrics.csv") == (
        "https://github.com/Be1an001/secom-fail-screening-streamlit/blob/main/"
        "outputs/metrics/final_test_metrics.csv"
    )


def test_all_six_model_names_are_represented_in_display_mapping() -> None:
    expected_model_names = {
        "dummy_majority_baseline",
        "logistic_regression_pca_baseline",
        "random_forest_reference",
        "xgboost_cost_sensitive",
        "lightgbm_class_weighted",
        "xgboost_training_only_smote",
    }

    assert set(MODEL_DISPLAY_ROLES) == expected_model_names


def test_manifest_paths_still_validate() -> None:
    manifest = load_artifact_manifest()

    artifact_paths = validate_manifest_paths(manifest)

    assert len(artifact_paths) == len(manifest["artifacts"])


def _parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _imported_roots(tree: ast.Module) -> set[str]:
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    return imported


def _normalize_source(text: str) -> str:
    return " ".join(text.split())
