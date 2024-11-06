# Standard library imports
import time
from datetime import datetime

# Third-party imports
import octoprint.plugin
from flask import jsonify, make_response, request
import logging
import dicttoxml
from xml.dom.minidom import parseString

# Set up logging
_logger = logging.getLogger("octoprint.plugins.mtconnect")
_logger.setLevel(logging.DEBUG)
_logger.debug("MTConnect plugin module loaded")

class MtconnectPlugin(octoprint.plugin.StartupPlugin,
                     octoprint.plugin.SettingsPlugin,
                     octoprint.plugin.AssetPlugin,
                     octoprint.plugin.BlueprintPlugin):
    
    def __init__(self):
        """Initialize plugin and set up logging"""
        _logger.debug("MTConnect plugin initializing")
        self._sequence = 0
        self._start_time = time.time()
        
    def build_mtconnect_response(self, completion, temps, printer_data):
        """
        Build the MTConnect response structure
        Returns a dictionary formatted according to MTConnect standard
        """
        try:
            timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            position = printer_data.get("currentZ", 0)
            if position is None:
                position = 0
                
            # Increment sequence number
            self._sequence += 1
            
            return {
                "MTConnectStreams": {
                    "Header": {
                        "instanceId": "1",
                        "version": "1.7.0",
                        "sender": "OctoPrint MTConnect Adapter",
                        "creationTime": timestamp,
                        "nextSequence": str(self._sequence + 1),
                        "firstSequence": "1",
                        "lastSequence": str(self._sequence)
                    },
                    "Streams": [{
                        "DeviceStream": {
                            "uuid": self._settings.get(["uuid"]),
                            "name": self._settings.get(["device_name"]),
                            "ComponentStreams": {
                                "ComponentStream": [
                                    {
                                        "component": "Head",
                                        "componentId": "print_head",
                                        "Samples": {
                                            "Sample": [
                                                {
                                                    "name": "nozzle_temperature",
                                                    "timestamp": timestamp,
                                                    "sequence": str(self._sequence),
                                                    "value": str(temps.get("tool0", {}).get("actual", 0))
                                                },
                                                {
                                                    "name": "z_position",
                                                    "timestamp": timestamp,
                                                    "sequence": str(self._sequence),
                                                    "value": str(position)
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        "component": "Table",
                                        "componentId": "build_plate",
                                        "Samples": {
                                            "Sample": [
                                                {
                                                    "name": "bed_temperature",
                                                    "timestamp": timestamp,
                                                    "sequence": str(self._sequence),
                                                    "value": str(temps.get("bed", {}).get("actual", 0))
                                                }
                                            ]
                                        }
                                    }
                                ]
                            },
                            "Events": {
                                "Event": [
                                    {
                                        "name": "availability",
                                        "timestamp": timestamp,
                                        "sequence": str(self._sequence),
                                        "value": "AVAILABLE" if self._printer.is_operational() else "UNAVAILABLE"
                                    },
                                    {
                                        "name": "system_status",
                                        "timestamp": timestamp,
                                        "sequence": str(self._sequence),
                                        "value": self.map_printer_state(printer_data.get("state", {}).get("text", "UNKNOWN"))
                                    },
                                    {
                                        "name": "execution",
                                        "timestamp": timestamp,
                                        "sequence": str(self._sequence),
                                        "value": "ACTIVE" if self._printer.is_printing() else "READY"
                                    }
                                ]
                            },
                            "Samples": {
                                "Sample": [
                                    {
                                        "name": "percent_complete",
                                        "timestamp": timestamp,
                                        "sequence": str(self._sequence),
                                        "value": "{:.1f}".format(float(completion))
                                    },
                                    {
                                        "name": "process_time",
                                        "timestamp": timestamp,
                                        "sequence": str(self._sequence),
                                        "value": str(int(printer_data.get("progress", {}).get("printTime", 0) or 0))
                                    }
                                ]
                            }
                        }
                    }]
                }
            }
        except Exception as e:
            _logger.error(f"Error building MTConnect response: {str(e)}")
            raise

    def format_response(self, data, want_xml=False):
        """Format the response as either XML or JSON"""
        try:
            if want_xml:
                xml = dicttoxml.dicttoxml(data, custom_root='MTConnectStreams', attr_type=False)
                dom = parseString(xml)
                response = make_response(dom.toprettyxml(indent="  "))
                response.headers['Content-Type'] = 'application/xml'
                return response
            else:
                return jsonify(data)
        except Exception as e:
            _logger.error(f"Error formatting response: {str(e)}")
            raise

    @octoprint.plugin.BlueprintPlugin.route("/current", methods=["GET"])
    def handle_current(self):
        """Handle requests for current state in MTConnect format"""
        try:
            _logger.debug("Getting printer data...")
            printer_data = self._printer.get_current_data()
            _logger.debug(f"Printer data: {printer_data}")
            
            temps = self._printer.get_current_temperatures()
            _logger.debug(f"Temperature data: {temps}")
            
            # Safe extraction of completion percentage
            completion = 0.0
            if printer_data and "progress" in printer_data:
                completion = printer_data["progress"].get("completion", 0.0)
                if completion is None:
                    completion = 0.0
            
            _logger.debug(f"Completion: {completion}")
            
            # Build and return response
            current_data = self.build_mtconnect_response(completion, temps, printer_data)
            want_xml = request.args.get('format', '').lower() == 'xml'
            
            return self.format_response(current_data, want_xml)
            
        except Exception as e:
            _logger.error(f"Error handling current request: {str(e)}")
            return make_response(jsonify({"error": str(e)}), 500)

    def map_printer_state(self, state):
        """Map OctoPrint states to MTConnect states"""
        state_map = {
            "Operational": "READY",
            "Printing": "ACTIVE",
            "Cancelling": "INTERRUPTED",
            "Paused": "INTERRUPTED",
            "Pausing": "INTERRUPTED",
            "Error": "FAULT",
            "Offline": "UNAVAILABLE",
            "Starting": "READY",
            "Connecting": "READY"
        }
        return state_map.get(state, "UNKNOWN")

    def is_blueprint_protected(self):
        """Determine if the blueprint requires authentication"""
        return False  # Open endpoint for MTConnect standard compliance

    def get_settings_defaults(self):
        """Define default settings"""
        return dict(
            uuid="OCTO001",
            device_name="OctoPrint Device",
            manufacturer="CubeSpawn",
            serialNumber="001",
            station="3D-PRINTER-01"
        )

    def get_update_information(self):
        """Define update information for plugin manager"""
        return dict(
            mtconnect=dict(
                displayName=self._plugin_name,
                displayVersion=self._plugin_version,
                type="github_release",
                current=self._plugin_version,
                user="CubeSpawn",
                repo="octoprint-mtconnect",
                pip="https://github.com/CubeSpawn/octoprint-mtconnect/archive/{target}.zip"
            )
        )

# Plugin registration
__plugin_name__ = "MTConnect"
__plugin_version__ = "0.1.0"
__plugin_description__ = "MTConnect adapter for OctoPrint"
__plugin_author__ = "CubeSpawn"
__plugin_license__ = "AGPLv3"
__plugin_pythoncompat__ = ">=3.7,<4"

def __plugin_load__():
    plugin = MtconnectPlugin()
    global __plugin_implementation__
    __plugin_implementation__ = plugin
    
    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": plugin.get_update_information
    }