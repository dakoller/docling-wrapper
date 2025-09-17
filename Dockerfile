FROM python:3.12-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml README.md ./
COPY src ./src

# Install dependencies directly with pip
RUN pip install -e .
RUN pip install uvicorn fastapi httpx pydantic

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "src/main.py"]
