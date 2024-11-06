import octoprint.plugin
from flask import jsonify, make_response
import logging
import time

class MTConnectPlugin(octoprint.plugin.StartupPlugin,
                     octoprint.plugin.SettingsPlugin,
                     octoprint.plugin.AssetPlugin,
                     octoprint.plugin.BlueprintPlugin):

    def __init__(self):
        self._logger = logging.getLogger("octoprint.plugins.mtconnect")
        self._sequence = 0
        self._start_time = time.time()

    def is_blueprint_protected(self):
        return False

    def map_printer_state(self, state, temps):
        """Map printer state with temperature context"""
        if not self._printer.is_operational():
            return "OFFLINE"
            
        if self._printer.is_printing():
            return "PRINTING"
            
        # Check if heating
        tool_temp = temps.get("tool0", {})
        bed_temp = temps.get("bed", {})
        if (tool_temp.get("target", 0) > 0 and tool_temp.get("actual", 0) < tool_temp.get("target", 0)) or \
           (bed_temp.get("target", 0) > 0 and bed_temp.get("actual", 0) < bed_temp.get("target", 0)):
            return "HEATING"
            
        return "STANDBY"

    def get_movement_type(self, printer_data):
        """Determine movement type based on printer state"""
        if self._printer.is_printing():
            return "PRINTING"
        return "IDLE"

    @octoprint.plugin.BlueprintPlugin.route("/current", methods=["GET"])
    def handle_current(self):
        try:
            printer_data = self._printer.get_current_data()
            temps = self._printer.get_current_temperatures()
            
            # Get current state and progress info
            state = self.map_printer_state(printer_data.get("state", {}).get("text"), temps)
            movement_type = self.get_movement_type(printer_data)
            
            # Get progress information
            completion = 0.0
            if printer_data and "progress" in printer_data:
                completion = printer_data["progress"].get("completion", 0.0)
                if completion is None:
                    completion = 0.0

            timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            self._sequence += 1

            response = {
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
                                        "name": "system_status",
                                        "timestamp": timestamp,
                                        "sequence": str(self._sequence),
                                        "value": state
                                    },
                                    {
                                        "name": "movement_type",
                                        "timestamp": timestamp,
                                        "sequence": str(self._sequence),
                                        "value": movement_type
                                    }
                                ]
                            },
                            "Samples": {
                                "Sample": [
                                    {
                                        "name": "percent_complete",
                                        "timestamp": timestamp,
                                        "sequence": str(self._sequence),
                                        "value": str(completion)
                                    }
                                ]
                            }
                        }
                    }]
                }
            }
            
            return jsonify(response)
            
        except Exception as e:
            self._logger.error(f"Error handling current request: {str(e)}")
            return make_response(jsonify({"error": str(e)}), 500)

    def get_settings_defaults(self):
        return dict(
            uuid="OCTO001",
            device_name="OctoPrint Device"
        )

    def get_update_information(self):
        return dict(
            mtconnect=dict(
                displayName="MTConnect Plugin",
                displayVersion=self._plugin_version,
                type="github_release",
                user="CubeSpawn",
                repo="OctoPrint-MTConnect",
                current=self._plugin_version,
                pip="https://github.com/CubeSpawn/OctoPrint-MTConnect/archive/{target_version}.zip"
            )
        )

__plugin_name__ = "MTConnect"
__plugin_version__ = "0.1.0"
__plugin_description__ = "MTConnect adapter for OctoPrint"
__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = MTConnectPlugin()
