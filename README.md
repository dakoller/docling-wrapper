# Claude - Docling API Wrapper

A lightweight API service that wraps IBM's Docling library to provide document conversion capabilities for knowledge management systems. The service converts PDF documents and HTML content into clean, structured Markdown format via REST API endpoints.

## Overview

Claude is designed to solve the problem of converting various document formats (PDF, HTML) into Markdown for consistent processing, indexing, and storage in knowledge management systems. It provides a reliable API interface with observability and containerized deployment options.

## Features

- Convert PDF files via URL
- Convert HTML content via URL or raw source
- Preserve document structure (headings, lists, tables)
- Extract and handle images
- OpenTelemetry integration for observability
- Docker containerization for easy deployment

## Project Status

This project is currently in the initial development phase. See the [architecture documentation](./architecture_docs/) for more details on the project roadmap, current tasks, and architecture decisions.

## Technology Stack

- Python 3.12+
- FastAPI
- Docling (IBM's document processing library)
- Docker & Docker Compose
- OpenTelemetry for observability

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Docker and Docker Compose (for containerized deployment)
- uv (recommended for package management)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd docling-wrapper
   ```

2. Install dependencies:
   ```bash
   # Using uv (recommended)
   uv pip install -e .
   
   # Or using pip
   pip install -e .
   ```

### Running Locally

You can run the application locally using the provided script:

```bash
./run_local.sh
```

This script will:
1. Install dependencies (including uvicorn, fastapi, httpx, and pydantic)
2. Start the API server
3. Run tests with sample HTML content and URLs
4. Generate Markdown output files in the test directory

> **Note:** The script will automatically handle the case where the Docling library is not available by using a mock implementation. In a real-world scenario, you would need to install the actual Docling library.

#### Troubleshooting

If you encounter dependency issues when running the script, you can manually install the required packages:

```bash
# Using pip
pip install uvicorn fastapi httpx pydantic

# Using uv
uv pip install uvicorn fastapi httpx pydantic
```

### Running with Docker

1. Build and start the containers:
   ```bash
   docker compose build
   docker compose up
   ```

2. The API will be available at http://localhost:8000

3. You can access the API documentation at http://localhost:8000/docs

#### Troubleshooting Docker Build

If you encounter issues with the Docker build process, such as:

```
error: No virtual environment found; run `uv venv` to create an environment, or pass `--system` to install into a non-virtual environment
```

The Dockerfile has been updated to use pip directly instead of uv for dependency installation. If you still encounter issues, you can modify the Dockerfile to use a different installation method:

```dockerfile
# Option 1: Use pip directly (current approach)
RUN pip install -e .
RUN pip install uvicorn fastapi httpx pydantic

# Option 2: Use uv with --system flag
# RUN pip install uv
# RUN uv pip install --system -e .
# RUN uv pip install --system uvicorn fastapi httpx pydantic
```

### Testing

To test the HTML to Markdown conversion functionality:

```bash
# Convert an HTML file to Markdown
python test/test_conversion.py --file test/sample.html --output output.md

# Convert HTML from a URL to Markdown
python test/test_conversion.py --url https://example.com --output output.md

# Test the API
python test/test_conversion.py --url https://example.com --api http://localhost:8000/api/v1/convert --output output.md
```

## Documentation

For detailed documentation, see the [architecture_docs](./architecture_docs/) directory:

- [Project Roadmap](./architecture_docs/projectRoadmap.md)
- [Current Task](./architecture_docs/currentTask.md)
- [Architecture](./architecture_docs/architecture.md)
- [Codebase Summary](./architecture_docs/codebaseSummary.md)
