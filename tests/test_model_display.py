"""Tests for prototype model display grouping."""

from __future__ import annotations

from collections import Counter

from app_utils.model_display import MODEL_DISPLAY_ROLES


EXPECTED_MODEL_NAMES = {
    "dummy_majority_baseline",
    "logistic_regression_pca_baseline",
    "random_forest_reference",
    "xgboost_cost_sensitive",
    "lightgbm_class_weighted",
    "xgboost_training_only_smote",
}
EXPECTED_ROLE_COUNTS = {
    "Main comparison": 3,
    "Baseline warning": 1,
    "Secondary prototype comparison": 2,
}


def test_all_six_models_have_display_roles() -> None:
    assert set(MODEL_DISPLAY_ROLES) == EXPECTED_MODEL_NAMES


def test_each_display_role_has_required_fields() -> None:
    for metadata in MODEL_DISPLAY_ROLES.values():
        assert metadata["display_role"]
        assert metadata["short_label"]
        assert metadata["main_message"]


def test_expected_display_role_counts() -> None:
    role_counts = Counter(
        metadata["display_role"] for metadata in MODEL_DISPLAY_ROLES.values()
    )

    assert role_counts == EXPECTED_ROLE_COUNTS
