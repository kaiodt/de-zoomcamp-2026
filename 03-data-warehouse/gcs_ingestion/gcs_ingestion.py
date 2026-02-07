import logging
import os
from enum import Enum
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm

from gcs_utils import (
    check_bucket_exists,
    create_bucket,
    download_file,
    file_exists_in_gcs,
    get_gcs_client,
    standardize_parquet,
    upload_to_gcs,
)


# Initialize Typer and Rich
app = typer.Typer(rich_markup_mode="rich")
console = Console()

# Configure logging with Rich
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("rich")

# Constants
CREDENTIALS_FILE = "service-account.json"
DEFAULT_BUCKET = os.environ.get("GCS_BUCKET_NAME", "nyc-taxi-tripdata")
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"


class TaxiService(str, Enum):
    YELLOW = "yellow"
    GREEN = "green"


def process_month(
    client,
    service: str,
    year: str,
    month: str,
    bucket: str,
    force: bool = False
) -> None:
    """Processes a single month of data."""
    file_name = f"{service}_tripdata_{year}-{month}.parquet"
    url = f"{BASE_URL}/{file_name}"
    local_path = Path(file_name)
    gcs_path = f"{service}/{file_name}"

    try:
        # Check if file exists in GCS
        if file_exists_in_gcs(client, bucket, gcs_path):
            if not force and not Confirm.ask(
                f"[yellow]File {gcs_path} exists in GCS. Replace it?[/yellow]"
            ):
                console.print(f"[cyan]Skipping {file_name}[/cyan]")
                return

        # Download and Upload with progress indicator
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description=f"Processing {file_name}...", total=None
            )

            download_file(url, local_path)
            standardize_parquet(local_path, service)
            upload_to_gcs(client, bucket, gcs_path, local_path)

        console.print(f"[green]✅ Successful:[/green] {service}/{file_name}")

    except Exception as e:
        console.print(f"[red]❌ Error processing {file_name}:[/red] {e}")
    finally:
        if local_path.exists():
            local_path.unlink()


@app.command()
def ingest(
    service: TaxiService = typer.Option(
        ..., "--service", "-s", help="Taxi service type (yellow or green)"
    ),
    year: str = typer.Option(
        ..., "--year", "-Y", help="Year of the data (e.g., 2019)"
    ),
    month: Optional[int] = typer.Option(
        None, "--month", "-m", help="Month (1-12). If omitted, all months."
    ),
    bucket: str = typer.Option(
        DEFAULT_BUCKET, "--bucket", "-b", help="GCS bucket name"
    ),
    yes: bool = typer.Option(
        False, "--yes", "-y", help="Skip all confirmation prompts"
    ),
):
    """
    [bold blue]Ingest NYC Taxi trip data from web to GCS.[/bold blue]
    """
    client = get_gcs_client(CREDENTIALS_FILE)

    # Bucket creation logic
    if not check_bucket_exists(client, bucket):
        if yes or Confirm.ask(
            f"[bold red]Bucket '{bucket}' not found. Create it?[/bold red]"
        ):
            create_bucket(client, bucket)
        else:
            console.print("[bold red]Aborting:[/bold red] Bucket is required.")
            raise typer.Exit(code=1)

    # Month logic
    if month:
        months = [f"{month:02d}"]
    else:
        months = [f"{m:02d}" for m in range(1, 13)]

    console.print(
        f"🚀 [bold]Starting ingestion for {service.value} {year}[/bold] "
        f"({len(months)} months)"
    )

    for m in months:
        process_month(client, service.value, year, m, bucket, force=yes)

    console.print(
        "\n[bold green]✨ All requested datasets processed![/bold green]"
    )


if __name__ == "__main__":
    app()
