FROM ubuntu:20.04

# Avoid timezone prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    openjdk-11-jre \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Install TrakHound
RUN wget https://github.com/TrakHound/MTConnect.NET/releases/download/v2.0.0/MTConnect.NET-2.0.0.zip \
    && unzip MTConnect.NET-2.0.0.zip \
    && rm MTConnect.NET-2.0.0.zip

# Expose MTConnect port
EXPOSE 7878

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7878/ || exit 1

CMD ["java", "-jar", "MTConnect.NET-2.0.0.jar"]