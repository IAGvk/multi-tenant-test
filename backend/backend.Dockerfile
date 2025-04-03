FROM python:3.9-slim

WORKDIR /app

# Copy the entire backend directory into the container
COPY ./app /app/app

# Set PYTHONPATH to the working directory
ENV PYTHONPATH=/app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn pydantic openai sqlalchemy passlib[bcrypt] python-jose python-dotenv

# Run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]