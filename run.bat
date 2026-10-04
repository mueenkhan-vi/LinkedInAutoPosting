@echo off
REM LinkedIn Automation Runner Script for Windows

echo 🤖 LinkedIn Content Generator & Poster
echo ======================================

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install/update dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  .env file not found!
    echo Please create .env file with your credentials:
    echo   OPENAI_API_KEY=your_key
    echo   LINKEDIN_ACCESS_TOKEN=your_token
    echo   LINKEDIN_USER_ID=your_user_id
    pause
    exit /b 1
)

REM Create necessary directories
if not exist "logs" mkdir logs
if not exist "generated_posts" mkdir generated_posts

REM Run the application
echo 🚀 Starting LinkedIn automation...
python main.py

echo ✅ Done! Check generated_post.txt for your content.
pause