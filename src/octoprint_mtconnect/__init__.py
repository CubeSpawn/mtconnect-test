# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.events import Events

class MTConnectPlugin(octoprint.plugin.StartupPlugin,
                     octoprint.plugin.SettingsPlugin,
                     octoprint.plugin.EventHandlerPlugin,
                     octoprint.plugin.RestartNeedingPlugin):

    def on_after_startup(self):
        self._logger.info("MTConnect Plugin Started")
        
    def get_settings_defaults(self):
        return {
            "shdr_enabled": True,  # Enable SHDR protocol
            "rest_enabled": True,  # Enable REST endpoints
            "port": 7878,         # Default SHDR port
            "device_uuid": "OCTO1",  # Unique device identifier
            "device_name": "OctoPrint 3D Printer"  # Human readable name
        }
    
    def on_event(self, event, payload):
        """Handle OctoPrint events and convert to MTConnect events"""
        if event == Events.PRINT_STARTED:
            self._handle_print_started(payload)
        elif event == Events.PRINT_DONE:
            self._handle_print_done(payload)
        elif event == Events.PRINT_FAILED:
            self._handle_print_failed(payload)
        elif event == Events.PRINT_PAUSED:
            self._handle_print_paused(payload)
        elif event == Events.PRINT_RESUMED:
            self._handle_print_resumed(payload)
        elif event == Events.TEMPERATURE_UPDATED:
            self._handle_temperature_update(payload)
            
    def _handle_print_started(self, payload):
        # Convert to MTConnect EXECUTION state
        self._logger.info("Print started: Converting to MTConnect ACTIVE state")
        
    def _handle_print_done(self, payload):
        self._logger.info("Print completed: Converting to MTConnect READY state")
        
    def _handle_print_failed(self, payload):
        self._logger.info("Print failed: Converting to MTConnect FAULT state")
        
    def _handle_print_paused(self, payload):
        self._logger.info("Print paused: Converting to MTConnect INTERRUPTED state")
        
    def _handle_print_resumed(self, payload):
        self._logger.info("Print resumed: Converting to MTConnect ACTIVE state")
        
    def _handle_temperature_update(self, payload):
        self._logger.info("Temperature updated: Updating MTConnect samples")

    def get_update_information(self):
        return {
            "mtconnect": {
                "displayName": "MTConnect Plugin",
                "displayVersion": self._plugin_version,
                "type": "github_release",
                "current": self._plugin_version,
                "pip": "https://github.com/yourusername/OctoPrint-MTConnect/archive/{target_version}.zip"
            }
        }
        
__plugin_name__ = "MTConnect"
__plugin_pythoncompat__ = ">=3,<4"
__plugin_implementation__ = MTConnectPlugin()