#!/bin/bash

# Create base directories
mkdir -p nodered_data/flows
mkdir -p src/nodered/flows
mkdir -p src/octoprint_mtconnect

# Create Node-RED settings file
cat > nodered_data/settings.js << 'EOL'
module.exports = {
    flowFile: 'flows.json',
    flowFilePretty: true,
    userDir: '/data',
    functionGlobalContext: {
        xml2js: require('xml2js')
    },
    editorTheme: {
        projects: {
            enabled: true
        }
    },
    httpStatic: '/data/public',
    // Enable CORS for development
    httpNodeCors: {
        origin: "*",
        methods: "GET,PUT,POST,DELETE"
    },
    uiPort: 1880,
    // Secure credentials encryption key
    credentialSecret: "mtconnect-dev-secret",
    diagnostics: {
        enabled: true
    }
}
EOL

# Create initial flows file
cat > nodered_data/flows/flows.json << 'EOL'
{
    "id": "mtconnect-base-flow",
    "label": "MTConnect Flow",
    "nodes": [],
    "configs": []
}
EOL

# Create package.json for Node-RED dependencies
cat > nodered_data/package.json << 'EOL'
{
    "name": "mtconnect-nodered",
    "version": "1.0.0",
    "description": "MTConnect Node-RED Configuration",
    "dependencies": {
        "node-red-contrib-mtconnect": "latest",
        "node-red-dashboard": "latest",
        "xml2js": "latest"
    }
}
EOL

# Update docker-compose.yml
cat > docker-compose.yml << 'EOL'
version: '3.8'

services:
  nodered:
    image: nodered/node-red:latest
    user: "0"
    ports:
      - "1880:1880"
      - "7878:7878"
    volumes:
      - ./nodered_data:/data
      - ./src/nodered/flows:/data/flows
    environment:
      - TZ=UTC
      - FLOWS=flows.json
      - NODE_RED_ENABLE_PROJECTS=true
    command: >
      sh -c "cd /data && 
             npm install && 
             npm start -- --userDir /data"
    networks:
      - mtconnect_net

  octoprint:
    image: octoprint/octoprint:latest
    ports:
      - "5000:5000"
    volumes:
      - ./src/octoprint_mtconnect:/plugin/mtconnect
    environment:
      - ENABLE_VIRTUAL_PRINTER=true
    networks:
      - mtconnect_net

networks:
  mtconnect_net:
    driver: bridge
EOL

# Create .gitignore
cat > .gitignore << 'EOL'
nodered_data/node_modules/
nodered_data/.npm/
nodered_data/.config/
nodered_data/.node-red/
*.log
EOL

# Make script executable
chmod +x setup.sh
EOL