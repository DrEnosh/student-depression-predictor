"""
Configuration module for the ML classification pipeline.
Defines feature columns, model parameters, and environment settings.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
_project_root = Path(__file__).resolve().parent.parent
load_dotenv(_project_root / ".env", override=True)

# --- Database ---
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/student_db"
)
TABLE_NAME = "student_lifestyle"

# --- Feature Engineering ---
TARGET_COLUMN = "Depression"
ID_COLUMN = "Student_ID"

NUMERICAL_FEATURES = [
    "Age",
    "CGPA",
    "Sleep_Duration",
    "Study_Hours",
    "Social_Media_Hours",
    "Physical_Activity",
    "Stress_Level",
]

CATEGORICAL_FEATURES = [
    "Gender",
    "Department",
]

FEATURE_COLUMNS = NUMERICAL_FEATURES + CATEGORICAL_FEATURES

# --- Model ---
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "best_model.joblib")
RANDOM_STATE = 42
TEST_SIZE = 0.2

# --- W&B ---
WANDB_API_KEY = os.getenv("WANDB_API_KEY", "")
WANDB_PROJECT = os.getenv("WANDB_PROJECT", "student-depression-classifier")

# --- API ---
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_URL = os.getenv("API_URL", "http://localhost:8000")
