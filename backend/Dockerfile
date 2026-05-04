# Backend Dockerfile - FastAPI with Docker SDK
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies required by some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml and build requirements
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Copy source code
COPY src/ ./src/

# Expose the API port
EXPOSE 8000

# Set default environment variables (can be overridden by docker-compose)
ENV API_HOST=0.0.0.0
ENV API_PORT=8000

# Run the FastAPI application with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
