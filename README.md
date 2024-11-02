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

Project Structure

mtconnect-test/
├── docker/
│   ├── octoprint/
│   │   └── Dockerfile
│   └── trakhound/
│       └── Dockerfile
├── src/
│   ├── octoprint_mtconnect/
│   │   └── __init__.py
│   └── trakhound/
├── logs/
│   ├── octoprint/
│   └── trakhound/
└── docker-compose.yml

Development
This environment provides:

Virtual printer simulation in OctoPrint
MTConnect adapter development and testing
Network communication validation
Log monitoring and debugging

License
MIT License
Copyright (c) 2024 CubeSpawn
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.