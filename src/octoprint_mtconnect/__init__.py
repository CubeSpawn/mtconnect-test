import octoprint.plugin
from octoprint.events import Events
import xml.etree.ElementTree as ET
import socket
import threading
import time

class MTConnectPlugin(octoprint.plugin.StartupPlugin,
                     octoprint.plugin.EventHandlerPlugin,
                     octoprint.plugin.SettingsPlugin):
    
    def __init__(self):
        self.current_position = {"X": 0, "Y": 0, "Z": 0}
        self.current_temps = {"tool0": 0, "bed": 0}
        self.printer_state = "UNAVAILABLE"
        self.mtconnect_socket = None
        
    def on_after_startup(self):
        self._logger.info("MTConnect adapter starting up...")
        self.start_mtconnect_server()
        
    def get_settings_defaults(self):
        return dict(
            port=7878,  # Default MTConnect port
            update_interval=1.0  # Update frequency in seconds
        )
    
    def on_event(self, event, payload):
        if event == Events.POSITION_UPDATE:
            self.current_position = payload
        elif event == Events.TEMPERATURE_UPDATED:
            self.current_temps = payload
        elif event == Events.PRINTER_STATE_CHANGED:
            self.printer_state = payload["state_id"]
            
    def generate_mtconnect_response(self):
        # Create MTConnect XML response
        root = ET.Element("MTConnectDevices")
        devices = ET.SubElement(root, "Devices")
        device = ET.SubElement(devices, "Device", 
                             uuid="printer1",
                             name="3D_Printer")
                             
        # Add position components
        for axis in ["X", "Y", "Z"]:
            ET.SubElement(device, "DataItem",
                         category="SAMPLE",
                         id=f"pos_{axis}",
                         type="POSITION",
                         subType=axis)
                         
        # Add temperature components
        for heater in ["tool0", "bed"]:
            ET.SubElement(device, "DataItem",
                         category="SAMPLE",
                         id=f"temp_{heater}",
                         type="TEMPERATURE")
                         
        return ET.tostring(root)
        
    def start_mtconnect_server(self):
        def server_thread():
            port = self._settings.get_int(["port"])
            self.mtconnect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.mtconnect_socket.bind(("0.0.0.0", port))
            self.mtconnect_socket.listen(5)
            
            while True:
                client, addr = self.mtconnect_socket.accept()
                self._logger.info(f"MTConnect client connected from {addr}")
                
                try:
                    while True:
                        data = self.generate_mtconnect_response()
                        client.send(data)
                        time.sleep(self._settings.get_float(["update_interval"]))
                except:
                    self._logger.info("Client disconnected")
                    client.close()
                    
        thread = threading.Thread(target=server_thread)
        thread.daemon = True
        thread.start()

    def get_update_information(self):
        return dict(
            mtconnect=dict(
                displayName="MTConnect Adapter",
                displayVersion=self._plugin_version,
                type="utility",
                python=">=3,<4"
            )
        )

__plugin_name__ = "MTConnect Adapter"
__plugin_pythoncompat__ = ">=3,<4"
__plugin_implementation__ = MTConnectPlugin()
