@echo off
REM Run the FastAPI inference server

echo ========================================
echo Heart Disease Prediction API Server
echo ========================================
echo.

cd /d "%~dp0"

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting FastAPI server on http://127.0.0.1:8000
echo.
echo API Documentation:
echo   - Swagger UI: http://127.0.0.1:8000/docs
echo   - ReDoc: http://127.0.0.1:8000/redoc
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn inference.app:app --host 127.0.0.1 --port 8000 --reload
