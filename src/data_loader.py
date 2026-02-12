"""
Data loader module.
Provides functions to load the student lifestyle dataset
from Neon Postgres or a local CSV fallback.
"""
import pandas as pd
from sqlalchemy import create_engine, text

from src.config import DATABASE_URL, TABLE_NAME, FEATURE_COLUMNS, TARGET_COLUMN


def load_data_from_postgres(database_url: str = None) -> pd.DataFrame:
    """
    Load the student lifestyle dataset from Neon Postgres.

    Args:
        database_url: Optional override for the database connection string.

    Returns:
        pd.DataFrame with all rows from the student_lifestyle table.
    """
    url = database_url or DATABASE_URL
    engine = create_engine(url)

    query = text(f"SELECT * FROM {TABLE_NAME}")  # noqa: S608
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    print(f"[DataLoader] Loaded {len(df)} rows from Postgres table '{TABLE_NAME}'")
    return df


def load_data_from_csv(filepath: str = "data/student_lifestyle_100k.csv") -> pd.DataFrame:
    """
    Fallback: load the dataset from a local CSV file.

    Args:
        filepath: Path to the CSV file.

    Returns:
        pd.DataFrame with all rows from the CSV.
    """
    df = pd.read_csv(filepath)
    print(f"[DataLoader] Loaded {len(df)} rows from CSV '{filepath}'")
    return df


def get_features_and_target(df: pd.DataFrame):
    """
    Split a DataFrame into features (X) and target (y).

    Args:
        df: Input DataFrame containing feature and target columns.

    Returns:
        Tuple of (X, y) where X is a DataFrame of features and y is a Series.
    """
    x = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].astype(int).copy()
    return x, y


def validate_dataframe(df: pd.DataFrame) -> bool:
    """
    Validate that the DataFrame has the required columns and no critical issues.

    Args:
        df: Input DataFrame to validate.

    Returns:
        True if valid, raises ValueError otherwise.
    """
    required_cols = FEATURE_COLUMNS + [TARGET_COLUMN]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    null_counts = df[required_cols].isnull().sum()
    cols_with_nulls = null_counts[null_counts > 0]
    if len(cols_with_nulls) > 0:
        print(f"[DataLoader] Warning: columns with nulls:\n{cols_with_nulls}")

    return True
