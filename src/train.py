"""
Model training pipeline with W&B experiment tracking.
Builds a scikit-learn Pipeline with preprocessing and classification,
performs hyperparameter tuning, and logs everything to Weights & Biases.

Usage:
    python -m src.train
"""
import os
import json
import warnings

import joblib
import numpy as np

import wandb

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score,
    precision_score,
    recall_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config import (
    CATEGORICAL_FEATURES,
    MODEL_DIR,
    MODEL_PATH,
    NUMERICAL_FEATURES,
    RANDOM_STATE,
    TARGET_COLUMN,
    TEST_SIZE,
    WANDB_API_KEY,
    WANDB_PROJECT,
)
from src.data_loader import load_data_from_csv, get_features_and_target, validate_dataframe

warnings.filterwarnings("ignore")


def build_preprocessor():
    """Build the ColumnTransformer for preprocessing."""
    numerical_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numerical_transformer, NUMERICAL_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )
    return preprocessor


def build_pipeline(preprocessor, model):
    """Build the full sklearn Pipeline."""
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", model),
        ]
    )


def get_param_distributions():
    """Define hyperparameter search space for RandomizedSearchCV."""
    return {
        "classifier__n_estimators": [50, 100, 200, 300, 500],
        "classifier__max_depth": [5, 10, 15, 20, None],
        "classifier__min_samples_split": [2, 5, 10, 20],
        "classifier__min_samples_leaf": [1, 2, 4, 8],
        "classifier__max_features": ["sqrt", "log2", None],
        "classifier__class_weight": ["balanced", "balanced_subsample", None],
    }


def evaluate_model(y_true, y_pred, y_prob):
    """Compute all classification metrics."""
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "f1_score": f1_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_true, y_prob),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
    }
    return metrics


def train():
    """
    Full training pipeline:
    1. Load data
    2. Split train/test
    3. Build pipeline
    4. Hyperparameter tuning with RandomizedSearchCV
    5. Evaluate on test set
    6. Log everything to W&B
    7. Save best model
    """
    # --- 1. Load data ---
    print("=" * 60)
    print("STUDENT DEPRESSION CLASSIFICATION PIPELINE")
    print("=" * 60)

    # Try Postgres first, fall back to CSV
    try:
        from src.data_loader import load_data_from_postgres
        df = load_data_from_postgres()
    except Exception as e:
        print(f"[Train] Postgres unavailable ({e}), falling back to CSV...")
        df = load_data_from_csv("student_lifestyle_100k.csv")

    validate_dataframe(df)

    # Convert Depression column
    if df[TARGET_COLUMN].dtype == object:
        df[TARGET_COLUMN] = df[TARGET_COLUMN].map({"True": True, "False": False})

    X, y = get_features_and_target(df)
    print(f"\n[Train] Dataset: {X.shape[0]} samples, {X.shape[1]} features")
    print(f"[Train] Target distribution:\n{y.value_counts(normalize=True)}")
    print(f"[Train] Class balance: {y.mean():.2%} positive (Depression=True)")

    # --- 2. Split data ---
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"[Train] Train: {len(X_train)}, Test: {len(X_test)}")

    # --- 3. Initialize W&B ---
    wandb_enabled = bool(WANDB_API_KEY)
    if wandb_enabled:
        wandb.login(key=WANDB_API_KEY)
        run = wandb.init(
            project=WANDB_PROJECT,
            name="rf-randomized-search",
            config={
                "model": "RandomForestClassifier",
                "search": "RandomizedSearchCV",
                "n_features": X.shape[1],
                "n_samples": X.shape[0],
                "test_size": TEST_SIZE,
                "random_state": RANDOM_STATE,
            },
        )
        print("[Train] W&B run initialized")
    else:
        print("[Train] W&B disabled (no API key). Running locally.")
        run = None

    # --- 4. Build pipeline and search ---
    preprocessor = build_preprocessor()
    base_model = RandomForestClassifier(random_state=RANDOM_STATE)
    pipeline = build_pipeline(preprocessor, base_model)
    param_dist = get_param_distributions()

    print("\n[Train] Starting RandomizedSearchCV (50 iterations, 3-fold CV)...")
    search = RandomizedSearchCV(
        pipeline,
        param_distributions=param_dist,
        n_iter=50,
        cv=3,
        scoring="roc_auc",
        n_jobs=-1,
        random_state=RANDOM_STATE,
        verbose=1,
        return_train_score=True,
    )
    search.fit(X_train, y_train)

    print(f"\n[Train] Best CV ROC-AUC: {search.best_score_:.4f}")
    print(f"[Train] Best params: {search.best_params_}")

    # --- 5. Evaluate on test set ---
    best_model = search.best_estimator_
    y_pred = best_model.predict(X_test)
    y_prob = best_model.predict_proba(X_test)[:, 1]

    metrics = evaluate_model(y_test, y_pred, y_prob)

    print("\n" + "=" * 40)
    print("TEST SET RESULTS")
    print("=" * 40)
    for name, value in metrics.items():
        print(f"  {name:>12s}: {value:.4f}")

    print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")

    cm = confusion_matrix(y_test, y_pred)
    print(f"Confusion Matrix:\n{cm}")

    # --- 6. Log to W&B ---
    if wandb_enabled and run:
        wandb.log(metrics)
        wandb.log({"best_cv_roc_auc": search.best_score_})
        wandb.log({"best_params": search.best_params_})

        # Log confusion matrix
        wandb.log({
            "confusion_matrix": wandb.plot.confusion_matrix(
                y_true=y_test.values,
                preds=y_pred,
                class_names=["No Depression", "Depression"],
            )
        })

        # Log ROC curve
        wandb.log({
            "roc_curve": wandb.plot.roc_curve(
                y_test.values, np.column_stack([1 - y_prob, y_prob]),
                labels=["No Depression", "Depression"],
            )
        })

    # --- 7. Save model ---
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)
    print(f"\n[Train] Best model saved to {MODEL_PATH}")

    # Save metrics to JSON
    metrics_path = os.path.join(MODEL_DIR, "metrics.json")
    metrics["best_params"] = {k: str(v) for k, v in search.best_params_.items()}
    metrics["best_cv_roc_auc"] = search.best_score_
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"[Train] Metrics saved to {metrics_path}")

    # Log model artifact to W&B
    if wandb_enabled and run:
        artifact = wandb.Artifact(
            name="best-model",
            type="model",
            description="Best RandomForest pipeline from RandomizedSearchCV",
        )
        artifact.add_file(MODEL_PATH)
        artifact.add_file(metrics_path)
        run.log_artifact(artifact)
        wandb.finish()
        print("[Train] Model artifact logged to W&B")

    print("\n[Train] Training pipeline complete!")
    return best_model, metrics


if __name__ == "__main__":
    train()
