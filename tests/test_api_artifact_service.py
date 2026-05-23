"""Tests for the minimal read-only FastAPI artifact service."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api import main as api_main


client = TestClient(api_main.app)


def test_health_endpoint_is_read_only() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["read_only"] is True
    assert payload["production_backend"] is False


def test_manifest_endpoint_returns_artifact_list() -> None:
    response = client.get("/manifest")

    assert response.status_code == 200
    payload = response.json()
    assert payload["project"] == "secom-fail-screening-streamlit"
    assert payload["artifacts"]


def test_metric_endpoints_return_existing_artifacts() -> None:
    endpoints = [
        "/metrics/benchmark",
        "/metrics/cost-selected-thresholds",
        "/metrics/explainability/top-sensors",
    ]

    for endpoint in endpoints:
        response = client.get(endpoint)
        payload = response.json()

        assert response.status_code == 200
        assert payload["row_count"] > 0
        assert payload["columns"]
        assert payload["records"]


def test_report_endpoints_return_markdown_content() -> None:
    endpoints = [
        "/reports/model-card",
        "/reports/cost-threshold",
        "/reports/explainability",
    ]

    for endpoint in endpoints:
        response = client.get(endpoint)
        payload = response.json()

        assert response.status_code == 200
        assert payload["content"]
        assert payload["path"].endswith(".md")


def test_controlled_summary_endpoints_use_preset_questions() -> None:
    questions_response = client.get("/summary/questions")
    summary_response = client.get("/summary/project_overview")
    missing_response = client.get("/summary/free_form_question")

    assert questions_response.status_code == 200
    assert "project_overview" in questions_response.json()["questions"]
    assert summary_response.status_code == 200
    assert summary_response.json()["used_openai"] is False
    assert "screening decision support" in summary_response.json()["answer"]
    assert missing_response.status_code == 404


def test_missing_artifact_returns_404(monkeypatch) -> None:
    monkeypatch.setattr(
        api_main,
        "BENCHMARK_METRICS",
        "outputs/metrics/not_a_real_artifact.csv",
    )

    response = client.get("/metrics/benchmark")

    assert response.status_code == 404
    assert "Artifact not found" in response.json()["detail"]
