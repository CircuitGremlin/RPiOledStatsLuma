#!/bin/bash

# Go into home directory
echo "Go into home directory"
cd ~/

# Get repo
echo "Get repo"
git clone https://github.com/CircuitGremlin/RPiOledStatsLuma.git

# Open directory
echo "Open directory"
cd RPiOledStatsLuma

# Create virtual python environment
echo "Create virtual python environment"
python3 -m venv --system-site-packages pyvenv

# Activate virtual python environment
echo "Activate virtual python environment"
source ./pyvenv/bin/activate

# Install pip packages
echo "Install pip packages"
pip3 install pyyaml psutil luma.oled

# Done
echo "Done!"
