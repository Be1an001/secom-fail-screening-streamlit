# Project Summary

This project is an artifact-driven Streamlit portfolio app for the UCI SECOM
semiconductor fail-screening problem. It is best understood as an applied
machine learning decision-support project, not a production manufacturing
system.

The business problem is rare-fail screening. Sensor measurements may help flag
units that deserve extra review, but fail cases are uncommon and raw accuracy
can be misleading. The app helps reviewers compare benchmark results,
threshold trade-offs, cost assumptions, and model-important anonymous sensor
signals.

Technical stack:

- Python, pandas, and scikit-learn
- XGBoost, LightGBM, and imbalanced-learn for prototype comparisons
- Streamlit for the portfolio app
- FastAPI for a local read-only artifact service
- MLflow for local experiment tracking
- optional OpenAI summaries with preset questions and compact project artifacts
- optional Docker packaging for local Streamlit review
- pytest, Ruff, and GitHub Actions for validation

The baseline group came from the original master's coursework version and
general public example learning. The upgraded benchmark and analysis methods
are supported by [Literature References](literature_references.md). The
references support method choices, not paper reproduction claims.

Main result interpretation:

- Random Forest Reference currently has the strongest prototype F2.
- XGBoost Cost-Sensitive provides a higher-recall option with higher review
  workload.
- Dummy Majority shows why accuracy alone is misleading.
- Cost scenarios are illustrative and not validated manufacturing costs.
- Explainability artifacts identify model-important sensor signals, not
  physical causes.

My contribution was to package the baseline workflow and later upgrades into a
reviewable data product: Streamlit pages, committed artifacts, reports,
schema tests, local API endpoints, controlled AI Summary behavior, Docker
local packaging, and public documentation.

The app uses a light portfolio-style interface with a guided overview
workflow, benchmark grouping, threshold / cost trade-offs, vertical
explainability figures, artifact tracking, local API usage, and controlled AI
Summary. It demonstrates practical ML workflow design, honest model
evaluation, artifact-driven app development, responsible AI boundaries, and
clear portfolio communication.

This project does not claim production use, automatic decision-making,
physical root cause, causal explanation, or research-leading performance.
