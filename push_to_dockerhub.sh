#!/bin/bash
# Script to push the Docker image to Docker Hub

# Set the version
VERSION="0.1.0"

# Tag the images
echo "Tagging images..."
docker tag docling-wrapper-claude-api:latest dakoller/docling-wrapper:latest
docker tag docling-wrapper-claude-api:latest dakoller/docling-wrapper:$VERSION

# Push the images
echo "Pushing images to Docker Hub..."
docker push dakoller/docling-wrapper:latest
docker push dakoller/docling-wrapper:$VERSION

echo "Done!"
