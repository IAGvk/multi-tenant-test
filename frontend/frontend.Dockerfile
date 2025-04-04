FROM python:3.9-slim

WORKDIR /app

# Copy the entire frontend directory into the container
COPY ./streamlit_app /app/streamlit_app

# Copy the requirements.txt file from the root directory
COPY ./requirements.txt /app/requirements.txt

# Install only frontend-related dependencies from requirements.txt
# also removed --no-cache-dir after pip install to speed up testing)
RUN pip install -r /app/requirements.txt 

# Run the Streamlit application
CMD ["streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--logger.level=debug"]