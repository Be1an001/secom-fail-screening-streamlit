"""Artifact loading helpers for the Streamlit app and tests."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Iterable

import pandas as pd


DEFAULT_MANIFEST_PATH = "outputs/artifact_manifest.json"


def project_root() -> Path:
    """Return the repository root for the app utility package."""

    return Path(__file__).resolve().parents[1]


def artifact_path(relative_path: str | Path) -> Path:
    """Resolve an artifact path inside the repository root."""

    root = project_root().resolve()
    candidate = (root / relative_path).resolve()

    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError("Artifact path must stay inside the project root.") from exc

    return candidate


def artifact_exists(relative_path: str | Path) -> bool:
    """Return whether a repository artifact exists."""

    return artifact_path(relative_path).exists()


def load_csv_artifact(relative_path: str | Path) -> pd.DataFrame:
    """Load a required CSV artifact."""

    return pd.read_csv(_require_file(relative_path))


def load_markdown_artifact(relative_path: str | Path) -> str:
    """Load a required Markdown artifact as text."""

    return _require_file(relative_path).read_text(encoding="utf-8")


def load_json_artifact(relative_path: str | Path) -> object:
    """Load a required JSON artifact."""

    with _require_file(relative_path).open(encoding="utf-8") as file:
        return json.load(file)


def load_artifact_manifest(
    relative_path: str | Path = DEFAULT_MANIFEST_PATH,
) -> dict[str, object]:
    """Load the required artifact manifest."""

    manifest = load_json_artifact(relative_path)
    if not isinstance(manifest, dict):
        raise ValueError("Artifact manifest must be a JSON object.")
    return manifest


def validate_manifest_paths(manifest: Mapping[str, object]) -> list[str]:
    """Validate that every manifest artifact path exists."""

    artifact_paths = [
        str(artifact["path"])
        for artifact in _manifest_artifacts(manifest)
        if "path" in artifact
    ]
    missing_paths = [
        path for path in artifact_paths if not artifact_path(path).is_file()
    ]

    if missing_paths:
        missing = ", ".join(missing_paths)
        raise FileNotFoundError(f"Manifest references missing artifacts: {missing}")

    return artifact_paths


def filter_manifest_artifacts(
    manifest: Mapping[str, object],
    *,
    page: str | None = None,
    artifact_type: str | None = None,
) -> list[dict[str, object]]:
    """Filter manifest artifacts by page label or artifact type."""

    filtered: list[dict[str, object]] = []
    for artifact in _manifest_artifacts(manifest):
        if artifact_type is not None and artifact.get("type") != artifact_type:
            continue
        if page is not None and page not in artifact.get("used_by", []):
            continue
        filtered.append(artifact)
    return filtered


def list_existing_artifacts(relative_paths: Iterable[str | Path]) -> list[str]:
    """Return the relative artifact paths that exist, preserving input order."""

    existing: list[str] = []
    for relative_path in relative_paths:
        if artifact_exists(relative_path):
            existing.append(str(relative_path).replace("\\", "/"))
    return existing


def _require_file(relative_path: str | Path) -> Path:
    path = artifact_path(relative_path)
    if not path.is_file():
        raise FileNotFoundError(f"Required artifact not found: {relative_path}")
    return path


def _manifest_artifacts(
    manifest: Mapping[str, object],
) -> list[dict[str, object]]:
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError("Artifact manifest must include an artifacts list.")

    normalized: list[dict[str, object]] = []
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            raise ValueError("Each manifest artifact must be a JSON object.")
        normalized.append(artifact)
    return normalized
