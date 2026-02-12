"""
FastAPI backend for student depression prediction.
Provides REST endpoints for prediction, health checks, and Prometheus metrics.

Usage:
    uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
"""
import os
import sys
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from api.schemas import StudentInput, PredictionResponse, HealthResponse, ErrorResponse  # noqa: E402
from api.metrics import (  # noqa: E402
    PREDICTION_REQUESTS_TOTAL,
    PREDICTION_RESULTS,
    PREDICTION_LATENCY,
    MODEL_LOADED,
    MODEL_INFO,
)
from src.predict import load_model, predict_single  # noqa: E402
from src.config import MODEL_PATH  # noqa: E402


# --- App Setup ---
app = FastAPI(
    title="Student Depression Prediction API",
    description=(
        "ML-powered API for predicting student depression risk "
        "based on lifestyle factors. Built with FastAPI and scikit-learn."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Model Loading ---
model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the model on application startup."""
    global model
    try:
        model = load_model(MODEL_PATH)
        MODEL_LOADED.set(1)
        MODEL_INFO.info({
            "version": "1.0.0",
            "algorithm": "RandomForest",
            "path": MODEL_PATH,
        })
        print("[API] Model loaded successfully")
    except FileNotFoundError:
        print(f"[API] WARNING: Model not found at {MODEL_PATH}. "
              "Run training first: python -m src.train")
        MODEL_LOADED.set(0)
    except Exception as e:
        print(f"[API] ERROR loading model: {e}")
        MODEL_LOADED.set(0)
    yield


# --- App Setup ---
app = FastAPI(
    title="Student Depression Prediction API",
    description=(
        "ML-powered API for predicting student depression risk "
        "based on lifestyle factors. Built with FastAPI and scikit-learn."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# --- Endpoints ---


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None,
        version="1.0.0",
    )


@app.post(
    "/predict",
    response_model=PredictionResponse,
    responses={500: {"model": ErrorResponse}},
    tags=["Prediction"],
)
async def predict(student: StudentInput):
    """
    Predict depression risk for a student based on lifestyle factors.

    Accepts student data and returns a prediction with confidence scores.
    """
    if model is None:
        PREDICTION_REQUESTS_TOTAL.labels(status="error").inc()
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please run training first.",
        )

    start_time = time.time()

    try:
        input_data = student.model_dump()
        result = predict_single(model, input_data)

        # Record metrics
        latency = time.time() - start_time
        PREDICTION_LATENCY.observe(latency)
        PREDICTION_REQUESTS_TOTAL.labels(status="success").inc()
        PREDICTION_RESULTS.labels(outcome=result["label"]).inc()

        return PredictionResponse(
            prediction=result["prediction"],
            label=result["label"],
            probability_no_depression=round(result["probability_no_depression"], 4),
            probability_depression=round(result["probability_depression"], 4),
            model_version="1.0.0",
        )

    except Exception as e:
        PREDICTION_REQUESTS_TOTAL.labels(status="error").inc()
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}",
        )


@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """Prometheus metrics endpoint."""
    return PlainTextResponse(
        content=generate_latest().decode("utf-8"),
        media_type=CONTENT_TYPE_LATEST,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
