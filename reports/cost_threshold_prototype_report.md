# Prototype Threshold / Cost Trade-Off Report

This report summarizes a prototype threshold analysis for SECOM
screening decision support. It uses existing Phase 4 threshold sweep
artifacts and does not retrain models.

## Interpretation Notes

- Threshold is a decision lever, not an automatic pass/fail decision.
- False negatives are missed fail cases.
- False positives are pass cases flagged for extra review workload.
- Cost assumptions are illustrative and can change the preferred threshold.
- High recall can require a high flagged sample rate.
- No threshold in this report is a production decision rule.

## Cost Formula

`total_cost = false_negative_cost * fn + false_positive_cost * fp`

`cost_per_sample = total_cost / validation_samples`

## Cost-Only Selected Thresholds

| model_name | scenario | selected_threshold | total_cost | recall | precision | f2 | flagged_sample_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dummy_majority_baseline | balanced_review | 0.0500 | 105.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| dummy_majority_baseline | quality_first | 0.0500 | 210.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| dummy_majority_baseline | strict_quality | 0.0500 | 420.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| lightgbm_class_weighted | balanced_review | 0.1500 | 101.0000 | 0.1429 | 0.2143 | 0.1531 | 0.0446 |
| lightgbm_class_weighted | quality_first | 0.1500 | 191.0000 | 0.1429 | 0.2143 | 0.1531 | 0.0446 |
| lightgbm_class_weighted | strict_quality | 0.0850 | 370.0000 | 0.1905 | 0.1176 | 0.1695 | 0.1083 |
| logistic_regression_pca_baseline | balanced_review | 0.6550 | 100.0000 | 0.3333 | 0.1892 | 0.2893 | 0.1178 |
| logistic_regression_pca_baseline | quality_first | 0.6550 | 170.0000 | 0.3333 | 0.1892 | 0.2893 | 0.1178 |
| logistic_regression_pca_baseline | strict_quality | 0.3050 | 301.0000 | 0.3810 | 0.1633 | 0.3008 | 0.1561 |
| random_forest_reference | balanced_review | 0.2250 | 104.0000 | 0.0952 | 0.1818 | 0.1053 | 0.0350 |
| random_forest_reference | quality_first | 0.1150 | 172.0000 | 0.5714 | 0.1277 | 0.3371 | 0.2994 |
| random_forest_reference | strict_quality | 0.1150 | 262.0000 | 0.5714 | 0.1277 | 0.3371 | 0.2994 |
| xgboost_cost_sensitive | balanced_review | 0.4000 | 104.0000 | 0.0952 | 0.1818 | 0.1053 | 0.0350 |
| xgboost_cost_sensitive | quality_first | 0.1150 | 179.0000 | 0.6190 | 0.1161 | 0.3316 | 0.3567 |
| xgboost_cost_sensitive | strict_quality | 0.1000 | 256.0000 | 0.6667 | 0.1077 | 0.3271 | 0.4140 |
| xgboost_training_only_smote | balanced_review | 0.4300 | 100.0000 | 0.1429 | 0.2308 | 0.1546 | 0.0414 |
| xgboost_training_only_smote | quality_first | 0.1650 | 174.0000 | 0.3333 | 0.1707 | 0.2800 | 0.1306 |
| xgboost_training_only_smote | strict_quality | 0.0500 | 271.0000 | 0.6190 | 0.1048 | 0.3125 | 0.3949 |

## Review-Capacity Constrained Selected Thresholds

| model_name | scenario | selected_threshold | total_cost | recall | precision | f2 | flagged_sample_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dummy_majority_baseline | balanced_review__high_review | 0.0500 | 105.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| dummy_majority_baseline | balanced_review__moderate_review | 0.0500 | 105.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| dummy_majority_baseline | quality_first__high_review | 0.0500 | 210.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| dummy_majority_baseline | quality_first__moderate_review | 0.0500 | 210.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| dummy_majority_baseline | strict_quality__high_review | 0.0500 | 420.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| dummy_majority_baseline | strict_quality__moderate_review | 0.0500 | 420.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| lightgbm_class_weighted | balanced_review__high_review | 0.1500 | 101.0000 | 0.1429 | 0.2143 | 0.1531 | 0.0446 |
| lightgbm_class_weighted | balanced_review__moderate_review | 0.1500 | 101.0000 | 0.1429 | 0.2143 | 0.1531 | 0.0446 |
| lightgbm_class_weighted | quality_first__high_review | 0.1500 | 191.0000 | 0.1429 | 0.2143 | 0.1531 | 0.0446 |
| lightgbm_class_weighted | quality_first__moderate_review | 0.1500 | 191.0000 | 0.1429 | 0.2143 | 0.1531 | 0.0446 |
| lightgbm_class_weighted | strict_quality__high_review | 0.0850 | 370.0000 | 0.1905 | 0.1176 | 0.1695 | 0.1083 |
| lightgbm_class_weighted | strict_quality__moderate_review | 0.0850 | 370.0000 | 0.1905 | 0.1176 | 0.1695 | 0.1083 |
| logistic_regression_pca_baseline | balanced_review__high_review | 0.6550 | 100.0000 | 0.3333 | 0.1892 | 0.2893 | 0.1178 |
| logistic_regression_pca_baseline | balanced_review__moderate_review | 0.6550 | 100.0000 | 0.3333 | 0.1892 | 0.2893 | 0.1178 |
| logistic_regression_pca_baseline | quality_first__high_review | 0.6550 | 170.0000 | 0.3333 | 0.1892 | 0.2893 | 0.1178 |
| logistic_regression_pca_baseline | quality_first__moderate_review | 0.6550 | 170.0000 | 0.3333 | 0.1892 | 0.2893 | 0.1178 |
| logistic_regression_pca_baseline | strict_quality__high_review | 0.3050 | 301.0000 | 0.3810 | 0.1633 | 0.3008 | 0.1561 |
| logistic_regression_pca_baseline | strict_quality__moderate_review | 0.3050 | 301.0000 | 0.3810 | 0.1633 | 0.3008 | 0.1561 |
| random_forest_reference | balanced_review__high_review | 0.2250 | 104.0000 | 0.0952 | 0.1818 | 0.1053 | 0.0350 |
| random_forest_reference | balanced_review__moderate_review | 0.2250 | 104.0000 | 0.0952 | 0.1818 | 0.1053 | 0.0350 |
| random_forest_reference | quality_first__high_review | 0.1150 | 172.0000 | 0.5714 | 0.1277 | 0.3371 | 0.2994 |
| random_forest_reference | quality_first__moderate_review | 0.1150 | 172.0000 | 0.5714 | 0.1277 | 0.3371 | 0.2994 |
| random_forest_reference | strict_quality__high_review | 0.1150 | 262.0000 | 0.5714 | 0.1277 | 0.3371 | 0.2994 |
| random_forest_reference | strict_quality__moderate_review | 0.1150 | 262.0000 | 0.5714 | 0.1277 | 0.3371 | 0.2994 |
| xgboost_cost_sensitive | balanced_review__high_review | 0.4000 | 104.0000 | 0.0952 | 0.1818 | 0.1053 | 0.0350 |
| xgboost_cost_sensitive | balanced_review__moderate_review | 0.4000 | 104.0000 | 0.0952 | 0.1818 | 0.1053 | 0.0350 |
| xgboost_cost_sensitive | quality_first__high_review | 0.1150 | 179.0000 | 0.6190 | 0.1161 | 0.3316 | 0.3567 |
| xgboost_cost_sensitive | quality_first__moderate_review | 0.2900 | 188.0000 | 0.2381 | 0.1515 | 0.2137 | 0.1051 |
| xgboost_cost_sensitive | strict_quality__high_review | 0.1150 | 259.0000 | 0.6190 | 0.1161 | 0.3316 | 0.3567 |
| xgboost_cost_sensitive | strict_quality__moderate_review | 0.1550 | 312.0000 | 0.4286 | 0.1111 | 0.2727 | 0.2580 |
| xgboost_training_only_smote | balanced_review__high_review | 0.4300 | 100.0000 | 0.1429 | 0.2308 | 0.1546 | 0.0414 |
| xgboost_training_only_smote | balanced_review__moderate_review | 0.4300 | 100.0000 | 0.1429 | 0.2308 | 0.1546 | 0.0414 |
| xgboost_training_only_smote | quality_first__high_review | 0.1650 | 174.0000 | 0.3333 | 0.1707 | 0.2800 | 0.1306 |
| xgboost_training_only_smote | quality_first__moderate_review | 0.1650 | 174.0000 | 0.3333 | 0.1707 | 0.2800 | 0.1306 |
| xgboost_training_only_smote | strict_quality__high_review | 0.0500 | 271.0000 | 0.6190 | 0.1048 | 0.3125 | 0.3949 |
| xgboost_training_only_smote | strict_quality__moderate_review | 0.0800 | 314.0000 | 0.4286 | 0.1084 | 0.2695 | 0.2643 |

## Exported Artifacts

- Cost threshold sweep: `outputs/metrics/cost_threshold_sweep_prototype.csv`
- Selected thresholds: `outputs/metrics/cost_selected_thresholds_prototype.csv`
- Cost threshold sweep rows: 9774
- Selected threshold rows: 54

## Caution

A model can be best under this illustrative scenario while still being
too costly for a real review workflow. Future phases should compare
these scenarios with clearer review-capacity and quality assumptions.