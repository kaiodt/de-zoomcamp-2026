FROM python:3.13.11-slim

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /code

# Set timezone and install required system packages
RUN apt-get update && apt-get install -y tzdata && rm -rf /var/lib/apt/lists/*
ENV TZ=America/Sao_Paulo

# Add virtual environment to PATH so we can use installed packages
ENV PATH="/code/.venv/bin:$PATH"

# Copy dependency files first (better layer caching)
COPY ".python-version" "pyproject.toml" "uv.lock" ./

# Install dependencies from lock file (ensures reproducible builds)
RUN uv sync --locked

# Copy environment variables
COPY ".env" ./

# Copy application code last (ensures maximum cache reusability)
COPY "app/" "./app/"
COPY "utils/" "./utils/"

# Set entrypoint to run the pipeline
ENTRYPOINT ["python", "-m", "app.ingest_data"]
