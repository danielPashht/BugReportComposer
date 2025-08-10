FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install build tools
RUN pip install --upgrade pip setuptools wheel

# Copy project configuration files first for better Docker layer caching
COPY pyproject.toml .
COPY requirements.txt .
COPY requirements-dev.txt .
COPY README.md .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install the package in development mode
RUN pip install --no-cache-dir -e .

# Copy the application code
COPY src/ ./src/
COPY main.py .

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash --uid 1000 app \
    && chown -R app:app /app
USER app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from src.core import models; print('OK')" || exit 1

# Default entrypoint uses main.py for direct execution
ENTRYPOINT ["python", "main.py"]

# Default help command (can be overridden)
CMD ["--help"]
