"""Schema tests for prototype explainability artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "configs" / "explainability_prototype.yaml"
PERMUTATION_PATH = (
    PROJECT_ROOT / "outputs" / "metrics" / "permutation_importance_prototype.csv"
)
STABILITY_PATH = (
    PROJECT_ROOT / "outputs" / "metrics" / "feature_stability_prototype.csv"
)
TOP_SIGNALS_PATH = (
    PROJECT_ROOT / "outputs" / "metrics" / "top_sensor_signals_prototype.csv"
)
PERMUTATION_FIGURE_PATH = (
    PROJECT_ROOT / "outputs" / "figures" / "permutation_importance_prototype.png"
)
STABILITY_FIGURE_PATH = (
    PROJECT_ROOT / "outputs" / "figures" / "feature_stability_prototype.png"
)
REPORT_PATH = PROJECT_ROOT / "reports" / "explainability_prototype_report.md"
MANIFEST_PATH = PROJECT_ROOT / "outputs" / "artifact_manifest.json"

REQUIRED_PERMUTATION_COLUMNS = {
    "model_name",
    "feature",
    "importance_mean",
    "importance_std",
    "rank",
    "split",
    "scoring",
    "notes",
}
REQUIRED_STABILITY_COLUMNS = {
    "model_name",
    "feature",
    "appearance_count",
    "appearance_rate",
    "mean_rank",
    "best_rank",
    "worst_rank",
    "seeds",
    "notes",
}
REQUIRED_TOP_SIGNAL_COLUMNS = {
    "feature",
    "models_where_top",
    "model_count",
    "best_rank",
    "mean_rank",
    "notes",
}
EXPLAINABILITY_ARTIFACT_PATHS = {
    "outputs/metrics/permutation_importance_prototype.csv",
    "outputs/metrics/feature_stability_prototype.csv",
    "outputs/metrics/top_sensor_signals_prototype.csv",
    "outputs/figures/permutation_importance_prototype.png",
    "outputs/figures/feature_stability_prototype.png",
    "reports/explainability_prototype_report.md",
}


def test_explainability_config_exists_and_names_focus_models() -> None:
    config_text = CONFIG_PATH.read_text(encoding="utf-8")

    assert "random_forest_reference" in config_text
    assert "xgboost_cost_sensitive" in config_text
    assert "evaluation_split: validation" in config_text


def test_permutation_importance_schema() -> None:
    rows = read_csv_rows(PERMUTATION_PATH)

    assert REQUIRED_PERMUTATION_COLUMNS.issubset(rows[0])
    assert {row["model_name"] for row in rows} == {
        "random_forest_reference",
        "xgboost_cost_sensitive",
    }


def test_feature_stability_schema() -> None:
    rows = read_csv_rows(STABILITY_PATH)

    assert REQUIRED_STABILITY_COLUMNS.issubset(rows[0])
    for row in rows:
        assert 0 <= float(row["appearance_rate"]) <= 1


def test_top_sensor_signal_schema() -> None:
    rows = read_csv_rows(TOP_SIGNALS_PATH)

    assert REQUIRED_TOP_SIGNAL_COLUMNS.issubset(rows[0])
    assert rows[0]["feature"].startswith("sensor_")


def test_explainability_manifest_entries_and_figures_exist() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    artifacts = manifest["artifacts"]
    paths = {artifact["path"] for artifact in artifacts}
    explainability_entries = [
        artifact
        for artifact in artifacts
        if artifact["path"] in EXPLAINABILITY_ARTIFACT_PATHS
    ]

    assert EXPLAINABILITY_ARTIFACT_PATHS.issubset(paths)
    assert len(explainability_entries) == len(EXPLAINABILITY_ARTIFACT_PATHS)
    for artifact in explainability_entries:
        assert artifact["current_status"] == "prototype"
        assert (PROJECT_ROOT / artifact["path"]).is_file()

    assert PERMUTATION_FIGURE_PATH.is_file()
    assert STABILITY_FIGURE_PATH.is_file()


def test_explainability_report_has_responsible_wording() -> None:
    report_text = REPORT_PATH.read_text(encoding="utf-8").lower()

    assert "model-important sensor signals" in report_text
    assert "not physical root-cause analysis" in report_text
    assert "not causal proof" in report_text
    assert "production diagnostic" not in report_text
    assert "causal explanation" not in report_text


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    assert rows
    return rows
