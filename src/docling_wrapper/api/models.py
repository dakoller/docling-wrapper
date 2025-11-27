"""
API models for request and response validation.
"""
from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, HttpUrl


class SourceType(str, Enum):
    """
    Enum for the type of source to convert.
    """

    PDF = "pdf"
    HTML_URL = "html_url"
    HTML_SOURCE = "html_source"


class ConversionOptions(BaseModel):
    """
    Options for the conversion process.
    """

    include_metadata: bool = Field(
        default=True, description="Whether to include metadata in the response"
    )
    preserve_images: bool = Field(
        default=False, description="Whether to preserve images in the markdown output"
    )
    headers: Optional[Dict[str, str]] = Field(
        default=None, description="Headers to use when fetching the URL"
    )
    verify_ssl: bool = Field(
        default=False, description="Whether to verify SSL certificates when fetching URLs"
    )


class ConversionRequest(BaseModel):
    """
    Request model for the conversion endpoint.
    """

    type: SourceType = Field(description="Type of source to convert")
    source: str = Field(description="URL or HTML source content to convert")
    options: Optional[ConversionOptions] = Field(
        default=None, description="Options for the conversion process"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "type": "html_url",
                "source": "https://example.com",
                "options": {
                    "include_metadata": True,
                    "preserve_images": False,
                    "headers": {"Authorization": "Bearer token"},
                    "verify_ssl": False,
                },
            }
        }


class ConversionMetadata(BaseModel):
    """
    Metadata about the conversion process.
    """

    title: Optional[str] = Field(default=None, description="Document title")
    source_type: SourceType = Field(description="Type of source that was converted")
    processing_time_ms: int = Field(description="Time taken to process the document in ms")
    file_size_bytes: Optional[int] = Field(
        default=None, description="Size of the source file in bytes"
    )


class ConversionResponse(BaseModel):
    """
    Response model for the conversion endpoint.
    """

    success: bool = Field(description="Whether the conversion was successful")
    markdown: Optional[str] = Field(default=None, description="The converted markdown content")
    metadata: Optional[ConversionMetadata] = Field(
        default=None, description="Metadata about the conversion"
    )
    error: Optional[str] = Field(default=None, description="Error message if conversion failed")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "markdown": "# Document Title\n\nDocument content...",
                "metadata": {
                    "title": "Example Document",
                    "source_type": "html_url",
                    "processing_time_ms": 1500,
                    "file_size_bytes": 12345,
                },
            }
        }


class ErrorResponse(BaseModel):
    """
    Error response model.
    """

    success: bool = Field(default=False, description="Always false for error responses")
    error: str = Field(description="Error message")
    details: Optional[Dict[str, Union[str, List[str]]]] = Field(
        default=None, description="Additional error details"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Failed to convert document",
                "details": {"reason": "Invalid URL format"},
            }
        }
