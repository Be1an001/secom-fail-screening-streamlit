# MLflow and Artifact Tracking Summary

This project uses an artifact-driven Streamlit app. The public app reads
curated files from [outputs](../outputs/), [reports](../reports/), and
[outputs/artifact_manifest.json](../outputs/artifact_manifest.json).

## Current Artifact Tracking

- [outputs/artifact_manifest.json](../outputs/artifact_manifest.json) acts as a
  lightweight artifact registry.
- Benchmark, threshold / cost, and explainability outputs are committed as
  reviewed portfolio artifacts.
- The app does not retrain models at runtime.

## Local MLflow Tracking

MLflow is used for local experiment tracking when experiment scripts are run
locally. Local MLflow files such as `mlflow.db`, `mlruns/`, and `mlartifacts/`
are intentionally ignored because they are environment-specific tracking
outputs.

The script
[export_mlflow_runs_summary.py](../scripts/export_mlflow_runs_summary.py) can
export a compact `outputs/metrics/mlflow_runs_summary.csv` file when real local
MLflow run data exists. No exported MLflow summary is committed unless it comes
from actual local MLflow data.

## Local API and Controlled Summaries

The repository includes a minimal FastAPI artifact service for local portfolio
review. It reads committed artifacts and returns JSON. It is not a production
backend and does not run training or artifact generation.

The repository also includes controlled RAG-lite summaries. These summaries use
preset questions and compact artifact-grounded context. Fallback summaries work
without an API key. Optional OpenAI summaries can be enabled through Streamlit
secrets or environment variables.

Raw CSVs are not sent to an LLM, and no free-form chatbot is included.

## Not Implemented

- No deployed MLflow tracking server is included.
- No production MLOps platform is claimed.
- No production backend is claimed.
- No general chatbot is included.
- Agentic workflow automation is outside the current portfolio app scope.
