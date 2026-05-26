# Repo Maintenance Notes

Use these notes when maintaining this repository.

## Safe Audit Checklist

- Run `git status --short`.
- Inspect relevant files before editing.
- Summarize raw data and large artifacts without printing huge files.
- Check for secrets, local MLflow files, caches, and model binaries.
- Separate confirmed facts from assumptions.

## Documentation Update Checklist

- Use concise public-facing English.
- Preserve useful existing content.
- Fix stale paths and unsupported claims.
- Keep limitations clear and release-ready.
- Prefer Markdown links for referenced project files.
- Link upgrade method claims to
  [Literature References](../../literature_references.md) when relevant.

## Artifact Safety Checklist

- Do not edit raw SECOM data unless explicitly asked.
- Do not commit `.env` or `.streamlit/secrets.toml`.
- Do not commit `mlflow.db`, `mlruns/`, or `mlartifacts/`.
- Treat generated metrics, figures, and reports as intentional artifacts.

## Commit Message Style

Use concise conventional-style summaries, for example:

```text
docs: refine final documentation structure
```

## PR Description Checklist

- Summary of changes
- Validation commands and results
- Wording review
- Artifact and secret review
- Human review notes

## Validation Checklist

Run when available:

```bash
python -m pytest
python -m ruff check .
python -m compileall app.py app_pages app_utils api src scripts tests
git diff --check
git status --short
```

If `python` is unavailable, try `py`.

## Wording Rules

Use:

- screening decision support
- fail-screening benchmark
- baseline workflow
- reference-supported upgrade methods
- model-important sensor signals
- artifact-driven Streamlit app
- controlled RAG-lite summary
- agentic workflow concept

Do not claim production deployment, automatic pass/fail decision, physical root
cause, causal sensor explanation, full enterprise MLOps platform, research-leading
performance, or better than existing research.
