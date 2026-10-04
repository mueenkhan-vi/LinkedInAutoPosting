# LinkedIn Agent - Single Executable Installer

A complete guide to creating and distributing a single standalone executable of the LinkedIn Agent.

## Overview

The `build_executable.py` script creates a self-contained executable that:
- **Requires no Python installation** on target machines
- **Bundles all dependencies** (OpenAI, LinkedIn API, cryptography, etc.)
- **Runs on Windows, macOS, and Linux**
- **Supports automatic posting** with valid credentials

## Prerequisites (for building)

Before building the installer, you need:
- Python 3.8+
- All dependencies from `requirements.txt` installed
- PyInstaller (will be auto-installed if missing)

## Building the Executable

### Option 1: Windows (Easiest)

```batch
REM Double-click or run:
install.bat
```

This will:
1. Check for Python and PyInstaller
2. Install PyInstaller if needed
3. Build the executable
4. Output to `./installer/LinkedInAgent.exe`

### Option 2: Linux/macOS

```bash
# Make script executable
chmod +x install.sh

# Run the installer
./install.sh
```

### Option 3: Manual Build

```bash
# Install PyInstaller if not present
pip install pyinstaller

# Run the build script
python build_executable.py
```

## What Gets Built

```
./installer/
├── LinkedInAgent.exe        (Windows executable)
├── LinkedInAgent            (Linux/macOS executable)
├── .env.example             (bundled configuration template)
├── config/                  (configuration package)
├── services/                (LinkedIn service package)
├── utils/                   (utility functions)
└── agents/                  (AI agents)
```

## Distribution

### For a Single Machine

1. Copy the entire `installer/` folder to the target machine
2. In `installer/`, create a `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env with valid LinkedIn + OpenAI credentials
   ```
3. Double-click `LinkedInAgent.exe` (or run `./LinkedInAgent` on Linux/macOS)

### For Multiple Machines

1. Build once on your machine
2. Create a distribution package:
   ```bash
   mkdir LinkedIn-Agent-Setup
   cp -r installer/* LinkedIn-Agent-Setup/
   cp README_INSTALL.md LinkedIn-Agent-Setup/
   zip -r LinkedIn-Agent-Setup.zip LinkedIn-Agent-Setup/
   ```
3. Distribute `LinkedIn-Agent-Setup.zip` to users
4. Users extract and follow "Single Machine" steps above

### With Windows Installer (Advanced)

Create a professional Windows installer using NSIS:

```bash
# Install NSIS
choco install nsis

# Create installer script (save as linkedin-agent-installer.nsi):
```

See `NSIS_INSTALLER.nsi` template in this repo.

## Post-Installation Setup

### On Target Machine

1. **Extract files** (if distributed as .zip)
   ```bash
   unzip LinkedIn-Agent-Setup.zip
   cd LinkedIn-Agent-Setup
   ```

2. **Create .env file** with your credentials:
   ```bash
   cp .env.example .env
   ```
   
3. **Edit .env** with your actual credentials:
   ```env
   # Get your OpenAI API key from https://platform.openai.com/
   OPENAI_API_KEY=sk-...

   # Get LinkedIn credentials from https://www.linkedin.com/developers/
   LINKEDIN_ACCESS_TOKEN=AQWR...
   LINKEDIN_USER_ID=FUIMe...
   ```

4. **Run the agent**:
   - Windows: Double-click `LinkedInAgent.exe`
   - Linux/macOS: `./LinkedInAgent`

5. **Enter topic** when prompted, confirm posting

## Scheduling Automatic Posts

### Windows Task Scheduler

```batch
# Open Task Scheduler
tasksched.msc

# Create new task:
# - Name: LinkedIn Agent Auto-Post
# - Trigger: Daily at 9:00 AM
# - Action: Start program "C:\path\to\LinkedInAgent.exe"
```

### Linux/macOS Cron

```bash
# Edit crontab
crontab -e

# Add cron job (post every day at 9 AM):
0 9 * * * /path/to/LinkedInAgent

# Or with a topic:
0 9 * * * echo "AI Trends" | /path/to/LinkedInAgent
```

## Troubleshooting

### "Python not found" error

- Ensure Python is installed on your system
- Add Python to system PATH
- Download Python from https://www.python.org/

### "Module not found" errors

- Re-run `build_executable.py` to rebuild
- Ensure all files are extracted from the .zip
- Check that the `config/`, `services/`, `utils/` directories exist

### "Credentials not found" error

- Verify `.env` file exists in the same directory as the executable
- Check that `.env` contains valid API keys
- Ensure `.env` is not in a subdirectory

### Executable won't start

- Run from command line to see error messages:
  - Windows: `LinkedInAgent.exe` in cmd.exe
  - Linux/macOS: `./LinkedInAgent` in terminal

### Large file size

The executable is ~100-150 MB because it bundles Python runtime and all dependencies. This is normal.

## File Sizes

- `LinkedInAgent.exe` (Windows): ~120 MB
- `LinkedInAgent` (Linux/macOS): ~110 MB

**Optimization**: Use `--onedir` instead of `--onefile` in `build_executable.py` for a smaller executable (~30 MB) plus a dependencies folder.

## Customization

### Change the executable name

Edit `build_executable.py`:
```python
"--name", "MyLinkedInBot",  # Change from "LinkedInAgent"
```

### Add a custom icon

1. Create or find a `.ico` file
2. Save it as `linkedin_icon.ico` in the project root
3. Re-run build script (it will auto-detect the icon)

### Disable GUI mode

Edit `build_executable.py`:
```python
# Remove or comment out this line:
"--windowed",
```

## Security Considerations

- **Never commit `.env`** to version control
- **Never include real API keys** in the distributed executable
- Users must create their own `.env` file locally
- The `.env.example` is bundled only as a template
- Encryption key (`.encryption.key`) is machine-specific and not bundled

## Next Steps

1. Run `python build_executable.py` to create the executable
2. Test the executable on your machine
3. Create a `.zip` distribution package
4. Share with users along with setup instructions
5. Users create their own `.env` with their credentials

---

For questions or issues, check the main [README.md](README.md).
