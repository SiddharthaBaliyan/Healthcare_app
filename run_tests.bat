@echo off
REM Quick Test Runner Script
REM Run pytest tests locally before pushing to GitHub

cls
echo ========================================
echo Heart Disease Predictor - Test Suite
echo ========================================
echo.

cd /d "%~dp0"

echo Checking virtual environment...
if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then run: venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✓ Virtual environment found
echo.

echo Installing test dependencies...
call venv\Scripts\pip install -q pytest pytest-cov pytest-asyncio requests 2>nul

echo.
echo ========================================
echo Running Test Suite
echo ========================================
echo.

REM Run all tests with coverage
call venv\Scripts\pytest tests/ -v --cov=inference --cov=training --cov-report=html

echo.
echo ========================================
echo Test Results
echo ========================================
echo.
echo ✓ Coverage report generated: htmlcov/index.html
echo ✓ Open the HTML file in your browser to view coverage details
echo.

pause
