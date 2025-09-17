#!/usr/bin/env python3
"""
Test script for the HTML to Markdown conversion functionality.

This script tests the conversion of HTML to Markdown using the Claude - Docling API Wrapper.
It can be used to test both the local API and the mock implementation directly.
"""
import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from docling_wrapper.services.html_converter import convert_html_source_to_markdown
from docling_wrapper.utils.http_client import fetch_url_content


async def test_html_file_conversion(file_path: str, output_path: str = None):
    """
    Test the conversion of an HTML file to Markdown.

    Args:
        file_path: Path to the HTML file
        output_path: Path to save the Markdown output (optional)
    """
    print(f"Testing conversion of HTML file: {file_path}")
    
    # Read the HTML file
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Convert HTML to Markdown
    markdown_content, metadata = await convert_html_source_to_markdown(html_content)
    
    # Print the results
    print("\n" + "=" * 80)
    print(f"Title: {metadata.title}")
    print(f"Processing time: {metadata.processing_time_ms} ms")
    print(f"File size: {metadata.file_size_bytes} bytes")
    print("=" * 80)
    print("\nMarkdown output:\n")
    print(markdown_content)
    print("\n" + "=" * 80)
    
    # Save the Markdown output if requested
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"\nMarkdown output saved to: {output_path}")
    
    return markdown_content, metadata


async def test_html_url_conversion(url: str, output_path: str = None):
    """
    Test the conversion of HTML from a URL to Markdown.

    Args:
        url: URL of the HTML page
        output_path: Path to save the Markdown output (optional)
    """
    print(f"Testing conversion of HTML from URL: {url}")
    
    try:
        # Fetch the HTML content
        html_content, _, _ = await fetch_url_content(url)
        
        # Convert HTML to Markdown
        markdown_content, metadata = await convert_html_source_to_markdown(html_content)
        
        # Print the results
        print("\n" + "=" * 80)
        print(f"Title: {metadata.title}")
        print(f"Processing time: {metadata.processing_time_ms} ms")
        print(f"File size: {metadata.file_size_bytes} bytes")
        print("=" * 80)
        print("\nMarkdown output:\n")
        print(markdown_content)
        print("\n" + "=" * 80)
        
        # Save the Markdown output if requested
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            print(f"\nMarkdown output saved to: {output_path}")
        
        return markdown_content, metadata
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None


async def test_api_conversion(url: str, api_url: str, output_path: str = None):
    """
    Test the conversion of HTML from a URL using the API.

    Args:
        url: URL of the HTML page
        api_url: URL of the API endpoint
        output_path: Path to save the Markdown output (optional)
    """
    import httpx
    
    print(f"Testing conversion of HTML from URL: {url} using API: {api_url}")
    
    try:
        # Prepare the request
        request_data = {
            "type": "html_url",
            "source": url,
            "options": {
                "include_metadata": True,
                "preserve_images": True
            }
        }
        
        # Send the request
        async with httpx.AsyncClient() as client:
            response = await client.post(
                api_url,
                json=request_data,
                timeout=60
            )
            
            # Check the response
            if response.status_code != 200:
                print(f"Error: API returned status code {response.status_code}")
                print(response.text)
                return None, None
            
            # Parse the response
            result = response.json()
            
            # Print the results
            print("\n" + "=" * 80)
            if result.get("metadata"):
                print(f"Title: {result['metadata'].get('title')}")
                print(f"Processing time: {result['metadata'].get('processing_time_ms')} ms")
                print(f"File size: {result['metadata'].get('file_size_bytes')} bytes")
            print("=" * 80)
            print("\nMarkdown output:\n")
            print(result.get("markdown", "No markdown content returned"))
            print("\n" + "=" * 80)
            
            # Save the Markdown output if requested
            if output_path and result.get("markdown"):
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(result["markdown"])
                print(f"\nMarkdown output saved to: {output_path}")
            
            return result.get("markdown"), result.get("metadata")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None


async def main():
    parser = argparse.ArgumentParser(description="Test HTML to Markdown conversion")
    parser.add_argument("--file", help="Path to an HTML file to convert")
    parser.add_argument("--url", help="URL of an HTML page to convert")
    parser.add_argument("--api", help="Use the API for conversion (provide API URL)")
    parser.add_argument("--output", help="Path to save the Markdown output")
    
    args = parser.parse_args()
    
    if not args.file and not args.url:
        parser.error("Either --file or --url must be provided")
    
    if args.file:
        await test_html_file_conversion(args.file, args.output)
    elif args.url and args.api:
        await test_api_conversion(args.url, args.api, args.output)
    elif args.url:
        await test_html_url_conversion(args.url, args.output)


if __name__ == "__main__":
    asyncio.run(main())
