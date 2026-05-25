"""Generate prototype explainability artifacts for selected benchmark models."""

from __future__ import annotations

import argparse
import importlib
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from secom_ml.data import load_secom_data
from secom_ml.models import build_random_forest
from secom_ml.preprocessing import (
    apply_missingness_selection,
    fit_tree_preprocessor,
    select_feature_columns_by_missingness,
    transform_tree_preprocessor,
)
from secom_ml.splitting import create_train_validation_test_split


DEFAULT_CONFIG = Path("configs/explainability_prototype.yaml")
PERMUTATION_COLUMNS = [
    "model_name",
    "feature",
    "importance_mean",
    "importance_std",
    "rank",
    "split",
    "scoring",
    "notes",
]
STABILITY_COLUMNS = [
    "model_name",
    "feature",
    "appearance_count",
    "appearance_rate",
    "mean_rank",
    "best_rank",
    "worst_rank",
    "seeds",
    "notes",
]
TOP_SIGNAL_COLUMNS = [
    "feature",
    "models_where_top",
    "model_count",
    "best_rank",
    "mean_rank",
    "notes",
]


@dataclass(frozen=True)
class PreparedExplainabilityData:
    """Prepared arrays and labels for one explainability run."""

    X_train: object
    X_eval: object
    y_train: pd.Series
    y_eval: pd.Series
    feature_names: list[str]
    eval_split_name: str
    positive_scale_weight: float
    train_rows: int
    eval_rows: int
    reserved_test_rows: int
    kept_features: int
    dropped_features: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate prototype permutation importance and feature stability "
            "artifacts for selected SECOM benchmark models."
        )
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Path to the explainability YAML config.",
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
    config_path = project_path(args.config)
    if not config_path.is_file():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    config = load_yaml_config(config_path)
    benchmark_config = load_yaml_config(project_path(config["benchmark_config"]))
    outputs = run_explainability(
        config=config,
        benchmark_config=benchmark_config,
    )
    write_outputs(outputs=outputs, config=config)
    print_summary(outputs)
    return 0


def run_explainability(
    config: dict[str, Any],
    benchmark_config: dict[str, Any],
) -> dict[str, Any]:
    focus_models = list(config["focus_models"])
    seeds = [int(seed) for seed in config["stability_seeds"]]
    primary_seed = seeds[0]
    n_repeats = int(config.get("n_repeats", 5))
    n_top_features = int(config.get("n_top_features", 20))
    candidate_features_per_model = int(config.get("candidate_features_per_model", 80))
    scoring = str(config.get("scoring", "average_precision"))

    permutation_rows: list[dict[str, Any]] = []
    stability_seed_rows: list[dict[str, Any]] = []
    prepared_for_report: PreparedExplainabilityData | None = None

    for seed in seeds:
        prepared = prepare_explainability_data(
            benchmark_config=benchmark_config,
            explainability_config=config,
            seed=seed,
        )
        if seed == primary_seed:
            prepared_for_report = prepared

        for model_name in focus_models:
            candidate = find_model_config(benchmark_config, model_name)
            model = build_focus_model(candidate, prepared, seed)
            model.fit(prepared.X_train, prepared.y_train)
            importance = calculate_permutation_rows(
                model=model,
                model_name=model_name,
                prepared=prepared,
                n_repeats=n_repeats,
                n_top_features=n_top_features,
                candidate_features_per_model=candidate_features_per_model,
                scoring=scoring,
                seed=seed,
            )

            if seed == primary_seed:
                permutation_rows.extend(importance)
            stability_seed_rows.extend(
                {
                    **row,
                    "seed": seed,
                }
                for row in importance
            )

    permutation_importance_frame = pd.DataFrame(
        permutation_rows,
        columns=PERMUTATION_COLUMNS,
    )
    feature_stability = build_feature_stability(
        stability_seed_rows=stability_seed_rows,
        seeds=seeds,
    )
    top_sensor_signals = build_top_sensor_signals(feature_stability)

    if prepared_for_report is None:
        raise ValueError("At least one stability seed is required.")

    return {
        "permutation_importance": permutation_importance_frame,
        "feature_stability": feature_stability,
        "top_sensor_signals": top_sensor_signals,
        "prepared": prepared_for_report,
        "focus_models": focus_models,
        "seeds": seeds,
        "n_repeats": n_repeats,
        "n_top_features": n_top_features,
        "candidate_features_per_model": candidate_features_per_model,
        "scoring": scoring,
    }


def prepare_explainability_data(
    benchmark_config: dict[str, Any],
    explainability_config: dict[str, Any],
    seed: int,
) -> PreparedExplainabilityData:
    X, y, _metadata = load_secom_data(data_dir=data_dir_from_config(benchmark_config))

    split_config = benchmark_config.get("split", {})
    splits = create_train_validation_test_split(
        X=X,
        y=y,
        test_size=float(split_config.get("test_size", 0.20)),
        validation_size=float(split_config.get("validation_size", 0.20)),
        random_state=seed,
        stratify=bool(split_config.get("stratify", True)),
    )

    preprocessing_config = benchmark_config.get("preprocessing", {})
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

    evaluation_split = str(explainability_config.get("evaluation_split", "validation"))
    if evaluation_split == "test":
        X_eval_raw = splits.X_test
        y_eval = splits.y_test
    elif evaluation_split == "validation":
        X_eval_raw = splits.X_validation
        y_eval = splits.y_validation
    else:
        raise ValueError("evaluation_split must be validation or test.")

    X_eval_keep = apply_missingness_selection(X_eval_raw, missingness_selection)
    tree_preprocessor, X_train_tree = fit_tree_preprocessor(
        X_train_keep,
        strategy=preprocessing_config.get("imputation_strategy", "median"),
    )
    X_eval_tree = transform_tree_preprocessor(X_eval_keep, tree_preprocessor)

    negative_count = int((splits.y_train == 0).sum())
    positive_count = int((splits.y_train == 1).sum())
    positive_scale_weight = (
        float(negative_count / positive_count) if positive_count else 1.0
    )

    return PreparedExplainabilityData(
        X_train=X_train_tree,
        X_eval=X_eval_tree,
        y_train=splits.y_train,
        y_eval=y_eval,
        feature_names=list(tree_preprocessor.feature_columns),
        eval_split_name=evaluation_split,
        positive_scale_weight=positive_scale_weight,
        train_rows=len(splits.y_train),
        eval_rows=len(y_eval),
        reserved_test_rows=len(splits.y_test),
        kept_features=len(missingness_selection.keep_columns),
        dropped_features=len(missingness_selection.drop_columns),
    )


def calculate_permutation_rows(
    model: Any,
    model_name: str,
    prepared: PreparedExplainabilityData,
    n_repeats: int,
    n_top_features: int,
    candidate_features_per_model: int,
    scoring: str,
    seed: int,
) -> list[dict[str, Any]]:
    candidate_indices = select_candidate_feature_indices(
        model=model,
        feature_names=prepared.feature_names,
        n_top_features=n_top_features,
        candidate_features_per_model=candidate_features_per_model,
    )
    baseline_score = score_model(model, prepared.X_eval, prepared.y_eval, scoring)
    rng = np.random.default_rng(seed)

    rows = []
    for feature_index in candidate_indices:
        feature = prepared.feature_names[feature_index]
        repeat_scores = []
        for _repeat in range(n_repeats):
            X_permuted = np.asarray(prepared.X_eval).copy()
            X_permuted[:, feature_index] = rng.permutation(
                X_permuted[:, feature_index]
            )
            repeat_scores.append(
                baseline_score
                - score_model(model, X_permuted, prepared.y_eval, scoring)
            )

        rows.append(
            {
                "model_name": model_name,
                "feature": feature,
                "importance_mean": float(np.mean(repeat_scores)),
                "importance_std": float(np.std(repeat_scores)),
                "split": prepared.eval_split_name,
                "scoring": scoring,
                "notes": (
                    "Permutation importance for model-important sensor signals "
                    "from a model-selected candidate set."
                ),
            }
        )

    ranked = sorted(
        rows,
        key=lambda row: (-row["importance_mean"], row["feature"]),
    )[:n_top_features]
    for rank, row in enumerate(ranked, start=1):
        row["rank"] = rank
    return ranked


def select_candidate_feature_indices(
    model: Any,
    feature_names: list[str],
    n_top_features: int,
    candidate_features_per_model: int,
) -> list[int]:
    """Select a compact candidate set before permutation scoring."""

    importances = getattr(model, "feature_importances_", None)
    candidate_count = min(
        len(feature_names),
        max(n_top_features, candidate_features_per_model),
    )
    if importances is None:
        return list(range(candidate_count))

    ranked_indices = np.argsort(np.asarray(importances, dtype=float))[::-1]
    return [int(index) for index in ranked_indices[:candidate_count]]


def score_model(model: Any, X: object, y: pd.Series, scoring: str) -> float:
    """Score a model using the configured explainability scorer."""

    if scoring != "average_precision":
        raise ValueError("Only average_precision scoring is supported.")

    if hasattr(model, "predict_proba"):
        scores = model.predict_proba(X)[:, 1]
    elif hasattr(model, "decision_function"):
        scores = model.decision_function(X)
    else:
        scores = model.predict(X)
    return float(average_precision_score(y, scores))


def build_feature_stability(
    stability_seed_rows: list[dict[str, Any]],
    seeds: list[int],
) -> pd.DataFrame:
    frame = pd.DataFrame(stability_seed_rows)
    grouped_rows: list[dict[str, Any]] = []
    for (model_name, feature), group in frame.groupby(["model_name", "feature"]):
        ranks = group["rank"].astype(float)
        seed_values = sorted(str(seed) for seed in group["seed"].unique())
        appearance_count = int(len(group))
        grouped_rows.append(
            {
                "model_name": model_name,
                "feature": feature,
                "appearance_count": appearance_count,
                "appearance_rate": appearance_count / len(seeds),
                "mean_rank": float(ranks.mean()),
                "best_rank": int(ranks.min()),
                "worst_rank": int(ranks.max()),
                "seeds": ";".join(seed_values),
                "notes": "Top-feature stability across configured seeds.",
            }
        )

    stability = pd.DataFrame(grouped_rows, columns=STABILITY_COLUMNS)
    return stability.sort_values(
        by=["model_name", "appearance_count", "mean_rank", "feature"],
        ascending=[True, False, True, True],
        kind="mergesort",
    ).reset_index(drop=True)


def build_top_sensor_signals(feature_stability: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for feature, group in feature_stability.groupby("feature"):
        model_names = sorted(group["model_name"].unique().tolist())
        rows.append(
            {
                "feature": feature,
                "models_where_top": ";".join(model_names),
                "model_count": int(len(model_names)),
                "best_rank": int(group["best_rank"].min()),
                "mean_rank": float(group["mean_rank"].mean()),
                "notes": (
                    "Anonymous sensor feature appearing in top prototype "
                    "explainability rankings."
                ),
            }
        )

    top_signals = pd.DataFrame(rows, columns=TOP_SIGNAL_COLUMNS)
    return top_signals.sort_values(
        by=["model_count", "mean_rank", "feature"],
        ascending=[False, True, True],
        kind="mergesort",
    ).reset_index(drop=True)


def build_focus_model(
    candidate: dict[str, Any],
    prepared: PreparedExplainabilityData,
    seed: int,
) -> Any:
    model_type = candidate["model_type"]
    params = dict(candidate.get("params") or {})

    if model_type == "random_forest":
        params.setdefault("random_state", seed)
        params["n_jobs"] = 1
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

    raise ValueError(f"Unsupported explainability focus model type: {model_type}")


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


def candidate_scale_pos_weight(
    candidate: dict[str, Any],
    base_scale_pos_weight: float,
) -> float:
    imbalance_config = candidate.get("imbalance") or {}
    multiplier = float(imbalance_config.get("scale_pos_weight_multiplier", 1.0))
    return float(base_scale_pos_weight * multiplier)


def find_model_config(
    benchmark_config: dict[str, Any],
    model_name: str,
) -> dict[str, Any]:
    for candidate in benchmark_config.get("models", []):
        if candidate.get("name") == model_name:
            return candidate
    raise ValueError(f"Focus model not found in benchmark config: {model_name}")


def write_outputs(outputs: dict[str, Any], config: dict[str, Any]) -> None:
    output_paths = resolve_output_paths(config)
    for path in output_paths.values():
        path.parent.mkdir(parents=True, exist_ok=True)

    outputs["permutation_importance"].to_csv(
        output_paths["permutation_importance"],
        index=False,
    )
    outputs["feature_stability"].to_csv(
        output_paths["feature_stability"],
        index=False,
    )
    outputs["top_sensor_signals"].to_csv(
        output_paths["top_sensor_signals"],
        index=False,
    )
    write_figures(outputs=outputs, output_paths=output_paths)
    output_paths["report"].write_text(
        build_report(outputs=outputs, output_paths=output_paths),
        encoding="utf-8",
    )


def write_figures(outputs: dict[str, Any], output_paths: dict[str, Path]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    permutation = outputs["permutation_importance"]
    focus_models = outputs["focus_models"]
    fig, axes = plt.subplots(1, len(focus_models), figsize=(14, 7), sharex=False)
    if len(focus_models) == 1:
        axes = [axes]

    for axis, model_name in zip(axes, focus_models, strict=True):
        rows = (
            permutation[permutation["model_name"] == model_name]
            .sort_values("rank")
            .head(12)
            .sort_values("importance_mean")
        )
        axis.barh(rows["feature"], rows["importance_mean"], color="#3A6EA5")
        axis.set_title(model_name)
        axis.set_xlabel("Mean importance")
        axis.grid(axis="x", alpha=0.25)

    fig.suptitle("Prototype permutation importance")
    fig.tight_layout()
    fig.savefig(output_paths["permutation_importance_figure"], dpi=160)
    plt.close(fig)

    stability = outputs["feature_stability"].copy()
    stability["label"] = stability["model_name"] + " / " + stability["feature"]
    stability_rows = (
        stability.sort_values(
            by=["appearance_count", "mean_rank", "label"],
            ascending=[False, True, True],
        )
        .head(20)
        .sort_values(["appearance_count", "mean_rank"], ascending=[True, False])
    )
    fig, axis = plt.subplots(figsize=(10, 8))
    axis.barh(
        stability_rows["label"],
        stability_rows["appearance_rate"],
        color="#4C956C",
    )
    axis.set_xlabel("Appearance rate across seeds")
    axis.set_xlim(0, 1.05)
    axis.set_title("Prototype feature stability")
    axis.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_paths["feature_stability_figure"], dpi=160)
    plt.close(fig)


def build_report(outputs: dict[str, Any], output_paths: dict[str, Path]) -> str:
    prepared = outputs["prepared"]
    top_signals = outputs["top_sensor_signals"].head(12)
    stability = outputs["feature_stability"]
    stable_features = stability[stability["appearance_rate"] >= 1.0]

    lines = [
        "# Prototype Explainability Report",
        "",
        "This report summarizes prototype explainability artifacts for "
        "model-important sensor signals in the SECOM fail-screening benchmark.",
        "Analysis method references are summarized in "
        "[Literature References](../docs/literature_references.md).",
        "",
        "## Focus Models",
        "",
        "- `random_forest_reference`: current strongest prototype F2 reference.",
        "- `xgboost_cost_sensitive`: higher-recall option with higher review workload.",
        "",
        "These focus models are useful for the current portfolio story. The "
        "other benchmark models remain in the benchmark artifacts.",
        "",
        "## Method",
        "",
        f"- Method: permutation importance on the {prepared.eval_split_name} split.",
        f"- Scoring: `{outputs['scoring']}`.",
        f"- Repeats per model: {outputs['n_repeats']}.",
        f"- Candidate sensor features per model: {outputs['candidate_features_per_model']}.",
        f"- Stability seeds: {', '.join(str(seed) for seed in outputs['seeds'])}.",
        "- Split, missingness filtering, imputation, and model fitting are "
        "performed without using validation rows for training.",
        "- Candidate sensor features are selected from model-native importance "
        "before permutation scoring to keep this prototype runtime practical.",
        "",
        "## Data Context",
        "",
        f"- Training rows: {prepared.train_rows}",
        f"- Explainability split rows: {prepared.eval_rows}",
        f"- Reserved test rows: {prepared.reserved_test_rows}",
        f"- Kept sensor features: {prepared.kept_features}",
        f"- Dropped sensor features: {prepared.dropped_features}",
        "",
        "## Top Model-Important Sensor Signals",
        "",
        markdown_table(
            top_signals,
            ["feature", "models_where_top", "model_count", "best_rank", "mean_rank"],
        ),
        "",
        "## Feature Stability",
        "",
        f"- Stable feature rows with appearance rate 1.0: {len(stable_features)}",
        "- Stability means the anonymous sensor feature appeared in the top "
        "ranked set across configured seeds for the same model.",
        "",
        "## Exported Artifacts",
        "",
        f"- Permutation importance: `{relative_path(output_paths['permutation_importance'])}`",
        f"- Feature stability: `{relative_path(output_paths['feature_stability'])}`",
        f"- Top sensor signals: `{relative_path(output_paths['top_sensor_signals'])}`",
        f"- Permutation importance figure: `{relative_path(output_paths['permutation_importance_figure'])}`",
        f"- Feature stability figure: `{relative_path(output_paths['feature_stability_figure'])}`",
        "",
        "## Limitations",
        "",
        "- Sensor names are anonymous, so these results do not identify process "
        "mechanisms.",
        "- This is not physical root-cause analysis.",
        "- These rankings are not causal proof.",
        "- A process engineer could use these signals as investigation support, "
        "not as proof.",
        "- This report does not select a final champion model.",
        "- SHAP was not added in this phase to keep the project lightweight.",
    ]
    return "\n".join(lines)


def print_summary(outputs: dict[str, Any]) -> None:
    print("Prototype explainability artifacts generated:")
    print(
        outputs["top_sensor_signals"]
        .head(10)
        .loc[:, ["feature", "models_where_top", "model_count", "best_rank"]]
        .to_string(index=False)
    )


def markdown_table(data: pd.DataFrame, columns: list[str]) -> str:
    if data.empty:
        return "No rows."

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _column in columns) + " |"
    rows = []
    for _index, row in data.loc[:, columns].iterrows():
        values = [format_markdown_value(row[column]) for column in columns]
        rows.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *rows])


def format_markdown_value(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def resolve_output_paths(config: dict[str, Any]) -> dict[str, Path]:
    outputs = config.get("outputs", {})
    return {
        "permutation_importance": project_path(outputs["permutation_importance"]),
        "feature_stability": project_path(outputs["feature_stability"]),
        "top_sensor_signals": project_path(outputs["top_sensor_signals"]),
        "permutation_importance_figure": project_path(
            outputs["permutation_importance_figure"]
        ),
        "feature_stability_figure": project_path(
            outputs["feature_stability_figure"]
        ),
        "report": project_path(outputs["report"]),
    }


def data_dir_from_config(config: dict[str, Any]) -> Path | None:
    feature_path = config.get("data", {}).get("feature_path")
    if not feature_path:
        return None
    return project_path(feature_path).parent


def project_path(path_value: str | Path) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def relative_path(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT).as_posix()


if __name__ == "__main__":
    raise SystemExit(main())
