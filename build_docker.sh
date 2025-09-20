#!/bin/bash
# Script to build the Docker image locally

# Build the Docker image
echo "Building Docker image locally..."
docker compose build

echo "Done! The image has been built locally."
echo "To run the application, use ./run_docker.sh"
echo "To push the image to Docker Hub, use ./push_to_dockerhub.sh"
