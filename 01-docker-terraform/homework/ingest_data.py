import click
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


# Load environment variables from .env file
load_dotenv()


@click.command()
@click.option(
    "--pg-user",
    default=os.getenv("POSTGRES_USER"),
    help="PostgreSQL user",
)
@click.option(
    "--pg-pass",
    default=os.getenv("POSTGRES_PASSWORD"),
    help="PostgreSQL password",
)
@click.option(
    "--pg-host",
    default=os.getenv("POSTGRES_HOST"),
    help="PostgreSQL host",
)
@click.option(
    "--pg-port",
    type=int,
    default=os.getenv("POSTGRES_PORT"),
    help="PostgreSQL port",
)
@click.option(
    "--pg-db",
    default=os.getenv("POSTGRES_DB"),
    help="PostgreSQL database name",
)
@click.option(
    "--target-table",
    default="green_taxi_data",
    help="Target table name",
)
@click.option(
    "--year",
    type=int,
    help="Year of the data",
)
@click.option(
    "--month",
    type=int,
    help="Month of the data",
)
def run(
    pg_user: str,
    pg_pass: str,
    pg_host: str,
    pg_port: int,
    pg_db: str,
    target_table: str,
    year: int,
    month: int,
):
    """Ingest data into PostgreSQL database."""

    engine = create_engine(
        f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    )

    # Ingest Green Taxi Data
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"
    file_name = f"green_tripdata_{year}-{month:02d}.parquet"
    url = f"{base_url}/{file_name}"

    df = pd.read_parquet(url)

    df.to_sql(
        name=target_table,
        con=engine,
        if_exists="replace",
    )

    # Ingest Taxi Zone Data
    url = (
        "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/"
        "misc/taxi_zone_lookup.csv"
    )

    df = pd.read_csv(url)

    df.to_sql(
        name="taxi_zone_data",
        con=engine,
        if_exists="replace",
    )


if __name__ == "__main__":
    run()
