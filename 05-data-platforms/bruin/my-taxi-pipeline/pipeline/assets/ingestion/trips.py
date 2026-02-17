"""@bruin
name: ingestion.trips
connection: duckdb-default
image: python:3.11

materialization:
  type: table
  strategy: append

@bruin"""

import os
import json
import io
import requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


# NYC TLC data endpoint
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/"


def get_month_range(
    start_date: datetime,
    end_date: datetime,
) -> list[tuple[int, int]]:
    """
    Yields (year, month) tuples for each month in the range.
    """
    current_date = start_date.replace(day=1)

    while current_date <= end_date:
        yield current_date.year, current_date.month
        current_date += relativedelta(months=1)


def build_url(
    taxi_type: str,
    year: int,
    month: int,
) -> str:
    """
    Constructs the download URL for a specific taxi type and month.
    """
    return f"{BASE_URL}{taxi_type}_tripdata_{year}-{month:02d}.parquet"


def normalize_schema(df: pd.DataFrame, taxi_type: str) -> pd.DataFrame:
    """
    Normalizes columns and data types to ensure consistent schema.
    """
    # Normalize datetime columns
    df = df.rename(columns={
        'tpep_pickup_datetime': 'pickup_datetime',
        'lpep_pickup_datetime': 'pickup_datetime',
        'tpep_dropoff_datetime': 'dropoff_datetime',
        'lpep_dropoff_datetime': 'dropoff_datetime'
    })

    # Add missing columns for Yellow taxi
    if taxi_type == 'yellow':
        df['trip_type'] = 1
        df['ehail_fee'] = 0.0

    # Convert all datetime columns to string (Windows/PyArrow fix)
    dt_cols = df.select_dtypes(include=['datetime', 'datetimetz']).columns
    for col in dt_cols:
        df[col] = df[col].astype(str)

    return df


def fetch_dataset(
    taxi_type: str,
    year: int,
    month: int
) -> pd.DataFrame:
    """
    Fetches and processes a single month of data.
    """
    url = build_url(taxi_type, year, month)
    print(f"Fetching: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()

        # Read parquet
        df = pd.read_parquet(io.BytesIO(response.content))

        # Add metadata
        df['extracted_at'] = datetime.now().isoformat()
        df['source_url'] = url
        df['taxi_type'] = taxi_type

        # Normalize
        df = normalize_schema(df, taxi_type)

        print(f"Successfully fetched {len(df)} rows")
        return df

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return pd.DataFrame()


def fetch_trips(
    taxi_types: list[str],
    start_date: datetime,
    end_date: datetime,
) -> pd.DataFrame:
    """
    Iterates through taxi types and date range to fetch trip data.
    Returns a concatenated DataFrame.
    """
    dfs = []

    for taxi_type in taxi_types:
        print(f"Processing taxi type: {taxi_type}")
        for year, month in get_month_range(start_date, end_date):
            df = fetch_dataset(taxi_type, year, month)
            if not df.empty:
                dfs.append(df)

    if not dfs:
        print("No data fetched")
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)


def materialize() -> pd.DataFrame:
    """
    Main entry point for Bruin.
    """
    start_date_str = os.getenv('BRUIN_START_DATE')
    end_date_str = os.getenv('BRUIN_END_DATE')
    bruin_vars_str = os.getenv('BRUIN_VARS', '{}')

    if not start_date_str or not end_date_str:
        raise ValueError("BRUIN_START_DATE and BRUIN_END_DATE must be set")

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    bruin_vars = json.loads(bruin_vars_str)
    taxi_types = bruin_vars.get('taxi_types', ['yellow'])

    print(
        f"Ingesting data for {taxi_types} from "
        f"{start_date_str} to {end_date_str}"
    )

    df = fetch_trips(taxi_types, start_date, end_date)

    print(f"Total rows ingested: {len(df)}")

    return df
