import sys
import argparse
import logging
from pathlib import Path

import duckdb
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"


def download_and_convert_files(taxi_type: str, years: list[int]):
    """Downloads and converts taxi trip data files to Parquet.

    Downloads CSV.gz files from the NYC TLC data repository and converts
    them to Parquet format using DuckDB.

    Args:
        taxi_type (str): The type of taxi data to download (e.g., 'yellow',
            'green', 'fhv').
        years (list[int]): The years to download data for.
    """
    data_dir = Path("data") / taxi_type

    try:
        data_dir.mkdir(exist_ok=True, parents=True)
    except OSError as e:
        logger.error(f"Failed to create directory {data_dir}: {e}")
        return

    for year in years:
        for month in range(1, 13):
            parquet_filename = (
                f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
            )
            parquet_filepath = data_dir / parquet_filename

            if parquet_filepath.exists():
                logger.info(
                    f"Skipping {parquet_filename} (already exists)"
                )
                continue

            # Download CSV.gz file
            csv_gz_filename = (
                f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
            )
            csv_gz_filepath = data_dir / csv_gz_filename
            url = f"{BASE_URL}/{taxi_type}/{csv_gz_filename}"

            try:
                logger.info(f"Downloading {url}...")

                response = requests.get(url, stream=True)
                response.raise_for_status()

                with open(csv_gz_filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

            except requests.RequestException as e:
                logger.error(f"Failed to download {url}: {e}")
                continue

            except OSError as e:
                logger.error(f"Failed to save {csv_gz_filename}: {e}")
                continue

            logger.info(f"Converting {csv_gz_filename} to Parquet...")

            try:
                con = duckdb.connect()
                # Auto-detect schema from CSV
                con.execute(f"""
                    COPY (
                      SELECT *
                      FROM read_csv_auto('{csv_gz_filepath}')
                    )
                    TO '{parquet_filepath}' (FORMAT PARQUET)
                """)
                con.close()

                # Remove the CSV.gz file to save space
                csv_gz_filepath.unlink()

                logger.info(f"Completed {parquet_filename}")

            except Exception as e:
                logger.error(
                    f"Failed to convert {csv_gz_filename} to parquet: {e}"
                )

                if csv_gz_filepath.exists():
                    csv_gz_filepath.unlink()


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Ingest NYC Taxi data into DuckDB."
    )

    parser.add_argument(
        "dataset",
        choices=["nyc-tlc", "nyc-fhv"],
        help=(
            "The dataset to ingest: 'nyc-tlc' (Yellow/Green 2019-2020) "
            "or 'nyc-fhv' (FHV 2019)."
        ),
    )

    args = parser.parse_args()

    # Define configuration based on chosen dataset
    if args.dataset == "nyc-tlc":
        configs = [
            {"type": "yellow", "years": [2019, 2020]},
            {"type": "green", "years": [2019, 2020]}
        ]
    elif args.dataset == "nyc-fhv":
        configs = [
            {"type": "fhv", "years": [2019]}
        ]
    else:
        # Should not happen due to argparse choices, but good for safety
        logger.error(f"Unknown dataset: {args.dataset}")
        sys.exit(1)

    # 1. Download and convert files
    for config in configs:
        download_and_convert_files(config["type"], config["years"])

    # 2. Load into DuckDB
    try:
        con = duckdb.connect("taxi_rides_ny.duckdb")
        con.execute("CREATE SCHEMA IF NOT EXISTS prod")

        for config in configs:
            taxi_type = config["type"]
            table_name = f"{taxi_type}_tripdata"
            
            logger.info(f"Creating table prod.{table_name}...")

            # Use union_by_name to handle potential schema evolution
            con.execute(f"""
                CREATE OR REPLACE TABLE prod.{table_name} AS
                SELECT *
                FROM read_parquet(
                  'data/{taxi_type}/*.parquet',
                  union_by_name=true
                )
            """)

        con.close()
        logger.info(f"Database update completed for {args.dataset}.")

    except Exception as e:
        logger.error(f"Database operation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
