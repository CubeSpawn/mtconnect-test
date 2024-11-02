# MTConnect/OctoPrint Testing Environment with Node-RED

## Overview
Development and testing environment for MTConnect integration with OctoPrint using Node-RED for visualization and testing. Part of the CubeSpawn project.

## Components
- OctoPrint with Virtual Printer
- Node-RED for MTConnect monitoring and testing
- Development tools container
- MTConnect adapter plugin for OctoPrint

## Prerequisites
- Docker (v20.10 or higher)
- Docker Compose (v2.24 or higher)
- Git
- VSCode (recommended)

## Quick Start
1. Clone the repository:
```bash
git clone https://github.com/CubeSpawn/mtconnect-test.git
cd mtconnect-test

2. Build and start the containers

docker-compose up -d

3.Access the services

OctoPrint: http://localhost:5000
Node-RED: http://localhost:1880
Development Environment: http://localhost:3000

Project Structure

mtconnect-test/
  ├─ docker/
  │  ├─ octoprint/
  │  │  └─ Dockerfile
  │  └─ dev-tools/
  │     └─ Dockerfile
  ├─ src/
  │  ├─ octoprint_mtconnect/
  │  │  └─ __init__.py
  │  └─ nodered/
  │     ├─ settings.js
  │     └─ flows/
  ├─ logs/
  │  ├─ octoprint/
  │  └─ nodered/
  └─ docker-compose.yml

License
MIT License