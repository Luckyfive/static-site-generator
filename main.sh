#!/bin/bash

# Generate the site
python3 src/main.py

# Start the web server from the public directory
cd public && python3 -m http.server 8888