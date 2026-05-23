# Repo Maintenance Skill

Use this skill for future maintenance phases in this repository.

## Safe Audit Checklist

- Run `git status --short`.
- Inspect relevant files before editing.
- Summarize raw data and large artifacts without printing huge files.
- Check for secrets, local MLflow files, caches, and model binaries.
- Keep confirmed facts separate from assumptions.

## Documentation Update Checklist

- Use simple English.
- Preserve useful existing content.
- Fix stale paths and unsupported claims.
- Keep future features clearly labeled as planned.
- Do not turn governance docs into enterprise process.

## Artifact Safety Checklist

- Do not edit raw SECOM data unless explicitly asked.
- Do not commit `.env` or `.streamlit/secrets.toml`.
- Do not commit `mlflow.db`, `mlruns/`, or `mlartifacts/`.
- Treat generated metrics, figures, and reports as intentional artifacts.

## Commit Message Style

Use concise conventional-style summaries, for example:

```text
docs: add project governance foundation
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
py -m pytest
py -m ruff check .
py -m compileall src scripts tests
git diff --check
git status --short
```

If `py` is unavailable, try `python`.

## Wording Rules

Use:

- screening decision support
- fail-screening benchmark
- baseline workflow
- literature-inspired methods
- SOTA-inspired methods
- model-important sensor signals
- artifact-driven Streamlit app
- controlled RAG-lite summary
- future agentic workflow concept

Do not claim production deployment, automatic pass/fail decision, physical root cause, causal sensor explanation, full enterprise MLOps platform, SOTA performance, or better than existing research.
