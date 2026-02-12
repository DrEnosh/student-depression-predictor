"""
Tests for FastAPI endpoints.
"""
import os
import sys
import numpy as np
import pandas as pd
import joblib

from fastapi.testclient import TestClient
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.config import NUMERICAL_FEATURES, CATEGORICAL_FEATURES, MODEL_DIR, MODEL_PATH  # noqa: E402


def _create_dummy_model():
    """Create and save a dummy model for testing."""
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

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return model


# Create model before importing app
_dummy_model = _create_dummy_model()

from api.main import app  # noqa: E402
import api.main as api_main_module  # noqa: E402

# Manually inject model since TestClient doesn't trigger on_event("startup")
api_main_module.model = _dummy_model

client = TestClient(app)


def _valid_payload():
    """Return a valid prediction payload."""
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


class TestAPIEndpoints:
    """Tests for FastAPI endpoints."""

    def test_health_endpoint(self):
        """Test GET /health returns 200 with expected fields."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "model_loaded" in data
        assert "version" in data

    def test_predict_valid_input(self):
        """Test POST /predict with valid input returns prediction."""
        response = client.post("/predict", json=_valid_payload())
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert "label" in data
        assert data["prediction"] in [0, 1]

    def test_predict_invalid_input_missing_field(self):
        """Test POST /predict with missing field returns 422."""
        payload = {"Age": 20, "Gender": "Male"}  # Missing fields
        response = client.post("/predict", json=payload)
        assert response.status_code == 422

    def test_predict_invalid_age_range(self):
        """Test POST /predict with out-of-range age returns 422."""
        payload = _valid_payload()
        payload["Age"] = 100  # Out of range
        response = client.post("/predict", json=payload)
        assert response.status_code == 422

    def test_metrics_endpoint(self):
        """Test GET /metrics returns Prometheus metrics."""
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "prediction_requests_total" in response.text or "python_info" in response.text
