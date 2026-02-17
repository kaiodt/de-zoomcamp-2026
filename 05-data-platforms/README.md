# Module 05: Data Platforms

## Overview

This module focuses on **Data Platforms** using **Bruin**. Bruin is an end-to-end data platform that combines ingestion, transformation, orchestration, data quality checks, and lineage into a single tool. It simplifies the modern data stack by allowing you to manage code logic, configurations, and dependencies in one place.

## Prerequisites

- [Bruin CLI](https://getbruin.com/install/cli)
- [Bruin VS Code Extension](https://marketplace.visualstudio.com/items?itemName=Bruin.bruin) (or for Cursor)
- Basic knowledge of SQL and Python

## Key Concepts

### Bruin

Bruin unifies the data pipeline process:

- **Ingestion**: Extract data from various sources (APIs, databases) using Python or YAML assets.
- **Transformation**: Clean and model data using SQL with Jinja templating.
- **Orchestration**: Automatically manage dependencies and execution order based on asset lineage.
- **Data Quality**: Built-in data quality checks (unique, not null, custom queries) that run with the pipeline.

### Asset Types

- **Python Assets (`.py`)**: Scripts for complex logic, API interactions, or data extraction.
- **SQL Assets (`.sql`)**: Transformations running on the database (DuckDB in this module).
- **Ingestion Assets (`.asset.yml`)**: specialized YAML files for configuring data loading from sources like standard databases or flat files.

### DuckDB

We use **DuckDB** as the local embedded OLAP database for this module. It allows efficient processing of analytical queries on local files without requiring a cloud warehouse.

## Repository Structure

- [`bruin/`](./bruin): The root directory for the Bruin project.
    - [`.bruin.yml`](./bruin/.bruin.yml): Configuration for environments and connections (e.g., DuckDB).
    - [`my-taxi-pipeline/`](./bruin/my-taxi-pipeline): The main pipeline directory containing:
        - [`pipeline.yml`](./bruin/my-taxi-pipeline/pipeline.yml): Pipeline definition (schedule, start date).
        - [`assets/`](./bruin/my-taxi-pipeline/assets): logical grouping of assets.
            - `ingestion/`: Scripts to fetch data (e.g. `trips.py`) and seed files (`payment_lookup.asset.yml`).
            - `staging/`: SQL transformations (e.g. `trips.sql`).
            - `reports/`: Aggregation queries (e.g. `trips_report.sql`).

- [`class_notes/`](./class_notes): Detailed notes on Bruin concepts and pipeline construction.

- [`homework/`](./homework): Questions and answers for the Module 05 homework.

## Getting Started

1.  **Install Bruin CLI**:

    ```bash
    curl -LsSf https://getbruin.com/install/cli | sh
    ```

2.  **Navigate to the project directory**:

    ```bash
    cd bruin
    ```

3.  **Run the pipeline**:

    You can run the entire pipeline or specific assets.

    ```bash
    # Run the full pipeline for January 2022 (both taxi types)
    bruin run my-taxi-pipeline/pipeline/pipeline.yml \
      --start-date 2022-01-01 \
      --end-date 2022-02-01 \
      --var 'taxi_types=["yellow","green"]' \
      --config-file .bruin.yml \
      --full-refresh
    ```

4.  **Validate the pipeline**:

    Check for syntax errors and dependency issues.

    ```bash
    bruin validate my-taxi-pipeline/pipeline/pipeline.yml \
      --config-file .bruin.yml
    ```
