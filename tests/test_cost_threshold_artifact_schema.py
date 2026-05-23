"""Schema tests for prototype threshold / cost artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "configs" / "cost_scenarios_prototype.yaml"
BENCHMARK_SWEEP_PATH = (
    PROJECT_ROOT / "outputs" / "metrics" / "benchmark_threshold_sweep_prototype.csv"
)
COST_SWEEP_PATH = (
    PROJECT_ROOT / "outputs" / "metrics" / "cost_threshold_sweep_prototype.csv"
)
SELECTED_PATH = (
    PROJECT_ROOT / "outputs" / "metrics" / "cost_selected_thresholds_prototype.csv"
)
REPORT_PATH = PROJECT_ROOT / "reports" / "cost_threshold_prototype_report.md"
MANIFEST_PATH = PROJECT_ROOT / "outputs" / "artifact_manifest.json"

REQUIRED_COST_SWEEP_COLUMNS = {
    "model_name",
    "threshold",
    "scenario",
    "false_negative_cost",
    "false_positive_cost",
    "tp",
    "fp",
    "fn",
    "tn",
    "recall",
    "precision",
    "f2",
    "flagged_sample_rate",
    "total_cost",
    "cost_per_sample",
}
REQUIRED_SELECTED_COLUMNS = {
    "model_name",
    "scenario",
    "selected_threshold",
    "total_cost",
    "cost_per_sample",
    "recall",
    "precision",
    "f2",
    "flagged_sample_rate",
    "tp",
    "fp",
    "fn",
    "tn",
    "notes",
}
PROTOTYPE_COST_ARTIFACT_PATHS = {
    "outputs/metrics/cost_threshold_sweep_prototype.csv",
    "outputs/metrics/cost_selected_thresholds_prototype.csv",
    "reports/cost_threshold_prototype_report.md",
}


def test_cost_scenario_config_has_required_fields() -> None:
    config_text = CONFIG_PATH.read_text(encoding="utf-8")

    for scenario_name in ("balanced_review", "quality_first", "strict_quality"):
        assert scenario_name in config_text
    assert "false_negative_cost" in config_text
    assert "false_positive_cost" in config_text
    assert "review_capacity_limits" in config_text


def test_cost_threshold_sweep_artifact_schema_and_costs() -> None:
    rows = _read_csv_rows(COST_SWEEP_PATH)
    fieldnames = set(rows[0].keys())

    assert REQUIRED_COST_SWEEP_COLUMNS.issubset(fieldnames)
    for row in rows:
        assert float(row["total_cost"]) >= 0
        assert float(row["cost_per_sample"]) >= 0


def test_selected_threshold_artifact_schema_and_sources() -> None:
    selected_rows = _read_csv_rows(SELECTED_PATH)
    cost_rows = _read_csv_rows(COST_SWEEP_PATH)
    benchmark_rows = _read_csv_rows(BENCHMARK_SWEEP_PATH)

    selected_fieldnames = set(selected_rows[0].keys())
    cost_threshold_keys = {
        (row["model_name"], row["scenario"], row["threshold"])
        for row in cost_rows
    }
    benchmark_threshold_keys = {
        (row["model_name"], row["threshold"])
        for row in benchmark_rows
    }

    assert REQUIRED_SELECTED_COLUMNS.issubset(selected_fieldnames)
    for row in selected_rows:
        assert row["notes"]
        selected_threshold = row["selected_threshold"]
        assert (row["model_name"], row["scenario"], selected_threshold) in (
            cost_threshold_keys
        )
        assert (row["model_name"], selected_threshold) in benchmark_threshold_keys


def test_cost_artifacts_are_listed_in_manifest() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    artifacts = manifest["artifacts"]
    paths = {artifact["path"] for artifact in artifacts}
    cost_entries = [
        artifact
        for artifact in artifacts
        if artifact["path"] in PROTOTYPE_COST_ARTIFACT_PATHS
    ]

    assert PROTOTYPE_COST_ARTIFACT_PATHS.issubset(paths)
    assert len(cost_entries) == len(PROTOTYPE_COST_ARTIFACT_PATHS)
    for artifact in cost_entries:
        assert artifact["current_status"] == "prototype"
        assert (PROJECT_ROOT / artifact["path"]).is_file()


def test_cost_threshold_report_exists_and_is_cautious() -> None:
    report_text = REPORT_PATH.read_text(encoding="utf-8")

    assert "# Prototype Threshold / Cost Trade-Off Report" in report_text
    assert "best under this illustrative scenario" in report_text.lower()
    assert "final champion" not in report_text.lower()


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    assert rows
    return rows
