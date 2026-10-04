#!/usr/bin/env python3
"""
Complete Package Builder for LinkedIn Agent Installer
Creates a distributable, self-contained package with all dependencies
Run: python build_package.py
"""
import os
import sys
import shutil
import subprocess
import json
import zipfile
from pathlib import Path
from datetime import datetime

class PackageBuilder:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parent
        self.build_dir = self.project_root / "dist" / "LinkedInAgent_Package"
        self.package_zip = self.project_root / "dist" / f"LinkedInAgent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def clean_build_dir(self):
        """Clean previous build directories"""
        print("\n[1/8] Cleaning previous builds...")
        if self.build_dir.exists():
            import stat
            def remove_readonly(func, path, exc):
                os.chmod(path, stat.S_IWRITE)
                func(path)
            
            shutil.rmtree(self.build_dir, onerror=remove_readonly)
            print(f"  ✓ Removed {self.build_dir}")
        
        self.build_dir.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created build directory: {self.build_dir}")
        
    def copy_source_files(self):
        """Copy necessary source files to package"""
        print("\n[2/8] Copying source files...")
        
        # Directories to copy
        dirs_to_copy = {
            "config": self.build_dir / "config",
            "services": self.build_dir / "services",
            "utils": self.build_dir / "utils",
            "agents": self.build_dir / "agents",
        }
        
        for src_dir, dest_dir in dirs_to_copy.items():
            if (self.project_root / src_dir).exists():
                shutil.copytree(self.project_root / src_dir, dest_dir)
                print(f"  ✓ Copied {src_dir}/")
            else:
                print(f"  ⚠ Skipped {src_dir}/ (not found)")
        
        # Files to copy
        files_to_copy = [
            "main.py",
            "main_simple.py",
            "linkedin_oauth_handler.py",
            "linkedin_api_poster.py",
            "requirements.txt",
            ".env.example",
            "README.md",
        ]
        
        if (self.project_root / ".encryption.key").exists():
            files_to_copy.append(".encryption.key")

        for file in files_to_copy:
            src_file = self.project_root / file
            dest_file = self.build_dir / file
            if src_file.exists():
                shutil.copy2(src_file, dest_file)
                print(f"  ✓ Copied {file}")
            else:
                print(f"  ⚠ Skipped {file} (not found)")
    
    def create_installer_scripts(self):
        """Create platform-specific installer scripts"""
        print("\n[3/8] Creating installer scripts...")
        
        # Windows batch installer
        windows_installer = """@echo off
setlocal enabledelayedexpansion

cls
echo.
echo ============================================================
echo    LinkedIn Agent - Setup Wizard
echo ============================================================
echo.
echo This wizard will set up the LinkedIn Agent on your machine.
echo.

REM Check Python
echo Checking for Python installation...
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python 3.8+ is required but not installed.
    echo.
    echo Please install Python from: https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)
echo [OK] Python is installed
echo.

REM Check pip
python -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] pip is not available via python -m pip
    echo Please install pip for the Python installation above.
    echo You can run: python -m ensurepip --upgrade
    pause
    exit /b 1
)
echo [OK] pip is available via python -m pip
echo.

REM Install dependencies
echo Installing dependencies from requirements.txt...
echo This may take a few minutes...
echo.
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed successfully
echo.

REM Create .env file
echo.
echo ============================================================
echo    Configuration Setup
echo ============================================================
echo.
if exist .env (
    echo [!] .env file already exists
    echo Keep existing .env file? (Y/n)
    set /p keep_env=
    if /i NOT "!keep_env!"=="n" goto skip_env_create
)

echo Creating .env file from template...
copy .env.example .env >nul
echo [OK] Created .env file

echo.
echo [!] IMPORTANT: Edit the .env file with your credentials:
echo     - OPENAI_API_KEY: Your OpenAI API key
echo     - LINKEDIN_CLIENT_ID: Your LinkedIn app client ID
echo     - LINKEDIN_CLIENT_SECRET: Your LinkedIn app secret
echo     - LINKEDIN_REDIRECT_URI: Your LinkedIn app redirect URI
echo.
echo Edit .env in your preferred text editor before running the agent.
echo.

:skip_env_create
echo ============================================================
echo    Installation Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Edit .env file with your credentials
echo 2. Run: python main.py
echo    OR run the startup script: startup.bat
echo.
pause
"""
        
        # Linux/macOS installer
        linux_installer = """#!/bin/bash

clear

echo ""
echo "============================================================"
echo "    LinkedIn Agent - Setup Wizard"
echo "============================================================"
echo ""
echo "This wizard will set up the LinkedIn Agent on your machine."
echo ""

# Check Python
echo "Checking for Python 3.8+..."
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "[ERROR] Python 3.8+ is required but not installed."
    echo ""
    echo "Install Python using:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  macOS: brew install python3"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi
echo "[OK] Python is installed: $(python3 --version)"
echo ""

# Check pip
python3 -m pip --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[WARNING] pip3 is not available via python3 -m pip"
    echo "Attempting to install pip via python3 -m ensurepip..."
    python3 -m ensurepip --upgrade > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo ""
        echo "[ERROR] pip is not available and could not be installed automatically."
        echo "Install pip manually and rerun this script."
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

echo "[OK] pip is available via python3 -m pip"
echo ""

# Install dependencies
echo "Installing dependencies from requirements.txt..."
echo "This may take a few minutes..."
echo ""
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Failed to install dependencies"
    read -p "Press Enter to exit..."
    exit 1
fi
echo "[OK] Dependencies installed successfully"
echo ""

# Create .env file
echo ""
echo "============================================================"
echo "    Configuration Setup"
echo "============================================================"
echo ""
if [ -f .env ]; then
    read -p "[!] .env file exists. Keep existing? (Y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        echo "Using existing .env file"
    else
        echo "Creating new .env file from template..."
        cp .env.example .env
        echo "[OK] Created .env file"
    fi
else
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "[OK] Created .env file"
fi

echo ""
echo "[!] IMPORTANT: Edit the .env file with your credentials:"
echo "    - OPENAI_API_KEY: Your OpenAI API key"
echo "    - LINKEDIN_CLIENT_ID: Your LinkedIn app client ID"
echo "    - LINKEDIN_CLIENT_SECRET: Your LinkedIn app secret"
echo "    - LINKEDIN_REDIRECT_URI: Your LinkedIn app redirect URI"
echo ""
echo "Edit .env in your preferred text editor before running the agent."
echo ""
echo "============================================================"
echo "    Installation Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Run: python3 main.py"
echo "3. Or run the startup script: ./startup.sh"
echo ""
read -p "Press Enter to exit..."
"""
        
        # Windows startup script
        windows_startup = """@echo off
setlocal enabledelayedexpansion

echo.
echo ============================================================
echo    LinkedIn Agent - Startup
echo ============================================================
echo.

REM Check if .env exists
if not exist .env (
    echo [ERROR] .env file not found!
    echo.
    echo Please run setup first:
    echo   setup.bat
    echo.
    pause
    exit /b 1
)

echo Starting LinkedIn Agent...
echo.
python main.py
pause
"""
        
        # Linux/macOS startup script
        linux_startup = """#!/bin/bash

clear

echo ""
echo "============================================================"
echo "    LinkedIn Agent - Startup"
echo "============================================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "[ERROR] .env file not found!"
    echo ""
    echo "Please run setup first:"
    echo "  ./setup.sh"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Starting LinkedIn Agent..."
echo ""
python3 main.py
"""
        
        # Write scripts with UTF-8 encoding
        (self.build_dir / "setup.bat").write_text(windows_installer, encoding='utf-8')
        (self.build_dir / "setup.sh").write_text(linux_installer, encoding='utf-8')
        (self.build_dir / "startup.bat").write_text(windows_startup, encoding='utf-8')
        (self.build_dir / "startup.sh").write_text(linux_startup, encoding='utf-8')
        
        # Make shell scripts executable
        import stat
        for script in ["setup.sh", "startup.sh"]:
            script_path = self.build_dir / script
            st = script_path.stat()
            script_path.chmod(st.st_mode | stat.S_IEXEC)
        
        print("  ✓ Created setup.bat (Windows)")
        print("  ✓ Created setup.sh (Linux/macOS)")
        print("  ✓ Created startup.bat (Windows)")
        print("  ✓ Created startup.sh (Linux/macOS)")
    
    def create_documentation(self):
        """Create installation and usage documentation"""
        print("\n[4/8] Creating documentation...")
        
        readme_content = """# LinkedIn Agent - Complete Package

A complete, production-ready package for the LinkedIn AI Content Generator.

## What's Included

- **main.py** - Main entry point with OpenAI + LinkedIn API integration
- **main_simple.py** - Alternative simple version
- **linkedin_oauth_handler.py** - OAuth setup for LinkedIn
- **LinkedIn API Integration** - Official LinkedIn API posting
- **OpenAI Integration** - GPT-4 powered content generation
- **Complete Source Code** - All modules and utilities included

## Quick Start

### Windows
1. Double-click `setup.bat`
2. Edit `.env` with your credentials
3. Run `startup.bat` to start the agent

### Linux/macOS
1. Run `chmod +x setup.sh && ./setup.sh`
2. Edit `.env` with your credentials
3. Run `./startup.sh` to start the agent

## Prerequisites

- **Python 3.8+** (https://www.python.org/downloads/)
- **OpenAI API Key** (https://platform.openai.com/api-keys)
- **LinkedIn App Credentials** (see LINKEDIN_SETUP.md)

## Configuration

### 1. OpenAI Setup
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Add to `.env`: `OPENAI_API_KEY=your_key_here`

### 2. LinkedIn OAuth Setup
1. Go to https://www.linkedin.com/developers/
2. Create or select your app
3. Add these credentials to `.env`:
   - `LINKEDIN_CLIENT_ID=your_client_id`
   - `LINKEDIN_CLIENT_SECRET=your_secret`
   - `LINKEDIN_REDIRECT_URI=http://localhost:8000/callback`
4. Run: `python linkedin_oauth_handler.py` to get access token

## Usage

### Generate and Post Content
```bash
python main.py
```
Follow the prompts:
1. Enter a topic for your post
2. Review the generated content
3. Choose to post or save to file

### Get LinkedIn Access Token
```bash
python linkedin_oauth_handler.py
```
This opens a browser for OAuth login and saves the access token to `.env`.

## File Structure

```
LinkedInAgent_Package/
├── setup.bat                (Windows setup)
├── setup.sh                 (Linux/macOS setup)
├── startup.bat              (Windows launcher)
├── startup.sh               (Linux/macOS launcher)
├── main.py                  (Main entry point)
├── main_simple.py           (Alternative simple version)
├── linkedin_oauth_handler.py (OAuth authentication)
├── linkedin_api_poster.py   (LinkedIn API wrapper)
├── requirements.txt         (Python dependencies)
├── .env.example             (Configuration template)
├── README.md                (This file)
├── LINKEDIN_SETUP.md        (LinkedIn setup guide)
├── config/                  (Configuration modules)
├── services/                (LinkedIn service)
├── utils/                   (Utility functions)
└── agents/                  (AI agents)
```

## Troubleshooting

### "Python not found"
- Ensure Python 3.8+ is installed
- Add Python to your system PATH
- Restart your terminal/IDE

### "OPENAI_API_KEY not set"
1. Edit `.env` file
2. Add your API key: `OPENAI_API_KEY=sk-...`
3. Save and restart

### "LinkedIn credentials missing"
Run: `python linkedin_oauth_handler.py` to set up OAuth

### "Module not found" errors
Run: `pip install -r requirements.txt`

## Support

For issues or questions:
1. Check `.env` configuration
2. Review the logs
3. Ensure all dependencies are installed: `pip install -r requirements.txt`

## Version Info

- Package Date: {timestamp}
- Python Required: 3.8+
- Main Framework: OpenAI, Official LinkedIn API
"""
        
        linkedin_setup = """# LinkedIn OAuth Setup Guide

## Overview

This guide helps you set up LinkedIn OAuth 2.0 authentication for the LinkedIn Agent.

## Step 1: Create LinkedIn Developer Account

1. Visit https://www.linkedin.com/developers/
2. Sign in with your LinkedIn account (or create one)
3. Accept the terms and conditions

## Step 2: Create or Select Your App

1. Click "Create app"
2. Fill in the application details:
   - **App name**: LinkedIn Agent
   - **LinkedIn Page**: Choose existing or create new
   - **App logo**: Upload or skip
   - **Legal agreement**: Accept and continue

3. Verify your email (check inbox for verification link)

## Step 3: Generate Credentials

After app creation:

1. Go to "Auth" tab
2. Copy your credentials:
   - **Client ID** - Add to `.env` as `LINKEDIN_CLIENT_ID`
   - **Client Secret** - Add to `.env` as `LINKEDIN_CLIENT_SECRET`

3. Under "Authorized redirect URLs", add:
   ```
   http://localhost:8000/callback
   ```

## Step 4: Get Access Token

1. Edit `.env` with your credentials:
   ```
   LINKEDIN_CLIENT_ID=your_client_id_here
   LINKEDIN_CLIENT_SECRET=your_secret_here
   LINKEDIN_REDIRECT_URI=http://localhost:8000/callback
   ```

2. Run the OAuth handler:
   ```bash
   python linkedin_oauth_handler.py
   ```

3. A browser window will open for you to authorize
4. Grant permission to the app
5. Copy the access token that appears
6. It will be saved to `.env` automatically

## Step 5: Get Your LinkedIn User ID

1. Visit https://www.linkedin.com/me/
2. The URL format is: `https://www.linkedin.com/in/yourprofile/`
3. Your user ID can be found in:
   - API responses
   - Or use the oauth handler which provides it

4. Add to `.env`:
   ```
   LINKEDIN_USER_ID=your_user_id
   ```

## Permissions

Your app needs the following scopes:
- `w_member_social` - Write to your feed
- `r_liteprofile` - Read profile info

These are usually enabled by default.

## Testing

To verify your setup:

```bash
python linkedin_api_poster.py
```

This will:
1. Check your credentials
2. Read sample post content
3. Post to your LinkedIn feed (if valid)

## Troubleshooting

### "Invalid credentials" error
- Verify Client ID and Secret are correct
- Check redirect URI matches exactly
- Re-run `python linkedin_oauth_handler.py`

### "Permission denied" (403)
- Ensure app has proper permissions
- Check LinkedIn app settings
- May need to wait for LinkedIn to process changes (up to 24 hours)

### Token expired
- Run `python linkedin_oauth_handler.py` again
- This refreshes your access token

## Token Expiration

Access tokens expire after 2 months. To refresh:
```bash
python linkedin_oauth_handler.py
```

This updates your `.env` with a new token.
"""
        
        (self.build_dir / "README.md").write_text(readme_content.format(timestamp=self.timestamp), encoding='utf-8')
        (self.build_dir / "LINKEDIN_SETUP.md").write_text(linkedin_setup, encoding='utf-8')
        
        print("  ✓ Created README.md")
        print("  ✓ Created LINKEDIN_SETUP.md")
    
    def create_config(self):
        """Create package configuration file"""
        print("\n[5/8] Creating package configuration...")
        
        config = {
            "name": "LinkedIn Agent",
            "version": "2.0.0",
            "build_date": self.timestamp,
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}+",
            "features": [
                "OpenAI GPT-4 Content Generation",
                "LinkedIn Official API Integration",
                "OAuth 2.0 Authentication",
                "Cross-platform Support",
                "Credential Encryption"
            ],
            "entry_points": {
                "main": "main.py",
                "simple": "main_simple.py",
                "oauth_setup": "linkedin_oauth_handler.py"
            }
        }
        
        config_file = self.build_dir / "package.json"
        config_file.write_text(json.dumps(config, indent=2), encoding='utf-8')
        print(f"  ✓ Created package.json")
    
    def verify_package(self):
        """Verify package completeness"""
        print("\n[6/8] Verifying package...")
        
        required_files = [
            "main.py",
            "requirements.txt",
            ".env.example",
            "README.md",
            "setup.bat",
            "setup.sh",
            "package.json"
        ]
        
        required_dirs = ["config", "utils"]
        
        all_good = True
        for file in required_files:
            if (self.build_dir / file).exists():
                print(f"  ✓ {file}")
            else:
                print(f"  ✗ {file} (missing)")
                all_good = False
        
        for dir in required_dirs:
            if (self.build_dir / dir).exists():
                print(f"  ✓ {dir}/")
            else:
                print(f"  ✗ {dir}/ (missing)")
                all_good = False
        
        return all_good
    
    def create_zip_package(self):
        """Create a distributable zip file"""
        print("\n[7/8] Creating distribution package...")
        
        if self.package_zip.exists():
            self.package_zip.unlink()
        
        with zipfile.ZipFile(self.package_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.build_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(self.build_dir.parent)
                    zipf.write(file_path, arcname)
        
        size_mb = self.package_zip.stat().st_size / (1024 * 1024)
        print(f"  ✓ Created {self.package_zip.name} ({size_mb:.2f} MB)")
    
    def create_summary(self):
        """Create a build summary"""
        print("\n[8/8] Creating build summary...")
        
        summary = f"""BUILD SUMMARY
{'='*60}
Build Date: {self.timestamp}
Package Location: {self.build_dir}
Distribution ZIP: {self.package_zip}

Contents:
- Main entry point: main.py
- Source code: config/, services/, utils/, agents/
- Setup scripts: setup.bat, setup.sh
- Documentation: README.md, LINKEDIN_SETUP.md
- Configuration: .env.example, package.json
- Dependencies: requirements.txt

Installation Instructions:
1. Extract the package
2. Run: setup.bat (Windows) or ./setup.sh (Linux/macOS)
3. Edit .env with your credentials
4. Run: python main.py

For distribution:
- Share the ZIP file: {self.package_zip.name}
- Recipients extract and run setup scripts
- No additional files needed

Package is ready for distribution!
{'='*60}
"""
        
        summary_file = self.project_root / "dist" / "BUILD_SUMMARY.txt"
        summary_file.write_text(summary, encoding='utf-8')
        print(f"  ✓ Created BUILD_SUMMARY.txt")
        print("\n" + summary)
    
    def build(self):
        """Execute the complete build process"""
        print("\n" + "="*60)
        print("LINKEDIN AGENT - PACKAGE BUILDER")
        print("="*60)
        
        try:
            self.clean_build_dir()
            self.copy_source_files()
            self.create_installer_scripts()
            self.create_documentation()
            self.create_config()
            
            if not self.verify_package():
                print("\n[WARNING] Some files are missing, continuing anyway...")
            
            self.create_zip_package()
            self.create_summary()
            
            print("\n" + "="*60)
            print("✓ PACKAGE BUILD COMPLETE")
            print("="*60)
            return True
            
        except Exception as e:
            print(f"\n[ERROR] Build failed: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    builder = PackageBuilder()
    success = builder.build()
    sys.exit(0 if success else 1)
