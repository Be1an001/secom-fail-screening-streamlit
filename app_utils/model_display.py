"""Display roles for prototype benchmark models."""

from __future__ import annotations


MAIN_COMPARISON = "Main comparison"
BASELINE_WARNING = "Baseline warning"
SECONDARY_PROTOTYPE_COMPARISON = "Secondary prototype comparison"

ROLE_ORDER = [
    MAIN_COMPARISON,
    BASELINE_WARNING,
    SECONDARY_PROTOTYPE_COMPARISON,
]

MODEL_DISPLAY_ROLES = {
    "dummy_majority_baseline": {
        "display_role": BASELINE_WARNING,
        "short_label": "Dummy Majority",
        "main_message": (
            "Shows why accuracy alone is misleading in rare-fail screening."
        ),
    },
    "logistic_regression_pca_baseline": {
        "display_role": MAIN_COMPARISON,
        "short_label": "Logistic + PCA",
        "main_message": "Classical linear baseline with lower review workload.",
    },
    "random_forest_reference": {
        "display_role": MAIN_COMPARISON,
        "short_label": "Random Forest Reference",
        "main_message": "Current strongest prototype F2 reference.",
    },
    "xgboost_cost_sensitive": {
        "display_role": MAIN_COMPARISON,
        "short_label": "XGBoost Cost-Sensitive",
        "main_message": "Higher-recall option with higher review workload.",
    },
    "lightgbm_class_weighted": {
        "display_role": SECONDARY_PROTOTYPE_COMPARISON,
        "short_label": "LightGBM Weighted",
        "main_message": "Secondary boosting-family comparison.",
    },
    "xgboost_training_only_smote": {
        "display_role": SECONDARY_PROTOTYPE_COMPARISON,
        "short_label": "XGBoost + Training-only SMOTE",
        "main_message": (
            "Shows leakage-safe resampling as a prototype comparison."
        ),
    },
}


def get_model_display(model_name: str) -> dict[str, str]:
    """Return display metadata for a model name."""

    fallback = {
        "display_role": "Unassigned",
        "short_label": model_name,
        "main_message": "No display note is available for this model.",
    }
    return MODEL_DISPLAY_ROLES.get(model_name, fallback)


def model_names_for_role(display_role: str) -> list[str]:
    """Return model names assigned to one display role."""

    return [
        model_name
        for model_name, metadata in MODEL_DISPLAY_ROLES.items()
        if metadata["display_role"] == display_role
    ]
