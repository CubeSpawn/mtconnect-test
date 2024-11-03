# coding=utf-8
from setuptools import setup

plugin_identifier = "mtconnect"
plugin_package = "octoprint_mtconnect"
plugin_name = "OctoPrint-MTConnect"
plugin_version = "0.1.0"
plugin_description = """Adds MTConnect capability to OctoPrint"""
plugin_author = "CubeSpawn"
plugin_author_email = "cubespawn@gmail.com"
plugin_url = "https://github.com/CubeSpawn/mtconnect-test"
plugin_license = "AGPLv3"

plugin_requires = [
    "OctoPrint>=1.4.0"
]

setup(
    name=plugin_name,
    version=plugin_version,
    description=plugin_description,
    author=plugin_author,
    author_email=plugin_author_email,
    url=plugin_url,
    license=plugin_license,
    requires=plugin_requires,
    
    packages=["octoprint_mtconnect"],
    package_data={
        "octoprint_mtconnect": []
    },
    
    entry_points={
        "octoprint.plugin": [
            "mtconnect = octoprint_mtconnect:__plugin_implementation__"
        ]
    }
)