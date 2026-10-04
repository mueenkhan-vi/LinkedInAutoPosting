# LinkedIn Agent - Installation & Deployment Guide

## Overview

This guide covers installing and deploying the LinkedIn Agent package on different systems.

## Two Installation Methods

### Method 1: Quick Setup (Recommended)

**For most users - includes automated setup**

1. Extract `LinkedInAgent_Package.zip`
2. Run the setup script:
   - **Windows**: Double-click `setup.bat`
   - **Linux/macOS**: Run `chmod +x setup.sh && ./setup.sh`
3. Edit `.env` with your credentials
4. Run `startup.bat` or `./startup.sh` to launch

### Method 2: Manual Installation

**For advanced users - full control**

1. Extract the package
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env`
4. Configure `.env` with your credentials
5. Run:
   ```bash
   python main.py
   ```

## System Requirements

| Component | Requirement |
|-----------|------------|
| **OS** | Windows, macOS, or Linux |
| **Python** | 3.8 or newer |
| **RAM** | 512 MB minimum (1 GB recommended) |
| **Disk** | 500 MB for installation |
| **Internet** | Required (for OpenAI and LinkedIn APIs) |

## Detailed Setup by OS

### Windows 10/11

#### Prerequisites
- Python 3.8+ from https://www.python.org/downloads/
- During installation, **check "Add Python to PATH"**

#### Installation Steps
1. Extract `LinkedInAgent_Package.zip`
2. Open File Explorer to the extracted folder
3. Double-click `setup.bat`
4. Follow the prompts
5. Edit `.env` with your credentials
6. Run `startup.bat` to start

#### Verify Installation
```batch
python --version
pip --version
python main.py
```

### macOS

#### Prerequisites
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3@3.11
```

#### Installation Steps
```bash
# Extract the package
unzip LinkedInAgent_Package.zip
cd LinkedInAgent_Package/

# Run setup
chmod +x setup.sh
./setup.sh

# Edit configuration
nano .env

# Start the agent
./startup.sh
```

### Linux (Ubuntu/Debian)

#### Prerequisites
```bash
# Update packages
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv
```

#### Installation Steps
```bash
# Extract the package
unzip LinkedInAgent_Package.zip
cd LinkedInAgent_Package/

# Run setup
chmod +x setup.sh
./setup.sh

# Edit configuration
nano .env

# Start the agent
./startup.sh
```

#### Linux (Red Hat/CentOS)
```bash
# Install Python
sudo yum install python3 python3-pip

# Then follow Ubuntu steps above
```

## Configuration Guide

### 1. OpenAI API Key

1. Visit https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (it won't show again!)
5. Add to `.env`:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

### 2. LinkedIn Credentials

#### Option A: OAuth (Recommended)
1. Run: `python linkedin_oauth_handler.py`
2. Follow the browser prompt to authorize
3. Token is automatically saved to `.env`

#### Option B: Manual Setup
1. Go to https://www.linkedin.com/developers/
2. Create or select your app
3. Add credentials to `.env`:
   ```
   LINKEDIN_CLIENT_ID=your_client_id
   LINKEDIN_CLIENT_SECRET=your_client_secret
   LINKEDIN_REDIRECT_URI=http://localhost:8000/callback
   LINKEDIN_USER_ID=your_user_id
   ```

See `LINKEDIN_SETUP.md` for detailed LinkedIn setup.

## First Run

### Step 1: Verify Installation
```bash
python main.py
```

### Step 2: Generate Content
- Enter a topic when prompted
- Wait for content generation (1-2 minutes)
- Review the generated post

### Step 3: Post to LinkedIn
- Choose to post or save to file
- If posting, follow LinkedIn OAuth flow
- Post will be published to your feed

## Troubleshooting

### Python Not Found
```bash
# Check if Python is installed
python --version

# If not found, install from https://www.python.org
```

### Dependencies Missing
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### OpenAI API Error
- Verify your API key is correct
- Check your OpenAI account has credits
- Ensure key is in `.env` as `OPENAI_API_KEY`

### LinkedIn Auth Failed
```bash
# Refresh the OAuth token
python linkedin_oauth_handler.py
```

### Module Import Errors
```bash
# Clear Python cache and reinstall
pip install --upgrade --force-reinstall -r requirements.txt
```

## Advanced Configuration

### Using Different Entry Points

```bash
# Standard: Interactive mode with content generation
python main.py

# Simple version: Direct posting
python main_simple.py

# OAuth setup: Get/refresh LinkedIn token
python linkedin_oauth_handler.py

# Direct API test: Post content directly
python linkedin_api_poster.py
```

### Environment Variables

All settings are in `.env` file:

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | OpenAI authentication |
| `LINKEDIN_CLIENT_ID` | LinkedIn OAuth client ID |
| `LINKEDIN_CLIENT_SECRET` | LinkedIn OAuth secret |
| `LINKEDIN_REDIRECT_URI` | LinkedIn OAuth callback URL |
| `LINKEDIN_ACCESS_TOKEN` | LinkedIn API token |
| `LINKEDIN_USER_ID` | Your LinkedIn user ID |

### Encryption

Sensitive credentials can be encrypted:

```bash
python -c "from utils.encryption import encrypt_credential; print(encrypt_credential('your_secret'))"
```

Then in `.env`:
```
OPENAI_API_KEY=encrypted:your_encrypted_key
```

## Updating the Package

### Check for Updates
```bash
git pull  # If cloned from repository
```

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

## Uninstall

### Windows
1. Delete the package folder
2. Done! (No registry entries or system files modified)

### Linux/macOS
```bash
rm -rf LinkedInAgent_Package/
pip uninstall -r requirements.txt  # Optional
```

## Support & Issues

If you encounter problems:

1. **Check logs** - Look at console output
2. **Verify config** - Review `.env` file
3. **Test dependencies** - Run `pip install -r requirements.txt`
4. **Clear cache** - Delete `__pycache__` folders
5. **Reinstall** - Extract fresh copy of package

## Next Steps

After successful installation:

1. ✓ Run your first post: `python main.py`
2. ✓ Test LinkedIn posting
3. ✓ Automate with task scheduler (optional)
4. ✓ Integrate with other tools (optional)

## Security Notes

- ✓ Never commit `.env` to version control
- ✓ Keep API keys confidential
- ✓ Use strong passwords for LinkedIn
- ✓ Rotate tokens periodically
- ✓ Use OAuth instead of password storage

---

**Package Version**: 2.0.0  
**Last Updated**: 2026-05-13  
**Python Support**: 3.8+
