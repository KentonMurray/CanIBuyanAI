@echo off
REM Simple batch script to run the Wheel of Fortune game with commentary

echo 🎪 Starting Wheel of Fortune with FREE AI Commentary...
echo.

cd /d "%~dp0\src\PlayGame"

REM Check if python exists
python --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python
    goto :run_game
)

python3 --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python3
    goto :run_game
)

py --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=py
    goto :run_game
)

echo ❌ Error: Python not found!
echo Please install Python 3.x from https://python.org
pause
exit /b 1

:run_game
echo Using: %PYTHON_CMD%
echo.

echo 🎭 Running demo to show features...
%PYTHON_CMD% demo_commentary.py

echo.
echo 🎮 Now starting the interactive game...
echo Press Ctrl+C to exit at any time
echo.

%PYTHON_CMD% play_with_commentary.py smart smart smart
pause