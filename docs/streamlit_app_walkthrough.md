# Streamlit App Walkthrough

## Purpose

This app is an artifact-driven Streamlit app for the UCI SECOM fail-screening benchmark. It presents the current baseline workflow and existing baseline artifacts for screening decision support.

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
- final holdout threshold metrics
- threshold sweep artifact preview
- model-important sensor signals
- existing reports and artifact manifest status

## Planned Future Work

Later phases may add a planned literature-inspired upgrade, SOTA-inspired methods as a future method direction, cost threshold views, richer explainability artifacts, a minimal FastAPI artifact service, a future controlled RAG-lite summary, and a future agentic workflow concept.

These future items are not implemented yet.

## Responsible-Use Note

This project supports screening decision support only. It is not a production deployment, does not make automatic pass/fail decisions, and does not identify physical root causes or causal sensor explanations.
