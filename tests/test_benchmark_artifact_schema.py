"""Schema tests for the benchmark prototype artifacts.

These tests validate exported artifacts without running model training in CI.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "configs" / "model_benchmark_prototype.yaml"
COMPARISON_PATH = (
    PROJECT_ROOT / "outputs" / "metrics" / "benchmark_model_comparison_prototype.csv"
)
THRESHOLD_SWEEP_PATH = (
    PROJECT_ROOT / "outputs" / "metrics" / "benchmark_threshold_sweep_prototype.csv"
)
MANIFEST_PATH = PROJECT_ROOT / "outputs" / "artifact_manifest.json"

EXPECTED_MODEL_NAMES = {
    "dummy_majority_baseline",
    "logistic_regression_pca_baseline",
    "random_forest_reference",
    "xgboost_cost_sensitive",
    "lightgbm_class_weighted",
    "xgboost_training_only_smote",
}
REQUIRED_COMPARISON_COLUMNS = {
    "model_name",
    "model_group",
    "status",
    "threshold",
    "accuracy",
    "balanced_accuracy",
    "precision",
    "recall",
    "f1",
    "f2",
    "specificity",
    "roc_auc",
    "pr_auc",
    "tp",
    "fp",
    "fn",
    "tn",
    "flagged_sample_rate",
    "notes",
}
REQUIRED_SWEEP_COLUMNS = {
    "model_name",
    "threshold",
    "precision",
    "recall",
    "f1",
    "f2",
    "specificity",
    "balanced_accuracy",
    "flagged_sample_rate",
    "tp",
    "fp",
    "fn",
    "tn",
}
PROTOTYPE_ARTIFACT_PATHS = {
    "outputs/metrics/benchmark_model_comparison_prototype.csv",
    "outputs/metrics/benchmark_threshold_sweep_prototype.csv",
    "reports/benchmark_prototype_summary.md",
}


def test_benchmark_config_lists_expected_models() -> None:
    config_text = CONFIG_PATH.read_text(encoding="utf-8")

    for model_name in EXPECTED_MODEL_NAMES:
        assert model_name in config_text

    assert "training-only SMOTE" in config_text
    assert "so" + "ta" not in config_text.lower()


def test_benchmark_comparison_artifact_schema() -> None:
    rows = _read_csv_rows(COMPARISON_PATH)
    fieldnames = set(rows[0].keys())
    model_names = {row["model_name"] for row in rows}

    assert REQUIRED_COMPARISON_COLUMNS.issubset(fieldnames)
    assert EXPECTED_MODEL_NAMES.issubset(model_names)

    for row in rows:
        assert row["status"] in {"completed", "skipped", "failed"}
        assert row["status"] != "placeholder"
        if row["status"] != "completed":
            assert row["notes"]


def test_benchmark_threshold_sweep_artifact_schema() -> None:
    rows = _read_csv_rows(THRESHOLD_SWEEP_PATH)
    fieldnames = set(rows[0].keys())

    assert REQUIRED_SWEEP_COLUMNS.issubset(fieldnames)
    assert {row["model_name"] for row in rows}


def test_artifact_manifest_lists_prototype_outputs() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    artifacts = manifest["artifacts"]
    paths = {artifact["path"] for artifact in artifacts}
    prototype_entries = [
        artifact
        for artifact in artifacts
        if artifact["path"] in PROTOTYPE_ARTIFACT_PATHS
    ]

    assert PROTOTYPE_ARTIFACT_PATHS.issubset(paths)
    assert len(prototype_entries) == len(PROTOTYPE_ARTIFACT_PATHS)
    for artifact in prototype_entries:
        assert artifact["current_status"] == "prototype"
        assert (PROJECT_ROOT / artifact["path"]).is_file()


def test_resampling_is_documented_as_training_only() -> None:
    script_text = (
        PROJECT_ROOT / "scripts" / "run_model_benchmark_prototype.py"
    ).read_text(encoding="utf-8")

    assert "apply_training_only_resampling" in script_text
    assert "fit_resample(X_train, y_train)" in script_text


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    assert rows
    return rows
