FROM ubuntu:20.04

# Avoid timezone prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install development tools
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    wget \
    vim \
    htop \
    tcpdump \
    tshark \
    && rm -rf /var/lib/apt/lists/*

# Install VSCode Server
RUN curl -fsSL https://code-server.dev/install.sh | sh

# Install Python tools
RUN pip3 install \
    ipython \
    pytest \
    black \
    flake8 \
    mypy \
    debugpy

# Set up workspace
WORKDIR /workspace

# Add development scripts
COPY setup-dev.sh /usr/local/bin/setup-dev
RUN chmod +x /usr/local/bin/setup-dev

# Default command starts code-server
CMD ["code-server", "--bind-addr", "0.0.0.0:3000", "--auth", "none", "/workspace"]