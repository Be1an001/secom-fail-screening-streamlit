# Scripts Guide

Scripts are run manually to create or inspect artifacts. The Streamlit app and
local API read committed artifacts and do not run these scripts at runtime.
Upgrade method references for benchmark, cost, and explainability scripts are
in [Literature References](../docs/literature_references.md).

## Baseline Experiment Scripts

- [run_rf_experiments.py](run_rf_experiments.py) runs baseline Random Forest
  experiments.
- [evaluate_final_model.py](evaluate_final_model.py) exports baseline holdout
  metrics and figures.
- [export_experiment_summary.py](export_experiment_summary.py) writes baseline
  report content.

## Prototype Benchmark Scripts

- [run_model_benchmark_prototype.py](run_model_benchmark_prototype.py) runs the
  six-model prototype benchmark.
- [run_cost_threshold_analysis_prototype.py](run_cost_threshold_analysis_prototype.py)
  computes illustrative threshold / cost trade-offs from threshold sweep
  artifacts.
- [run_explainability_prototype.py](run_explainability_prototype.py) creates
  permutation importance, feature stability, figures, and the explainability
  report.

## Artifact Tracking Script

- [export_mlflow_runs_summary.py](export_mlflow_runs_summary.py) exports a
  compact MLflow run summary only when real local MLflow data exists.

These scripts should not write secrets or local MLflow databases into the
repository.
