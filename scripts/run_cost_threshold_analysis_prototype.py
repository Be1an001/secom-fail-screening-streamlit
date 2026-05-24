"""Run prototype threshold / cost trade-off analysis.

This script consumes the Phase 4 benchmark threshold sweep artifact. It does
not retrain models.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = Path("configs/cost_scenarios_prototype.yaml")
REQUIRED_THRESHOLD_COLUMNS = {
    "model_name",
    "threshold",
    "precision",
    "recall",
    "f2",
    "flagged_sample_rate",
    "tp",
    "fp",
    "fn",
    "tn",
}
COST_SWEEP_COLUMNS = [
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
    "model_group",
    "base_scenario",
    "review_capacity_label",
    "max_flagged_sample_rate",
    "scenario_description",
]
SELECTED_COLUMNS = [
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
    "base_scenario",
    "review_capacity_label",
    "max_flagged_sample_rate",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Calculate prototype threshold / cost trade-offs from the "
            "existing benchmark threshold sweep artifact."
        )
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Path to the cost scenario YAML config.",
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
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    config = load_yaml_config(config_path)
    cost_sweep, selected = run_cost_analysis(config)
    write_outputs(cost_sweep=cost_sweep, selected=selected, config=config)
    print_summary(selected)
    return 0


def run_cost_analysis(config: dict[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame]:
    threshold_sweep = load_threshold_sweep(config)
    scenario_rows = build_scenario_rows(config)
    cost_sweep = build_cost_sweep(
        threshold_sweep=threshold_sweep,
        scenario_rows=scenario_rows,
    )
    selected = select_thresholds(cost_sweep)
    return cost_sweep, selected


def load_threshold_sweep(config: dict[str, Any]) -> pd.DataFrame:
    threshold_path = project_path(
        config.get("inputs", {}).get(
            "threshold_sweep",
            "outputs/metrics/benchmark_threshold_sweep_prototype.csv",
        )
    )
    if not threshold_path.is_file():
        raise FileNotFoundError(f"Threshold sweep artifact not found: {threshold_path}")

    threshold_sweep = pd.read_csv(threshold_path)
    missing = REQUIRED_THRESHOLD_COLUMNS - set(threshold_sweep.columns)
    if missing:
        missing_columns = ", ".join(sorted(missing))
        raise ValueError(f"Threshold sweep is missing columns: {missing_columns}")

    numeric_columns = [
        "threshold",
        "precision",
        "recall",
        "f2",
        "flagged_sample_rate",
        "tp",
        "fp",
        "fn",
        "tn",
    ]
    threshold_sweep[numeric_columns] = threshold_sweep[numeric_columns].apply(
        pd.to_numeric,
        errors="raise",
    )
    return threshold_sweep


def build_scenario_rows(config: dict[str, Any]) -> list[dict[str, Any]]:
    scenario_rows: list[dict[str, Any]] = []
    scenarios = config.get("scenarios", {})
    review_limits = config.get("review_capacity_limits", {})

    for scenario_name, scenario_config in scenarios.items():
        base_row = {
            "scenario": scenario_name,
            "base_scenario": scenario_name,
            "false_negative_cost": float(scenario_config["false_negative_cost"]),
            "false_positive_cost": float(scenario_config["false_positive_cost"]),
            "review_capacity_label": "none",
            "max_flagged_sample_rate": None,
            "scenario_description": str(scenario_config.get("description", "")),
        }
        scenario_rows.append(base_row)

        for capacity_name, capacity_config in review_limits.items():
            scenario_rows.append(
                {
                    **base_row,
                    "scenario": f"{scenario_name}__{capacity_name}",
                    "review_capacity_label": capacity_name,
                    "max_flagged_sample_rate": float(
                        capacity_config["max_flagged_sample_rate"]
                    ),
                    "scenario_description": (
                        f"{base_row['scenario_description']} "
                        f"Capacity limit: {capacity_config.get('description', '')}"
                    ).strip(),
                }
            )

    if not scenario_rows:
        raise ValueError("At least one cost scenario is required.")
    return scenario_rows


def build_cost_sweep(
    threshold_sweep: pd.DataFrame,
    scenario_rows: list[dict[str, Any]],
) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for scenario in scenario_rows:
        frame = threshold_sweep.copy()
        total_samples = frame[["tp", "fp", "fn", "tn"]].sum(axis=1)
        total_cost = (
            float(scenario["false_negative_cost"]) * frame["fn"]
            + float(scenario["false_positive_cost"]) * frame["fp"]
        )
        frame["scenario"] = scenario["scenario"]
        frame["false_negative_cost"] = scenario["false_negative_cost"]
        frame["false_positive_cost"] = scenario["false_positive_cost"]
        frame["total_cost"] = total_cost
        frame["cost_per_sample"] = total_cost / total_samples
        frame["base_scenario"] = scenario["base_scenario"]
        frame["review_capacity_label"] = scenario["review_capacity_label"]
        frame["max_flagged_sample_rate"] = scenario["max_flagged_sample_rate"]
        frame["scenario_description"] = scenario["scenario_description"]
        frames.append(frame)

    cost_sweep = pd.concat(frames, ignore_index=True)
    return cost_sweep.loc[:, COST_SWEEP_COLUMNS]


def select_thresholds(cost_sweep: pd.DataFrame) -> pd.DataFrame:
    selected_rows: list[dict[str, Any]] = []
    for (model_name, scenario), group in cost_sweep.groupby(
        ["model_name", "scenario"],
        sort=True,
    ):
        candidate_rows = group.copy()
        max_flagged = candidate_rows["max_flagged_sample_rate"].iloc[0]
        if pd.notna(max_flagged):
            candidate_rows = candidate_rows[
                candidate_rows["flagged_sample_rate"] <= float(max_flagged)
            ].copy()

        if candidate_rows.empty:
            selected_rows.append(empty_selection_row(group.iloc[0]))
            continue

        ranked = candidate_rows.sort_values(
            by=["total_cost", "fn", "flagged_sample_rate", "threshold"],
            ascending=[True, True, True, True],
            kind="mergesort",
        )
        selected = ranked.iloc[0]
        selected_rows.append(selection_row(selected))

    selected = pd.DataFrame(selected_rows, columns=SELECTED_COLUMNS)
    return selected


def selection_row(row: pd.Series) -> dict[str, Any]:
    max_flagged = row["max_flagged_sample_rate"]
    capacity_note = ""
    if pd.notna(max_flagged):
        capacity_note = (
            f" under max flagged sample rate {float(max_flagged):.2f}"
        )

    return {
        "model_name": row["model_name"],
        "scenario": row["scenario"],
        "selected_threshold": row["threshold"],
        "total_cost": row["total_cost"],
        "cost_per_sample": row["cost_per_sample"],
        "recall": row["recall"],
        "precision": row["precision"],
        "f2": row["f2"],
        "flagged_sample_rate": row["flagged_sample_rate"],
        "tp": int(row["tp"]),
        "fp": int(row["fp"]),
        "fn": int(row["fn"]),
        "tn": int(row["tn"]),
        "notes": f"Best under this illustrative scenario{capacity_note}.",
        "base_scenario": row["base_scenario"],
        "review_capacity_label": row["review_capacity_label"],
        "max_flagged_sample_rate": row["max_flagged_sample_rate"],
    }


def empty_selection_row(row: pd.Series) -> dict[str, Any]:
    return {
        "model_name": row["model_name"],
        "scenario": row["scenario"],
        "selected_threshold": None,
        "total_cost": None,
        "cost_per_sample": None,
        "recall": None,
        "precision": None,
        "f2": None,
        "flagged_sample_rate": None,
        "tp": None,
        "fp": None,
        "fn": None,
        "tn": None,
        "notes": "No threshold met the review-capacity constraint.",
        "base_scenario": row["base_scenario"],
        "review_capacity_label": row["review_capacity_label"],
        "max_flagged_sample_rate": row["max_flagged_sample_rate"],
    }


def write_outputs(
    cost_sweep: pd.DataFrame,
    selected: pd.DataFrame,
    config: dict[str, Any],
) -> None:
    outputs = config.get("outputs", {})
    cost_sweep_path = project_path(
        outputs.get(
            "cost_threshold_sweep",
            "outputs/metrics/cost_threshold_sweep_prototype.csv",
        )
    )
    selected_path = project_path(
        outputs.get(
            "selected_thresholds",
            "outputs/metrics/cost_selected_thresholds_prototype.csv",
        )
    )
    report_path = project_path(
        outputs.get("report", "reports/cost_threshold_prototype_report.md")
    )

    cost_sweep_path.parent.mkdir(parents=True, exist_ok=True)
    selected_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    cost_sweep.to_csv(cost_sweep_path, index=False)
    selected.to_csv(selected_path, index=False)
    report_path.write_text(
        build_report(
            selected=selected,
            cost_sweep=cost_sweep,
            cost_sweep_path=cost_sweep_path,
            selected_path=selected_path,
        ),
        encoding="utf-8",
    )


def build_report(
    selected: pd.DataFrame,
    cost_sweep: pd.DataFrame,
    cost_sweep_path: Path,
    selected_path: Path,
) -> str:
    cost_only = selected[selected["review_capacity_label"] == "none"].copy()
    constrained = selected[selected["review_capacity_label"] != "none"].copy()

    lines = [
        "# Prototype Threshold / Cost Trade-Off Report",
        "",
        "This report summarizes a prototype threshold analysis for SECOM ",
        "screening decision support. It uses existing Phase 4 threshold sweep ",
        "artifacts and does not retrain models.",
        "",
        "## Interpretation Notes",
        "",
        "- Threshold is a decision lever, not an automatic pass/fail decision.",
        "- False negatives are missed fail cases.",
        "- False positives are pass cases flagged for extra review workload.",
        "- Cost assumptions are illustrative and can change the preferred threshold.",
        "- High recall can require a high flagged sample rate.",
        "- No threshold in this report is a production decision rule.",
        "",
        "## Cost Formula",
        "",
        "`total_cost = false_negative_cost * fn + false_positive_cost * fp`",
        "",
        "`cost_per_sample = total_cost / validation_samples`",
        "",
        "## Cost-Only Selected Thresholds",
        "",
        markdown_table(
            cost_only,
            [
                "model_name",
                "scenario",
                "selected_threshold",
                "total_cost",
                "recall",
                "precision",
                "f2",
                "flagged_sample_rate",
            ],
        ),
        "",
        "## Review-Capacity Constrained Selected Thresholds",
        "",
        markdown_table(
            constrained,
            [
                "model_name",
                "scenario",
                "selected_threshold",
                "total_cost",
                "recall",
                "precision",
                "f2",
                "flagged_sample_rate",
            ],
        ),
        "",
        "## Exported Artifacts",
        "",
        f"- Cost threshold sweep: `{relative_path(cost_sweep_path)}`",
        f"- Selected thresholds: `{relative_path(selected_path)}`",
        f"- Cost threshold sweep rows: {len(cost_sweep)}",
        f"- Selected threshold rows: {len(selected)}",
        "",
        "## Caution",
        "",
        "A model can be best under this illustrative scenario while still being ",
        "too costly for a real review workflow. Additional review can compare ",
        "these scenarios with clearer review-capacity and quality assumptions.",
    ]
    return "\n".join(lines).replace(" \n", "\n")


def print_summary(selected: pd.DataFrame) -> None:
    columns = [
        "model_name",
        "scenario",
        "selected_threshold",
        "total_cost",
        "recall",
        "precision",
        "f2",
        "flagged_sample_rate",
    ]
    print("Prototype cost-selected thresholds:")
    print(selected.loc[:, columns].to_string(index=False))


def markdown_table(data: pd.DataFrame, columns: list[str]) -> str:
    if data.empty:
        return "No rows."

    rows = []
    for _index, row in data.loc[:, columns].iterrows():
        rows.append([format_value(row[column]) for column in columns])

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _column in columns) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def format_value(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    if isinstance(value, float):
        if math.isnan(value):
            return ""
        return f"{value:.4f}"
    return str(value)


def project_path(path_value: str | Path) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def relative_path(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT).as_posix()


if __name__ == "__main__":
    raise SystemExit(main())
