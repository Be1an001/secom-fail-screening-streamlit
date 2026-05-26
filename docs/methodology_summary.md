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

The main modeling challenge is class imbalance. Raw accuracy can look high even
when a model misses fail cases. The project emphasizes fail recall, F2-score,
balanced accuracy, PR-AUC, confusion counts, and flagged sample rate.

The imbalanced metric framing is supported by
[Literature References](literature_references.md).

## Leakage-Safe Preprocessing

The baseline workflow uses:

- stratified train, validation, and test splits
- preprocessing fit on the training split only
- training-only missingness filtering
- median imputation
- separate tree-model and linear-model preprocessing paths

The test split should not be used for model selection, threshold selection, or
tuning.

## Original Baseline Workflow

The first version came from a master's coursework baseline and general public
example learning. It established a practical comparison group:

- dummy majority baseline
- logistic regression with PCA baseline
- Random Forest variants
- validation threshold sweeps
- final holdout evaluation for a validation-selected Random Forest candidate
- local MLflow tracking
- generated metrics, figures, and Markdown reports

These baseline models are kept as comparison references. They are not presented
as direct paper reproductions.

## Evaluation Benchmark

The project compares the original baseline group with later
literature-informed upgrade methods. This wording means the upgrade methods
are motivated by documented approaches. It does not mean the project claims
research-leading performance.

The reference layer is centralized in
[Literature References](literature_references.md). It links the upgraded
benchmark and analysis choices to verified method sources without claiming
paper reproduction.

## Literature-Informed Upgrade Benchmark

The literature-informed benchmark prototype tests fixed, practical upgrade
candidates against the baseline group:

- boosting and ensemble classifiers
- class weighting for severe imbalance
- training-only resampling
- validation threshold sweeps

This is prototype work. It does not claim research-leading performance, does
not select a final champion model, and does not reproduce the cited papers.

The main benchmark table uses the validation split. The final holdout Random
Forest artifact is a separate baseline evaluation artifact and should not be
mixed with the prototype validation benchmark.

## Prototype Model Display Grouping

All six models remain in the prototype benchmark artifacts. The Streamlit app
uses display grouping to make the portfolio story easier to follow:

- baseline group: Dummy Majority, Logistic Regression + PCA, and Random Forest
  Reference
- upgrade group: XGBoost Cost-Sensitive, LightGBM Class-Weighted, and XGBoost +
  Training-only SMOTE
- display grouping: main comparison, baseline warning, and secondary prototype
  comparison roles

This grouping is for readability. It does not remove models from the benchmark
and does not create a final champion model.

## Threshold and Cost Trade-Off

Threshold work explains how lower or higher thresholds affect:

- fail recall
- false positives
- false negatives
- flagged sample rate
- review capacity
- simple cost assumptions

This is framed as screening decision support.

## Prototype Threshold / Cost Trade-Off Analysis

The threshold / cost analysis adds illustrative cost scenarios for the
prototype threshold sweeps. The analysis treats false negatives as missed fail
cases and false positives as added review workload.

The current prototype uses simple false-negative and false-positive cost
assumptions. These assumptions are not production rules or validated
manufacturing economics. They are a practical way to show that the preferred
threshold can change when quality risk and review workload are weighted
differently.

## Explainability

Explainability outputs are described as model-important sensor signals. They
can help reviewers understand which anonymous inputs influenced the model, but
they do not prove physical root cause or causal sensor explanation.

## Prototype Explainability

The explainability artifacts use permutation importance and feature stability
for the main comparison models that best support the portfolio story:

- Random Forest Reference
- XGBoost Cost-Sensitive

These artifacts show model-important sensor signals on the validation split.
They are investigation support for anonymous sensor features. They are not
physical root-cause analysis and are not causal proof. The explainability
wording is aligned with the references in
[Literature References](literature_references.md).

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

The minimal FastAPI artifact service supports local portfolio review. The
service is read-only and returns committed artifacts as JSON. It is not a
production backend and does not run model training or artifact generation.

The controlled RAG-lite summary helper accepts preset question keys only,
builds compact artifact-grounded context, and falls back to deterministic
summaries when OpenAI is unavailable. It does not accept free-form questions,
and raw CSVs are not sent to an LLM.

Optional OpenAI summaries are enabled when `OPENAI_SUMMARY_ENABLED`,
`OPENAI_API_KEY`, and `OPENAI_SUMMARY_MODEL` are configured in Streamlit
secrets or environment variables. The app falls back safely when OpenAI is not
configured or a call fails.

The app does not provide a free-form chatbot, raw CSV upload to an LLM, or an
autonomous agent. The agentic workflow content is an extension concept only.

## Build Process Concept

The repository follows a simple artifact-first workflow:

1. Scripts read the public SECOM files and create reviewed artifacts.
2. The artifact manifest records how metrics, figures, and reports are used.
3. The Streamlit app, local API, and controlled summaries read those artifacts.
4. Tests check schemas, app wiring, API behavior, summary boundaries, and
   public wording.

This keeps model computation separate from app rendering and makes the
portfolio evidence easier to review.

## Limitations and Non-Goals

- The dataset is public and anonymous.
- The fail class is small.
- Current results include baseline workflow artifacts and prototype benchmark
  artifacts.
- Literature-informed upgrade methods do not imply research-leading performance.
- The project is not a production deployment.
- The project does not provide automatic pass/fail decisions.
- The project does not identify physical root causes.
- The project does not include a deployed MLflow tracking server.
- The project does not include a production backend or general chatbot.
