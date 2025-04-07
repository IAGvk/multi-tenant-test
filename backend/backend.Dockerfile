FROM python:3.9-slim

WORKDIR /app

# Copy the entire backend directory into the container
COPY ./app /app/app

# Copy the requirements.txt file
COPY ./requirements.txt /app/requirements.txt

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Install dependencies
RUN pip install -r /app/requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

# Create a startup script
COPY ./start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Use the startup script as the entry point
CMD ["/app/start.sh"]