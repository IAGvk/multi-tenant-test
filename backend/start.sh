#!/bin/bash
echo "Waiting for database..."
python -c "from app.core.wait_for_db import wait_for_db; wait_for_db()"

echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000