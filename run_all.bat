@echo off
REM Start both API and Frontend servers

echo ========================================
echo Heart Disease Predictor System
echo ========================================
echo.
echo Starting API Server (Port 8000)...
echo Starting Frontend Server (Port 5000)...
echo.

cd /d "%~dp0"

REM Start API in a new window
start "API Server" cmd /k "venv\Scripts\python -m uvicorn inference.app:app --host 0.0.0.0 --port 8000 --reload"

REM Wait a moment for API to start
timeout /t 3 /nobreak

REM Start Frontend in a new window
start "Frontend Server" cmd /k "venv\Scripts\python frontend/app.py"

echo.
echo ========================================
echo Servers Started!
echo ========================================
echo.
echo API Documentation:   http://localhost:8000/docs
echo Frontend:            http://localhost:5000
echo.
echo Two terminal windows have been opened:
echo 1. API Server (uvicorn) on port 8000
echo 2. Frontend Server (Flask) on port 5000
echo.
echo Close either window to stop that server.
echo.
pause
