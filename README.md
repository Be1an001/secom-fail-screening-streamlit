# SECOM Fail-Screening Decision Support App

## Short Summary

This project is a portfolio Streamlit decision-support app for UCI SECOM
rare-fail screening, with benchmark comparison, threshold / cost trade-offs,
explainability artifacts, a read-only local API, and controlled AI summaries.

The goal is to show how an imbalanced manufacturing screening problem can be
reviewed with clear metrics, reproducible artifacts, and honest limitations.
It is not a production semiconductor QA system and does not make automatic
pass/fail decisions.

## Project Type / Status / Tools

- Project type: applied machine learning decision support and Streamlit data
  product
- Domain: semiconductor / manufacturing analytics portfolio project
- Status: completed portfolio app with committed artifacts
- Live app: <https://secom-fail-screening.streamlit.app/>
- Main tools: Python, pandas, scikit-learn, XGBoost, LightGBM,
  imbalanced-learn, Streamlit, FastAPI, optional OpenAI summaries, MLflow,
  Docker, pytest, Ruff, and GitHub Actions

The FastAPI artifact service is local/demo-oriented unless a separate API URL
is explicitly provided.

Documentation starts at the [documentation guide](docs/README.md). A short
project summary is available in [project_summary.md](docs/project_summary.md),
app usage details are in [user_guide.md](docs/user_guide.md), and upgrade
method references are summarized in
[literature_references.md](docs/literature_references.md).

## Business Problem

The SECOM dataset contains semiconductor sensor readings where fail cases are
rare. A model can look strong by raw accuracy while still missing the fail
class, which is the class that matters for screening review.

This project focuses on fail recall, F2-score, PR-AUC, balanced accuracy,
confusion counts, threshold choice, and flagged sample rate. These measures
make the screening trade-off easier to see than accuracy alone.

## Project Objective

The goal was to build a reviewable portfolio app around a leakage-safe SECOM
workflow:

- load the public SECOM files
- separate train, validation, and test data before preprocessing
- compare a baseline model group with later upgrade methods
- evaluate rare-fail screening with recall-focused metrics
- show how threshold choices affect review workload
- explain model-important anonymous sensor signals
- package the evidence in a Streamlit app with supporting docs, reports,
  tests, a local API, and controlled AI summaries

## Dataset and Scope

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

The sensor variables are anonymous. Any feature importance or permutation
importance result should be read as model behavior, not as physical
root-cause evidence.

## My Role / Contribution

This was an individual portfolio project. I built the Streamlit app around a
leakage-safe SECOM rare-fail screening workflow, benchmark artifacts,
threshold / cost analysis, explainability outputs, and controlled AI summary
support.

The original baseline group came from a master's coursework version and
general public example learning. Later portfolio upgrades added
reference-supported model comparisons, threshold / cost artifacts,
explainability artifacts, MLOps-lite documentation, a read-only local FastAPI
service, optional OpenAI summaries, Docker local packaging, tests, and CI.

## Methodology

The workflow uses:

- stratified train / validation / test splits
- training-only missingness filtering
- training-only median imputation
- PCA for the linear baseline path
- validation threshold sweeps
- reserved holdout test evaluation for baseline artifacts
- local MLflow tracking when scripts are run locally
- committed metrics, figures, reports, and an artifact manifest for the app

The Streamlit app reads committed artifacts from [outputs](outputs/),
[reports](reports/), and
[the artifact manifest](outputs/artifact_manifest.json). It does not retrain
models at runtime.

## Model Benchmark and Evaluation

The full prototype benchmark keeps all six models in the artifacts.

Baseline group:

- Dummy Majority Baseline
- Logistic Regression + PCA Baseline
- Random Forest Reference

Upgrade group:

- XGBoost Cost-Sensitive
- LightGBM Class-Weighted
- XGBoost + Training-only SMOTE

The baseline group is kept as the original comparison group. The upgrade
group adds literature-informed or method-reference-supported comparisons. The
project does not claim paper reproduction or research-leading performance.

Key findings from the prototype validation benchmark:

- Dummy Majority shows why accuracy alone is misleading.
- Logistic Regression + PCA is a useful classical baseline.
- Random Forest Reference had the strongest prototype validation F2 in this
  benchmark.
- XGBoost Cost-Sensitive showed a higher-recall, higher-review-workload
  trade-off.
- LightGBM and XGBoost + SMOTE remain useful secondary prototype comparisons.

The upgraded methods and analysis choices are linked to verified references in
[Literature References](docs/literature_references.md).

## Threshold and Cost Trade-off

The threshold / cost analysis shows how operating points affect missed fail
cases and review workload. Thresholds are treated as decision levers for
review, not automatic pass/fail rules.

Cost scenarios are illustrative. They help compare trade-offs, but they are
not validated manufacturing economics and should not be used as production
decision rules.

## Explainability

Explainability artifacts include baseline feature importance, prototype
permutation importance, feature stability, and top sensor signal summaries.
They describe model-important anonymous sensor signals.

These artifacts can support investigation, but they do not identify physical
root causes and are not causal proof.

## Streamlit App

The Streamlit app has five pages:

1. Overview
2. Benchmark
3. Cost Trade-off
4. Explainability
5. API & AI Summary

The Overview page frames the project as a guided workflow from rare-fail data
through leakage-safe benchmarking, threshold trade-offs, explainability, and
artifact-grounded summaries. Evidence links are kept in collapsed sections so
the app stays focused on the project story.

## API and AI Summary Boundaries

The repository includes a minimal read-only FastAPI artifact service for local
review. It serves the manifest, benchmark metrics, selected cost thresholds,
top sensor signals, reports, and fallback summaries as JSON. It does not train
models, regenerate files, or act as a production backend.

The controlled RAG-lite summary layer uses preset questions and compact
artifact-grounded context. Optional OpenAI summaries can be enabled with
Streamlit secrets or environment variables. Raw CSVs are not sent to the LLM,
and there is no free-form chatbot. In the app, summaries are generated only
after the reviewer chooses a preset question and clicks `Generate summary`.

The agentic workflow content in the app is an extension concept only. No
autonomous agent is implemented.

## MLOps-lite Notes

The app uses [outputs/artifact_manifest.json](outputs/artifact_manifest.json)
as a lightweight artifact registry. It tracks metrics, figures, reports,
benchmark artifacts, cost-analysis artifacts, explainability artifacts, and
documentation reports.

Local MLflow tracking can support experiment review. Local files such as
`mlflow.db`, `mlruns/`, and `mlartifacts/` are ignored. A compact exported
MLflow summary may be generated only when real local MLflow run data exists.

Docker is included only as optional local packaging for the Streamlit app. It
is not a production deployment workflow.

## Repository Structure

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

## Local Run

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

## How to Review This Project

Good review paths:

- Start with the live Streamlit app.
- Read the [User Guide](docs/user_guide.md) for page-by-page context.
- Review the benchmark, cost, and explainability reports in [reports](reports/).
- Check [outputs/artifact_manifest.json](outputs/artifact_manifest.json) to see
  how artifacts connect to the app.
- Inspect [docs/literature_references.md](docs/literature_references.md) for
  the upgraded method references.
- Run the local validation commands if you want to check tests and source
  consistency.

Execute the portfolio summary notebook only as supporting evidence:

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

## Reproducibility Notes

From the repository root:

```bash
python -m pytest
python -m ruff check .
python -m compileall app.py app_pages app_utils api src scripts tests
git diff --check
```

Detailed validation and local run notes are in the
[User Guide](docs/user_guide.md).

## Limitations

- This is a portfolio-scale project using a public, anonymous dataset.
- The fail class is small, so split-specific results should be interpreted
  carefully.
- The benchmark is a prototype comparison, not a published benchmark result.
- The final holdout Random Forest artifact is a screening baseline, not a
  production decision system.
- Literature-informed upgrade methods do not imply paper reproduction or
  research-leading performance.
- Cost scenarios are illustrative and are not validated manufacturing
  economics.
- Explainability artifacts show model-important sensor signals, not physical
  root causes or causal explanations.
- The local API is not a production backend.
- The controlled RAG-lite summary is not a general chatbot or full open-ended
  RAG system.
- MLflow usage is local tracking and optional summary export, not a production
  model registry.
- Docker is local packaging, not deployment automation.

## Future Improvements

- Validate threshold and cost assumptions with domain input.
- Add more detailed missingness and drift review if newer manufacturing data
  becomes available.
- Compare calibrated probabilities before operational threshold use.
- Add additional explainability methods only if they stay lightweight and
  clearly scoped.
- Create a short project walkthrough video for portfolio review.

## Related Files

- [Main Streamlit app](app.py)
- [App pages](app_pages/)
- [App utilities](app_utils/)
- [Local FastAPI service](api/)
- [Data README](data/README.md)
- [Raw SECOM features](data/secom.data)
- [Raw SECOM labels](data/secom_labels.data)
- [Documentation guide](docs/README.md)
- [Project summary](docs/project_summary.md)
- [User guide](docs/user_guide.md)
- [Methodology summary](docs/methodology_summary.md)
- [Literature references](docs/literature_references.md)
- [Product Requirements Document](docs/product_requirements_document_prd.md)
- [Technical Design Document](docs/technical_design_document_tdd.md)
- [Docker usage](docs/docker_usage.md)
- [Outputs guide](outputs/README.md)
- [Artifact manifest](outputs/artifact_manifest.json)
- [Benchmark metrics](outputs/metrics/benchmark_model_comparison_prototype.csv)
- [Cost threshold metrics](outputs/metrics/cost_selected_thresholds_prototype.csv)
- [Explainability metrics](outputs/metrics/top_sensor_signals_prototype.csv)
- [Output figures](outputs/figures/)
- [Reports guide](reports/README.md)
- [Model card](reports/model_card.md)
- [Benchmark report](reports/benchmark_prototype_summary.md)
- [Cost report](reports/cost_threshold_prototype_report.md)
- [Explainability report](reports/explainability_prototype_report.md)
- [Scripts guide](scripts/README.md)
- [Configs guide](configs/README.md)
- [Requirements file](requirements.txt)
- [CI workflow](.github/workflows/ci.yml)
