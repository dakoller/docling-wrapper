# Codebase Summary: Claude - Docling API Wrapper

## Project Structure

The project is currently in its initial setup phase. Here's the current structure:

```
docling-wrapper/
├── .git/
├── .gitignore
├── .python-version
├── architecture_docs/
│   ├── architecture.md
│   ├── codebaseSummary.md
│   ├── currentTask.md
│   └── projectRoadmap.md
├── claude.md
├── pyproject.toml
└── README.md
```

## Key Components and Their Interactions

The project is planned to have the following components, but they are not yet implemented:

### API Layer
- FastAPI application with endpoints for document conversion
- Request/response models using Pydantic
- Input validation and error handling

### Service Layer
- Document processing service using Docling
- URL fetching for remote documents
- Markdown conversion logic

### Infrastructure Layer
- OpenTelemetry integration for observability
- Docker containerization
- Health check and metrics endpoints

## Data Flow

The planned data flow for the application:

1. Client sends a request to the `/convert` endpoint with document URL or content
2. API validates the request and passes it to the service layer
3. Service layer fetches the document if needed and processes it using Docling
4. Markdown output is generated and returned to the client
5. Metrics and traces are collected throughout the process

## External Dependencies

The project will rely on the following external dependencies (not yet added to pyproject.toml):

- **FastAPI**: Web framework for building the API
- **Docling**: IBM's document processing library
- **httpx**: HTTP client for URL fetching
- **Pydantic**: Data validation and serialization
- **OpenTelemetry**: Observability framework
- **uv**: Package manager for dependency management

## Recent Significant Changes

- Initial project setup
- Created architecture documentation
- Defined project scope and requirements

## User Feedback Integration

No user feedback has been collected yet as the project is in its initial setup phase.

## Next Steps

See [currentTask.md](./currentTask.md) for detailed next steps.

The immediate focus is on:
1. Setting up the basic project structure
2. Adding required dependencies
3. Implementing the core API functionality
4. Setting up Docker containerization
