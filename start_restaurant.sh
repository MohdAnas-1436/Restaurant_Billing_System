#!/bin/bash

echo "==============================================="
echo "   Royal Restaurant Billing System"
echo "   Offline Restaurant Management"
echo "==============================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed"
        echo "Please install Python 3.7+ and try again"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Python found! Starting application..."
echo

# Install requirements
echo "Installing/checking required packages..."
$PYTHON_CMD -m pip install streamlit pandas plotly

echo
echo "Starting Royal Restaurant Billing System..."
echo
echo "IMPORTANT:"
echo "- The application will open in your browser at http://localhost:5000"
echo "- Keep this terminal open while using the application"
echo "- Press Ctrl+C to stop the application"
echo

# Start the application
$PYTHON_CMD -m streamlit run app.py --server.port 5000 --server.headless true

echo
echo "Application stopped. Thank you for using Royal Restaurant Billing System!"