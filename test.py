#!/bin/bash

# Build Docker image
if docker build -t my-image .; then
    echo "Docker image built successfully."
else
    echo "Failed to build Docker image."
    exit 1
fi

# Run Docker container
if docker run -d -p 8080:80 --name my-container my-image; then
    echo "Docker container started successfully."
else
    echo "Failed to start Docker container."
    exit 1
fi

# Push Docker image to registry
if docker push my-registry/my-image:tag; then
    echo "Docker image pushed to registry successfully."
else
    echo "Failed to push Docker image to registry."
    exit 1
fi

# Pull Docker image from registry
if docker pull my-registry/my-image:tag; then
    echo "Docker image pulled from registry successfully."
else
    echo "Failed to pull Docker image from registry."
    exit 1
fi

# Stop Docker container
if docker stop my-container; then
    echo "Docker container stopped successfully."
else
    echo "Failed to stop Docker container."
    exit 1
fi

# Remove Docker container
if docker rm my-container; then
    echo "Docker container removed successfully."
else
    echo "Failed to remove Docker container."
    exit 1
fi

# Remove Docker image
if docker rmi my-image; then
    echo "Docker image removed successfully."
else
    echo "Failed to remove Docker image."
    exit 1
fi
