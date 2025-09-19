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
    
    # Check if docling has the necessary functionality
    required_functions = ['convert_html_to_markdown']
    missing_functions = [func for func in required_functions if not hasattr(docling, func)]
    
    if missing_functions:
        print(f"Docling library found but missing required functions: {', '.join(missing_functions)}")
        print("Using mock implementation for missing functionality")
        # Import our mock module and add the missing functions to the docling module
        mock_docling = __import__('docling_wrapper.utils.mock_docling')
        for func in missing_functions:
            setattr(docling, func, getattr(mock_docling.docling_wrapper.utils.mock_docling, func))
    else:
        print("Using actual Docling library with all required functionality")
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
    
    # Add additional info to the OpenAPI schema
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    # Add contact information
    openapi_schema["info"]["contact"] = {
        "name": "Claude API Team",
        "url": "https://github.com/claude/docling-wrapper",
        "email": "api@claude-docling.example.com",
    }
    
    # Add license information
    openapi_schema["info"]["license"] = {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
    
    # Add tags metadata
    openapi_schema["tags"] = [
        {
            "name": "Conversion",
            "description": "Operations related to document conversion",
        },
        {
            "name": "Health",
            "description": "Health check endpoints",
        },
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# OpenAPI endpoint to retrieve the OpenAPI specification
@app.get("/openapi", tags=["Documentation"])
async def get_openapi_spec():
    """
    Get the OpenAPI specification for the API.
    
    Returns the complete OpenAPI specification in JSON format.
    This can be used to generate API documentation or client libraries.
    """
    return app.openapi()


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy", "version": app.version}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
