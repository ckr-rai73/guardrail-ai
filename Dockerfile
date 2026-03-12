# File: Dockerfile
# Guardrail.ai Community Edition
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY backend/app ./app
COPY .env.example .env

# Expose the API port
EXPOSE 8000

# Set default env to community edition
ENV COMMUNITY_EDITION=True

# Run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
