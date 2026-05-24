# Product Requirements Document

## Project Goal

Build a polished portfolio project for the UCI SECOM semiconductor
fail-screening problem. The project presents a practical evaluation benchmark
through an artifact-driven Streamlit app for screening decision support.

The repository includes the baseline workflow, prototype benchmark artifacts,
threshold / cost trade-off analysis, prototype explainability, MLOps-lite
artifact tracking notes, a minimal local FastAPI artifact service, and
controlled RAG-lite summaries with optional OpenAI support.

Related docs:

- [User Guide](user_guide.md)
- [Technical Design Document](technical_design_document_tdd.md)
- [Methodology Summary](methodology_summary.md)
- [Development History](development_history.md)

## Target Audience

- Data science and machine learning reviewers
- Portfolio reviewers and hiring teams
- Technical reviewers who value careful methodology and honest limitations

## User Stories

- As a reviewer, I want to understand the SECOM problem, class imbalance, and
  why raw accuracy is misleading.
- As a reviewer, I want to see leakage-safe preprocessing and a reproducible
  baseline workflow.
- As a reviewer, I want to compare the full six-model prototype benchmark.
- As a reviewer, I want to understand threshold / cost trade-offs for screening
  decision support.
- As a reviewer, I want explainability framed as model-important sensor
  signals, not physical root causes.
- As a reviewer, I want generated artifacts, validation evidence, app pages,
  API boundaries, and limitations to be easy to find.

## App Pages

1. Overview
2. Benchmark
3. Cost Trade-off
4. Explainability
5. API & AI Summary

The Overview page opens with the project story, KPI cards, and workflow
timeline. Page 3 focuses on threshold and cost trade-offs and does not select a
final champion model.

## Core Features

- Baseline workflow summary
- Light portfolio-style Streamlit interface with calm scope notes
- Full six-model prototype benchmark table
- Display grouping for main comparison, baseline warning, and secondary
  prototype comparison models
- Threshold / cost trade-off view with illustrative cost scenarios
- Model-important sensor signal view from prototype explainability artifacts
- Artifact manifest and evidence links
- Collapsed evidence sections for source metrics, reports, and figures
- MLOps-lite artifact tracking summary
- Minimal read-only FastAPI artifact service for local portfolio review
- Controlled RAG-lite summaries using preset questions and artifact-grounded
  context
- Optional OpenAI controlled summaries with fallback behavior
- Generate-on-click controlled summary panel with preset questions only
- Optional local Docker packaging for Streamlit app review

## Non-Goals

- No production deployment claim
- No automatic pass/fail decision
- No physical root cause claim
- No causal sensor explanation
- No full enterprise MLOps platform
- No SOTA performance claim
- No claim of being better than existing research
- No general chatbot
- No raw SECOM data upload or raw CSV transfer to an LLM

## Responsible-Use Constraints

The project should be described as screening decision support for a public,
anonymous dataset. Any model output should be framed as a screening signal that
would require domain review before real operational use.

Cost scenarios are illustrative and are not validated manufacturing costs.
Explainability artifacts show model-important sensor signals only.

## Success Criteria

- The app explains the problem and class imbalance clearly.
- The benchmark is reproducible from scripts and reviewed artifacts.
- The methodology separates training, validation, threshold selection, and
  reserved test evaluation.
- The README and docs use cautious wording.
- The app loads artifacts instead of retraining at runtime.
- The API reads committed artifacts only and does not run model code.
- Controlled summaries use preset questions and compact artifact context.
- Tests and validation commands are documented.
- Optional Docker packaging can run the Streamlit app locally without implying
  deployment automation.

## Baseline and Prototype Upgrade Distinction

Baseline workflow:

- Public SECOM data loading
- Leakage-aware split and preprocessing
- Dummy, logistic regression, and Random Forest comparisons
- Validation threshold selection
- Final holdout evaluation for a validation-selected Random Forest candidate
- Local MLflow tracking support

Prototype upgrade:

- Literature-inspired methods and SOTA-inspired method direction
- Full six-model prototype benchmark
- Cost-aware threshold analysis
- Prototype explainability with permutation importance and feature stability
- Artifact-driven Streamlit app
- Minimal read-only FastAPI artifact service
- Controlled RAG-lite summary with optional OpenAI support
- Optional local Docker packaging for the Streamlit app

The prototype upgrade does not claim SOTA performance or a final champion
model.
