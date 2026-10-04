#!/bin/bash
# LinkedIn Automation Runner Script

echo "🤖 LinkedIn Content Generator & Poster"
echo "======================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Please create .env file with your credentials:"
    echo "  OPENAI_API_KEY=your_key"
    echo "  LINKEDIN_ACCESS_TOKEN=your_token"
    echo "  LINKEDIN_USER_ID=your_user_id"
    exit 1
fi

# Create necessary directories
mkdir -p logs generated_posts

# Run the application
echo "🚀 Starting LinkedIn automation..."
python main.py

echo "✅ Done! Check generated_post.txt for your content."