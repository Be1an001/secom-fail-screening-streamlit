# Prototype Explainability Report

This report summarizes prototype explainability artifacts for model-important sensor signals in the SECOM fail-screening benchmark.

## Focus Models

- `random_forest_reference`: current strongest prototype F2 reference.
- `xgboost_cost_sensitive`: higher-recall option with higher review workload.

These focus models are useful for the current portfolio story. The other benchmark models remain in the benchmark artifacts.

## Method

- Method: permutation importance on the validation split.
- Scoring: `average_precision`.
- Repeats per model: 5.
- Candidate sensor features per model: 80.
- Stability seeds: 42, 202, 777.
- Split, missingness filtering, imputation, and model fitting are performed without using validation rows for training.
- Candidate sensor features are selected from model-native importance before permutation scoring to keep this prototype runtime practical.

## Data Context

- Training rows: 939
- Explainability split rows: 314
- Reserved test rows: 314
- Kept sensor features: 566
- Dropped sensor features: 24

## Top Model-Important Sensor Signals

| feature | models_where_top | model_count | best_rank | mean_rank |
| --- | --- | --- | --- | --- |
| sensor_091 | random_forest_reference;xgboost_cost_sensitive | 2 | 2 | 2.500 |
| sensor_022 | random_forest_reference;xgboost_cost_sensitive | 2 | 2 | 3.500 |
| sensor_334 | random_forest_reference;xgboost_cost_sensitive | 2 | 3 | 4.500 |
| sensor_060 | random_forest_reference;xgboost_cost_sensitive | 2 | 1 | 5.667 |
| sensor_104 | random_forest_reference;xgboost_cost_sensitive | 2 | 1 | 6.000 |
| sensor_011 | random_forest_reference;xgboost_cost_sensitive | 2 | 7 | 7.000 |
| sensor_337 | random_forest_reference;xgboost_cost_sensitive | 2 | 6 | 7.000 |
| sensor_065 | random_forest_reference;xgboost_cost_sensitive | 2 | 4 | 7.500 |
| sensor_574 | random_forest_reference;xgboost_cost_sensitive | 2 | 6 | 7.500 |
| sensor_034 | random_forest_reference;xgboost_cost_sensitive | 2 | 1 | 8.250 |
| sensor_470 | random_forest_reference;xgboost_cost_sensitive | 2 | 2 | 8.500 |
| sensor_520 | random_forest_reference;xgboost_cost_sensitive | 2 | 6 | 8.500 |

## Feature Stability

- Stable feature rows with appearance rate 1.0: 3
- Stability means the anonymous sensor feature appeared in the top ranked set across configured seeds for the same model.

## Exported Artifacts

- Permutation importance:
  [permutation_importance_prototype.csv](../outputs/metrics/permutation_importance_prototype.csv)
- Feature stability:
  [feature_stability_prototype.csv](../outputs/metrics/feature_stability_prototype.csv)
- Top sensor signals:
  [top_sensor_signals_prototype.csv](../outputs/metrics/top_sensor_signals_prototype.csv)
- Permutation importance figure:
  [permutation_importance_prototype.png](../outputs/figures/permutation_importance_prototype.png)
- Feature stability figure:
  [feature_stability_prototype.png](../outputs/figures/feature_stability_prototype.png)

## Limitations

- Sensor names are anonymous, so these results do not identify process mechanisms.
- This is not physical root-cause analysis.
- These rankings are not causal proof.
- A process engineer could use these signals as investigation support, not as proof.
- This report does not select a final champion model.
- SHAP was not added in this phase to keep the project lightweight.
