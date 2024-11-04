from setuptools import setup

setup(
    name="OctoPrint-MTConnect",
    version="0.1.0",
    description="MTConnect adapter for OctoPrint",
    author="CubeSpawn",
    author_email="your.email@example.com",
    license="AGPLv3",
    packages=["octoprint_mtconnect"],  # Changed back to package name
    python_requires=">=3.7,<4",  # Add Python version requirement
    install_requires=[
        'dicttoxml==1.7.4',
    ],
    entry_points={
        "octoprint.plugin": [
            "mtconnect = octoprint_mtconnect:MtconnectPlugin"  # Fixed entry point
        ]
    }
)