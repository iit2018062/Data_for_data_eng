#!/bin/bash

# Install Python if not already installed
sudo apt-get update
sudo apt-get install -y python3 python3-pip

# Set up virtual environment
python3 -m venv myenv
source myenv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Python script
#python3 /home/kumari/Pub-sub/clean.py
#python3 create-sub.py
python3 code.py
git add .
git commit -m "Auto commit by script"
git push origin main


# Deactivate virtual environment
deactivate

