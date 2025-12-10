#!/bin/bash

# Smart Parking Management System - Quick Start Script
# This script sets up and runs the application

echo "=================================="
echo "Smart Parking Management System"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if dependencies are installed
if ! python -c "import reportlab" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
else
    echo "✓ Dependencies already installed"
fi

echo ""
echo "Starting application..."
echo "Default login: admin / admin123"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Run the application
python finaloop.py
