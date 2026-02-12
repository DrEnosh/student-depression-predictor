"""
Tests for model inference logic.
"""
import pytest
import numpy as np
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

from src.config import NUMERICAL_FEATURES, CATEGORICAL_FEATURES
from src.predict import predict_single, predict_batch


@pytest.fixture
def dummy_model(tmp_path):
    """Create and save a dummy model for testing."""
    # Build a minimal pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERICAL_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
        ]
    )
    model = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(n_estimators=10, random_state=42)),
    ])

    # Fit on minimal dummy data
    X = pd.DataFrame({
        "Age": [20, 22, 19, 21, 23],
        "Gender": ["Male", "Female", "Male", "Female", "Male"],
        "Department": ["Science", "Engineering", "Arts", "Medical", "Business"],
        "CGPA": [3.5, 2.8, 3.0, 2.5, 3.2],
        "Sleep_Duration": [7.0, 6.0, 8.0, 5.0, 7.5],
        "Study_Hours": [4.0, 5.0, 3.0, 6.0, 4.5],
        "Social_Media_Hours": [2.0, 3.0, 1.5, 4.0, 2.5],
        "Physical_Activity": [100, 50, 120, 30, 80],
        "Stress_Level": [3, 7, 2, 8, 5],
    })
    y = np.array([0, 1, 0, 1, 0])
    model.fit(X, y)

    model_path = tmp_path / "test_model.joblib"
    joblib.dump(model, model_path)
    return model, str(model_path)


def _sample_input():
    """Return a sample student input dictionary."""
    return {
        "Age": 20,
        "Gender": "Male",
        "Department": "Engineering",
        "CGPA": 3.5,
        "Sleep_Duration": 7.0,
        "Study_Hours": 4.0,
        "Social_Media_Hours": 2.0,
        "Physical_Activity": 100,
        "Stress_Level": 3,
    }


class TestModelInference:
    """Tests for model inference."""

    def test_predict_single_returns_dict(self, dummy_model):
        """Test that predict_single returns a dictionary with expected keys."""
        model, _ = dummy_model
        result = predict_single(model, _sample_input())
        assert isinstance(result, dict)
        assert "prediction" in result
        assert "label" in result
        assert "probability_depression" in result
        assert "probability_no_depression" in result

    def test_predict_single_valid_prediction(self, dummy_model):
        """Test that prediction is 0 or 1."""
        model, _ = dummy_model
        result = predict_single(model, _sample_input())
        assert result["prediction"] in [0, 1]

    def test_predict_single_probabilities_sum_to_one(self, dummy_model):
        """Test that probabilities sum to approximately 1."""
        model, _ = dummy_model
        result = predict_single(model, _sample_input())
        total = result["probability_depression"] + result["probability_no_depression"]
        assert abs(total - 1.0) < 1e-6

    def test_predict_batch_returns_list(self, dummy_model):
        """Test that predict_batch returns a list of results."""
        model, _ = dummy_model
        inputs = [_sample_input(), _sample_input()]
        results = predict_batch(model, inputs)
        assert isinstance(results, list)
        assert len(results) == 2

    def test_predict_label_matches_prediction(self, dummy_model):
        """Test that label matches the prediction value."""
        model, _ = dummy_model
        result = predict_single(model, _sample_input())
        if result["prediction"] == 1:
            assert result["label"] == "Depression"
        else:
            assert result["label"] == "No Depression"
