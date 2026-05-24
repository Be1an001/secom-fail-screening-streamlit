# Docker Usage

Docker is optional for this project. It provides a local container run option
for the Streamlit app. Streamlit Community Cloud deployment does not require
Docker.

## Build

From the repository root:

```bash
cd path\to\secom-fail-screening-streamlit
docker build -t secom-fail-screening-streamlit:local .
```

The first build may take several minutes because Python dependencies are
installed inside the image.

## Run

```bash
cd path\to\secom-fail-screening-streamlit
docker run --rm -p 8501:8501 secom-fail-screening-streamlit:local
```

Then open:

<http://localhost:8501>

## Optional OpenAI Summary Secrets

Do not bake API keys into the image. For local container testing, pass secrets
through environment variables:

```bash
docker run --rm -p 8501:8501 \
  -e OPENAI_API_KEY="your-key-here" \
  -e OPENAI_SUMMARY_MODEL="gpt-5.4-mini" \
  -e OPENAI_SUMMARY_ENABLED="true" \
  secom-fail-screening-streamlit:local
```

The app works without OpenAI settings by using fallback summaries.

For Streamlit Community Cloud, configure optional OpenAI summaries in app
settings secrets instead of using Docker environment variables.

## Scope

- Local Streamlit container only
- No Docker Compose
- No MLflow server
- No image push requirement
- No deployment automation
- No production deployment claim
- No secrets baked into the image
