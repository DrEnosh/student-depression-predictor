"""
Script to load the student lifestyle CSV into Neon Postgres.
Usage:
    python data/load_to_postgres.py
"""
import os
import sys

import pandas as pd
from sqlalchemy import create_engine

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.config import DATABASE_URL, TABLE_NAME  # noqa: E402


def load_csv_to_postgres(
    csv_path: str = None,
    database_url: str = None,
    table_name: str = None,
):
    """
    Read the CSV dataset and upload it to Neon Postgres.

    Args:
        csv_path: Path to the CSV file.
        database_url: Postgres connection URL.
        table_name: Target table name.
    """
    csv_path = csv_path or os.path.join(
        os.path.dirname(__file__), "student_lifestyle_100k.csv"
    )
    database_url = database_url or DATABASE_URL
    table_name = table_name or TABLE_NAME

    # Read CSV
    print(f"[Loader] Reading CSV from {csv_path} ...")
    df = pd.read_csv(csv_path)
    print(f"[Loader] Loaded {len(df)} rows, {len(df.columns)} columns")
    print(f"[Loader] Columns: {list(df.columns)}")
    print(f"[Loader] Dtypes:\n{df.dtypes}")

    # Convert Depression boolean strings to actual booleans
    if df["Depression"].dtype == object:
        df["Depression"] = df["Depression"].map({"True": True, "False": False})

    # Create engine and upload
    print(f"\n[Loader] Connecting to Postgres ...")
    engine = create_engine(database_url)

    print(f"[Loader] Uploading to table '{table_name}' ...")
    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=5000,
    )
    print(f"[Loader] Successfully uploaded {len(df)} rows to '{table_name}'")

    # Verify
    with engine.connect() as conn:
        from sqlalchemy import text
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))  # noqa: S608
        count = result.scalar()
        print(f"[Loader] Verification: {count} rows in table '{table_name}'")


if __name__ == "__main__":
    load_csv_to_postgres()
