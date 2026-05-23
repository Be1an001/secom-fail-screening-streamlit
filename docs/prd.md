# Product Requirements Document

## Project Goal

Build a master's-graduate-level portfolio project for the UCI SECOM semiconductor fail-screening problem. The final project should present a clear fail-screening benchmark and screening decision support story through an artifact-driven Streamlit app.

The current repository contains a baseline workflow. Future phases will upgrade it with broader model comparison, threshold trade-off analysis, explainability artifacts, MLOps-lite evidence, and a small app/API layer.

## Target Audience

- Data science and machine learning reviewers
- Portfolio reviewers and hiring teams
- Technical reviewers who value careful methodology and honest limitations

## User Stories

- As a reviewer, I want to understand the SECOM problem, class imbalance, and why raw accuracy is misleading.
- As a reviewer, I want to see leakage-safe preprocessing and a reproducible baseline workflow.
- As a reviewer, I want to compare baseline models and future literature-inspired methods.
- As a reviewer, I want to inspect the champion model threshold and cost trade-off.
- As a reviewer, I want explainability framed as model-important sensor signals.
- As a reviewer, I want generated artifacts, validation evidence, and limitations to be easy to find.

## Planned App Pages

1. Project overview and responsible-use note
2. Data and class imbalance
3. Fail-screening benchmark
4. Threshold and cost trade-off
5. Explainability and MLOps-lite evidence

Later phases may add a controlled RAG-lite summary page if it can remain artifact-grounded and clearly bounded.

## Core Features

- Baseline workflow summary
- Six-model benchmark table
- Champion threshold view
- Cost or review-capacity trade-off view
- Model-important sensor signal view
- Artifact manifest and evidence links
- MLOps-lite run summary
- Minimal FastAPI artifact service
- Controlled RAG-lite summary as an optional app feature

## Non-Goals

- No production deployment claim
- No automatic pass/fail decision
- No physical root cause claim
- No causal sensor explanation
- No full enterprise MLOps platform
- No SOTA performance claim
- No claim of being better than existing research

## Responsible-Use Constraints

The project should be described as screening decision support for a public, anonymous dataset. Any model output should be framed as a screening signal that would require domain review before real operational use.

## Success Criteria

- The app explains the problem and class imbalance clearly.
- The benchmark is reproducible from scripts and artifacts.
- The methodology separates training, validation, threshold selection, and test evaluation.
- The README and docs use cautious wording.
- The app loads artifacts instead of retraining at runtime.
- Tests and validation commands are documented.

## Baseline vs Future Upgrade

Current baseline workflow:

- Public SECOM data loading
- Leakage-aware split and preprocessing
- Dummy, logistic regression, and Random Forest comparisons
- Validation threshold selection
- Final holdout evaluation
- Local MLflow tracking

Future upgrade direction:

- Literature-inspired methods
- SOTA-inspired methods
- Six-model benchmark
- Cost-aware threshold view
- Explainability artifacts
- Artifact-driven Streamlit app
- Minimal FastAPI artifact service
- Controlled RAG-lite summary
