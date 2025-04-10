FROM public.docker.nexus3.auiag.corp/library/python:3.12.7-slim AS base

# for vm
# ARG http_proxy
# ARG https_proxy

COPY ca-bundle.pem /usr/local/share/ca-certificates/ca-bundle.crt
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && update-ca-certificates

WORKDIR /app

# Copy the entire backend directory into the container
COPY ./app /app/app

# Copy the requirements.txt file
COPY ./requirements.txt /app/requirements.txt

# Set PYTHONPATH
ENV PYTHONPATH=/app \
    PYTHONBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    REQUESTS_CA_BUNDLE="/etc/ssl/certs/ca-certificates.crt" \
    SSL_CERT_FILE="/etc/ssl/certs/ca-certificates.crt" \
    CURL_CA_BUNDLE="/etc/ssl/certs/ca-certificates.crt" \
    GRPC_DEFAULT_SSL_ROOTS_FILE_PATH="/etc/ssl/certs/ca-certificates.crt"\
    NODE_EXTRA_CA_CERTS="/etc/ssl/certs/ca-certificates.crt" 

# for vm
# ENV http_proxy=http://cloudproxy.auiag.corp:8080 \
#     https_proxy=http://cloudproxy.auiag.corp:8080

# Install dependencies
RUN pip install uv
RUN uv pip install -r /app/requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org --system

# # Download the model
# RUN python -c "from transformers import AutoTokenizer, AutoModel; \
#     AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2'); \
#     AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')"

# Create a startup script
COPY ./start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Use the startup script as the entry point
CMD ["/app/start.sh"]