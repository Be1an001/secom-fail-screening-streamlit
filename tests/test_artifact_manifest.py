"""Tests for the baseline artifact manifest."""

from __future__ import annotations

from app_utils.artifact_loader import artifact_path, load_artifact_manifest


REQUIRED_TOP_LEVEL_FIELDS = {
    "project",
    "manifest_version",
    "scope",
    "notes",
    "artifacts",
}

REQUIRED_ARTIFACT_FIELDS = {
    "name",
    "type",
    "path",
    "created_by",
    "used_by",
    "description",
    "current_status",
    "future_status",
}


def test_artifact_manifest_exists_and_has_required_top_level_fields() -> None:
    manifest_path = artifact_path("outputs/artifact_manifest.json")
    manifest = load_artifact_manifest()

    assert manifest_path.is_file()
    assert REQUIRED_TOP_LEVEL_FIELDS.issubset(manifest)
    assert manifest["scope"] == "baseline and prototype artifacts"


def test_manifest_artifact_entries_have_required_fields() -> None:
    manifest = load_artifact_manifest()

    assert manifest["artifacts"]
    for artifact in manifest["artifacts"]:
        assert REQUIRED_ARTIFACT_FIELDS.issubset(artifact)


def test_every_manifest_artifact_path_exists() -> None:
    manifest = load_artifact_manifest()

    for artifact in manifest["artifacts"]:
        assert artifact_path(artifact["path"]).is_file()
