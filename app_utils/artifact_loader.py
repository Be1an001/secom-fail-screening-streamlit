"""Artifact loading helpers for the Streamlit app and tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import pandas as pd


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
