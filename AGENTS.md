# Agent Instructions

## Project Purpose

This repository is a portfolio project for the UCI SECOM semiconductor fail-screening problem. The current repo is a baseline workflow with data loading, leakage-aware preprocessing, Random Forest experiments, generated metrics, reports, and tests.

The final direction is an artifact-driven Streamlit app that explains a fail-screening benchmark for screening decision support. The project should stay practical, honest, and portfolio-scale.

## Current Repo State

- Raw public SECOM data is tracked in `data/`.
- Current modeling code lives in `src/secom_ml/`.
- Current experiment scripts live in `scripts/`.
- Current generated evidence lives in `outputs/` and `reports/`.
- The app, API, Docker, CI, artifact manifest, and controlled RAG-lite summary are planned but not implemented yet.

## Required Wording

Use these terms when appropriate:

- screening decision support
- fail-screening benchmark
- baseline workflow
- literature-inspired methods
- SOTA-inspired methods
- model-important sensor signals
- artifact-driven Streamlit app
- controlled RAG-lite summary
- future agentic workflow concept

## Banned Overclaims

Do not claim:

- production deployment
- automatic pass/fail decision
- physical root cause
- causal sensor explanation
- full enterprise MLOps platform
- SOTA performance
- better than existing research

SOTA-inspired methods may be discussed as a future methodology direction. Do not claim SOTA performance unless the repo later includes a reproducible same-condition comparison against cited papers.

## Read Before Editing

Before editing, inspect the relevant files and current `git status --short`. Work with existing user changes. Do not revert user work unless the user explicitly asks.

## Phase Workflow

Use a two-step phase pattern:

1. Phase XA: planning only.
2. Phase XB: implementation after the plan is accepted.

Keep each phase small enough to review.

## Validation Expectations

When code changes are made, run the relevant commands if available:

```bash
py -m pytest
py -m ruff check .
py -m compileall src scripts tests
git diff --check
git status --short
```

If `py` is unavailable, try `python`. If Python is unavailable, report that clearly and still run Git checks.

## Data and Artifact Safety

- Do not edit raw data files unless the user explicitly asks.
- Do not commit local MLflow tracking artifacts.
- Do not commit Streamlit secrets.
- Do not add model binaries unless there is a clear artifact plan.
- Keep generated metrics, figures, and reports intentional and reviewable.

## Runtime Rules

- Do not retrain models inside the Streamlit runtime.
- The Streamlit app should load curated artifacts.
- Training and benchmark scripts should stay separate from app rendering.

## Secrets Rule

Never commit API keys, tokens, passwords, `.env`, `.streamlit/secrets.toml`, or local credentials.

## Interpretation Rules

This project supports screening decision support only. Do not describe the output as an automatic pass/fail decision. Describe explainability outputs as model-important sensor signals, not physical root causes or causal sensor explanations.
