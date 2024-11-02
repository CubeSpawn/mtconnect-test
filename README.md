# MTConnect/OctoPrint Virtual Test Environment

## Overview
A testing environment for MTConnect integration with OctoPrint, part of the CubeSpawn project. This environment provides containerized instances of OctoPrint and TrakHound for developing and testing MTConnect communications.

## Prerequisites
- Docker (v20.10 or higher)
- Docker Compose (v2.24 or higher)
- Git
- VSCode (recommended)

## Quick Start
1. Clone the repository:

git clone https://github.com/CubeSpawn/mtconnect-test.git
cd mtconnect-test

2. Build and start the containers:

docker-compose up -d

3. Access the services:

OctoPrint: http://localhost:5000
TrakHound: http://localhost:7878

Development
This environment provides:

Virtual printer simulation in OctoPrint
MTConnect adapter development and testing
Network communication validation
Log monitoring and debugging