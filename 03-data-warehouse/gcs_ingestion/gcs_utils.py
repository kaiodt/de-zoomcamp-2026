import logging
from pathlib import Path

import pandas as pd
import requests
from google.cloud import storage
from google.cloud.exceptions import NotFound

from schema import TAXI_SCHEMAS

logger = logging.getLogger(__name__)


def get_gcs_client(credentials_path: str) -> storage.Client:
    """
    Creates and returns a GCS client using a service account JSON file.

    Args:
        credentials_path (str): Path to the service account JSON file.

    Returns:
        storage.Client: The authenticated GCS client.
    """
    if not Path(credentials_path).exists():
        logger.warning(f"Credentials file {credentials_path} not found.")
        logger.warning("Falling back to default credentials.")
        return storage.Client()
    return storage.Client.from_service_account_json(credentials_path)


def check_bucket_exists(client: storage.Client, bucket_name: str) -> bool:
    """
    Checks if a GCS bucket exists.

    Args:
        client (storage.Client): The GCS client.
        bucket_name (str): The name of the bucket.

    Returns:
        bool: True if it exists, False otherwise.
    """
    try:
        client.get_bucket(bucket_name)
        return True
    except NotFound:
        return False


def create_bucket(client: storage.Client, bucket_name: str) -> None:
    """
    Creates a GCS bucket.

    Args:
        client (storage.Client): The GCS client.
        bucket_name (str): The name of the bucket to create.
    """
    client.create_bucket(bucket_name)
    logger.info(f"Bucket '{bucket_name}' created.")


def file_exists_in_gcs(
    client: storage.Client,
    bucket_name: str,
    blob_name: str
) -> bool:
    """
    Checks if a file (blob) already exists in the given GCS bucket.

    Args:
        client (storage.Client): The GCS client.
        bucket_name (str): Target bucket name.
        blob_name (str): Path in GCS.

    Returns:
        bool: True if exists, False otherwise.
    """
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    return blob.exists()


def upload_to_gcs(
    client: storage.Client,
    bucket_name: str,
    destination_blob_name: str,
    source_file_path: Path
) -> None:
    """
    Uploads a local file to GCS.

    Args:
        client (storage.Client): The GCS client.
        bucket_name (str): Target bucket name.
        destination_blob_name (str): Destination path in GCS.
        source_file_path (Path): Path to the local file.
    """
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(str(source_file_path))


def download_file(url: str, local_path: Path) -> None:
    """
    Downloads a file from a URL with basic error handling.

    Args:
        url (str): Source URL.
        local_path (Path): Destination local path.
    """
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()
    with open(local_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


def standardize_parquet(file_path: Path, service: str) -> None:
    """
    Reads a parquet file, applies a strict schema, and overwrites it.
    This ensures consistency for BigQuery external tables.

    Args:
        file_path (Path): Path to the local parquet file.
        service (str): Taxi service type (yellow or green).
    """
    schema = TAXI_SCHEMAS.get(service)
    if not schema:
        logger.warning(
            f"No schema found for service: {service}. "
            "Skipping standardization."
        )
        return

    logger.info(f"Standardizing schema for {file_path.name}...")
    df = pd.read_parquet(file_path)

    # Ensure all schema columns exist
    for col, dtype in schema.items():
        if col not in df.columns:
            df[col] = pd.Series(dtype=dtype)

    # Cast columns and handle datetimes
    for col, dtype in schema.items():
        try:
            if "datetime" in str(dtype):
                df[col] = pd.to_datetime(df[col])
            else:
                df[col] = df[col].astype(dtype)
        except Exception as e:
            logger.warning(f"Could not cast column {col} to {dtype}: {e}")

    # Reorder columns to match schema exactly
    df = df[list(schema.keys())]

    # Save back to the same path
    df.to_parquet(file_path, index=False)
