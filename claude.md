# Claude - Docling API Wrapper

## Overview

Claude is a lightweight API service that wraps IBM's Docling library to provide document conversion capabilities for knowledge management systems. The service converts PDF documents and HTML content into clean, structured Markdown format via REST API endpoints.

## Problem Statement

Knowledge management systems need a reliable way to convert various document formats (PDF, HTML) into Markdown for consistent processing, indexing, and storage. Current solutions often lack proper API interfaces, observability, and containerized deployment options.

## Solution

A Python-based REST API that leverages Docling's document processing capabilities, packaged as a Docker container with built-in observability and metrics collection.

Use uv as a package manager & for executing the script logic. When code is changed, do a "docker compose build" before starting the docker container.

## Core Requirements

### Functional Requirements

**Input Processing**
- Accept PDF files via URL (download and process)
- Accept HTML content via URL (fetch and process) 
- Accept raw HTML source code directly
- Support common PDF formats and web content
- Handle authentication headers for protected resources (optional)

**Output Generation**
- Convert documents to clean Markdown format
- Preserve document structure (headings, lists, tables)
- Extract and handle images appropriately
- Return structured JSON response with metadata

**API Design**
- RESTful HTTP endpoints
- JSON request/response format
- Proper HTTP status codes and error handling
- Request validation and sanitization
- Swagger/OpenAPI documentation

### Non-Functional Requirements

**Performance**
- Process typical documents (1-50 pages) within 30 seconds
- Support concurrent requests (at least 5 simultaneous)
- Implement request timeouts and resource limits

**Reliability**
- Graceful error handling and recovery
- Input validation and sanitization
- Resource cleanup after processing
- Health check endpoints

**Observability**
- OpenTelemetry (OTEL) integration for traces and metrics
- Structured logging with correlation IDs
- Performance metrics (processing time, success/failure rates)
- Resource utilization monitoring

**Security**
- Input validation to prevent malicious content
- Resource limits to prevent DoS
- Secure handling of temporary files

## Technical Specifications

### API Endpoints

#### `POST /convert`
Convert document from URL or HTML source to Markdown

**Request Body:**
```json
{
  "type": "pdf|html_url|html_source",
  "source": "https://example.com/doc.pdf | HTML content",
  "options": {
    "include_metadata": true,
    "preserve_images": false,
    "headers": {"Authorization": "Bearer token"}
  }
}
```

**Response:**
```json
{
  "success": true,
  "markdown": "# Document Content\n...",
  "metadata": {
    "title": "Document Title",
    "pages": 10,
    "processing_time_ms": 15000,
    "source_type": "pdf",
    "file_size_bytes": 1048576
  }
}
```

#### `GET /health`
Health check endpoint

#### `GET /metrics`
Prometheus-compatible metrics endpoint

### Technology Stack

**Core Framework**
- **Python 3.11+** - Runtime environment
- **FastAPI** - Web framework for REST API
- **Docling** - Document processing library
- **Pydantic** - Data validation and serialization

**Infrastructure**
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **OpenTelemetry** - Observability and tracing
- **Prometheus** - Metrics collection (via OTEL)

**Dependencies**
- `docling` - Core document processing
- `fastapi[all]` - Web framework with extras
- `httpx` - HTTP client for URL fetching
- `opentelemetry-api` - OTEL instrumentation
- `opentelemetry-sdk` - OTEL SDK
- `opentelemetry-exporter-otlp` - OTEL exporter
- `opentelemetry-instrumentation-fastapi` - FastAPI auto-instrumentation

### Docker Compose Structure

```yaml
version: '3.8'

services:
  claude-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
      - OTEL_SERVICE_NAME=claude-docling-api
      - OTEL_RESOURCE_ATTRIBUTES=service.version=1.0.0
    depends_on:
      - otel-collector
    volumes:
      - /tmp/claude-temp:/app/temp  # Temporary file storage

  otel-collector:
    image: otel/opentelemetry-collector-contrib:latest
    # OTEL configuration provided by user
```

## Metrics and Observability

### Key Metrics
- **Request Metrics**: Count, duration, success/error rates by endpoint
- **Processing Metrics**: Document processing time, file sizes, conversion success rates
- **Resource Metrics**: Memory usage, CPU utilization, disk I/O
- **Business Metrics**: Documents processed by type, error categories

### Logging
- Structured JSON logging
- Request correlation IDs
- Error details with stack traces
- Processing pipeline stages

### Tracing
- End-to-end request tracing
- Document processing pipeline spans
- External HTTP calls (URL fetching)
- Database operations (if applicable)

## Implementation Phases

### Phase 1: Core API (MVP)
- Basic FastAPI application structure
- Docling integration for PDF and HTML processing
- Essential endpoints (`/convert`, `/health`)
- Docker containerization
- Basic error handling

### Phase 2: Observability
- OpenTelemetry integration
- Metrics collection and export
- Structured logging implementation
- Health check enhancements

### Phase 3: Production Readiness
- Comprehensive input validation
- Security hardening
- Performance optimization
- Documentation and testing
- Docker Compose configuration

## Success Criteria

- **Functionality**: Successfully convert PDF and HTML documents to Markdown with 95%+ accuracy
- **Performance**: Process typical documents within SLA timeouts
- **Reliability**: 99%+ uptime with proper error handling
- **Observability**: Complete visibility into system performance and errors via OTEL backend
- **Deployment**: One-command deployment via Docker Compose

## Risks and Mitigation

**Risk: Docling Library Limitations**
- *Mitigation*: Implement fallback mechanisms and clear error reporting

**Risk: Resource Exhaustion**
- *Mitigation*: Request limits, timeouts, and temporary file cleanup

**Risk: Security Vulnerabilities**
- *Mitigation*: Input validation, sandboxed processing, resource limits

## Future Enhancements

- Batch processing capabilities
- Additional output formats (reStructuredText, AsciiDoc)
- Document caching and deduplication
- Webhook notifications for async processing
- Integration with popular knowledge management platforms