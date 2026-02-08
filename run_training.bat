@echo off
REM Run the training pipeline

echo ========================================
echo Heart Disease Prediction Training
echo ========================================
echo.

cd /d "%~dp0"

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Running training pipeline...
python training\train.py

echo.
echo ========================================
echo Training complete!
echo ========================================
pause
