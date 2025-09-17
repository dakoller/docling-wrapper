#!/bin/bash
# Script to run the application locally for testing

# Make the script executable
chmod +x test/test_conversion.py

# Create temp directory if it doesn't exist
mkdir -p temp

# Check if Python 3.12 is available
if command -v python3.12 &> /dev/null; then
    PYTHON=python3.12
elif command -v python3 &> /dev/null; then
    PYTHON=python3
else
    echo "Error: Python 3 is required but not found"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
if command -v uv &> /dev/null; then
    uv pip install -e .
    # Ensure required packages are installed
    uv pip install uvicorn fastapi httpx pydantic
else
    $PYTHON -m pip install -e .
    # Ensure required packages are installed
    $PYTHON -m pip install uvicorn fastapi httpx pydantic
fi

# Run the application
echo "Starting the application..."
$PYTHON src/main.py &
APP_PID=$!

# Wait for the application to start
echo "Waiting for the application to start..."
sleep 3

# Test the application with the sample HTML file
echo "Testing the application with the sample HTML file..."
$PYTHON test/test_conversion.py --file test/sample.html --output test/sample_output.md

# Test the application with a URL
echo "Testing the application with a URL..."
$PYTHON test/test_conversion.py --url https://example.com --output test/example_output.md

# Test the API
echo "Testing the API..."
$PYTHON test/test_conversion.py --url https://example.com --api http://localhost:8000/api/v1/convert --output test/api_output.md

# Clean up
echo "Cleaning up..."
kill $APP_PID

echo "Done!"
