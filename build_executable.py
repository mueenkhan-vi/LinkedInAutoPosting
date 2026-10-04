#!/usr/bin/env python3
"""
Build script to create a single executable installer for LinkedIn Agent
Run: python build_executable.py
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print("[OK] PyInstaller is installed")
        return True
    except ImportError:
        print("[!] PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("[OK] PyInstaller installed successfully")
        return True

def build_executable():
    """Build the executable using PyInstaller"""
    print("\n" + "="*60)
    print("Building LinkedIn Agent Executable")
    print("="*60 + "\n")
    
    # Check PyInstaller
    if not check_pyinstaller():
        return False
    
    # Clean previous builds
    print("\nCleaning previous builds...")
    for folder in ["build", "dist", "__pycache__"]:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"  Removed {folder}/")
            except PermissionError:
                print(f"  Skipped {folder}/ (in use)")
                pass
    
    # PyInstaller command
    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", "LinkedInAgent",
        "--add-data", f"config{os.pathsep}config",
        "--add-data", f"services{os.pathsep}services",
        "--add-data", f"utils{os.pathsep}utils",
        "--add-data", f"agents{os.pathsep}agents",
        "--add-data", f".env.example{os.pathsep}.",
        "--hidden-import=cryptography",
        "--hidden-import=openai",
        "--hidden-import=requests",
        "--hidden-import=linkedin_api",
        "--hidden-import=pydantic",
        "--collect-all", "openai",
        "--collect-all", "cryptography",
        "--distpath", "./installer",
        "--workpath", "./build",
        "main.py"
    ]
    
    # Add icon if it exists
    if os.path.exists("linkedin_icon.ico"):
        pyinstaller_cmd.insert(6, "--icon")
        pyinstaller_cmd.insert(7, "linkedin_icon.ico")
    
    print("Running PyInstaller...")
    print(f"Command: {' '.join(pyinstaller_cmd)}\n")
    
    try:
        result = subprocess.run(pyinstaller_cmd, check=True)
        if result.returncode == 0:
            print("\n" + "="*60)
            print("[OK] Build successful!")
            print("="*60)
            
            # Copy required files to installer folder
            print("\nCopying required files to installer...")
            if os.path.exists(".env.example"):
                shutil.copy(".env.example", os.path.join("./installer", ".env.example"))
                print("  Copied: .env.example")
            
            if os.path.exists(".encryption.key"):
                shutil.copy(".encryption.key", os.path.join("./installer", ".encryption.key"))
                print("  Copied: .encryption.key")
            
            print("\nExecutable location: ./installer/LinkedInAgent.exe")
            print("\nNext steps:")
            print("1. Create .env file with your credentials")
            print("2. Run: ./installer/LinkedInAgent.exe")
            print("3. Or distribute ./installer/ folder to other machines")
            return True
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Build failed with error: {e}")
        return False

def create_installer_wrapper():
    """Create a Windows batch installer wrapper"""
    installer_script = """@echo off
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
"""
    with open("install.bat", "w") as f:
        f.write(installer_script)
    print("[OK] Created install.bat")

def create_installer_sh():
    """Create a Linux/macOS installer wrapper"""
    installer_script = """#!/bin/bash

set -e

echo ""
echo "============================================================"
echo "    LinkedIn Agent - Installer"
echo "============================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ using your package manager"
    exit 1
fi

# Check/install dependencies
echo "Checking dependencies..."
pip3 list | grep -q pyinstaller || {
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
}

# Build executable
echo "Building executable..."
python3 build_executable.py

echo ""
echo "============================================================"
echo "    Setup Complete!"
echo "============================================================"
echo ""
echo "Your LinkedIn Agent executable is ready at:"
echo "   ./installer/LinkedInAgent"
echo ""
echo "Next steps:"
echo "1. Copy your .env file to the same folder as LinkedInAgent"
echo "   (or rename .env.example to .env and add your credentials)"
echo "2. Run: ./installer/LinkedInAgent"
echo ""
"""
    with open("install.sh", "w") as f:
        f.write(installer_script)
    os.chmod("install.sh", 0o755)
    print("[OK] Created install.sh")

if __name__ == "__main__":
    print("\nPreparing to build LinkedIn Agent executable...\n")
    
    # Create installer wrappers
    print("Creating installer scripts...")
    create_installer_wrapper()
    create_installer_sh()
    
    # Build the executable
    success = build_executable()
    
    if success:
        print("\n[OK] All done! Executable is ready for distribution.\n")
        sys.exit(0)
    else:
        print("\n[ERROR] Build failed. Please check the output above.\n")
        sys.exit(1)
