# Repository Contributor Instructions

## Project Purpose

This repository is a portfolio project for the UCI SECOM semiconductor
fail-screening problem. It combines a baseline workflow, a six-model prototype
benchmark, threshold / cost trade-off analysis, explainability artifacts, an
artifact-driven Streamlit app, a local read-only FastAPI artifact service, and
controlled RAG-lite summaries.

The project supports screening decision support. It should stay practical,
honest, and portfolio-scale.

## Current Repo State

- Raw public SECOM data is tracked in [data](data/).
- Modeling helpers live in [src/secom_ml](src/secom_ml/).
- Reproducible scripts live in [scripts](scripts/).
- Config files live in [configs](configs/).
- Generated evidence lives in [outputs](outputs/) and [reports](reports/).
- The Streamlit app lives in [app.py](app.py), [app_pages](app_pages/), and
  [app_utils](app_utils/).
- The local FastAPI artifact service lives in [api](api/).
- Public documentation starts at [docs/README.md](docs/README.md).
- Upgrade method references are summarized in
  [docs/literature_references.md](docs/literature_references.md).

## Required Wording

Use these terms when appropriate:

- screening decision support
- fail-screening benchmark
- baseline workflow
- reference-supported upgrade methods
- model-important sensor signals
- artifact-driven Streamlit app
- controlled RAG-lite summary
- agentic workflow concept

## Banned Overclaims

Do not claim:

- production deployment
- automatic pass/fail decision
- physical root cause
- causal sensor explanation
- full enterprise MLOps platform
- research-leading performance
- better than existing research

Reference-supported upgrade methods may be discussed as a methodology
direction. Do not claim research-leading performance unless the repo includes a
reproducible same-condition comparison against cited papers.

## Read Before Editing

Before editing, inspect the relevant files and current `git status --short`.
Work with existing changes. Do not revert other work unless explicitly asked.

## Validation Expectations

When code changes are made, run the relevant commands if available:

```bash
python -m pytest
python -m ruff check .
python -m compileall app.py app_pages app_utils api src scripts tests
git diff --check
git status --short
```

If `python` is unavailable, try `py`. If no local Python launcher is available,
report that clearly and still run Git checks.

## Data and Artifact Safety

- Do not edit raw SECOM data unless explicitly asked.
- Do not commit local MLflow tracking artifacts.
- Do not commit Streamlit secrets.
- Do not add model binaries unless there is a clear artifact plan.
- Keep generated metrics, figures, and reports intentional and reviewable.

## Runtime Rules

- Do not retrain models inside the Streamlit runtime.
- The Streamlit app should load curated artifacts.
- Training and benchmark scripts should stay separate from app rendering.
- The local API should read committed artifacts only.

## Secrets Rule

Never commit API keys, tokens, passwords, `.env`, `.streamlit/secrets.toml`, or
local credentials.

## Interpretation Rules

This project supports screening decision support only. Do not describe the
output as an automatic pass/fail decision. Describe explainability outputs as
model-important sensor signals, not physical root causes or causal sensor
explanations.
