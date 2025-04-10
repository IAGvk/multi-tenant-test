FROM public.docker.nexus3.auiag.corp/library/python:3.12.7-slim AS base

COPY ca-bundle.pem /usr/local/share/ca-certificates/ca-bundle.crt
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ca-certificates \
    gcc \
    curl postgresql-client \
    && rm -rf /var/lib/apt/lists/* \
    && update-ca-certificates
    
WORKDIR /app

# Install uv
# RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
#     && echo 'export PATH="/root/.local/bin:$PATH"' >> ~/.bashrc \
#     && . ~/.bashrc

# Copy the entire frontend directory into the container
COPY ./streamlit_app /app/streamlit_app

# Copy the requirements.txt file from the root directory
COPY ./requirements.txt /app/requirements.txt

# Install only frontend-related dependencies from requirements.txt
# also removed --no-cache-dir after pip install to speed up testing)
# RUN pip install -r /app/requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org


# Use uv to install dependencies
RUN pip install uv
RUN uv pip install -r /app/requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org --system 


# Run the Streamlit application
CMD ["streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--logger.level=debug"]