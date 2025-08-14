@echo off
title Royal Restaurant Billing System
echo.
echo ===============================================
echo   Royal Restaurant Billing System
echo   Offline Restaurant Management
echo ===============================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found! Starting application...
echo.

:: Install requirements if needed
echo Installing/checking required packages...
pip install streamlit pandas plotly

echo.
echo Starting Royal Restaurant Billing System...
echo.
echo IMPORTANT:
echo - The application will open in your browser at http://localhost:5000
echo - Keep this window open while using the application
echo - Press Ctrl+C to stop the application
echo.

:: Start the application
streamlit run app.py --server.port 5000 --server.headless true

echo.
echo Application stopped. Thank you for using Royal Restaurant Billing System!
pause