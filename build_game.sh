#!/bin/bash

# Peluche Express Build Script
# This script builds the game as a standalone .exe file

echo "========================================"
echo "Building Peluche Express Game"
echo "========================================"
echo

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "Error: main.py not found. Please run this script from the project root directory."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment 'venv' not found."
    echo "Please create a virtual environment first:"
    echo "  python -m venv venv"
    echo "  source venv/Scripts/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

echo "Activating virtual environment..."
source venv/Scripts/activate

echo "Checking if PyInstaller is installed..."
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

echo
echo "Cleaning previous builds..."
if [ -d "build" ]; then
    rm -rf build
    echo "Removed build directory"
fi

if [ -d "dist" ]; then
    rm -rf dist
    echo "Removed dist directory"
fi

echo
echo "Building executable with PyInstaller..."
echo "This may take a few minutes..."
echo

# Run PyInstaller with the spec file
pyinstaller --clean peluche_express.spec

# Check if build was successful
if [ $? -eq 0 ]; then
    echo
    echo "========================================"
    echo "✅ Build completed successfully!"
    echo "========================================"
    echo
    echo "Your game executable is located at:"
    echo "  $(pwd)/dist/PelucheExpress.exe"
    echo
    echo "File size: $(du -h dist/PelucheExpress.exe | cut -f1)"
    echo
    echo "You can now share this .exe file with anyone!"
    echo "They don't need Python or any dependencies installed."
    echo
    echo "To test the game, run:"
    echo "  cd dist && ./PelucheExpress.exe"
    echo
else
    echo
    echo "========================================"
    echo "❌ Build failed!"
    echo "========================================"
    echo
    echo "Check the error messages above for details."
    echo "Common issues:"
    echo "  - Missing dependencies in requirements.txt"
    echo "  - File path issues in source code"
    echo "  - Missing assets or config files"
    echo
    exit 1
fi

echo "Build script completed."
