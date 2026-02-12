"""
Prediction helper module.
Loads the trained model and provides prediction functions.
"""
import joblib
import pandas as pd

from src.config import MODEL_PATH, FEATURE_COLUMNS


def load_model(model_path: str = None):
    """Load the trained model pipeline from disk."""
    path = model_path or MODEL_PATH
    model = joblib.load(path)
    print(f"[Predict] Model loaded from {path}")
    return model


def predict_single(model, input_data: dict) -> dict:
    """
    Make a prediction for a single student.

    Args:
        model: Trained sklearn pipeline.
        input_data: Dictionary with feature values.

    Returns:
        Dictionary with prediction, probability, and label.
    """
    df = pd.DataFrame([input_data])[FEATURE_COLUMNS]
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0]

    return {
        "prediction": int(prediction),
        "probability_no_depression": float(probability[0]),
        "probability_depression": float(probability[1]),
        "label": "Depression" if prediction == 1 else "No Depression",
    }


def predict_batch(model, input_data: list) -> list:
    """
    Make predictions for a batch of students.

    Args:
        model: Trained sklearn pipeline.
        input_data: List of dictionaries with feature values.

    Returns:
        List of prediction result dictionaries.
    """
    df = pd.DataFrame(input_data)[FEATURE_COLUMNS]
    predictions = model.predict(df)
    probabilities = model.predict_proba(df)

    results = []
    for pred, prob in zip(predictions, probabilities):
        results.append({
            "prediction": int(pred),
            "probability_no_depression": float(prob[0]),
            "probability_depression": float(prob[1]),
            "label": "Depression" if pred == 1 else "No Depression",
        })
    return results
