# Development History

This page summarizes how the project evolved from a script-based SECOM
baseline workflow into a public portfolio app. It is a high-level history, not
a private task log.

## Build Stages

### Stage 0 - Governance, CI, and Repository Structure

The repository started with lightweight project guidance, validation commands,
ignore rules for local MLflow and Streamlit secrets, and a baseline GitHub
Actions workflow.

### Stage 1 - App Foundation and Artifact Loading

The project added a Streamlit app shell, five page modules, app utilities, and
artifact loading helpers. The app was designed to read committed artifacts
instead of retraining models at runtime.

### Stage 2 - Baseline Artifact Display

The app began displaying baseline SECOM metrics, reports, figures, and the
artifact manifest. This established the artifact-driven Streamlit app pattern.

### Stage 3 - Literature-Inspired Benchmark

A six-model prototype benchmark added classical baselines, Random Forest,
cost-sensitive XGBoost, LightGBM, and training-only SMOTE comparisons. The
benchmark is literature-inspired and SOTA-inspired in method direction, but it
does not claim SOTA performance.

### Stage 4 - Threshold and Cost Trade-off Analysis

Threshold sweep artifacts were used to compute illustrative cost scenarios.
This made missed fail cases, false positives, and review workload visible as
screening decision support trade-offs.

### Stage 5 - Model Display Grouping

The app kept all six models in the full benchmark artifacts while grouping the
display into main comparison, baseline warning, and secondary prototype
comparison roles. The grouping improves readability and does not select a final
champion model.

### Stage 6 - Explainability Artifacts

Prototype explainability artifacts were added for Random Forest Reference and
XGBoost Cost-Sensitive. The outputs use permutation importance and feature
stability to identify model-important sensor signals.

### Stage 7 - MLOps-Lite and Artifact Tracking

The app clarified artifact tracking through
[the artifact manifest](../outputs/artifact_manifest.json). Local MLflow
tracking remains useful during experiments, but raw MLflow databases and run
folders are not committed.

### Stage 8 - Local API and Controlled Summaries

The project added a minimal read-only FastAPI artifact service and controlled
RAG-lite summaries. Summaries use preset questions and compact artifact-grounded
context. Optional OpenAI summaries are supported through secrets or environment
variables, with fallback summaries available when OpenAI is not configured.

### Stage 9 - Final Portfolio Polish

The final documentation pass aligned the README, user guide, product
requirements, technical design, reports, app wording, and release checklist for
public portfolio review.

### Stage 10 - Final Verification and Local Packaging Notes

The final repository cleanup added clearer documentation names, docs
navigation, folder guides, notebook positioning, copy-ready validation
commands, notebook execution instructions, and optional local Docker packaging
for the Streamlit app. The notebook and Docker container were validated locally
as release checks.

## Key Design Decisions

- Keep the project portfolio-scale rather than building an enterprise platform.
- Use screening decision support wording rather than automatic pass/fail
  decision wording.
- Keep raw public SECOM data tracked because it is small and useful for
  reproducible review.
- Ignore local MLflow databases, run folders, Streamlit secrets, and local
  credentials.
- Keep the Streamlit app artifact-driven and separate from training scripts.
- Keep all six prototype models in artifacts while grouping the app display for
  readability.
- Treat cost scenarios as illustrative, not validated manufacturing costs.
- Describe explainability as model-important sensor signals, not physical root
  causes or causal proof.
- Keep the FastAPI service local/demo-oriented and read-only.
- Keep controlled RAG-lite summaries preset-question only, with no raw CSV
  transfer and no general chatbot path.
- Enable OpenAI summaries only as an optional controlled path with fallback
  behavior.
- Keep Docker packaging optional and local, with no image push or deployment
  automation.
