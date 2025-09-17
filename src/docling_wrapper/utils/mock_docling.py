"""
Mock implementation of the Docling library for development and testing.

This module provides mock implementations of the Docling library functions
until the actual library is available.
"""
import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)


def convert_html_to_markdown(html_content: str) -> str:
    """
    Mock implementation of the Docling HTML to Markdown conversion.
    
    This is a simplified implementation that handles basic HTML elements.
    In a real implementation, this would use the actual Docling library.
    
    Args:
        html_content: The HTML content to convert
        
    Returns:
        The converted Markdown content
    """
    logger.info("Converting HTML to Markdown using mock implementation")
    
    # Extract the body content if present
    body_match = re.search(r"<body.*?>(.*?)</body>", html_content, re.IGNORECASE | re.DOTALL)
    if body_match:
        content = body_match.group(1)
    else:
        content = html_content
    
    # Extract title
    title = extract_title(html_content)
    markdown = f"# {title}\n\n" if title else ""
    
    # Process content
    # Replace headings
    content = re.sub(r"<h1.*?>(.*?)</h1>", r"# \1\n", content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r"<h2.*?>(.*?)</h2>", r"## \1\n", content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r"<h3.*?>(.*?)</h3>", r"### \1\n", content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r"<h4.*?>(.*?)</h4>", r"#### \1\n", content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r"<h5.*?>(.*?)</h5>", r"##### \1\n", content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r"<h6.*?>(.*?)</h6>", r"###### \1\n", content, flags=re.IGNORECASE | re.DOTALL)
    
    # Replace paragraphs
    content = re.sub(r"<p.*?>(.*?)</p>", r"\1\n\n", content, flags=re.IGNORECASE | re.DOTALL)
    
    # Replace links
    content = re.sub(r'<a.*?href="(.*?)".*?>(.*?)</a>', r"[\2](\1)", content, flags=re.IGNORECASE | re.DOTALL)
    
    # Replace bold and italic
    content = re.sub(r"<strong.*?>(.*?)</strong>", r"**\1**", content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r"<b.*?>(.*?)</b>", r"**\1**", content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r"<em.*?>(.*?)</em>", r"*\1*", content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r"<i.*?>(.*?)</i>", r"*\1*", content, flags=re.IGNORECASE | re.DOTALL)
    
    # Replace unordered lists
    content = re.sub(r"<ul.*?>(.*?)</ul>", process_ul, content, flags=re.IGNORECASE | re.DOTALL)
    
    # Replace ordered lists
    content = re.sub(r"<ol.*?>(.*?)</ol>", process_ol, content, flags=re.IGNORECASE | re.DOTALL)
    
    # Replace images
    content = re.sub(r'<img.*?src="(.*?)".*?alt="(.*?)".*?>', r"![\2](\1)", content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r'<img.*?src="(.*?)".*?>', r"![](\1)", content, flags=re.IGNORECASE | re.DOTALL)
    
    # Replace divs and spans with their content
    content = re.sub(r"<div.*?>(.*?)</div>", r"\1\n", content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r"<span.*?>(.*?)</span>", r"\1", content, flags=re.IGNORECASE | re.DOTALL)
    
    # Replace line breaks
    content = re.sub(r"<br.*?>", r"\n", content, flags=re.IGNORECASE)
    
    # Replace horizontal rules
    content = re.sub(r"<hr.*?>", r"\n---\n", content, flags=re.IGNORECASE)
    
    # Remove remaining HTML tags
    content = re.sub(r"<.*?>", "", content)
    
    # Decode HTML entities
    content = decode_html_entities(content)
    
    # Combine title and content
    markdown += content
    
    # Clean up extra whitespace and line breaks
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    markdown = markdown.strip()
    
    return markdown


def extract_title(html_content: str) -> Optional[str]:
    """
    Extract the title from HTML content.
    
    Args:
        html_content: The HTML content to extract the title from
        
    Returns:
        The title if found, None otherwise
    """
    title_match = re.search(r"<title.*?>(.*?)</title>", html_content, re.IGNORECASE | re.DOTALL)
    if title_match:
        return title_match.group(1).strip()
    return None


def process_ul(match) -> str:
    """
    Process an unordered list match and convert it to Markdown.
    
    Args:
        match: The regex match object
        
    Returns:
        The converted Markdown list
    """
    content = match.group(1)
    items = re.findall(r"<li.*?>(.*?)</li>", content, re.IGNORECASE | re.DOTALL)
    markdown = "\n"
    for item in items:
        markdown += f"- {item.strip()}\n"
    return markdown + "\n"


def process_ol(match) -> str:
    """
    Process an ordered list match and convert it to Markdown.
    
    Args:
        match: The regex match object
        
    Returns:
        The converted Markdown list
    """
    content = match.group(1)
    items = re.findall(r"<li.*?>(.*?)</li>", content, re.IGNORECASE | re.DOTALL)
    markdown = "\n"
    for i, item in enumerate(items, 1):
        markdown += f"{i}. {item.strip()}\n"
    return markdown + "\n"


def decode_html_entities(text: str) -> str:
    """
    Decode common HTML entities to their character equivalents.
    
    Args:
        text: The text containing HTML entities
        
    Returns:
        The text with HTML entities decoded
    """
    entities = {
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&quot;": '"',
        "&#39;": "'",
        "&nbsp;": " ",
    }
    for entity, char in entities.items():
        text = text.replace(entity, char)
    return text
