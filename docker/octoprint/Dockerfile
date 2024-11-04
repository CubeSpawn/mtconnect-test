FROM octoprint/octoprint:latest

# Create plugin directories
RUN mkdir -p /octoprint/plugins/lib/python3.10/site-packages

# Install dependencies into the plugin's site-packages
RUN pip install --target=/octoprint/plugins/lib/python3.10/site-packages dicttoxml==1.7.4

# Set environment
ENV PYTHONPATH=/octoprint/plugins

WORKDIR /octoprint