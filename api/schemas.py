"""
Pydantic models for FastAPI request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional


class StudentInput(BaseModel):
    """Input schema for student depression prediction."""

    Age: int = Field(..., ge=15, le=30, description="Student age (15-30)")
    Gender: str = Field(..., description="Gender: Male or Female")
    Department: str = Field(
        ...,
        description="Department: Science, Engineering, Medical, Arts, or Business",
    )
    CGPA: float = Field(..., ge=0.0, le=4.0, description="CGPA (0.0-4.0)")
    Sleep_Duration: float = Field(
        ..., ge=0.0, le=15.0, description="Sleep duration in hours"
    )
    Study_Hours: float = Field(
        ..., ge=0.0, le=15.0, description="Daily study hours"
    )
    Social_Media_Hours: float = Field(
        ..., ge=0.0, le=15.0, description="Daily social media hours"
    )
    Physical_Activity: float = Field(
        ..., ge=0, le=200, description="Physical activity score (0-200)"
    )
    Stress_Level: int = Field(
        ..., ge=0, le=10, description="Stress level (0-10)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
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
            ]
        }
    }


class PredictionResponse(BaseModel):
    """Response schema for prediction results."""

    prediction: int = Field(..., description="0 = No Depression, 1 = Depression")
    label: str = Field(..., description="Human-readable prediction label")
    probability_no_depression: float = Field(
        ..., description="Probability of no depression"
    )
    probability_depression: float = Field(
        ..., description="Probability of depression"
    )
    model_version: str = Field(default="1.0.0", description="Model version")


class HealthResponse(BaseModel):
    """Response schema for health check."""

    status: str = Field(default="healthy")
    model_loaded: bool = Field(..., description="Whether the model is loaded")
    version: str = Field(default="1.0.0")


class ErrorResponse(BaseModel):
    """Response schema for errors."""

    error: str
    detail: Optional[str] = None
