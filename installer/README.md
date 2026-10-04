# LinkedIn Agent - Executable Installer

Welcome! This folder contains the standalone **LinkedInAgent.exe** executable — no Python installation required.

## Quick Start

### 1. Setup Credentials (First Time Only)

Edit the `.env` file in this folder with your API keys:

```bash
# Open .env file and add:
OPENAI_API_KEY=sk-...your-key...
LINKEDIN_ACCESS_TOKEN=AQWR...your-token...
LINKEDIN_USER_ID=your-user-id
```

Get these from:
- **OpenAI API Key**: https://platform.openai.com/api-keys
- **LinkedIn API Token**: Run `python linkedin_oauth_handler.py` from the main project folder

### 2. Run the Application

Double-click `LinkedInAgent.exe` or run from command line:

```bash
LinkedInAgent.exe
```

### 3. Follow the Prompts

```
Enter the topic for your LinkedIn post: AI and automation
[WRITING] Generating LinkedIn post content...
[EDITING] Improving the post...
[SUCCESS] Generated LinkedIn Post:
...

Do you want to post this to LinkedIn? (yes/no): yes
[SUCCESS] Posted to LinkedIn!
```

## File Structure

```
installer/
├── LinkedInAgent.exe          # Standalone executable (no Python needed!)
├── .env.example               # Template for credentials
├── .env                       # Your actual credentials (created by you)
├── .encryption.key            # Machine-specific encryption key
└── generated_post.txt         # Last generated post (auto-saved)
```

## Environment File (.env)

Create a `.env` file in this folder with:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-...your-api-key...
OPENAI_MODEL_NAME=gpt-4

# LinkedIn Official API
LINKEDIN_ACCESS_TOKEN=AQWRGeJ4...your-access-token...
LINKEDIN_USER_ID=FUIMNnfuqh

# LinkedIn Personal Account (optional)
# LINKEDIN_EMAIL=your.email@linkedin.com
# LINKEDIN_PASSWORD=your-password
```

**⚠️ Important**: Never share your `.env` file or commit it to version control!

## Automatic Scheduling

### Windows Task Scheduler

```batch
# Press Win + R, type: tasksched.msc
# Create a new task:
#   Name: LinkedIn Auto-Post
#   Trigger: Daily at 9:00 AM
#   Action: Start program "C:\path\to\LinkedInAgent.exe"
```

### Linux/macOS Cron

```bash
# Edit crontab
crontab -e

# Add (post every day at 9 AM):
0 9 * * * /path/to/LinkedInAgent
```

## Troubleshooting

### "Python not found" / "Module not found"

Verify you're running the `.exe` from this folder and that `.env` exists.

### ".env file not found"

Create a `.env` file in the same folder as the executable:

```bash
cp .env.example .env
# Then edit .env with your real API keys
```

### "Credentials missing"

Check your `.env` file has valid:
- `OPENAI_API_KEY`
- `LINKEDIN_ACCESS_TOKEN`
- `LINKEDIN_USER_ID`

### Executable won't start

Run from command line to see error messages:

```bash
cmd> cd C:\path\to\installer
cmd> LinkedInAgent.exe
```

## System Requirements

- **Windows 10+**, **macOS 10.13+**, or **Linux** (most distros)
- **Internet connection** (for OpenAI and LinkedIn APIs)
- **No Python installation required** (bundled in executable)
- **~40 MB disk space** (executable size)

## Upgrading

To get the latest version:

1. Download the new `LinkedInAgent.exe` from releases
2. Keep your existing `.env` file
3. Replace the old executable
4. Run the new version

Your `.env` settings will be preserved!

## Getting Help

Check the main README at the project root for:
- Detailed setup instructions
- API configuration guides
- Troubleshooting tips
- Feature documentation

---

**Happy posting!** 🚀

For issues, visit the project repository.
