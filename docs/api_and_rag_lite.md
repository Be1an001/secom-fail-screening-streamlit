# API and Controlled RAG-Lite Notes

## Purpose

This project includes two optional portfolio-scale features:

- a minimal FastAPI artifact service
- a controlled RAG-lite summary helper

Both features read existing artifacts. They do not train models, regenerate
artifacts, or create a production backend.

## Local API

Run the read-only artifact service locally with:

```bash
uvicorn api.main:app --reload
```

Available endpoints:

- `GET /health`
- `GET /manifest`
- `GET /metrics/benchmark`
- `GET /metrics/cost-selected-thresholds`
- `GET /metrics/explainability/top-sensors`
- `GET /reports/model-card`
- `GET /reports/cost-threshold`
- `GET /reports/explainability`
- `GET /summary/questions`
- `GET /summary/{question_key}`

The service returns JSON from committed artifacts only. If an artifact is
missing, the service returns a clear 404 response.

## Controlled RAG-Lite Summary

The controlled summary layer uses preset questions only:

- `project_overview`
- `benchmark_summary`
- `threshold_tradeoff`
- `explainability_summary`
- `mlops_artifact_tracking`
- `limitations`

The context builder uses compact artifact-grounded snapshots. Raw CSVs are not
sent to an LLM, and raw SECOM data files are not sent to an LLM.

OpenAI API use is optional. The fallback summary works without an API key,
without network access, and without the OpenAI package.

## Optional OpenAI Setup

Do not commit secrets. Do not commit `.streamlit/secrets.toml` or `.env`.

For local Streamlit testing, use `.streamlit/secrets.toml` only on your local
machine:

```toml
OPENAI_API_KEY = "your-key-here"
OPENAI_SUMMARY_MODEL = "gpt-5.4-mini"
OPENAI_SUMMARY_ENABLED = true
```

For Streamlit Community Cloud, add the same TOML content in:

`App settings` -> `Secrets`

The app still shows fallback summaries when OpenAI is disabled, the key is
missing, the model is missing, the package is unavailable, or the API call
fails. The API key is stored in Streamlit secrets or environment variables, not
in the repository.

## Boundaries

- This is not a production backend.
- This is not a full RAG system.
- This is not a general chatbot.
- No arbitrary user prompt is accepted.
- Raw CSVs are not sent to an LLM.
- No API key is stored in the repository.
- No Docker or deployment automation is included.
