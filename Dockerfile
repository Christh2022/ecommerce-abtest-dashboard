# Dockerfile for E-commerce A/B Test Dashboard
# Multi-stage build for optimized image size

# Stage 1: Base image with Python
FROM python:3.12-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Stage 2: Dependencies
FROM base as dependencies

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file from root
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Application
FROM base as application

# Copy Python dependencies from previous stage
COPY --from=dependencies /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Copy application code
COPY dashboard/ /app/dashboard/

# Copy data files
COPY data/clean/ /app/data/clean/

# Create non-root user for security
RUN useradd -m -u 1000 dashuser && \
    chown -R dashuser:dashuser /app

# Switch to non-root user
USER dashuser

# Expose port
EXPOSE 8050

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8050', timeout=5)" || exit 1

# Set working directory to dashboard
WORKDIR /app/dashboard

# Run the application
CMD ["python", "app.py"]
