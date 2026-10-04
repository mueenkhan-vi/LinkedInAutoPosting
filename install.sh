#!/bin/bash

set -e

echo ""
echo "============================================================"
echo "    LinkedIn Agent - Installer"
echo "============================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ using your package manager"
    exit 1
fi

# Check/install dependencies
echo "Checking dependencies..."
pip3 list | grep -q pyinstaller || {
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
}

# Build executable
echo "Building executable..."
python3 build_executable.py

echo ""
echo "============================================================"
echo "    Setup Complete!"
echo "============================================================"
echo ""
echo "Your LinkedIn Agent executable is ready at:"
echo "   ./installer/LinkedInAgent"
echo ""
echo "Next steps:"
echo "1. Copy your .env file to the same folder as LinkedInAgent"
echo "   (or rename .env.example to .env and add your credentials)"
echo "2. Run: ./installer/LinkedInAgent"
echo ""
