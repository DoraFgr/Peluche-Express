#!/usr/bin/env bash

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    echo "Activating virtual environment and installing requirements..."
    source venv/Scripts/activate
    pip install --upgrade pip
    if [ -f requirements.txt ]; then
        pip install -r requirements.txt
    else
        echo "No requirements.txt found, skipping package installation."
    fi
else
    echo "Virtual environment already exists. Activating..."
    source venv/Scripts/activate
fi


echo "Virtual environment is ready."