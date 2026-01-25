"""
CLI Entry point for the NYC Taxi Data Ingestion Pipeline.
"""

import logging
import os
from typing import Optional

import dotenv
import typer
from rich.console import Console
from rich.logging import RichHandler

from app.schema import (
    TAXI_DATA_DTYPES,
    TAXI_DATA_PARSE_DATES,
    TAXI_ZONE_DTYPES,
)
from utils.db import get_engine
from utils.ingest import IngestStrategy, ingest_data


# Load environment variables
dotenv.load_dotenv()

# Initialize Rich console and logging
# Force terminal output for Docker.
console = Console(
    force_terminal=True,
)

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, console=console)],
)

logger = logging.getLogger("ingest_data")

app = typer.Typer(
    help="NYC Taxi Data Ingestion Tool",
)


@app.command()
def run(
    year: int = typer.Option(
        ...,
        help="Year of the taxi data",
    ),
    month: int = typer.Option(
        ...,
        help="Month of the taxi data",
    ),
    chunksize: Optional[int] = typer.Option(
        default=100_000,
        help="Chunk size for ingestion. Set to 0 to disable chunking.",
    ),
    if_exists: IngestStrategy = typer.Option(
        default=IngestStrategy.REPLACE,
        help="Strategy if table exists",
    ),
    pg_host: str = typer.Option(
        default=os.getenv("POSTGRES_HOST"),
        help="Postgres host",
    ),
    pg_port: int = typer.Option(
        default=os.getenv("POSTGRES_PORT"),
        help="Postgres port",
    ),
    pg_db: str = typer.Option(
        default=os.getenv("POSTGRES_DB"),
        help="Postgres database",
    ),
    pg_user: str = typer.Option(
        default=os.getenv("POSTGRES_USER"),
        help="Postgres user",
    ),
    pg_password: str = typer.Option(
        default=os.getenv("POSTGRES_PASSWORD"),
        help="Postgres password",
        show_default=False,
    ),
):
    """Downloads and ingests NYC Yellow Taxi data and Taxi Zone Lookup data."""
    # Adjust chunksize if 0 is passed
    actual_chunksize = chunksize if chunksize != 0 else None

    # Construct file paths
    taxi_data_url = (
        "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/"
        f"yellow/yellow_tripdata_{year}-{month:02d}.csv.gz"
    )
    
    taxi_zone_url = (
        "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/"
        "misc/taxi_zone_lookup.csv"
    )

    engine = None

    try:
        engine = get_engine(
            host=pg_host,
            port=pg_port,
            db=pg_db,
            user=pg_user,
            password=pg_password,
        )

        # Ingest Yellow Taxi Data
        ingest_data(
            filepath=taxi_data_url,
            engine=engine,
            target_table="yellow_taxi_data",
            if_exists=if_exists,
            chunksize=actual_chunksize,
            index=True,
            dtypes=TAXI_DATA_DTYPES,
            parse_dates=TAXI_DATA_PARSE_DATES,
        )

        # Ingest Taxi Zone Lookup (usually small, so we skip chunking)
        ingest_data(
            filepath=taxi_zone_url,
            engine=engine,
            target_table="taxi_zone_lookup",
            if_exists=IngestStrategy.SKIP,
            index=False,
            dtypes=TAXI_ZONE_DTYPES,
        )

        logger.info("Pipeline completed successfully!")

    except Exception as e:
        logger.critical(f"Pipeline failed: {e}")
        raise typer.Exit(code=1)

    finally:
        if engine:
            engine.dispose()
            logger.info("Database connection closed.")


if __name__ == "__main__":
    app()
