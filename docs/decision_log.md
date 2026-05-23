# Decision Log

Use this log for short project decisions that affect future phases.

| Date | Decision | Reason |
|---|---|---|
| 2026-05-23 | Keep the project portfolio-scale. | The goal is a clear master's-level data science portfolio project, not an enterprise platform. |
| 2026-05-23 | Build toward an artifact-driven Streamlit app. | The app should present reviewed artifacts instead of retraining models at runtime. |
| 2026-05-23 | Use screening decision support wording. | The model output should be framed as a screening signal, not an automatic pass/fail decision. |
| 2026-05-23 | Do not claim production deployment. | The project is a portfolio workflow and has no real fab validation or operational rollout. |
| 2026-05-23 | Do not claim physical root cause or causal sensor explanation. | SECOM sensor names are anonymous and model importance is not causal evidence. |
| 2026-05-23 | Ignore local MLflow artifacts. | `mlflow.db`, `mlruns/`, and `mlartifacts/` are local tracking outputs and should not be committed. |
| 2026-05-23 | Keep raw public SECOM data tracked. | The dataset is public, small enough for the repository, and needed for reproducible review. |
| 2026-05-23 | SOTA-inspired methods do not imply SOTA performance. | Future methods may be inspired by literature, but performance claims require same-condition evidence. |
