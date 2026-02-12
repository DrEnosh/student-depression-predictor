"""
Prometheus metrics for the FastAPI backend.
Tracks request counts, latency, and prediction outcomes.
"""
from prometheus_client import Counter, Histogram, Gauge, Info

# --- Counters ---
PREDICTION_REQUESTS_TOTAL = Counter(
    "prediction_requests_total",
    "Total number of prediction requests",
    ["status"],
)

PREDICTION_RESULTS = Counter(
    "prediction_results_total",
    "Prediction results by outcome",
    ["outcome"],
)

# --- Histograms ---
PREDICTION_LATENCY = Histogram(
    "prediction_latency_seconds",
    "Prediction request latency in seconds",
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)

# --- Gauges ---
MODEL_LOADED = Gauge(
    "model_loaded",
    "Whether the ML model is currently loaded (1=yes, 0=no)",
)

# --- Info ---
MODEL_INFO = Info(
    "model",
    "Information about the loaded model",
)
