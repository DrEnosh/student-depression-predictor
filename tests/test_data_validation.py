"""
Tests for data validation logic.
"""
import pytest
import pandas as pd
from src.data_loader import validate_dataframe, get_features_and_target
from src.config import FEATURE_COLUMNS, TARGET_COLUMN


def _make_valid_df():
    """Create a valid test DataFrame."""
    return pd.DataFrame({
        "Student_ID": [1, 2, 3],
        "Age": [20, 21, 22],
        "Gender": ["Male", "Female", "Male"],
        "Department": ["Science", "Engineering", "Arts"],
        "CGPA": [3.5, 2.8, 3.0],
        "Sleep_Duration": [7.0, 6.5, 8.0],
        "Study_Hours": [4.0, 5.0, 3.0],
        "Social_Media_Hours": [2.0, 3.0, 1.5],
        "Physical_Activity": [100, 80, 120],
        "Stress_Level": [3, 5, 7],
        "Depression": [0, 1, 0],
    })


class TestDataValidation:
    """Tests for data validation."""

    def test_valid_dataframe_passes(self):
        """Test that a valid DataFrame passes validation."""
        df = _make_valid_df()
        assert validate_dataframe(df) is True

    def test_missing_columns_raises_error(self):
        """Test that missing required columns raise ValueError."""
        df = pd.DataFrame({"Age": [20], "Gender": ["Male"]})
        with pytest.raises(ValueError, match="Missing required columns"):
            validate_dataframe(df)

    def test_features_and_target_split(self):
        """Test correct feature/target split."""
        df = _make_valid_df()
        x, y = get_features_and_target(df)
        assert list(x.columns) == FEATURE_COLUMNS
        assert y.name == TARGET_COLUMN
        assert len(x) == len(y) == 3

    def test_target_is_integer(self):
        """Test that target column is converted to int."""
        df = _make_valid_df()
        _, y = get_features_and_target(df)
        assert y.dtype in ["int64", "int32"]

    def test_empty_dataframe_raises_error(self):
        """Test that an empty DataFrame raises ValueError."""
        df = pd.DataFrame()
        with pytest.raises(ValueError):
            validate_dataframe(df)
