#!/usr/bin/env python3
"""
Simple HTTP server to serve the OpenAPI specification file.
This allows users to view the API documentation without running the full application.
"""
import argparse
import http.server
import socketserver
import webbrowser
from pathlib import Path


def serve_openapi(port=8080, open_browser=True):
    """
    Serve the OpenAPI specification file on the specified port.
    
    Args:
        port: Port to serve on
        open_browser: Whether to open a browser window
    """
    # Get the directory containing this script
    docs_dir = Path(__file__).parent.absolute()
    
    # Change to the docs directory
    import os
    os.chdir(docs_dir)
    
    # Create a simple HTTP server
    handler = http.server.SimpleHTTPRequestHandler
    
    # Create the server
    with socketserver.TCPServer(("", port), handler) as httpd:
        url = f"http://localhost:{port}/openapi.yaml"
        print(f"Serving OpenAPI specification at {url}")
        
        # Open the browser if requested
        if open_browser:
            # Open in Swagger UI
            swagger_url = f"https://petstore.swagger.io/?url={url}"
            print(f"Opening Swagger UI: {swagger_url}")
            webbrowser.open(swagger_url)
            
            # Also open in Redoc
            redoc_url = f"https://redocly.github.io/redoc/?url={url}"
            print(f"Opening Redoc: {redoc_url}")
            webbrowser.open(redoc_url)
        
        # Serve until interrupted
        try:
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serve the OpenAPI specification file")
    parser.add_argument("--port", type=int, default=8080, help="Port to serve on")
    parser.add_argument("--no-browser", action="store_true", help="Don't open a browser window")
    
    args = parser.parse_args()
    serve_openapi(port=args.port, open_browser=not args.no_browser)
