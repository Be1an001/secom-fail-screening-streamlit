# Technical Design Document

## Current Architecture

The repository is an artifact-driven portfolio app supported by reproducible
scripts and lightweight service boundaries:

- [data](../data/): public SECOM raw files
- [src/secom_ml](../src/secom_ml/): reusable data, split, preprocessing, model, metric,
  threshold, plot, and tracking helpers
- [scripts](../scripts/): benchmark, cost, explainability, report, and MLflow summary
  export scripts
- [configs](../configs/): experiment, benchmark, cost, and explainability settings
- [outputs](../outputs/): reviewed metrics, figures, and
  [artifact_manifest.json](../outputs/artifact_manifest.json)
- [reports](../reports/): generated and hand-reviewed Markdown reports
- [app.py](../app.py), [app_pages](../app_pages/), and
  [app_utils](../app_utils/): artifact-driven Streamlit app
- [api](../api/): minimal read-only FastAPI artifact service
- [Dockerfile](../Dockerfile): optional local Streamlit container packaging
- [tests](../tests/): unit, schema, app smoke, API, and RAG-lite tests

## Target Architecture

The target architecture is intentionally portfolio-scale:

- Training and analysis scripts create reviewed artifacts.
- A manifest describes artifact paths, meanings, and app usage.
- The Streamlit app loads artifacts and renders them.
- The FastAPI service exposes selected committed artifacts as JSON.
- The controlled RAG-lite summary answers preset questions from compact
  artifact-grounded context.
- Optional OpenAI summaries are enabled only when secrets or environment
  variables are configured.

No app or API runtime should retrain models, regenerate artifacts, or require
raw data upload.

## Data and Artifact Flow

1. Scripts read the public SECOM files from [data](../data/).
2. Scripts use settings from [configs](../configs/) and helpers from
   [src/secom_ml](../src/secom_ml/).
3. Reviewed metrics and figures are written to [outputs](../outputs/).
4. Markdown reports are written to [reports](../reports/).
5. [outputs/artifact_manifest.json](../outputs/artifact_manifest.json)
   describes app-facing artifacts.
6. The Streamlit app, local API, and controlled summaries read the committed
   artifacts.

## Artifact-Driven Streamlit Design

The Streamlit app loads:

- dataset and baseline workflow summaries
- prototype benchmark metrics
- threshold and cost trade-off outputs
- prototype explainability artifacts
- report summaries
- artifact manifest entries
- optional exported MLflow summaries if real local run data exists

The app presents screening decision support, not an automatic pass/fail
decision.

The app uses a light portfolio theme defined in
[.streamlit/config.toml](../.streamlit/config.toml) plus small shared layout
helpers. Page content is organized with hero sections, KPI cards, compact
tables, calm scope notes, full-width explainability figures, and collapsed
evidence links. The Overview page uses a guided workflow story for interview
review. The UI layer does not change metrics, artifacts, API behavior, or
model outputs.

## Six-Model Prototype Benchmark

The current prototype benchmark keeps all six models in artifacts:

- dummy majority baseline
- logistic regression with PCA baseline
- Random Forest reference
- XGBoost cost-sensitive model
- LightGBM class-weighted model
- XGBoost with training-only SMOTE

The app groups these models for readability. The grouping does not remove
models from the benchmark and does not create a final champion model.

## Threshold and Cost Trade-Off

The cost analysis consumes existing threshold sweep artifacts and computes:

- recall
- precision
- F2
- false positives
- false negatives
- flagged sample rate
- illustrative total cost and cost per sample

Cost scenarios are illustrative. They are not validated manufacturing costs and
do not create a production decision rule.

## Explainability

Prototype explainability uses permutation importance and feature stability for
the main comparison models:

- Random Forest Reference
- XGBoost Cost-Sensitive

These outputs are model-important sensor signals for anonymous sensor features.
They are not physical root-cause analysis and not causal proof.

## Artifact Manifest

`outputs/artifact_manifest.json` acts as a lightweight artifact registry. Each
entry describes the artifact path, type, creator, intended app use, current
status, and expected use.

The manifest tracks baseline, prototype benchmark, threshold / cost,
explainability, report, and app-support artifacts.

## FastAPI Boundary

The FastAPI service is minimal and read-only. It serves selected committed
artifacts, metrics, reports, and summary endpoints through local endpoints
such as:

- `/health`
- `/manifest`
- `/metrics/benchmark`
- `/metrics/cost-selected-thresholds`
- `/metrics/explainability/top-sensors`
- `/reports/model-card`
- `/reports/cost-threshold`
- `/reports/explainability`
- `/summary/questions`
- `/summary/{question_key}`

The service does not train models, regenerate files, accept raw data uploads,
or act as a production backend.

## Optional Local Docker Packaging

The [Dockerfile](../Dockerfile) packages the Streamlit app for local container
review. It installs [requirements.txt](../requirements.txt), copies the project
files, exposes port `8501`, and runs:

```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

Docker is optional. It is not deployment automation, does not start MLflow, and
does not bake secrets into the image. See [Docker Usage](docker_usage.md).

## Controlled RAG-Lite Summary Boundary

The controlled RAG-lite layer uses preset questions only. It builds compact
artifact-grounded context from reviewed artifacts and avoids raw CSV payloads.

Fallback summaries work without an API key. Optional OpenAI summaries require
explicit configuration through Streamlit secrets or environment variables.

No API keys should be committed. No free-form chatbot or arbitrary prompt path
is included. In the Streamlit app, a summary is generated only after the user
selects a preset question and clicks `Generate summary`. The button attempts
the optional OpenAI summary path when configuration is available, and the
fallback summary remains available when OpenAI is unavailable, disabled, or
fails.

## Agentic Analytics Extension Concept

The app includes an architecture extension concept for an agentic analytics
workflow: artifact monitor, benchmark reviewer, cost trade-off analyst,
explainability reviewer, summary generator, and human approval. A tool
framework such as LangGraph could orchestrate this review flow, but LangGraph
is not implemented in this project and the app does not perform autonomous
decision-making.

## Testing and Validation Plan

Validation layers:

- Unit tests for loaders, metrics, threshold logic, and summary helpers
- Schema tests for generated artifacts
- App smoke tests through source inspection
- API tests with FastAPI TestClient
- RAG-lite tests that require no API key or network access
- Wording and artifact review through the PR checklist

Recommended validation commands:

```bash
python -m pip install -r requirements.txt
python -m pytest
python -m ruff check .
python -m compileall app.py app_pages app_utils api src scripts tests
git diff --check
```

Notebook validation:

```bash
python -m pip install jupyter nbformat nbclient ipykernel
python -m jupyter nbconvert --to notebook --execute notebooks/SECOM_Fail_Screening_Portfolio_Summary.ipynb --inplace
```

Local app and API checks:

```bash
streamlit run app.py
python -m uvicorn api.main:app --reload
```

Optional Docker check:

```bash
docker build -t secom-fail-screening-streamlit:local .
docker run --rm -p 8501:8501 secom-fail-screening-streamlit:local
```
