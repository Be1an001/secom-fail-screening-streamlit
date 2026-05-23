"""Run the SECOM literature-inspired benchmark prototype.

This script trains a small, fixed set of baseline reference and
literature-inspired model candidates. It is intended for manual artifact
generation, not for GitHub Actions CI.
"""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from secom_ml.data import load_secom_data
from secom_ml.metrics import calculate_binary_classification_metrics
from secom_ml.models import (
    build_dummy_classifier,
    build_logistic_regression_baseline,
    build_random_forest,
)
from secom_ml.preprocessing import (
    apply_missingness_selection,
    fit_linear_preprocessor,
    fit_tree_preprocessor,
    select_feature_columns_by_missingness,
    transform_linear_preprocessor,
    transform_tree_preprocessor,
)
from secom_ml.splitting import create_train_validation_test_split
from secom_ml.threshold import default_threshold_grid, select_threshold


DEFAULT_CONFIG = Path("configs/model_benchmark_prototype.yaml")
COMPARISON_COLUMNS = [
    "model_name",
    "model_group",
    "status",
    "evaluation_split",
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
    "threshold_selection_metric",
    "preprocessing_path",
    "resampling",
    "notes",
]
THRESHOLD_SWEEP_COLUMNS = [
    "model_name",
    "model_group",
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
]
OPTIONAL_IMPORTS = {
    "xgboost": "xgboost",
    "lightgbm": "lightgbm",
    "imblearn": "imblearn",
}


@dataclass(frozen=True)
class PreparedData:
    """Prepared train and validation arrays for benchmark candidates."""

    X_train_tree: object
    X_validation_tree: object
    X_train_linear: object
    X_validation_linear: object
    y_train: pd.Series
    y_validation: pd.Series
    train_rows: int
    validation_rows: int
    test_rows_reserved: int
    kept_features: int
    dropped_features: int
    linear_pca_components: int
    positive_scale_weight: float


@dataclass(frozen=True)
class PrototypeResult:
    """One candidate result row and optional threshold sweep rows."""

    model_name: str
    status: str
    comparison_row: dict[str, Any]
    threshold_sweep: pd.DataFrame


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run a literature-inspired SECOM fail-screening benchmark "
            "prototype and export reproducible artifacts."
        )
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Path to the benchmark prototype YAML config.",
    )
    return parser.parse_args()


def load_yaml_config(path: Path) -> dict[str, Any]:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML is required to read YAML configs.") from exc

    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def main() -> int:
    args = parse_args()
    config_path = _project_path(args.config)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    config = load_yaml_config(config_path)
    results, prepared = run_benchmark(config=config)
    write_outputs(results=results, prepared=prepared, config=config)
    print_run_summary(results)
    return 0


def run_benchmark(
    config: dict[str, Any],
) -> tuple[list[PrototypeResult], PreparedData]:
    seed = int(config.get("random_seed", 42))
    prepared = prepare_data(config=config, seed=seed)
    thresholds = threshold_grid_from_config(config)
    selection_metric = (
        config.get("threshold_search", {}).get("selection_metric", "f2")
    )

    results: list[PrototypeResult] = []
    for candidate in config.get("models", []):
        result = run_candidate(
            candidate=candidate,
            prepared=prepared,
            thresholds=thresholds,
            selection_metric=selection_metric,
            seed=seed,
        )
        results.append(result)

    return results, prepared


def prepare_data(config: dict[str, Any], seed: int) -> PreparedData:
    X, y, _metadata = load_secom_data(data_dir=_data_dir_from_config(config))

    split_config = config.get("split", {})
    splits = create_train_validation_test_split(
        X=X,
        y=y,
        test_size=float(split_config.get("test_size", 0.20)),
        validation_size=float(split_config.get("validation_size", 0.20)),
        random_state=int(split_config.get("random_state", seed)),
        stratify=bool(split_config.get("stratify", True)),
    )

    preprocessing_config = config.get("preprocessing", {})
    missingness_selection = select_feature_columns_by_missingness(
        splits.X_train,
        missingness_threshold=float(
            preprocessing_config.get("missingness_threshold", 0.50)
        ),
    )
    X_train_keep = apply_missingness_selection(
        splits.X_train,
        missingness_selection,
    )
    X_validation_keep = apply_missingness_selection(
        splits.X_validation,
        missingness_selection,
    )

    imputation_strategy = preprocessing_config.get("imputation_strategy", "median")
    tree_preprocessor, X_train_tree = fit_tree_preprocessor(
        X_train_keep,
        strategy=imputation_strategy,
    )
    X_validation_tree = transform_tree_preprocessor(
        X_validation_keep,
        tree_preprocessor,
    )

    linear_config = preprocessing_config.get("linear_path", {})
    linear_preprocessor, X_train_linear = fit_linear_preprocessor(
        X_train_keep,
        strategy=imputation_strategy,
        pca_variance=float(linear_config.get("pca_variance", 0.95)),
        random_state=seed,
    )
    X_validation_linear = transform_linear_preprocessor(
        X_validation_keep,
        linear_preprocessor,
    )

    negative_count = int((splits.y_train == 0).sum())
    positive_count = int((splits.y_train == 1).sum())
    positive_scale_weight = (
        float(negative_count / positive_count) if positive_count else 1.0
    )

    return PreparedData(
        X_train_tree=X_train_tree,
        X_validation_tree=X_validation_tree,
        X_train_linear=X_train_linear,
        X_validation_linear=X_validation_linear,
        y_train=splits.y_train,
        y_validation=splits.y_validation,
        train_rows=len(splits.y_train),
        validation_rows=len(splits.y_validation),
        test_rows_reserved=len(splits.y_test),
        kept_features=len(missingness_selection.keep_columns),
        dropped_features=len(missingness_selection.drop_columns),
        linear_pca_components=int(X_train_linear.shape[1]),
        positive_scale_weight=positive_scale_weight,
    )


def run_candidate(
    candidate: dict[str, Any],
    prepared: PreparedData,
    thresholds: list[float],
    selection_metric: str,
    seed: int,
) -> PrototypeResult:
    missing_dependencies = missing_optional_dependencies(candidate)
    if missing_dependencies:
        missing = ", ".join(missing_dependencies)
        return skipped_result(
            candidate=candidate,
            status="skipped",
            notes=f"Missing optional dependency: {missing}",
            selection_metric=selection_metric,
        )

    try:
        return completed_result(
            candidate=candidate,
            prepared=prepared,
            thresholds=thresholds,
            selection_metric=selection_metric,
            seed=seed,
        )
    except Exception as exc:
        if candidate.get("model_group") == "baseline_reference":
            raise
        return skipped_result(
            candidate=candidate,
            status="failed",
            notes=f"Prototype candidate failed: {exc}",
            selection_metric=selection_metric,
        )


def completed_result(
    candidate: dict[str, Any],
    prepared: PreparedData,
    thresholds: list[float],
    selection_metric: str,
    seed: int,
) -> PrototypeResult:
    X_train, X_validation = candidate_arrays(candidate, prepared)
    y_train = prepared.y_train
    resampling_label = "none"

    resampling_config = candidate.get("resampling") or {}
    if resampling_config:
        X_train, y_train = apply_training_only_resampling(
            X_train=X_train,
            y_train=prepared.y_train,
            resampling_config=resampling_config,
            seed=seed,
        )
        resampling_label = str(resampling_config.get("method", "none"))

    model = build_model(candidate, prepared, seed=seed)
    model.fit(X_train, y_train)
    validation_score = positive_class_probability(model, X_validation)
    selection = select_threshold(
        prepared.y_validation,
        validation_score,
        metric=selection_metric,
        thresholds=thresholds,
    )
    selected_threshold = float(selection.threshold)
    metrics = calculate_binary_classification_metrics(
        prepared.y_validation,
        validation_score,
        threshold=selected_threshold,
    )

    comparison_row = comparison_row_from_metrics(
        candidate=candidate,
        metrics=metrics,
        status="completed",
        selection_metric=selection_metric,
        resampling_label=resampling_label,
        notes=str(candidate.get("notes", "")),
    )
    threshold_sweep = threshold_sweep_from_selection(
        candidate=candidate,
        selection_sweep=selection.sweep,
    )
    return PrototypeResult(
        model_name=str(candidate["name"]),
        status="completed",
        comparison_row=comparison_row,
        threshold_sweep=threshold_sweep,
    )


def candidate_arrays(
    candidate: dict[str, Any],
    prepared: PreparedData,
) -> tuple[object, object]:
    preprocessing_path = candidate.get("preprocessing_path", "tree")
    if preprocessing_path == "linear_pca":
        return prepared.X_train_linear, prepared.X_validation_linear
    return prepared.X_train_tree, prepared.X_validation_tree


def build_model(
    candidate: dict[str, Any],
    prepared: PreparedData,
    seed: int,
) -> Any:
    model_type = candidate["model_type"]
    params = dict(candidate.get("params") or {})

    if model_type == "dummy_majority":
        return build_dummy_classifier(strategy="most_frequent")
    if model_type == "logistic_regression_pca":
        return build_logistic_regression_baseline(random_state=seed)
    if model_type == "random_forest":
        params.setdefault("random_state", seed)
        return build_random_forest(**params)
    if model_type == "xgboost_cost_sensitive":
        return build_xgboost_classifier(
            params=params,
            seed=seed,
            scale_pos_weight=candidate_scale_pos_weight(
                candidate,
                prepared.positive_scale_weight,
            ),
        )
    if model_type == "lightgbm_class_weighted":
        return build_lightgbm_classifier(
            params=params,
            seed=seed,
            scale_pos_weight=candidate_scale_pos_weight(
                candidate,
                prepared.positive_scale_weight,
            ),
            imbalance_strategy=str(
                (candidate.get("imbalance") or {}).get("strategy", "scale_pos_weight")
            ),
        )
    if model_type == "xgboost_smote":
        return build_xgboost_classifier(
            params=params,
            seed=seed,
            scale_pos_weight=1.0,
        )

    raise ValueError(f"Unsupported prototype model type: {model_type}")


def build_xgboost_classifier(
    params: dict[str, Any],
    seed: int,
    scale_pos_weight: float,
) -> Any:
    xgboost = importlib.import_module("xgboost")
    normalized = dict(params)
    normalized.setdefault("objective", "binary:logistic")
    normalized.setdefault("random_state", seed)
    normalized.setdefault("scale_pos_weight", scale_pos_weight)
    return xgboost.XGBClassifier(**normalized)


def build_lightgbm_classifier(
    params: dict[str, Any],
    seed: int,
    scale_pos_weight: float,
    imbalance_strategy: str = "scale_pos_weight",
) -> Any:
    lightgbm = importlib.import_module("lightgbm")
    normalized = dict(params)
    normalized.setdefault("objective", "binary")
    normalized.setdefault("random_state", seed)
    if imbalance_strategy == "is_unbalance":
        normalized.setdefault("is_unbalance", True)
    else:
        normalized.setdefault("scale_pos_weight", scale_pos_weight)
    return lightgbm.LGBMClassifier(**normalized)


def apply_training_only_resampling(
    X_train: object,
    y_train: pd.Series,
    resampling_config: dict[str, Any],
    seed: int,
) -> tuple[object, object]:
    method = str(resampling_config.get("method", "")).lower()
    if method != "smote":
        raise ValueError(f"Unsupported resampling method: {method}")

    imblearn_over_sampling = importlib.import_module("imblearn.over_sampling")
    positive_count = int((y_train == 1).sum())
    configured_neighbors = int(resampling_config.get("k_neighbors", 5))
    k_neighbors = min(configured_neighbors, max(1, positive_count - 1))
    sampler = imblearn_over_sampling.SMOTE(
        random_state=seed,
        k_neighbors=k_neighbors,
        sampling_strategy=resampling_config.get("sampling_strategy", "auto"),
    )
    return sampler.fit_resample(X_train, y_train)


def candidate_scale_pos_weight(
    candidate: dict[str, Any],
    base_scale_pos_weight: float,
) -> float:
    imbalance_config = candidate.get("imbalance") or {}
    multiplier = float(imbalance_config.get("scale_pos_weight_multiplier", 1.0))
    return float(base_scale_pos_weight * multiplier)


def missing_optional_dependencies(candidate: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for package_name in candidate.get("requires", []):
        import_name = OPTIONAL_IMPORTS.get(str(package_name), str(package_name))
        if importlib.util.find_spec(import_name) is None:
            missing.append(str(package_name))
    return missing


def skipped_result(
    candidate: dict[str, Any],
    status: str,
    notes: str,
    selection_metric: str,
) -> PrototypeResult:
    comparison_row = {
        "model_name": candidate.get("name"),
        "model_group": candidate.get("model_group"),
        "status": status,
        "evaluation_split": "validation",
        "threshold": None,
        "accuracy": None,
        "balanced_accuracy": None,
        "precision": None,
        "recall": None,
        "f1": None,
        "f2": None,
        "specificity": None,
        "roc_auc": None,
        "pr_auc": None,
        "tp": None,
        "fp": None,
        "fn": None,
        "tn": None,
        "flagged_sample_rate": None,
        "threshold_selection_metric": selection_metric,
        "preprocessing_path": candidate.get("preprocessing_path"),
        "resampling": _resampling_label(candidate),
        "notes": notes,
    }
    return PrototypeResult(
        model_name=str(candidate.get("name")),
        status=status,
        comparison_row=comparison_row,
        threshold_sweep=pd.DataFrame(columns=THRESHOLD_SWEEP_COLUMNS),
    )


def comparison_row_from_metrics(
    candidate: dict[str, Any],
    metrics: dict[str, Any],
    status: str,
    selection_metric: str,
    resampling_label: str,
    notes: str,
) -> dict[str, Any]:
    return {
        "model_name": candidate.get("name"),
        "model_group": candidate.get("model_group"),
        "status": status,
        "evaluation_split": "validation",
        "threshold": metrics["threshold"],
        "accuracy": metrics["accuracy"],
        "balanced_accuracy": metrics["balanced_accuracy"],
        "precision": metrics["precision"],
        "recall": metrics["recall"],
        "f1": metrics["f1"],
        "f2": metrics["f2"],
        "specificity": metrics["specificity"],
        "roc_auc": metrics["roc_auc"],
        "pr_auc": metrics["pr_auc"],
        "tp": metrics["tp"],
        "fp": metrics["fp"],
        "fn": metrics["fn"],
        "tn": metrics["tn"],
        "flagged_sample_rate": metrics["review_rate"],
        "threshold_selection_metric": selection_metric,
        "preprocessing_path": candidate.get("preprocessing_path"),
        "resampling": resampling_label,
        "notes": notes,
    }


def threshold_sweep_from_selection(
    candidate: dict[str, Any],
    selection_sweep: pd.DataFrame,
) -> pd.DataFrame:
    sweep = selection_sweep.copy()
    sweep.insert(0, "model_group", candidate.get("model_group"))
    sweep.insert(0, "model_name", candidate.get("name"))
    sweep["flagged_sample_rate"] = sweep["review_rate"]
    return sweep.loc[:, THRESHOLD_SWEEP_COLUMNS]


def positive_class_probability(model: Any, X: object) -> object:
    probabilities = model.predict_proba(X)
    class_labels = list(model.classes_)
    if 1 not in class_labels:
        raise ValueError("Model does not expose probability for positive class 1.")
    return probabilities[:, class_labels.index(1)]


def write_outputs(
    results: list[PrototypeResult],
    prepared: PreparedData,
    config: dict[str, Any],
) -> None:
    outputs = config.get("outputs", {})
    comparison_path = _project_path(
        outputs.get(
            "model_comparison",
            "outputs/metrics/benchmark_model_comparison_prototype.csv",
        )
    )
    threshold_path = _project_path(
        outputs.get(
            "threshold_sweep",
            "outputs/metrics/benchmark_threshold_sweep_prototype.csv",
        )
    )
    summary_path = _project_path(
        outputs.get(
            "summary_report",
            "reports/benchmark_prototype_summary.md",
        )
    )

    comparison_path.parent.mkdir(parents=True, exist_ok=True)
    threshold_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    comparison = pd.DataFrame(
        [result.comparison_row for result in results],
        columns=COMPARISON_COLUMNS,
    )
    comparison.to_csv(comparison_path, index=False)

    threshold_frames = [
        result.threshold_sweep
        for result in results
        if not result.threshold_sweep.empty
    ]
    threshold_sweep = (
        pd.concat(threshold_frames, ignore_index=True)
        if threshold_frames
        else pd.DataFrame(columns=THRESHOLD_SWEEP_COLUMNS)
    )
    threshold_sweep.to_csv(threshold_path, index=False)

    summary = build_summary_report(
        comparison=comparison,
        threshold_sweep=threshold_sweep,
        prepared=prepared,
        config=config,
        comparison_path=comparison_path,
        threshold_path=threshold_path,
    )
    summary_path.write_text(summary, encoding="utf-8")


def build_summary_report(
    comparison: pd.DataFrame,
    threshold_sweep: pd.DataFrame,
    prepared: PreparedData,
    config: dict[str, Any],
    comparison_path: Path,
    threshold_path: Path,
) -> str:
    completed = comparison[comparison["status"] == "completed"].copy()
    skipped_or_failed = comparison[comparison["status"] != "completed"].copy()

    lines = [
        "# Benchmark Prototype Summary",
        "",
        "This report summarizes a literature-inspired benchmark prototype for ",
        "SECOM screening decision support. It is a prototype artifact, not a ",
        "final six-model benchmark and not a SOTA result.",
        "",
        "## Scope",
        "",
        "- Uses the public UCI SECOM data files already tracked in the repo.",
        "- Uses stratified train, validation, and reserved test splits.",
        "- Fits missingness filtering, imputation, PCA, and resampling only on ",
        "  training data.",
        "- Selects thresholds on validation predictions with a threshold sweep.",
        "- Reserves the test split for later final evaluation work.",
        "",
        "## Data Preparation",
        "",
        f"- Training rows: {prepared.train_rows}",
        f"- Validation rows: {prepared.validation_rows}",
        f"- Reserved test rows: {prepared.test_rows_reserved}",
        f"- Kept sensor features after missingness filtering: {prepared.kept_features}",
        f"- Dropped sensor features: {prepared.dropped_features}",
        f"- PCA components for linear baseline: {prepared.linear_pca_components}",
        "",
        "## Completed Prototype Results",
        "",
        _markdown_table(
            completed,
            [
                "model_name",
                "threshold",
                "recall",
                "precision",
                "f2",
                "pr_auc",
                "roc_auc",
                "flagged_sample_rate",
            ],
        ),
        "",
        "## Skipped or Failed Candidates",
        "",
        _markdown_table(skipped_or_failed, ["model_name", "status", "notes"]),
        "",
        "## Exported Artifacts",
        "",
        f"- Model comparison: `{_relative_path(comparison_path)}`",
        f"- Threshold sweep: `{_relative_path(threshold_path)}`",
        f"- Threshold sweep rows: {len(threshold_sweep)}",
        "",
        "## Limitations",
        "",
        "- The benchmark is fixed-parameter prototype work.",
        "- It does not claim SOTA performance or better-than-research results.",
        "- It does not select a final champion model.",
        "- Feature importance and physical root-cause analysis are out of scope.",
        "- Future phases should review papers formally and refine the protocol.",
        "",
        "## Config",
        "",
        f"- Selection metric: `{config.get('threshold_search', {}).get('selection_metric', 'f2')}`",
        f"- Benchmark split: `{config.get('split', {}).get('benchmark_split', 'validation')}`",
    ]
    return "\n".join(lines).replace(" \n", "\n")


def print_run_summary(results: list[PrototypeResult]) -> None:
    comparison = pd.DataFrame([result.comparison_row for result in results])
    columns = [
        "model_name",
        "status",
        "threshold",
        "recall",
        "precision",
        "f2",
        "pr_auc",
        "roc_auc",
        "flagged_sample_rate",
    ]
    print("Benchmark prototype summary:")
    print(comparison.loc[:, columns].to_string(index=False))
    print("\nSaved prototype artifacts under outputs/metrics and reports.")


def threshold_grid_from_config(config: dict[str, Any]) -> list[float]:
    threshold_config = config.get("threshold_search", {})
    return default_threshold_grid(
        min_threshold=float(threshold_config.get("min_threshold", 0.05)),
        max_threshold=float(threshold_config.get("max_threshold", 0.95)),
        num_thresholds=int(threshold_config.get("num_thresholds", 181)),
    ).tolist()


def _markdown_table(data: pd.DataFrame, columns: list[str]) -> str:
    if data.empty:
        return "No rows."

    safe = data.loc[:, columns].copy()
    formatted_rows = [
        [_format_markdown_value(row[column]) for column in columns]
        for _index, row in safe.iterrows()
    ]
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _column in columns) + " |"
    body = ["| " + " | ".join(row) + " |" for row in formatted_rows]
    return "\n".join([header, separator, *body])


def _format_markdown_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value):
            return ""
        return f"{value:.4f}"
    return str(value)


def _resampling_label(candidate: dict[str, Any]) -> str:
    resampling = candidate.get("resampling") or {}
    return str(resampling.get("method", "none"))


def _data_dir_from_config(config: dict[str, Any]) -> Path | None:
    feature_path = config.get("data", {}).get("feature_path")
    if not feature_path:
        return None
    return _project_path(feature_path).parent


def _project_path(path_value: str | Path) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def _relative_path(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT).as_posix()


if __name__ == "__main__":
    raise SystemExit(main())
