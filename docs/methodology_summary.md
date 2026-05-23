# Methodology Summary

## Dataset Summary

The project uses the public UCI SECOM dataset. The current loader reads:

- 1,567 rows
- 590 anonymous sensor features from `secom.data`
- pass/fail labels and timestamps from `secom_labels.data`
- raw label `-1` as pass class `0`
- raw label `1` as fail class `1`

The fail class is small, with 104 fail samples in the full dataset.

## Class Imbalance Framing

The main modeling challenge is class imbalance. Raw accuracy can look high even when a model misses fail cases. The project should emphasize fail recall, F2-score, balanced accuracy, PR-AUC, confusion counts, and flagged sample rate.

## Leakage-Safe Preprocessing

The baseline workflow uses:

- stratified train, validation, and test splits
- preprocessing fit on the training split only
- training-only missingness filtering
- median imputation
- separate tree-model and linear-model preprocessing paths

The test split should not be used for model selection, threshold selection, or tuning.

## Current Baseline Workflow

The current repository implements:

- dummy majority baseline
- logistic regression with PCA baseline
- Random Forest variants
- validation threshold sweeps
- final holdout evaluation for a validation-selected Random Forest candidate
- local MLflow tracking
- generated metrics, figures, and Markdown reports

## Planned Upgrade Direction

Future phases should add literature-inspired methods and SOTA-inspired methods for a broader fail-screening benchmark. This wording means the methods are motivated by documented approaches, not that the project achieves SOTA performance.

Do not add paper claims or citations until the relevant sources are actually reviewed and documented.

## Threshold and Cost Trade-Off

Future threshold work should explain how lower or higher thresholds affect:

- fail recall
- false positives
- false negatives
- flagged sample rate
- review capacity
- simple cost assumptions

This should be framed as screening decision support.

## Explainability

Explainability outputs should be described as model-important sensor signals. They can help reviewers understand which anonymous inputs influenced the model, but they do not prove physical root cause or causal sensor explanation.

## Limitations and Non-Goals

- The dataset is public and anonymous.
- The fail class is small.
- Current results are based on a baseline workflow.
- Future SOTA-inspired methods do not imply SOTA performance.
- The project is not a production deployment.
- The project does not provide automatic pass/fail decisions.
- The project does not identify physical root causes.
