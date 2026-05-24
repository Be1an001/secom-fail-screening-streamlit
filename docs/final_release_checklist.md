# Final Release Checklist

Use this checklist before public portfolio review.

## App QA

- [ ] Streamlit app loads.
- [ ] Five pages work.
- [ ] Page 2 benchmark table displays.
- [ ] Page 3 cost scenario selector works.
- [ ] Page 4 explainability artifacts display.
- [ ] Page 5 API / RAG-lite / OpenAI fallback text works.

## Artifact QA

- [ ] Artifact manifest exists.
- [ ] Key metrics files exist.
- [ ] Key report files exist.
- [ ] Figures load.
- [ ] No fake MLflow summary is committed.

## API QA

- [ ] `/health` works.
- [ ] `/manifest` works.
- [ ] Benchmark metrics endpoint works.
- [ ] Cost endpoint works.
- [ ] Explainability endpoint works.
- [ ] Summary endpoints work.

## OpenAI Summary QA

- [ ] Fallback summary works.
- [ ] Optional OpenAI summary works if secrets are configured.
- [ ] Raw CSVs are not sent.
- [ ] No free-form prompt input exists.
- [ ] No API key is shown in the app or logs.

## Local Validation QA

- [ ] `python -m pytest` passes.
- [ ] `python -m ruff check .` passes.
- [ ] `python -m compileall app.py app_pages app_utils api src scripts tests` passes.
- [ ] Notebook execution succeeds:
  `python -m jupyter nbconvert --to notebook --execute notebooks/SECOM_Fail_Screening_Portfolio_Summary.ipynb --inplace`
- [ ] `git diff --check` passes.
- [ ] CRLF normalization warnings, if present, are non-blocking.

## Optional Docker QA

- [ ] Dockerfile exists.
- [ ] `.dockerignore` excludes secrets and local MLflow files.
- [ ] Optional Docker build works if Docker is available.
- [ ] Docker container starts the Streamlit app.
- [ ] App is reachable at <http://localhost:8501>.
- [ ] No secrets are baked into the image.
- [ ] Docker docs do not claim production deployment.

## Local Release Notes

- [x] Notebook execution was validated locally with `jupyter nbconvert`.
- [x] Docker image build was validated locally.
- [x] Docker container startup was validated locally.
- [x] Streamlit app started in Docker and showed <http://localhost:8501>.
- [x] Notebook metadata and Windows event-loop warnings were non-blocking.

## Responsible Wording QA

- [ ] No production deployment claim.
- [ ] No automatic pass/fail decision claim.
- [ ] No physical root-cause claim.
- [ ] No SOTA performance claim.
- [ ] No final champion claim.
- [ ] No production backend claim.

## GitHub / CI QA

- [ ] GitHub Actions pass.
- [ ] No secrets committed.
- [ ] No local MLflow files committed.
- [ ] No unnecessary cache files committed.
