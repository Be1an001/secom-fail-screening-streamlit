# MLflow and Artifact Tracking Summary

This project uses an artifact-driven Streamlit app. The public app reads
curated files from `outputs/`, `reports/`, and
`outputs/artifact_manifest.json`.

## Current Artifact Tracking

- `outputs/artifact_manifest.json` acts as a lightweight artifact registry.
- Benchmark, threshold / cost, and explainability outputs are committed as
  reviewed portfolio artifacts.
- The app does not retrain models at runtime.

## Local MLflow Tracking

MLflow is used for local experiment tracking when experiment scripts are run
locally. Local MLflow files such as `mlflow.db`, `mlruns/`, and `mlartifacts/`
are intentionally ignored because they are environment-specific tracking
outputs.

The script `scripts/export_mlflow_runs_summary.py` can export a compact
`outputs/metrics/mlflow_runs_summary.csv` file when real local MLflow run data
exists. No exported MLflow summary is committed unless it comes from actual
local MLflow data.

## Not Implemented Yet

- No deployed MLflow tracking server is included.
- No production MLOps platform is claimed.
- No future FastAPI artifact service is implemented yet.
- Future controlled RAG-lite summary work remains planned.
- Future agentic workflow concept work remains planned.
