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

## Literature-Inspired Benchmark Prototype

Phase 4 adds a literature-inspired benchmark prototype. It tests fixed, practical model candidates that reflect common SECOM method directions:

- high-dimensional sensor preprocessing
- class weighting for severe imbalance
- boosting and ensemble classifiers
- training-only resampling
- validation threshold sweeps

This is prototype work. It does not claim SOTA performance, does not select a final champion model, and does not replace a later formal paper review.

## Prototype Model Display Grouping

All six models remain in the prototype benchmark artifacts. The Streamlit app
uses display grouping to make the portfolio story easier to follow:

- main comparison models for the classical baseline, Random Forest reference,
  and cost-sensitive XGBoost option
- a baseline warning model to show why accuracy alone is misleading
- secondary prototype comparison models for LightGBM and training-only SMOTE

This grouping is for readability. It does not remove models from the benchmark
and does not create a final champion model.

## Threshold and Cost Trade-Off

Threshold work should explain how lower or higher thresholds affect:

- fail recall
- false positives
- false negatives
- flagged sample rate
- review capacity
- simple cost assumptions

This should be framed as screening decision support.

## Prototype Threshold / Cost Trade-Off Analysis

Phase 5 adds illustrative cost scenarios for the Phase 4 prototype threshold
sweeps. The analysis treats false negatives as missed fail cases and false
positives as added review workload.

The current prototype uses simple false-negative and false-positive cost
assumptions. These assumptions are not production rules. They are a practical
way to show that the preferred threshold can change when quality risk and
review workload are weighted differently.

## Explainability

Explainability outputs should be described as model-important sensor signals. They can help reviewers understand which anonymous inputs influenced the model, but they do not prove physical root cause or causal sensor explanation.

## Prototype Explainability

Phase 7 adds permutation importance and feature stability artifacts for the
main comparison models that best support the current portfolio story:

- Random Forest Reference
- XGBoost Cost-Sensitive

These artifacts show model-important sensor signals on the validation split.
They are investigation support for anonymous sensor features. They are not
physical root-cause analysis and are not causal proof.

## MLOps-Lite Artifact Tracking

The Streamlit app is artifact-driven. It reads curated metrics, figures,
reports, and `outputs/artifact_manifest.json` instead of running training or
MLflow queries at app runtime.

Local MLflow tracking can support experiment review when scripts are run
locally. Local MLflow files such as `mlflow.db`, `mlruns/`, and `mlartifacts/`
are ignored. A compact exported MLflow summary may be generated only when real
local MLflow run data exists. This is portfolio-scale artifact tracking, not a
production MLOps platform.

## Minimal API and Controlled RAG-Lite Summary

Phase 9 adds a minimal FastAPI artifact service for local portfolio review. The
service is read-only and returns committed artifacts as JSON. It is not a
production backend and does not run model training or artifact generation.

Phase 9 also adds a controlled RAG-lite summary helper. It accepts preset
question keys only, builds compact artifact-grounded context, and falls back to
deterministic summaries when OpenAI is unavailable. It does not accept
free-form prompts, and raw CSVs are not sent to an LLM.

Phase 9.5 enables optional OpenAI summaries when `OPENAI_SUMMARY_ENABLED`,
`OPENAI_API_KEY`, and `OPENAI_SUMMARY_MODEL` are configured in Streamlit
secrets or environment variables. The app falls back safely when OpenAI is not
configured or a call fails.

## Limitations and Non-Goals

- The dataset is public and anonymous.
- The fail class is small.
- Current results are based on a baseline workflow.
- Future SOTA-inspired methods do not imply SOTA performance.
- The project is not a production deployment.
- The project does not provide automatic pass/fail decisions.
- The project does not identify physical root causes.
- The project does not include a deployed MLflow tracking server.
- The project does not include a production backend or general chatbot.
