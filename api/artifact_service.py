"""Read-only artifact service helpers for the FastAPI app."""

from __future__ import annotations

from typing import Any

from app_utils.artifact_loader import (
    artifact_path,
    load_artifact_manifest,
    load_csv_artifact,
    load_markdown_artifact,
)


class ArtifactNotFoundError(FileNotFoundError):
    """Raised when a requested artifact is missing."""


def get_manifest() -> dict[str, Any]:
    """Return the artifact manifest."""

    try:
        return load_artifact_manifest()
    except FileNotFoundError as exc:
        raise ArtifactNotFoundError("Artifact manifest is not available.") from exc


def get_csv_artifact_response(relative_path: str, name: str) -> dict[str, Any]:
    """Return a CSV artifact as JSON records."""

    try:
        frame = load_csv_artifact(relative_path)
    except FileNotFoundError as exc:
        raise ArtifactNotFoundError(f"Artifact not found: {relative_path}") from exc

    return {
        "name": name,
        "path": relative_path,
        "row_count": int(len(frame)),
        "columns": [str(column) for column in frame.columns],
        "records": frame.where(frame.notna(), None).to_dict(orient="records"),
    }


def get_report_response(relative_path: str, name: str) -> dict[str, str]:
    """Return a Markdown report artifact as JSON."""

    try:
        content = load_markdown_artifact(relative_path)
    except FileNotFoundError as exc:
        raise ArtifactNotFoundError(f"Report not found: {relative_path}") from exc

    return {
        "name": name,
        "path": relative_path,
        "content": content,
    }


def artifact_file_exists(relative_path: str) -> bool:
    """Return whether a repo artifact path exists as a file."""

    return artifact_path(relative_path).is_file()
