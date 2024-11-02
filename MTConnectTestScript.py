import requests
import time
import json

def test_mtconnect_connection():
    """Test MTConnect adapter connectivity"""
    try:
        # Test OctoPrint connection
        octoprint_response = requests.get('http://localhost:5000')
        print(f"OctoPrint Status: {octoprint_response.status_code}")

        # Test Node-RED connection
        nodered_response = requests.get('http://localhost:1880')
        print(f"Node-RED Status: {nodered_response.status_code}")

        # Test MTConnect endpoint
        mtconnect_response = requests.get('http://localhost:7878/current')
        print(f"MTConnect Status: {mtconnect_response.status_code}")
        
        return True
    except Exception as e:
        print(f"Connection test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_mtconnect_connection()