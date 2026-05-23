"""Tests for safe MLflow summary export behavior."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "export_mlflow_runs_summary.py"
MANIFEST_PATH = PROJECT_ROOT / "outputs" / "artifact_manifest.json"
MLFLOW_SUMMARY_PATH = PROJECT_ROOT / "outputs" / "metrics" / "mlflow_runs_summary.csv"
PAGE_5_PATH = PROJECT_ROOT / "app_pages" / "page_5_mlops_ai_api.py"
REPORT_PATH = PROJECT_ROOT / "reports" / "mlflow_artifact_tracking_summary.md"
SUMMARY_COLUMNS = {
    "run_id",
    "experiment_id",
    "status",
    "start_time",
    "end_time",
    "artifact_uri",
    "model_name",
    "threshold",
    "recall",
    "precision",
    "f2",
    "roc_auc",
    "pr_auc",
    "flagged_sample_rate",
    "source",
    "notes",
}


def test_mlflow_export_script_mentions_local_sources() -> None:
    source = SCRIPT_PATH.read_text(encoding="utf-8")

    assert "mlflow.db" in source
    assert "mlruns" in source
    assert "mlartifacts" in source
    assert "No local MLflow data found" in source
    assert "fake summary" in source


def test_mlflow_export_skips_without_local_tracking_data() -> None:
    module = load_export_module()
    with tempfile.TemporaryDirectory(dir=PROJECT_ROOT) as temp_dir:
        temp_root = Path(temp_dir)
        output_path = temp_root / "outputs" / "metrics" / "mlflow_runs_summary.csv"

        result = module.export_mlflow_runs_summary(
            project_root=temp_root,
            output_path=output_path,
        )

        assert result.exported is False
        assert result.row_count == 0
        assert result.source_paths == []
        assert not output_path.exists()


def test_mlflow_summary_manifest_matches_file_presence() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest_paths = {artifact["path"] for artifact in manifest["artifacts"]}

    if MLFLOW_SUMMARY_PATH.exists():
        assert "outputs/metrics/mlflow_runs_summary.csv" in manifest_paths
    else:
        assert "outputs/metrics/mlflow_runs_summary.csv" not in manifest_paths

    assert "reports/mlflow_artifact_tracking_summary.md" in manifest_paths


def test_mlflow_tracking_report_uses_portfolio_scale_wording() -> None:
    report = REPORT_PATH.read_text(encoding="utf-8").lower()

    assert "artifact-driven streamlit app" in report
    assert "lightweight artifact registry" in report
    assert "local mlflow tracking" in report
    assert "no production mlops platform is claimed" in report
    assert "future controlled rag-lite summary is implemented" not in report


def test_page_5_describes_mlflow_and_future_boundaries() -> None:
    page_text = PAGE_5_PATH.read_text(encoding="utf-8").lower()

    assert "artifact-driven" in page_text
    assert "local mlflow tracking" in page_text
    assert "exported mlflow summary" in page_text
    assert "fastapi artifact service" in page_text
    assert "controlled rag-lite summary" in page_text
    assert "optional openai api use" in page_text
    assert "deployed mlflow tracking server" in page_text
    assert "not a production backend" in page_text
    assert "not a general chatbot" in page_text
    assert "production mlops platform" not in page_text
    assert "full enterprise" not in page_text


def test_declared_mlflow_summary_columns_match_expected_schema() -> None:
    module = load_export_module()

    assert set(module.SUMMARY_COLUMNS) == SUMMARY_COLUMNS


def load_export_module():
    spec = importlib.util.spec_from_file_location(
        "export_mlflow_runs_summary",
        SCRIPT_PATH,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module
