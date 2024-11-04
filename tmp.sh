# Create the base directories
mkdir -p src/octoprint_mtconnect/static/js
mkdir -p src/octoprint_mtconnect/templates

# Create setup.py in the correct location
cat > src/octoprint_mtconnect/setup.py << 'EOL'
from setuptools import setup

plugin_identifier = "mtconnect"
plugin_package = "octoprint_mtconnect"
plugin_name = "OctoPrint-MTConnect"
plugin_version = "0.1.0"
plugin_description = "MTConnect adapter for OctoPrint"
plugin_author = "Your Name"
plugin_author_email = "you@example.com"
plugin_license = "AGPLv3"

setup(
    name=plugin_name,
    version=plugin_version,
    description=plugin_description,
    author=plugin_author,
    author_email=plugin_author_email,
    license=plugin_license,
    
    packages=["octoprint_mtconnect"],
    package_data={
        "octoprint_mtconnect": [
            "templates/*.jinja2",
            "static/js/*.js"
        ]
    },
    entry_points={
        "octoprint.plugin": [
            "mtconnect = octoprint_mtconnect:MTConnectPlugin"
        ]
    }
)
EOL

# Create MANIFEST.in
cat > src/octoprint_mtconnect/MANIFEST.in << 'EOL'
include README.md
recursive-include octoprint_mtconnect/templates *
recursive-include octoprint_mtconnect/static *
EOL

# Verify the file structure
ls -la src/octoprint_mtconnect/

# Next step would be to make sure __init__.py is in the correct location
# and contains our plugin code
