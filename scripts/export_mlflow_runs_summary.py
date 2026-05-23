"""Export a compact summary of local MLflow runs when local tracking data exists."""

from __future__ import annotations

import argparse
import importlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_PATH = Path("outputs/metrics/mlflow_runs_summary.csv")
LOCAL_MLFLOW_SOURCE_NAMES = ("mlflow.db", "mlruns", "mlartifacts")
SUMMARY_COLUMNS = [
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
]


@dataclass(frozen=True)
class ExportResult:
    """Result summary for a local MLflow export attempt."""

    exported: bool
    row_count: int
    output_path: Path
    source_paths: list[Path]
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Export a compact summary of local MLflow runs if local MLflow "
            "tracking data exists. This script does not copy raw MLflow artifacts."
        )
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="CSV path for the exported MLflow run summary.",
    )
    parser.add_argument(
        "--tracking-uri",
        default=None,
        help="Optional MLflow tracking URI. If omitted, local mlflow.db or mlruns is used.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = export_mlflow_runs_summary(
        project_root=PROJECT_ROOT,
        output_path=args.output,
        tracking_uri=args.tracking_uri,
    )
    print(result.message)
    return 0


def export_mlflow_runs_summary(
    *,
    project_root: Path,
    output_path: Path,
    tracking_uri: str | None = None,
) -> ExportResult:
    """Export a CSV summary if local MLflow tracking data is available."""

    root = project_root.resolve()
    output = resolve_project_path(root, output_path)
    source_paths = find_mlflow_sources(root)

    if not source_paths and not tracking_uri:
        return ExportResult(
            exported=False,
            row_count=0,
            output_path=output,
            source_paths=[],
            message=(
                "No local MLflow data found. Skipped export and did not create "
                "outputs/metrics/mlflow_runs_summary.csv."
            ),
        )

    try:
        mlflow = importlib.import_module("mlflow")
    except ImportError:
        return ExportResult(
            exported=False,
            row_count=0,
            output_path=output,
            source_paths=source_paths,
            message=(
                "MLflow is not installed in this environment. Skipped export "
                "without creating a fake summary."
            ),
        )

    selected_tracking_uri = tracking_uri or select_tracking_uri(root, source_paths)
    if selected_tracking_uri is None:
        return ExportResult(
            exported=False,
            row_count=0,
            output_path=output,
            source_paths=source_paths,
            message=(
                "Local MLflow artifact folders were found, but no supported "
                "tracking store was available for summary export."
            ),
        )

    mlflow.set_tracking_uri(selected_tracking_uri)
    summary = collect_run_summary(mlflow, selected_tracking_uri)
    output.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output, index=False)

    return ExportResult(
        exported=True,
        row_count=len(summary),
        output_path=output,
        source_paths=source_paths,
        message=(
            f"Exported {len(summary)} MLflow run rows to "
            f"{relative_project_path(root, output)}."
        ),
    )


def find_mlflow_sources(project_root: Path) -> list[Path]:
    """Return local MLflow source paths that exist in the project root."""

    return [
        project_root / name
        for name in LOCAL_MLFLOW_SOURCE_NAMES
        if (project_root / name).exists()
    ]


def select_tracking_uri(project_root: Path, source_paths: list[Path]) -> str | None:
    """Choose a supported local MLflow tracking URI."""

    sqlite_path = project_root / "mlflow.db"
    if sqlite_path in source_paths:
        return f"sqlite:///{sqlite_path.as_posix()}"

    mlruns_path = project_root / "mlruns"
    if mlruns_path in source_paths:
        return mlruns_path.resolve().as_uri()

    return None


def collect_run_summary(mlflow: Any, source: str) -> pd.DataFrame:
    """Collect a normalized run summary from an MLflow tracking store."""

    experiments = mlflow.search_experiments()
    experiment_ids = [experiment.experiment_id for experiment in experiments]
    if not experiment_ids:
        return pd.DataFrame(columns=SUMMARY_COLUMNS)

    runs = mlflow.search_runs(
        experiment_ids=experiment_ids,
        output_format="pandas",
    )
    if runs.empty:
        return pd.DataFrame(columns=SUMMARY_COLUMNS)

    rows = [normalize_run_row(row, source) for _index, row in runs.iterrows()]
    return pd.DataFrame(rows, columns=SUMMARY_COLUMNS)


def normalize_run_row(row: pd.Series, source: str) -> dict[str, object]:
    """Normalize one MLflow run row into public summary columns."""

    return {
        "run_id": value_from(row, "run_id"),
        "experiment_id": value_from(row, "experiment_id"),
        "status": value_from(row, "status"),
        "start_time": value_from(row, "start_time"),
        "end_time": value_from(row, "end_time"),
        "artifact_uri": value_from(row, "artifact_uri"),
        "model_name": first_available(
            row,
            ["params.model_name", "params.model", "tags.mlflow.runName"],
        ),
        "threshold": first_available(row, ["metrics.threshold", "params.threshold"]),
        "recall": value_from(row, "metrics.recall"),
        "precision": value_from(row, "metrics.precision"),
        "f2": value_from(row, "metrics.f2"),
        "roc_auc": value_from(row, "metrics.roc_auc"),
        "pr_auc": value_from(row, "metrics.pr_auc"),
        "flagged_sample_rate": first_available(
            row,
            ["metrics.flagged_sample_rate", "metrics.review_rate"],
        ),
        "source": source,
        "notes": "Exported from local MLflow tracking data.",
    }


def first_available(row: pd.Series, columns: list[str]) -> object:
    """Return the first non-empty value from candidate MLflow columns."""

    for column in columns:
        value = value_from(row, column)
        if value != "":
            return value
    return ""


def value_from(row: pd.Series, column: str) -> object:
    """Return a row value, using a blank string for unavailable values."""

    if column not in row or pd.isna(row[column]):
        return ""
    return row[column]


def resolve_project_path(project_root: Path, path: Path) -> Path:
    """Resolve a path inside the project root."""

    if path.is_absolute():
        return path
    return project_root / path


def relative_project_path(project_root: Path, path: Path) -> str:
    """Return a project-relative path for console messages."""

    return path.resolve().relative_to(project_root).as_posix()


if __name__ == "__main__":
    raise SystemExit(main())
