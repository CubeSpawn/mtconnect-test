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
    netcat \
    libxml2-utils \
    && rm -rf /var/lib/apt/lists/*

# Install latest Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Install VSCode Server
RUN curl -fsSL https://code-server.dev/install.sh | sh

# Install Python tools
RUN pip3 install \
    ipython \
    pytest \
    black \
    flake8 \
    mypy \
    debugpy \
    requests \
    xmltodict

# Install global Node.js tools
RUN npm install -g \
    node-red-admin \
    xml2js \
    prettier

# Set up workspace
WORKDIR /workspace

# Add development scripts
COPY setup-dev.sh /usr/local/bin/setup-dev
RUN chmod +x /usr/local/bin/setup-dev

# Install VSCode extensions
RUN code-server --install-extension dbaeumer.vscode-eslint \
    --install-extension esbenp.prettier-vscode \
    --install-extension redhat.vscode-xml \
    --install-extension eg2.vscode-npm-script \
    --install-extension ms-python.python \
    --install-extension eamodio.gitlens

# Create settings file for VSCode
RUN mkdir -p /root/.local/share/code-server/User
COPY settings.json /root/.local/share/code-server/User/settings.json

# Default command starts code-server
CMD ["code-server", "--bind-addr", "0.0.0.0:3000", "--auth", "none", "/workspace"]