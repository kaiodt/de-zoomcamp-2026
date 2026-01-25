FROM python:3.13.11-slim

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /code

# Add virtual environment to PATH so we can use installed packages
ENV PATH="/code/.venv/bin:$PATH"

# Copy dependency files first (better layer caching)
COPY ".python-version" "pyproject.toml" "uv.lock" ./

# Install dependencies from lock file (ensures reproducible builds)
RUN uv sync --locked

# Copy environment variables
COPY ".env" ./

# Copy application code last (ensures maximum cache reusability)
COPY "ingest_data.py" "./"

# Set entrypoint to run the pipeline
ENTRYPOINT ["python", "ingest_data.py"]
