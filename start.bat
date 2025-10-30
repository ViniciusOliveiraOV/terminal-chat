@echo off
echo =================================
echo Terminal Chat - Quick Start
echo =================================
echo.

echo Starting Terminal Chat Server...
cd server

REM Check if .env exists
if not exist .env (
    echo Creating server configuration...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit server\.env file with your email settings!
    echo Press any key when ready...
    pause >nul
    echo.
)

REM Install server dependencies
echo Installing server dependencies...
pip install -r requirements.txt >nul 2>&1

REM Start server in background
echo Server starting on http://localhost:8000
start /b python main.py

REM Wait a moment for server to start
timeout /t 3 >nul

echo.
echo Starting Terminal Chat Client...
cd ..\client

REM Check if .env exists
if not exist .env (
    echo Creating client configuration...
    copy .env.example .env
)

REM Install client dependencies
echo Installing client dependencies...
pip install -r requirements.txt >nul 2>&1

echo.
echo =================================
echo Terminal Chat is ready!
echo =================================
echo Server: http://localhost:8000
echo Client: Starting now...
echo.

REM Start client
python main.py

echo.
echo Thanks for using Terminal Chat!
pause