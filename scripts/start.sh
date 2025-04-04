#!/bin/bash

echo "Starting the application..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Start the application using Docker Compose
docker-compose up -d --build

if [ $? -eq 0 ]; then
    echo "Application started successfully. Access it at http://localhost"
else
    echo "Error: Failed to start the application. Check the Docker logs for more details."
    exit 1
fi