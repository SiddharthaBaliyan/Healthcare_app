@echo off
REM Quick Start Guide for Heart Disease Predictor

cls
echo.
echo =========================================================
echo   HEART DISEASE PREDICTOR - QUICK START GUIDE
echo =========================================================
echo.
echo This script will help you get started with the system.
echo.
echo Select an option:
echo.
echo   1. First Time Setup (Install Dependencies)
echo   2. Train Model (If not already trained)
echo   3. Start API Server (Port 8000)
echo   4. Start Frontend Server (Port 5000)
echo   5. Start Both Servers (API + Frontend)
echo   6. View Documentation
echo   7. Exit
echo.

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto setup
if "%choice%"=="2" goto train
if "%choice%"=="3" goto api
if "%choice%"=="4" goto frontend
if "%choice%"=="5" goto both
if "%choice%"=="6" goto docs
if "%choice%"=="7" goto exit

echo Invalid choice. Please try again.
timeout /t 2
goto start

:setup
echo.
echo Installing dependencies...
cd /d "%~dp0"
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo Installation complete!
pause
goto start

:train
echo.
echo Training the model...
cd /d "%~dp0"
call venv\Scripts\activate.bat
python training\train.py
echo Training complete!
pause
goto start

:api
echo.
echo Starting API Server on http://localhost:8000
echo.
echo API Documentation available at:
echo   - Swagger UI: http://localhost:8000/docs
echo   - ReDoc: http://localhost:8000/redoc
echo.
cd /d "%~dp0"
call venv\Scripts\activate.bat
python -m uvicorn inference.app:app --host 0.0.0.0 --port 8000 --reload
goto exit

:frontend
echo.
echo Starting Frontend Server on http://localhost:5000
echo.
cd /d "%~dp0"
call venv\Scripts\activate.bat
python frontend/app.py
goto exit

:both
echo.
echo Starting both servers...
cd /d "%~dp0"
start "API Server" cmd /k "venv\Scripts\python -m uvicorn inference.app:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak
start "Frontend Server" cmd /k "venv\Scripts\python frontend/app.py"
echo.
echo Both servers started!
echo Frontend: http://localhost:5000
echo API: http://localhost:8000/docs
pause
goto exit

:docs
echo.
echo Opening documentation...
start https://localhost:5000
timeout /t 2
goto start

:exit
exit /b 0
