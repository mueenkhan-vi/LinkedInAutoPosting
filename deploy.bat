@echo off
REM LinkedIn Automation Deployment Script for Windows

echo 🚀 LinkedIn Automation Deployment Script
echo =========================================

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found. Creating from template...
    if exist ".env.example" (
        copy .env.example .env
        echo ✅ Created .env file from template. Please edit it with your credentials.
        echo.
        echo    Required: OPENAI_API_KEY, LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET
        echo.
        echo    To get LinkedIn credentials:
        echo    1. Go to https://developer.linkedin.com/
        echo    2. Create an app with 'Sign In with LinkedIn' and 'Share on LinkedIn' products
        echo    3. Add redirect URI: http://localhost:8000/callback
        echo.
        pause
    ) else (
        echo ❌ .env.example not found. Please create .env manually.
        pause
        exit /b 1
    )
)

echo 🏗️  Building Docker image...
docker-compose build

echo 🚀 Starting LinkedIn automation...
docker-compose up -d

echo.
echo ✅ Deployment successful!
echo.
echo 📊 To check logs:
echo    docker-compose logs -f linkedin-automation
echo.
echo 🛑 To stop:
echo    docker-compose down
echo.
echo 🔄 To restart:
echo    docker-compose restart
echo.
echo 📁 Generated posts will be in ./generated_posts/
echo 📝 Logs will be in ./logs/

pause