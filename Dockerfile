# Build stage
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc6-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md ./
COPY src ./src

# Install dependencies
RUN pip install --upgrade pip && \
    pip install wheel setuptools && \
    pip install . && \
    pip install uvicorn fastapi httpx pydantic

# Final stage
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app:${PATH}"

# Create non-root user
RUN groupadd -r appuser && \
    useradd -r -g appuser -d /app -s /sbin/nologin -c "Docker image user" appuser && \
    mkdir -p /app/temp && \
    chown -R appuser:appuser /app

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends tini curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser src ./src

# Create temp directory with proper permissions
RUN mkdir -p /tmp/claude-temp && \
    chown -R appuser:appuser /tmp/claude-temp

# Expose port
EXPOSE 8000

# Set user
USER appuser

# Add metadata
LABEL org.opencontainers.image.title="Claude - Docling API Wrapper" \
      org.opencontainers.image.description="A lightweight API service that wraps IBM's Docling library to provide document conversion capabilities" \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.vendor="Claude" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.source="https://github.com/claude/docling-wrapper"

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Use tini as entrypoint to handle signals properly
ENTRYPOINT ["/usr/bin/tini", "--"]

# Run the application
CMD ["python", "src/main.py"]
