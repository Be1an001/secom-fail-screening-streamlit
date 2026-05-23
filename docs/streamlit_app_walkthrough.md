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
- model-important sensor signals
- existing reports and artifact manifest status

## Planned Future Work

Later phases may add richer explainability artifacts, final benchmark polish, a minimal FastAPI artifact service, a future controlled RAG-lite summary, and a future agentic workflow concept.

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

## Responsible-Use Note

This project supports screening decision support only. It is not a production deployment, does not make automatic pass/fail decisions, and does not identify physical root causes or causal sensor explanations.
