"""Tests for app artifact loading helpers."""

from __future__ import annotations

import pytest

from app_utils.artifact_loader import (
    filter_manifest_artifacts,
    list_existing_artifacts,
    load_artifact_manifest,
    load_csv_artifact,
    load_markdown_artifact,
    project_root,
    validate_manifest_paths,
)


def test_project_root_resolves_repository_root() -> None:
    root = project_root()

    assert (root / "README.md").is_file()
    assert (root / "data").is_dir()


def test_known_metrics_artifact_can_be_loaded() -> None:
    metrics = load_csv_artifact("outputs/metrics/final_test_metrics.csv")

    assert not metrics.empty
    assert "selected_experiment_name" in metrics.columns
    assert metrics.loc[0, "selected_experiment_name"] == (
        "rf_current_config_threshold_tuned"
    )


def test_known_markdown_report_can_be_loaded() -> None:
    report = load_markdown_artifact("reports/model_card.md")

    assert "# Model Card" in report
    assert "Random Forest" in report


def test_missing_required_artifact_raises_file_not_found() -> None:
    with pytest.raises(FileNotFoundError, match="Required artifact not found"):
        load_csv_artifact("outputs/metrics/missing_file.csv")


def test_list_existing_artifacts_returns_only_existing_paths() -> None:
    existing = list_existing_artifacts(
        [
            "outputs/metrics/final_test_metrics.csv",
            "outputs/metrics/missing_file.csv",
            "reports/model_card.md",
        ]
    )

    assert existing == [
        "outputs/metrics/final_test_metrics.csv",
        "reports/model_card.md",
    ]


def test_load_artifact_manifest_returns_baseline_manifest() -> None:
    manifest = load_artifact_manifest()

    assert manifest["project"] == "secom-fail-screening-streamlit"
    assert manifest["manifest_version"] == "0.1.0"
    assert manifest["scope"] == "baseline artifacts"
    assert len(manifest["artifacts"]) >= 1


def test_validate_manifest_paths_accepts_existing_artifacts() -> None:
    manifest = load_artifact_manifest()

    artifact_paths = validate_manifest_paths(manifest)

    assert "outputs/metrics/final_test_metrics.csv" in artifact_paths
    assert "reports/model_card.md" in artifact_paths


def test_validate_manifest_paths_catches_missing_paths() -> None:
    manifest = {
        "artifacts": [
            {
                "path": "outputs/metrics/missing_file.csv",
            }
        ]
    }

    with pytest.raises(FileNotFoundError, match="missing_file.csv"):
        validate_manifest_paths(manifest)


def test_filter_manifest_artifacts_by_page_and_type() -> None:
    manifest = load_artifact_manifest()

    page_artifacts = filter_manifest_artifacts(
        manifest,
        page="Page 3 - Champion Trade-off",
        artifact_type="metrics_table",
    )

    assert [artifact["name"] for artifact in page_artifacts] == [
        "threshold_sweep",
        "final_test_metrics",
    ]
