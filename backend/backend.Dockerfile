FROM python:3.9-slim

WORKDIR /app

# Copy the entire backend directory into the container
COPY ./app /app/app

# Copy the requirements.txt file from the root directory
COPY ./requirements.txt /app/requirements.txt

# Set PYTHONPATH to the working directory
ENV PYTHONPATH=/app

# Install only backend-related dependencies from requirements.txt (creating temp req file as bin/sh by docker doesn't support process substitution like bash --reqs <(grep -E ...)) 
# also removed --no-cache-dir after pip install to speed up testing)
RUN pip install -r /app/requirements.txt

# Run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]