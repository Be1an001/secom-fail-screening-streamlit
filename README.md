# SECOM Fail-Screening Decision Support App

## Project Overview

This repository is a portfolio-scale machine learning project for the public
UCI SECOM semiconductor dataset. It presents a rare fail-screening problem,
class imbalance, leakage-safe preprocessing, prototype model comparison,
threshold / cost trade-offs, explainability artifacts, and MLOps-lite evidence
through an artifact-driven Streamlit app.

The project is screening decision support. It is not an automatic pass/fail
decision system, not physical root-cause analysis, and not a production
manufacturing system.

## Live App / Demo

Live Streamlit app:

<https://secom-fail-screening.streamlit.app/>

The FastAPI artifact service is local/demo-oriented unless a separate API URL
is explicitly provided.

Documentation starts at the [documentation guide](docs/README.md). A short
reviewer summary is available in [project_summary.md](docs/project_summary.md),
app usage details are in [user_guide.md](docs/user_guide.md), and upgrade
method references are summarized in
[literature_references.md](docs/literature_references.md).

## Why This Project Matters

SECOM fail cases are rare. A model can look strong by raw accuracy while
missing the fail class. This project focuses on fail recall, F2-score,
PR-AUC, balanced accuracy, confusion counts, and flagged sample rate so the
screening trade-off is visible.

## Dataset

The repository includes the public UCI SECOM files:

| File | Purpose |
|---|---|
| [data/secom.data](data/secom.data) | Anonymous sensor feature matrix |
| [data/secom_labels.data](data/secom_labels.data) | Raw labels and timestamps |
| [data/secom.names](data/secom.names) | UCI metadata |

Dataset summary:

- Rows: 1,567
- Sensor features loaded from `secom.data`: 590
- Pass samples: 1,463
- Fail samples: 104
- Fail rate: about 6.64%
- Label mapping: `-1 -> 0` pass, `1 -> 1` fail

## What the App Shows

The Streamlit app has five polished portfolio pages:

1. Overview
2. Benchmark
3. Cost Trade-off
4. Explainability
5. API & AI Summary

The app reads committed artifacts from [outputs](outputs/),
[reports](reports/), and
[the artifact manifest](outputs/artifact_manifest.json). It does not retrain
models at runtime.

The first page now frames the project as a guided workflow story from
rare-fail data through leakage-safe benchmarking, threshold trade-offs,
explainability, and artifact-grounded summaries. Its "What to explore next"
cards navigate to the other app pages. Evidence links are secondary and appear
in collapsed sections so the app reads like a finished portfolio data product.

## Modeling Workflow

The workflow uses:

- stratified train / validation / test splits
- training-only missingness filtering
- training-only imputation
- PCA for the linear baseline path
- threshold selection on validation predictions
- reserved holdout test evaluation for baseline artifacts
- local MLflow tracking when scripts are run locally

## Prototype Benchmark Results

The full prototype benchmark keeps all six models in the artifacts:

Baseline group:

- Dummy Majority Baseline
- Logistic Regression + PCA
- Random Forest Reference

Upgrade group:

- XGBoost Cost-Sensitive
- LightGBM Class-Weighted
- XGBoost + Training-only SMOTE

The app groups models for readability only. It does not remove models and does
not select a final champion model.

The baseline group came from the original master's coursework version and
general public example learning. These models are comparison references, not
paper-reproduction models. The upgrade group adds literature-informed or
method-reference-supported comparisons.

Current interpretation:

- Dummy Majority shows why accuracy alone is misleading.
- Logistic Regression + PCA is a useful classical baseline.
- Random Forest Reference currently has the strongest prototype F2.
- XGBoost Cost-Sensitive provides a higher-recall trade-off with higher review
  workload.
- LightGBM and XGBoost + SMOTE remain secondary prototype comparisons.

These are prototype benchmark results, not research-leading performance claims.
The upgraded methods and analysis choices are linked to verified references in the
[Literature References](docs/literature_references.md) document.

## Threshold and Cost Trade-off

The threshold / cost analysis shows how operating points affect missed fail
cases and review workload. Cost scenarios are illustrative and are not
validated manufacturing costs.

Thresholds are decision levers for review, not automatic pass/fail rules.

## Explainability

Explainability artifacts include baseline feature importance, prototype
permutation importance, feature stability, and top sensor signal summaries.
They describe model-important sensor signals.

The SECOM sensor names are anonymous. These artifacts do not identify physical
root causes and are not causal proof.

## MLOps-lite and Artifact Tracking

The app uses [outputs/artifact_manifest.json](outputs/artifact_manifest.json) as a lightweight artifact
registry. It tracks metrics, figures, reports, benchmark artifacts,
cost-analysis artifacts, explainability artifacts, and documentation reports.

Local MLflow tracking can support experiment review. Local files such as
`mlflow.db`, `mlruns/`, and `mlartifacts/` are ignored. A compact exported
MLflow summary may be generated only when real local MLflow run data exists.

## FastAPI and Controlled RAG-lite Summary

The repo includes a minimal read-only FastAPI artifact service for local review.
It serves the manifest, benchmark metrics, selected cost thresholds, top sensor
signals, reports, and fallback summaries as JSON.

The controlled RAG-lite summary uses preset questions and compact
artifact-grounded context. Optional OpenAI summaries can be enabled with
Streamlit secrets or environment variables. Raw CSVs are not sent to the LLM,
and there is no free-form chatbot. In the app, summaries are generated only
after the reviewer chooses a preset question and clicks `Generate summary`.

The FastAPI layer is a read-only artifact service for local review and
integration testing. It serves selected project artifacts, metrics, reports,
and summary endpoints; it does not train models or regenerate files.

## Project Structure

| Path | Description |
|---|---|
| [app.py](app.py) | Streamlit app entry point |
| [app_pages/](app_pages/) | Five Streamlit page modules |
| [app_utils/](app_utils/) | Artifact loading, formatting, display, and summary helpers |
| [api/](api/) | Minimal read-only FastAPI artifact service |
| [configs/](configs/) | Experiment, benchmark, cost, and explainability configs |
| [data/](data/) | Public SECOM source files |
| [docs/](docs/) | Documentation guide, user guide, design notes, and release checklist |
| [Dockerfile](Dockerfile) | Optional local Streamlit container packaging |
| [outputs/](outputs/) | Committed metrics, figures, and artifact manifest |
| [reports/](reports/) | Markdown reports used by the app and reviewers |
| [scripts/](scripts/) | Reproducible experiment and artifact export scripts |
| [src/secom_ml/](src/secom_ml/) | Reusable data science and ML helpers |
| [tests/](tests/) | Lightweight validation and wording guardrails |

## How to Run Locally

From the repository root:

```bash
cd path\to\secom-fail-screening-streamlit
python -m pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run app.py
```

Expected local app URL:

<http://localhost:8501>

Run the local FastAPI artifact service:

```bash
python -m uvicorn api.main:app --reload
```

Open API docs locally:

<http://127.0.0.1:8000/docs>

Optional local Docker run:

```bash
docker build -t secom-fail-screening-streamlit:local .
docker run --rm -p 8501:8501 secom-fail-screening-streamlit:local
```

Docker is optional local packaging. Streamlit Community Cloud deployment does
not require Docker.

Execute the portfolio summary notebook:

```bash
python -m pip install jupyter nbformat nbclient ipykernel
python -m jupyter nbconvert --to notebook --execute notebooks/SECOM_Fail_Screening_Portfolio_Summary.ipynb --inplace
```

## Optional OpenAI Summary Setup

Do not commit secrets.

For Streamlit Community Cloud, add this in App settings -> Secrets. For local
testing, use environment variables or a local `.streamlit/secrets.toml` that is
not committed:

```toml
OPENAI_API_KEY = "your-key-here"
OPENAI_SUMMARY_MODEL = "gpt-5.4-mini"
OPENAI_SUMMARY_ENABLED = true
```

Fallback summaries work without OpenAI configuration.

## Validation

From the repository root:

```bash
python -m pytest
python -m ruff check .
python -m compileall app.py app_pages app_utils api src scripts tests
git diff --check
```

Detailed validation and local run notes are in the
[User Guide](docs/user_guide.md).

## Responsible Use and Limitations

- This is a portfolio-scale project using a public, anonymous dataset.
- The fail class is small.
- Results are prototype artifacts and split-specific.
- Literature-informed upgrade methods do not imply research-leading performance. See
  [Literature References](docs/literature_references.md) for the upgrade method
  sources used in the project story.
- The app supports screening decision support only.
- The project does not make automatic pass/fail decisions.
- The project does not identify physical root causes or causal sensor
  explanations.
- The local API is not a production backend.
- The controlled RAG-lite summary is not a general chatbot.

## Related Files

- [Documentation guide](docs/README.md)
- [Project summary](docs/project_summary.md)
- [User guide](docs/user_guide.md)
- [Product Requirements Document](docs/product_requirements_document_prd.md)
- [Technical Design Document](docs/technical_design_document_tdd.md)
- [Development history](docs/development_history.md)
- [Literature references](docs/literature_references.md)
- [Docker usage](docs/docker_usage.md)
- [Outputs guide](outputs/README.md)
- [Reports guide](reports/README.md)
- [Scripts guide](scripts/README.md)
- [Configs guide](configs/README.md)
- [Artifact manifest](outputs/artifact_manifest.json)
- [Benchmark report](reports/benchmark_prototype_summary.md)
- [Cost report](reports/cost_threshold_prototype_report.md)
- [Explainability report](reports/explainability_prototype_report.md)
