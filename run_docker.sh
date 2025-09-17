#!/bin/bash
# Script to run the application in Docker

# Build the Docker image
echo "Building Docker image..."
docker compose build

# Start the containers
echo "Starting containers..."
docker compose up -d

# Wait for the application to start
echo "Waiting for the application to start..."
sleep 5

# Test the API
echo "Testing the API..."
curl -X POST "http://localhost:8000/api/v1/convert" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "html_url",
    "source": "https://example.com",
    "options": {
      "include_metadata": true,
      "preserve_images": false
    }
  }' | jq .

# Show logs
echo "Showing logs (press Ctrl+C to exit)..."
docker compose logs -f
