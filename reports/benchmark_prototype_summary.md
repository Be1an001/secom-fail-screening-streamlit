# Benchmark Prototype Summary

This report summarizes a literature-inspired benchmark prototype for
SECOM screening decision support. It is a prototype artifact, not a
final model-selection result and not a research-leading result.
Upgrade method references are summarized in
[Literature References](../docs/literature_references.md).

## Scope

- Uses the public UCI SECOM data files already tracked in the repo.
- Uses stratified train, validation, and reserved test splits.
- Fits missingness filtering, imputation, PCA, and resampling only on
  training data.
- Selects thresholds on validation predictions with a threshold sweep.
- Reserves the test split for later final evaluation work.

## Data Preparation

- Training rows: 939
- Validation rows: 314
- Reserved test rows: 314
- Kept sensor features after missingness filtering: 566
- Dropped sensor features: 24
- PCA components for linear baseline: 157

## Completed Prototype Results

| model_name | threshold | recall | precision | f2 | pr_auc | roc_auc | flagged_sample_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dummy_majority_baseline | 0.0500 | 0.0000 | 0.0000 | 0.0000 | 0.0669 | 0.5000 | 0.0000 |
| logistic_regression_pca_baseline | 0.3050 | 0.3810 | 0.1633 | 0.3008 | 0.1509 | 0.6433 | 0.1561 |
| random_forest_reference | 0.1150 | 0.5714 | 0.1277 | 0.3371 | 0.1143 | 0.6251 | 0.2994 |
| xgboost_cost_sensitive | 0.1150 | 0.6190 | 0.1161 | 0.3316 | 0.1151 | 0.6176 | 0.3567 |
| lightgbm_class_weighted | 0.0850 | 0.1905 | 0.1176 | 0.1695 | 0.1072 | 0.6056 | 0.1083 |
| xgboost_training_only_smote | 0.0500 | 0.6190 | 0.1048 | 0.3125 | 0.1253 | 0.6402 | 0.3949 |

## Baseline and Upgrade Story

Baseline group:

- dummy_majority_baseline
- logistic_regression_pca_baseline
- random_forest_reference

Upgrade group:

- xgboost_cost_sensitive
- lightgbm_class_weighted
- xgboost_training_only_smote

The baseline group came from the original coursework baseline and general
public example learning. The upgrade group contains the later
literature-informed or method-reference-supported comparisons.

## Display Grouping

All six models remain in the benchmark artifacts. The Streamlit app uses
display grouping for readability:

- Main comparison: logistic_regression_pca_baseline, random_forest_reference,
  xgboost_cost_sensitive
- Baseline warning: dummy_majority_baseline
- Secondary prototype comparison: lightgbm_class_weighted,
  xgboost_training_only_smote

This display grouping does not remove models and does not create a final
champion model.

## Skipped or Failed Candidates

No rows.

## Exported Artifacts

- Model comparison:
  [benchmark_model_comparison_prototype.csv](../outputs/metrics/benchmark_model_comparison_prototype.csv)
- Threshold sweep:
  [benchmark_threshold_sweep_prototype.csv](../outputs/metrics/benchmark_threshold_sweep_prototype.csv)
- Threshold sweep rows: 1086

## Limitations

- The benchmark is fixed-parameter prototype work.
- It does not claim research-leading performance or better-than-research results.
- It does not select a final champion model.
- Feature importance and physical root-cause analysis are out of scope.
- The upgrade group applies referenced method families without reproducing
  papers.

## Config

- Selection metric: `f2`
- Benchmark split: `validation`
