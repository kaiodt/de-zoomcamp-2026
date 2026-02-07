# 🚕 NYC Taxi GCS Ingestion

A professional CLI tool designed to ingest NYC Taxi trip data (Yellow and Green) from public CloudFront repositories directly into Google Cloud Storage (GCS) as Parquet files.

This project follows best practices for modular Python development, providing a robust and interactive terminal experience with automated schema standardization for BigQuery compatibility.

## 🗃️ Project Structure

```text
📂 gcs_ingestion/
├── 📄 gcs_ingestion.py      # CLI entry point (Typer-based)
├── 📄 gcs_utils.py          # GCS and download logic
├── 📄 schema.py             # Strict data schemas for Yellow & Green taxis
├── 📄 pyproject.toml        # Project dependencies (PEP 621)
├── 📄 service-account.json  # GCP Credentials (user-provided)
└── 📄 uv.lock               # Dependency lock file (for uv)
```

## ✨ Features

- **Modern CLI**: Built with `Typer` and `Rich` for a premium terminal experience.
- **Shortcuts**: Fast aliases for all commands (`-s`, `-Y`, `-m`, `-b`, `-y`).
- **BigQuery Compatibility**: Automated **Schema Standardization** layer that:
    - Enforces strict data types (e.g., `Float64` / `DOUBLE`).
    - Adds missing columns (like `airport_fee`) with appropriate nulls.
    - Ensures identical column ordering across different months and years.
- **Smart Logic**:
    - **Bucket Management**: Automatically checks and creates buckets if missing.
    - **Idempotency**: Prompts before overwriting existing data in GCS.
- **Non-Interactive Mode**: Use the `--yes` / `-y` flag to skip all prompts for batch processing.
- **Resource Efficient**: Reuses GCS clients and cleans up local temporary files automatically.

## 📦 Getting Started

### 📋 Prerequisites

- [uv](https://github.com/astral-sh/uv)
- A Google Cloud Platform (GCP) account with GCS permissions.

### 🛠️ Setup

1. **GCP Credentials**:
   Obtain your GCP Service Account JSON key and save it as `service-account.json` in this directory.

2. **Install dependencies**:

   ```bash
   uv sync
   ```

## 📚 Usage

Run the ingestion tool for a specific year and service:

```bash
uv run gcs_ingestion.py -s yellow -Y 2019 -m 1
```

**Options:**

- `-s`, `--service`: Taxi service type (`yellow` or `green`).
- `-Y`, `--year`: Year of the data (e.g., `2019`).
- `-m`, `--month`: Month (1-12). If omitted, all 12 months are processed.
- `-b`, `--bucket`: Target GCS bucket name.
- `-y`, `--yes`: Skip all confirmation prompts (Force override/create).
