"""
Database utilities for data pipelines.
"""

from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine


def get_engine(
    host: str,
    port: int,
    db: str,
    user: str,
    password: str,
) -> Engine:
    """Creates and returns a SQLAlchemy engine for PostgreSQL.

    Args:
        host: Database host.
        port: Database port.
        db: Database name.
        user: Database user.
        password: Database password.

    Returns:
        SQLAlchemy Engine object.

    Raises:
        ValueError: If any required database parameter is missing.
    """
    if not all([host, port, db, user, password]):
        db_params = {
            "host": host,
            "port": port,
            "db": db,
            "user": user,
            "password": password,
        }

        missing = [k for k, v in db_params.items() if not v]

        raise ValueError(
            f"Missing required database configuration: {', '.join(missing)}"
        )
    
    connection_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"

    return create_engine(connection_url)


def table_exists(engine: Engine, table_name: str) -> bool:
    """Checks if a table exists in the database.
    
    Args:
        engine: SQLAlchemy Engine object.
        table_name: Name of the table to check.

    Returns:
        bool: True if the table exists, False otherwise.
    """
    return inspect(engine).has_table(table_name)
