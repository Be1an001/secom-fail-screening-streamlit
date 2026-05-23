"""Source-based smoke tests for the Streamlit app shell.

These tests avoid importing Streamlit so they can run in the minimal CI
environment.
"""

from __future__ import annotations

import ast
from pathlib import Path

from app_utils.artifact_loader import load_artifact_manifest, validate_manifest_paths
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
    "Project & Data Problem",
    "Model Benchmark",
    "Champion Trade-off",
    "Explainability",
    "MLOps, API, and AI Summary",
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

    for phrase in IMPLEMENTED_CLAIM_PHRASES:
        assert phrase not in app_text

    assert "not final model-selection results" in app_text
    assert "not implemented in this phase" in app_text
    assert "illustrative cost scenario" in app_text
    assert "does not select a final champion model" in app_text
    assert "not create a production decision rule" in app_text
    assert "sota performance achieved" not in app_text
    assert "does not" in app_text


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


def test_page_2_describes_model_display_grouping() -> None:
    page_2_text = PAGE_MODULES[1].read_text(encoding="utf-8")

    assert "Main comparison" in page_2_text
    assert "Baseline warning" in page_2_text
    assert "Secondary prototype comparison" in page_2_text
    assert "Full six-model benchmark table" in page_2_text
    assert "does not remove models" in page_2_text
    assert "does not create a final champion model" in page_2_text


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
