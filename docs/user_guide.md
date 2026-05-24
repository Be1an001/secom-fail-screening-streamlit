# User Guide

## Live App

Live Streamlit app:

<https://secom-fail-screening.streamlit.app/>

## Local Streamlit Run

From the repository root:

```bash
cd path\to\secom-fail-screening-streamlit
python -m pip install -r requirements.txt
streamlit run app.py
```

Expected local app URL:

<http://localhost:8501>

The app reads committed artifacts from [outputs](../outputs/),
[reports](../reports/), and
[the artifact manifest](../outputs/artifact_manifest.json). It does not train
models at runtime.

## Local Validation Commands

From the repository root:

```bash
cd path\to\secom-fail-screening-streamlit
python -m pip install -r requirements.txt
python -m pytest
python -m ruff check .
python -m compileall app.py app_pages app_utils api src scripts tests
git diff --check
```

If Ruff is not installed in the active environment, install the project
requirements or run the checks in the same environment used for development.

`git diff --check` may show CRLF normalization warnings on Windows. Those
warnings are non-blocking when no whitespace errors are reported.

## Notebook Execution

The notebook is a supporting portfolio summary. The Streamlit app is the
primary public interface.

From the repository root:

```bash
python -m pip install jupyter nbformat nbclient ipykernel
python -m jupyter nbconvert --to notebook --execute notebooks/SECOM_Fail_Screening_Portfolio_Summary.ipynb --inplace
```

This re-executes the portfolio summary notebook and writes the executed
notebook back to
[notebooks/SECOM_Fail_Screening_Portfolio_Summary.ipynb](../notebooks/SECOM_Fail_Screening_Portfolio_Summary.ipynb).

Non-blocking notebook metadata or Windows event-loop warnings may appear during
execution.

## Optional Docker Run

Docker is optional for local review:

```bash
cd path\to\secom-fail-screening-streamlit
docker build -t secom-fail-screening-streamlit:local .
docker run --rm -p 8501:8501 secom-fail-screening-streamlit:local
```

Expected local app URL:

<http://localhost:8501>

See [Docker Usage](docker_usage.md). The Docker setup is not deployment
automation and does not include secrets.

## App Pages

### 1. Overview

This page is the main project opening. It shows a hero summary, KPI cards,
the rare fail class, and a guided workflow story from data problem through
leakage-safe benchmarking, threshold / cost trade-off, explainability, and
artifact-grounded summaries.

Evidence links are kept in a collapsed section near the bottom so the page
stays focused on the portfolio story.

### 2. Benchmark

This page displays the prototype benchmark from
[benchmark_model_comparison_prototype.csv](../outputs/metrics/benchmark_model_comparison_prototype.csv).
All six models remain in the full table.

The display grouping is for readability:

- Main comparison: Logistic + PCA, Random Forest Reference, and XGBoost
  Cost-Sensitive
- Baseline warning: Dummy Majority
- Secondary prototype comparison: LightGBM Weighted and XGBoost +
  Training-only SMOTE

Random Forest Reference currently has the strongest prototype F2. XGBoost
Cost-Sensitive provides a higher-recall option with higher review workload.
This is not a final champion selection.

### 3. Cost Trade-off

The visible page content focuses on threshold and cost trade-offs. Use the
scenario and model controls to inspect selected thresholds from
[cost_selected_thresholds_prototype.csv](../outputs/metrics/cost_selected_thresholds_prototype.csv).

Cost scenarios are illustrative. They show how missed fail cases and review
workload can change the preferred threshold. They are not validated
manufacturing costs and do not create a production decision rule.

### 4. Explainability

This page displays explainability as evidence cards and full-width figures for
readability. It shows prototype permutation importance, feature stability, top
sensor signal tables, and baseline feature importance:

- [permutation_importance_prototype.csv](../outputs/metrics/permutation_importance_prototype.csv)
- [feature_stability_prototype.csv](../outputs/metrics/feature_stability_prototype.csv)
- [top_sensor_signals_prototype.csv](../outputs/metrics/top_sensor_signals_prototype.csv)

The figures summarize model-important sensor signals for Random Forest
Reference and XGBoost Cost-Sensitive:

![Permutation importance](../outputs/figures/permutation_importance_prototype.png)

![Feature stability](../outputs/figures/feature_stability_prototype.png)

These artifacts are not physical root-cause analysis and are not causal proof.
Detailed CSVs and report links are available in collapsed sections.

### 5. API & AI Summary

This page explains artifact tracking, local MLflow summary behavior, the
local/demo FastAPI artifact service, and AI Summary.

The controlled summary panel uses preset questions only. Choose a question and
click `Generate summary`. The app then shows a concise summary with a light
typewriter-style reveal. This is a controlled RAG-lite pattern: preset
questions over compact project artifacts, not free-form chat. Raw CSVs are not
sent to an LLM.

The local FastAPI service is a read-only artifact service. It exposes selected
project artifacts, metrics, reports, and summary endpoints for review or
integration testing. It does not train models or regenerate files.

Near the bottom, the page includes `Extension Concept: Agentic Analytics
Workflow`. This is an architecture extension concept only. It does not claim
LangGraph is implemented and does not perform autonomous decision-making.

## Local API Run

Run the read-only local API:

```bash
cd path\to\secom-fail-screening-streamlit
python -m uvicorn api.main:app --reload
```

Open local API docs:

<http://127.0.0.1:8000/docs>

The API serves JSON from committed artifacts only. It is a local/demo
read-only artifact service, not a production backend. It does not train models
or regenerate artifacts.

## Optional OpenAI Summary Setup

OpenAI summaries are optional. Fallback summaries work without an API key.

For Streamlit Community Cloud, add this TOML in `App settings` -> `Secrets`.
For local testing, use environment variables or a local
`.streamlit/secrets.toml` that is not committed:

```toml
OPENAI_API_KEY = "your-key-here"
OPENAI_SUMMARY_MODEL = "gpt-5.4-mini"
OPENAI_SUMMARY_ENABLED = true
```

Never commit `.streamlit/secrets.toml`, `.env`, or any API key.

Raw CSVs are not sent to the LLM. Summaries use preset questions only, and the
fallback summary works without OpenAI configuration.

## Responsible Use

This project supports screening decision support for a public, anonymous
dataset. It does not make automatic pass/fail decisions, identify physical
root causes, provide causal explanations, or claim SOTA performance.
