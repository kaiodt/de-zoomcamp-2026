"""
Data ingestion utils.
"""

import logging
from enum import Enum
from typing import Optional

import pandas as pd
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
)
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from utils.db import table_exists


logger = logging.getLogger(__name__)

# Force terminal output for Docker environments to ensure progress bars
# and colors are displayed correctly.
console = Console(
    force_terminal=True,
)


class IngestStrategy(str, Enum):
    """Strategies for handling existing tables in the database."""
    REPLACE = "replace"
    APPEND = "append"
    SKIP = "skip"


def _ingest_chunked(
    filepath: str,
    engine: Engine,
    target_table: str,
    if_exists: IngestStrategy,
    chunksize: int,
    index: bool,
    dtypes: Optional[dict],
    parse_dates: Optional[list],
) -> None:
    """Handles data ingestion in chunks with a progress bar.
    
    Args:
        filepath: Path or URL to the source data file (e.g., CSV).
        engine: SQLAlchemy engine for database connection.
        target_table: Name of the table to insert data into.
        if_exists: How to behave if the table already exists.
        chunksize: Number of rows to process per chunk. If None, process the
            whole file at once.
        index: Whether to write the index column to the database.
        dtypes: Dictionary mapping column names to data types.
        parse_dates: List of column names to parse as datetime objects.
    """
    df_iter = pd.read_csv(
        filepath,
        dtype=dtypes,
        parse_dates=parse_dates,
        chunksize=chunksize,
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(
            f"Ingesting into {target_table}...", total=None,
        )
        
        first_chunk = True

        for chunk in df_iter:
            # For the very first chunk, we use the specified
            # if_exists strategy. For subsequent chunks, we MUST
            # use "append" to avoid overwriting previous chunks.
            if first_chunk:
                # Pandas doesn't support "skip", but we've already checked
                # table existence. If we're here with SKIP, the table
                # doesn't exist, so we use "replace" (which creates it).
                current_if_exists = (
                    "replace"
                    if if_exists == IngestStrategy.SKIP
                    else if_exists.value
                )
            else:
                current_if_exists = "append"
            
            chunk.to_sql(
                name=target_table,
                con=engine,
                if_exists=current_if_exists,
                index=index,
            )
            
            first_chunk = False
            progress.update(task, advance=1)

    logger.info(
        f"Successfully ingested data into '{target_table}' in chunks."
    )


def _ingest_single_shot(
    filepath: str,
    engine: Engine,
    target_table: str,
    if_exists: IngestStrategy,
    index: bool,
    dtypes: Optional[dict],
    parse_dates: Optional[list],
) -> None:
    """Handles data ingestion for the entire file at once.
    
    Args:
        filepath: Path or URL to the source data file (e.g., CSV).
        engine: SQLAlchemy engine for database connection.
        target_table: Name of the table to insert data into.
        if_exists: How to behave if the table already exists.
        index: Whether to write the index column to the database.
        dtypes: Dictionary mapping column names to data types.
        parse_dates: List of column names to parse as datetime objects.
    """
    logger.info("Reading entire file into memory (no chunking)...")

    df = pd.read_csv(
        filepath,
        dtype=dtypes,
        parse_dates=parse_dates,
    )
    
    # Mapping SKIP to REPLACE for internal pandas call.
    # (Since we already checked existence in the coordinator).
    pandas_if_exists = (
        "replace" if if_exists == IngestStrategy.SKIP else if_exists.value
    )

    df.to_sql(
        name=target_table,
        con=engine,
        if_exists=pandas_if_exists,
        index=index,
    )
    logger.info(
        f"Successfully ingested data into '{target_table}' (single shot)."
    )


def ingest_data(
    filepath: str,
    engine: Engine,
    target_table: str,
    if_exists: IngestStrategy = IngestStrategy.REPLACE,
    chunksize: Optional[int] = None,
    index: Optional[bool] = False,
    dtypes: Optional[dict] = None,
    parse_dates: Optional[list] = None,
) -> None:
    """Ingests data from a file into a database table.

    Args:
        filepath: Path or URL to the source data file (e.g., CSV).
        engine: SQLAlchemy engine for database connection.
        target_table: Name of the table to insert data into.
        if_exists: How to behave if the table already exists.
        chunksize: Number of rows to process per chunk. If None, process the
            whole file at once.
        index: Whether to write the index column to the database.
        dtypes: Dictionary mapping column names to data types.
        parse_dates: List of column names to parse as datetime objects.

    Raises:
        SQLAlchemyError: If a database error occurs during ingestion.
        FileNotFoundError: If the local filepath does not exist.
        Exception: For other unexpected errors.
    """
    logger.info(f"Starting ingestion for '{target_table}' from '{filepath}'")

    if (
        if_exists == IngestStrategy.SKIP
        and table_exists(engine, target_table)
    ):
        logger.info(
            f"Table '{target_table}' already exists, skipping ingestion."
        )
        return
    
    try:
        if chunksize:
            _ingest_chunked(
                filepath=filepath,
                engine=engine,
                target_table=target_table,
                if_exists=if_exists,
                chunksize=chunksize,
                index=index,
                dtypes=dtypes,
                parse_dates=parse_dates,
            )
        else:
            _ingest_single_shot(
                filepath=filepath,
                engine=engine,
                target_table=target_table,
                if_exists=if_exists,
                index=index,
                dtypes=dtypes,
                parse_dates=parse_dates,
            )

    except SQLAlchemyError as e:
        logger.error(
            f"Database error during ingestion into '{target_table}': {e}"
        )
        raise

    except Exception as e:
        logger.error(
            f"Unexpected error during ingestion into '{target_table}': {e}"
        )
        raise
