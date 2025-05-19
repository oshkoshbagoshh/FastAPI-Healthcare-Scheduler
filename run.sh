#!/bin/bash

# Run the FastAPI application with Uvicorn
echo "Starting the Healthcare Scheduling API..."

# Check if the database exists, if not, seed it
if [ ! -f healthcare_scheduler.db ]; then
    echo "Database not found. Initializing and seeding the database..."
    # Start the server in the background
    uvicorn main:app --reload &
    PID=$!
    
    # Wait for the server to start
    sleep 3
    
    # Seed the database
    curl -X POST "http://localhost:8000/seed-database?patient_count=50&resource_count=10&days_ahead=30"
    
    # Kill the background server
    kill $PID
    
    echo "Database initialized and seeded."
fi

# Start the server
echo "Server is running at http://localhost:8000"
echo "API documentation is available at http://localhost:8000/docs"
uvicorn main:app --reload