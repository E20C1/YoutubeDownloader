@echo off

:: Make command window stay open
if "%~1"=="CMDRUN" goto start

cmd /k "%~f0" CMDRUN
exit /b

:start
color 0A
title YouTube Downloader - SERVER RUNNING
cls

echo ==============================================
echo    YouTube Downloader - Starting Server
echo ==============================================
echo.

:: Check Python
where py >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python not found.
    echo Please make sure Python is installed.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b
)

:: Check app.py
if not exist app.py (
    echo ERROR: app.py not found.
    echo This batch file must be in the YouTube Downloader folder.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b
)

:: Open browser after 5 seconds
echo Starting server and opening browser in 5 seconds...
start /b cmd /c "timeout /t 5 /nobreak >nul && start http://localhost:5000"

echo.
echo ------------------------------------
echo    IMPORTANT: KEEP THIS WINDOW OPEN!
echo    This window is running the server
echo    Close this window when you're done
echo ------------------------------------
echo.

echo Server logs will appear below:
echo (Closing this window will stop the server)
echo ----------------------------------------

:: Run with full error output
echo Testing Python and Flask installation...
py -c "import flask; print('Flask version:', flask.__version__); import yt_dlp; print('yt-dlp version:', yt_dlp.version.__version__)" 2>error.log

echo Starting server with detailed error reporting...
py app.py 2>error.log

:: Error handling
echo.
echo Server stopped or error occurred.
echo Checking error log...
echo.

if exist error.log (
    echo ERROR DETAILS:
    type error.log
    echo.
)

echo Press any key to exit...
pause >nul
