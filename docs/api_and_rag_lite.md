# API and Controlled RAG-Lite Notes

## Purpose

Phase 9 adds two optional portfolio-scale features:

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

The context builder uses compact artifact-grounded snapshots. It does not send
raw SECOM data files or full CSV files to an LLM.

OpenAI API use is optional and future-ready. The fallback summary works without
an API key, without network access, and without the OpenAI package.

## Boundaries

- This is not a production backend.
- This is not a full RAG system.
- This is not a general chatbot.
- No arbitrary user prompt is accepted.
- No API key is stored in the repository.
- No Docker or deployment automation is included in this phase.
