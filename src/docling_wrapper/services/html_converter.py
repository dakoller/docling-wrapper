"""
Service for converting HTML to Markdown using Docling.
"""
import logging
import sys
import time
from typing import Dict, Optional, Tuple

# Try to import from docling, if not available, use our mock implementation
try:
    from docling import convert_html_to_markdown
    print("Using actual Docling library for HTML conversion")
except ImportError:
    print("Docling library not found, using mock implementation for HTML conversion")
    from docling_wrapper.utils.mock_docling import convert_html_to_markdown

from docling_wrapper.api.models import ConversionMetadata, SourceType
from docling_wrapper.utils.http_client import fetch_url_content, is_valid_url

logger = logging.getLogger(__name__)


async def convert_html_url_to_markdown(
    url: str, headers: Optional[Dict[str, str]] = None, verify_ssl: bool = False
) -> Tuple[str, ConversionMetadata]:
    """
    Convert HTML from a URL to Markdown.

    Args:
        url: The URL to fetch HTML from
        headers: Optional headers to include in the request
        verify_ssl: Whether to verify SSL certificates (default: False)

    Returns:
        Tuple containing:
        - The converted Markdown content
        - Metadata about the conversion

    Raises:
        ValueError: If the URL is invalid
        httpx.HTTPError: If the request fails
    """
    # Validate URL
    if not await is_valid_url(url, verify_ssl=verify_ssl):
        raise ValueError(f"Invalid or inaccessible URL: {url}")

    start_time = time.time()
    
    # Fetch HTML content
    html_content, response_headers, content_size = await fetch_url_content(url, headers, verify_ssl=verify_ssl)
    
    # Extract title from HTML if available
    title = extract_title_from_html(html_content)
    
    # Convert HTML to Markdown
    markdown_content = convert_html_to_markdown(html_content)
    
    # Calculate processing time
    processing_time_ms = int((time.time() - start_time) * 1000)
    
    # Create metadata
    metadata = ConversionMetadata(
        title=title,
        source_type=SourceType.HTML_URL,
        processing_time_ms=processing_time_ms,
        file_size_bytes=content_size,
    )
    
    return markdown_content, metadata


async def convert_html_source_to_markdown(html_content: str) -> Tuple[str, ConversionMetadata]:
    """
    Convert HTML source to Markdown.

    Args:
        html_content: The HTML content to convert

    Returns:
        Tuple containing:
        - The converted Markdown content
        - Metadata about the conversion
    """
    start_time = time.time()
    
    # Extract title from HTML if available
    title = extract_title_from_html(html_content)
    
    # Convert HTML to Markdown
    markdown_content = convert_html_to_markdown(html_content)
    
    # Calculate processing time
    processing_time_ms = int((time.time() - start_time) * 1000)
    
    # Create metadata
    metadata = ConversionMetadata(
        title=title,
        source_type=SourceType.HTML_SOURCE,
        processing_time_ms=processing_time_ms,
        file_size_bytes=len(html_content.encode('utf-8')),
    )
    
    return markdown_content, metadata


def extract_title_from_html(html_content: str) -> Optional[str]:
    """
    Extract the title from HTML content.

    Args:
        html_content: The HTML content to extract the title from

    Returns:
        The title if found, None otherwise
    """
    # Simple regex-based title extraction
    import re
    title_match = re.search(r"<title>(.*?)</title>", html_content, re.IGNORECASE | re.DOTALL)
    if title_match:
        return title_match.group(1).strip()
    return None
