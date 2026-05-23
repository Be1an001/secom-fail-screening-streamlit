# Technical Design Document

## Current Architecture

The repository currently has a script-based baseline workflow:

- `data/`: public SECOM raw files
- `src/secom_ml/`: reusable data, split, preprocessing, model, metric, threshold, plot, and tracking helpers
- `scripts/`: experiment, final evaluation, and report export scripts
- `configs/`: Random Forest experiment settings
- `outputs/`: generated metrics and figures
- `reports/`: generated Markdown reports
- `tests/`: unit tests for data, metrics, and threshold logic

## Target Architecture

The target is an artifact-driven Streamlit app supported by reproducible scripts and lightweight service boundaries:

- Training and benchmark scripts create reviewed artifacts.
- A manifest describes artifact paths, meanings, and freshness.
- The Streamlit app loads artifacts and renders them.
- A minimal FastAPI service may expose selected artifacts.
- A controlled RAG-lite summary may summarize only approved artifacts.

## Artifact-Driven Streamlit Design

The Streamlit app should not retrain models at runtime. It should load:

- benchmark metrics
- threshold sweep outputs
- champion model summary
- explainability artifacts
- report summaries
- artifact manifest

The app should present screening decision support, not an automatic pass/fail decision.

## Six-Model Benchmark Plan

Future benchmark work should compare six clearly documented models. Candidate families may include:

- dummy majority baseline
- logistic regression baseline
- Random Forest baseline
- literature-inspired methods for imbalance handling
- SOTA-inspired gradient boosting methods
- one calibrated or resampling-aware champion candidate

Exact models should be selected in a later planning phase. Do not claim SOTA performance.

## Threshold and Cost Trade-Off Plan

Threshold analysis should extend the current validation threshold sweep with:

- fail recall
- false positives
- flagged sample rate
- review-capacity framing
- simple cost trade-off assumptions

The app should explain how threshold changes affect screening decision support.

## Explainability Plan

Explainability should be framed as model-important sensor signals. Future artifacts may include:

- feature importance
- permutation importance
- stability checks across splits
- SHAP-style summaries if added later

Do not describe these outputs as physical root causes or causal sensor explanations.

## Artifact Manifest Concept

A future artifact manifest should define:

- artifact path
- artifact type
- creation script
- source config
- intended app use
- freshness note
- whether the artifact is generated or hand-authored

## FastAPI Boundary

The FastAPI service should be minimal. It may serve curated metrics, figures, manifest data, and report snippets. It should not become a production platform.

## Controlled RAG-Lite Summary Boundary

The controlled RAG-lite summary should only use approved repository artifacts. It should cite artifact names or sections and avoid unsupported claims.

No API keys should be committed. Any OpenAI integration must use environment variables or Streamlit secrets outside Git.

## Testing and Validation Plan

Planned validation layers:

- Unit tests for loaders, metrics, threshold logic, and artifact manifest parsing
- Script-level smoke tests where practical
- App smoke tests once Streamlit exists
- API smoke tests once FastAPI exists
- Wording and artifact review through the PR checklist

Baseline validation commands:

```bash
py -m pytest
py -m ruff check .
py -m compileall src scripts tests
git diff --check
```
