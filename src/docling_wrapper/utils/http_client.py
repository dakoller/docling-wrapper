"""
HTTP client utilities for fetching content from URLs.
"""
import logging
from typing import Dict, Optional, Tuple, Union

import httpx

logger = logging.getLogger(__name__)


async def fetch_url_content(
    url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 30, verify_ssl: bool = False
) -> Tuple[Union[str, bytes], Dict[str, str], int]:
    """
    Fetch content from a URL.

    Args:
        url: The URL to fetch content from
        headers: Optional headers to include in the request
        timeout: Request timeout in seconds
        verify_ssl: Whether to verify SSL certificates (default: False)

    Returns:
        Tuple containing:
        - The content of the URL (as string for HTML, bytes for binary content)
        - Response headers
        - Content size in bytes

    Raises:
        httpx.HTTPError: If the request fails
    """
    logger.info(f"Fetching content from URL: {url}")
    
    async with httpx.AsyncClient(timeout=timeout, verify=verify_ssl) as client:
        response = await client.get(url, headers=headers, follow_redirects=True)
        response.raise_for_status()
        
        content_type = response.headers.get("content-type", "")
        content_length = len(response.content)
        
        logger.info(
            f"Successfully fetched content from URL: {url} "
            f"(type: {content_type}, size: {content_length} bytes)"
        )
        
        # Return content as string for HTML, bytes for binary content
        if "text/html" in content_type or "application/xhtml+xml" in content_type:
            return response.text, dict(response.headers), content_length
        else:
            return response.content, dict(response.headers), content_length


async def is_valid_url(url: str, verify_ssl: bool = False) -> bool:
    """
    Check if a URL is valid and accessible.

    Args:
        url: The URL to check
        verify_ssl: Whether to verify SSL certificates (default: False)

    Returns:
        True if the URL is valid and accessible, False otherwise
    """
    try:
        async with httpx.AsyncClient(timeout=5, verify=verify_ssl) as client:
            response = await client.head(url, follow_redirects=True)
            return response.status_code < 400
    except Exception as e:
        logger.warning(f"URL validation failed for {url}: {str(e)}")
        return False
