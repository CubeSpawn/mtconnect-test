FROM octoprint/octoprint:latest

# Install additional dependencies
RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install development tools
RUN pip install \
    pytest \
    pytest-cov \
    black \
    flake8

# Set up plugin development directory
WORKDIR /plugin

# Copy plugin requirements (we'll create this file next)
COPY requirements.txt /plugin/requirements.txt
RUN pip install -r requirements.txt

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1