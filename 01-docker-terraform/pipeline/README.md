# 🚕 NYC Taxi Data Ingestion Pipeline

A modular and agnostic data ingestion pipeline designed to download NYC Yellow Taxi data and load it into a PostgreSQL database. 

This project follows best practices for modular Python development, with a clear separation between application-specific logic and reusable utilities.


## 🗃️ Project Structure

```text
📂 pipeline/
├── 📂 app/                  # Application-specific logic
│   ├── 📄 ingest_data.py    # CLI entry point (Typer-based)
│   └── 📄 schema.py         # NYC Taxi-specific data schemas (dtypes, date columns)
├── 📂 utils/                # Agnostic, shareable utilities
│   ├── 📄 db.py             # Database connection & inspection (SQLAlchemy)
│   └── 📄 ingest.py         # Generic data ingestion logic (Pandas-based)
├── 📄 .env.example          # Template for environment variables
├── 📄 .python-version       # Python version (for uv)
├── 📄 compose.yaml          # Local infrastructure (PostgreSQL & pgAdmin)
├── 📄 Dockerfile            # Container definition
├── 📄 pyproject.toml        # Project dependencies (PEP 621)
└── 📄 uv.lock               # Dependency lock file (for uv)
```


## ✨ Features

- **Modular Design**: Utilities in `utils/` are agnostic and can be used in other pipelines.
- **Idempotency**: Supports a `skip` strategy to avoid re-ingesting data if target tables already exist.
- **Rich Interface**: Provides a premium terminal experience with progress bars and color-coded logs.
- **Reproducible**: Managed with `uv` for consistent environments across development and production.
- **Containerized**: Ready for deployment with a multi-stage Docker build.


## 📦 Getting Started

### 📋 Prerequisites

- [uv](https://github.com/astral-sh/uv)
- [Docker](https://www.docker.com/) (for containerized runs)


### 🛠️ Setup

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd pipeline
   ```

2. **Set up environment variables**:

   Create a `.env` file based on the available configuration:

   ```bash
   cp .env.example .env
   ```

3. **Install dependencies**:

   ```bash
   uv sync
   ```

4. **Spin up the database**:

   ```bash
   docker compose up -d
   ```


## 📚 Usage

### 💻 Local Execution (with uv)

Run the ingestion script for a specific year and month:

```bash
uv run python -m app.ingest_data --year 2021 --month 1
```

**Options:**

- `--year`: Year of the taxi data (e.g., 2021).
- `--month`: Month of the taxi data (e.g., 1).
- `--chunksize`: Rows per chunk (default: 100,000). Set to 0 to disable chunking.
- `--if-exists`: Strategy if table exists (`replace`, `append`, `skip`).


### 🐋 Docker Execution

Build and run the pipeline inside a container:

```bash
docker build -t taxi-ingest .
docker run -it --rm \
  --network pg-network \
  --env-file .env \
  taxi-ingest --year 2021 --month 1
```


## 🧰 Modular Utilities

The `utils/` package is designed to be agnostic:

- `utils.db.get_engine`: Creates a SQLAlchemy engine from generic parameters.
- `utils.ingest.ingest_data`: A flexible coordinator for loading CSV files into SQL tables with support for chunking and progress tracking.


## 📜 License

MIT License
