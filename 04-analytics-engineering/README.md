# Module 4: Analytics Engineering

## Overview

This module focuses on **Analytics Engineering** using **dbt (data build tool)** and **DuckDB**. It covers the transformation of raw data into analytics-ready models, implementing **dimensional modeling** concepts (Facts and Dimensions), and applying software engineering best practices to data pipelines (testing, documentation, version control).

## Prerequisites

- [uv](https://github.com/astral-sh/uv) (Python package manager)
- [DuckDB CLI](https://duckdb.org/install/?platform=windows&environment=cli)
- Basic knowledge of SQL

## Key Concepts

### Analytics Engineering

The practice of bringing software engineering best practices to the data transformation process. Analytics Engineers sit between Data Engineers (infrastructure/ingestion) and Data Analysts (insights/reporting).

### dbt (Data Build Tool)

dbt is a transformation tool that allows anyone that knows SQL to deploy analytics code following software engineering best practices like modularity, portability, CI/CD, and documentation.

- **T in ELT**: dbt focuses only on the specific "Transform" step in the ELT (Extract, Load, Transform) pipeline.
- **Jinja Templating**: Enables control structures (if statements, for loops) and DRY (Don't Repeat Yourself) code in SQL.
- **DAG (Directed Acyclic Graph)**: dbt automatically infers dependencies between models.

### Data Warehouse (DuckDB)

For this module, we use **DuckDB** as a local, in-process OLAP database. It provides a fast and easy way to process analytical queries on local files (Parquet, CSV) without needing a cloud warehouse setup.

## Repository Structure

- [`taxi_rides_ny/`](./taxi_rides_ny): The complete dbt project containing:

    - `models/`: SQL files defining the transformations (Staging, Intermediate, Marts).
    - `seeds/`: CSV files loaded as static tables (e.g., `taxi_zone_lookup`).
    - `macros/`: Reusable SQL snippets.
    - `tests/`: Data quality tests.

- [`homework/`](./homework): Questions and answers for the Module 04 homework.

- [`class_notes.md`](./class_notes.md): Notes from the course repository.

## Getting Started

1. Navigate to the dbt project directory:

   ```bash
   cd taxi_rides_ny
   ```

2. Follow the [README](./taxi_rides_ny/README.md) in that directory for detailed setup and running instructions.
