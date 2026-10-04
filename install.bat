@echo off
setlocal enabledelayedexpansion

echo.
echo ============================================================
echo    LinkedIn Agent - Installer
echo ============================================================
echo.

REM Check Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check dependencies
echo Checking dependencies...
pip list | findstr "pyinstaller" >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Build executable
echo Building executable...
python build_executable.py

if %errorlevel% neq 0 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo ============================================================
echo    Setup Complete!
echo ============================================================
echo.
echo Your LinkedIn Agent executable is ready at:
echo   ./installer/LinkedInAgent.exe
echo.
echo Next steps:
echo 1. Copy your .env file to the same folder as LinkedInAgent.exe
echo    (or rename .env.example to .env and add your credentials)
echo 2. Double-click LinkedInAgent.exe to run
echo.
pause
