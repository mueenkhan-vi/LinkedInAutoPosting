#!/bin/bash
# LinkedIn Automation Deployment Script

set -e

echo "🚀 LinkedIn Automation Deployment Script"
echo "========================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is available
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
elif docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    echo "❌ Docker Compose is not available. Please install Docker Compose."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env file from template. Please edit it with your credentials."
        echo "   Required: OPENAI_API_KEY, LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET"
        echo ""
        echo "   To get LinkedIn credentials:"
        echo "   1. Go to https://developer.linkedin.com/"
        echo "   2. Create an app with 'Sign In with LinkedIn' and 'Share on LinkedIn' products"
        echo "   3. Add redirect URI: http://localhost:8000/callback"
        echo ""
        read -p "Press Enter after configuring .env to continue..."
    else
        echo "❌ .env.example not found. Please create .env manually."
        exit 1
    fi
fi

echo "🏗️  Building Docker image..."
$DOCKER_COMPOSE build

echo "🚀 Starting LinkedIn automation..."
$DOCKER_COMPOSE up -d

echo ""
echo "✅ Deployment successful!"
echo ""
echo "📊 To check logs:"
echo "   $DOCKER_COMPOSE logs -f linkedin-automation"
echo ""
echo "🛑 To stop:"
echo "   $DOCKER_COMPOSE down"
echo ""
echo "🔄 To restart:"
echo "   $DOCKER_COMPOSE restart"
echo ""
echo "📁 Generated posts will be in ./generated_posts/"
echo "📝 Logs will be in ./logs/"