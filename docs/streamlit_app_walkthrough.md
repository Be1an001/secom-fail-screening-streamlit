# Streamlit App Walkthrough

## Purpose

This app is an artifact-driven Streamlit app for the UCI SECOM fail-screening benchmark. It presents the current baseline workflow, prototype benchmark artifacts, and threshold / cost trade-off artifacts for screening decision support.

The app does not retrain models at runtime. It reads metrics, figures, reports, and the artifact manifest that already exist in the repository.

## Local Run Command

```bash
streamlit run app.py
```

## Current Pages

- Project & Data Problem
- Model Benchmark
- Champion Trade-off
- Explainability
- MLOps, API, and AI Summary

## What the App Currently Shows

- SECOM dataset size and class imbalance
- current baseline validation metrics
- prototype benchmark model comparison
- prototype threshold sweep availability
- threshold / cost trade-off selected thresholds
- illustrative cost scenario report
- model-important sensor signals from baseline and prototype explainability artifacts
- existing reports and artifact manifest status

## Planned Future Work

Later phases may add final benchmark polish, optional OpenAI API use for
controlled summaries, and a future agentic workflow concept.

These future items are not implemented yet.

## Prototype Benchmark and Cost Views

Page 2 shows the prototype literature-inspired benchmark artifacts from `outputs/metrics/benchmark_model_comparison_prototype.csv`. These results are not final model-selection results.

The Page 2 display groups models for readability while keeping the full six-model benchmark table visible:

- Main comparison: Logistic + PCA, Random Forest Reference, and XGBoost Cost-Sensitive
- Baseline warning: Dummy Majority
- Secondary prototype comparison: LightGBM Weighted and XGBoost + Training-only SMOTE

This display grouping does not remove models from the benchmark and does not create a final champion model.

Page 3 shows selected thresholds from `outputs/metrics/cost_selected_thresholds_prototype.csv`. The cost scenarios are illustrative, are not validated manufacturing costs, and do not create a production decision rule.

The app may describe a row as best under this illustrative scenario, but it does not select a final champion model.

## Prototype Explainability View

Page 4 shows baseline feature importance plus prototype permutation importance,
feature stability, top sensor signal summaries, and explainability figures for
Random Forest Reference and XGBoost Cost-Sensitive.

These outputs describe model-important sensor signals. They are not physical
root-cause analysis and are not causal proof.

## MLOps-Lite and Artifact Tracking View

Page 5 explains that the app is artifact-driven. It uses
`outputs/artifact_manifest.json` as a lightweight artifact registry and reads
committed metrics, figures, and reports instead of local MLflow databases.

Local MLflow tracking can support experiment review when scripts are run
locally. Local files such as `mlflow.db`, `mlruns/`, and `mlartifacts/` are
ignored. The script `scripts/export_mlflow_runs_summary.py` can create an
exported MLflow summary only when real local run data exists.

This is MLOps-lite evidence for a portfolio project. It is not a production
MLOps platform, and no deployed MLflow tracking server is included.

## Local API and Controlled RAG-Lite View

Page 5 now documents the minimal FastAPI artifact service and controlled
RAG-lite summary helper. The local API can be run with:

```bash
uvicorn api.main:app --reload
```

The API is read-only and returns JSON from committed artifacts such as the
manifest, prototype benchmark metrics, selected cost thresholds, top sensor
signals, and Markdown reports.

The controlled RAG-lite summary uses preset questions and compact
artifact-grounded context. It is not a general chatbot, does not accept
arbitrary prompts, and does not send raw SECOM CSV files to an LLM. The fallback
summary works without an OpenAI API key.

## Responsible-Use Note

This project supports screening decision support only. It is not a production deployment, does not make automatic pass/fail decisions, and does not identify physical root causes or causal sensor explanations.
