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

#### Docker Image Features

The Docker image includes several optimizations and security features:

- **Multi-stage build**: Reduces the final image size by separating build and runtime dependencies
- **Security hardening**:
  - Runs as a non-root user (`appuser`)
  - Uses minimal base image (python:3.12-slim)
  - Includes only necessary runtime dependencies
  - Proper file permissions and ownership
  - Uses tini as init process to handle signals properly
- **Health check**: Monitors the application's health via the `/health` endpoint
- **Build optimizations**:
  - Layer caching for faster builds
  - Minimized number of layers
  - Proper cleanup of package manager caches

#### Troubleshooting Docker Build

If you encounter issues with the Docker build process, you can try the following:

1. Make sure Docker has enough resources allocated (memory, CPU)
2. Check if all required files are present and not excluded by .dockerignore
3. Try building with the `--no-cache` flag to start fresh:
   ```bash
   docker compose build --no-cache
   ```
4. If you're behind a proxy, ensure Docker is properly configured to use it

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

### API Documentation

The API documentation is available in multiple formats:

1. **Swagger UI**: When the application is running, you can access the interactive API documentation at http://localhost:8000/docs

2. **OpenAPI Specification**: The API provides an endpoint to retrieve the OpenAPI specification at http://localhost:8000/openapi

3. **Static OpenAPI File**: A static OpenAPI specification file is available in the [docs/openapi.yaml](./docs/openapi.yaml) file. This can be used with tools like Swagger UI, Redoc, or OpenAPI Generator.

4. **OpenAPI Documentation Server**: You can serve the OpenAPI documentation without running the full application using the provided script:

   ```bash
   # Run the OpenAPI documentation server
   ./docs/serve_openapi.py
   
   # Specify a custom port
   ./docs/serve_openapi.py --port 9000
   
   # Run without opening a browser
   ./docs/serve_openapi.py --no-browser
   ```
   
   This will start a simple HTTP server and open the OpenAPI documentation in Swagger UI and Redoc in your browser.

### Project Documentation

For detailed project documentation, see the [architecture_docs](./architecture_docs/) directory:

- [Project Roadmap](./architecture_docs/projectRoadmap.md)
- [Current Task](./architecture_docs/currentTask.md)
- [Architecture](./architecture_docs/architecture.md)
- [Codebase Summary](./architecture_docs/codebaseSummary.md)
