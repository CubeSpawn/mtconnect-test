FROM octoprint/octoprint:latest

# Install additional dependencies
RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install development tools
RUN pip install \
    pytest \
    pytest-cov \
    black \
    flake8

# Copy plugin requirements and install
COPY requirements.txt /plugin/requirements.txt
RUN pip install -r /plugin/requirements.txt

# Health check
HEALTHCHECK --interval=30s --timeout=60s --start-period=120s --retries=5 \
    CMD curl -f http://localhost:5000/ || exit 1