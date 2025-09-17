#!/usr/bin/env python3
"""
Main entry point for the Claude - Docling API Wrapper.
"""
import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

# Check if docling is installed, if not, use our mock implementation
try:
    import docling
    print("Using actual Docling library")
except ImportError:
    print("Docling library not found, using mock implementation")
    sys.modules['docling'] = __import__('docling_wrapper.utils.mock_docling')

from docling_wrapper.api.routes import router as api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events for the FastAPI application.
    """
    # Startup events
    logger.info("Starting up Claude - Docling API Wrapper")
    yield
    # Shutdown events
    logger.info("Shutting down Claude - Docling API Wrapper")


app = FastAPI(
    title="Claude - Docling API Wrapper",
    description="A lightweight API service that wraps IBM's Docling library to provide document conversion capabilities",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy", "version": app.version}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
