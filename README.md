<<<<<<< HEAD
# LinkedIn Content Generator & Poster

A Python application that generates LinkedIn content using OpenAI and posts it automatically using the official LinkedIn API.

## Features

- 🤖 AI-powered content generation using OpenAI GPT-4
- 📱 Automatic posting to LinkedIn via official API
- 🔐 Secure credential management with encryption
- ⏰ Optional scheduled posting
- 🐳 Docker containerization for easy deployment

## Project Structure

```
linkedin-automation/
├── main.py                 # Main content generator
├── main_simple.py          # Simplified version
├── linkedin_api_poster.py  # Official API poster
├── linkedin_oauth_handler.py # OAuth token handler
├── linkedin_personal_bot.py # Browser automation (alternative)
├── linkedin_scheduler.py   # Scheduled posting
├── config/                 # Configuration
├── services/               # LinkedIn services
├── utils/                  # Utilities
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose
├── .env.example          # Environment template
└── README.md             # This file
```

## Prerequisites

- Python 3.8+
- OpenAI API Key (for GPT-4)
- LinkedIn Developer App (for official API access)

## Quick Start

### Local Setup

1. **Clone and setup:**
   ```bash
   git clone <your-repo>
   cd linkedin-automation
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure credentials:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Get LinkedIn access token:**
   ```bash
   python linkedin_oauth_handler.py
   ```

4. **Generate and post content:**
   ```bash
   python main.py
   python linkedin_api_poster.py
   ```

## Environment Variables

Create a `.env` file with:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL_NAME=gpt-4

# LinkedIn API Configuration
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_REDIRECT_URI=http://localhost:8000/callback
LINKEDIN_ACCESS_TOKEN=your_access_token
LINKEDIN_USER_ID=your_user_id

# LinkedIn Personal Account (optional, for browser automation)
LINKEDIN_EMAIL=your_email
LINKEDIN_PASSWORD=your_password
```

## API Setup

### LinkedIn Developer App

1. Go to [LinkedIn Developers](https://developer.linkedin.com/)
2. Create a new app
3. Add products: "Sign In with LinkedIn using OpenID Connect" and "Share on LinkedIn"
4. Set authorized redirect URLs: `http://localhost:8000/callback`
5. Get Client ID and Secret

### OpenAI API

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create API key
3. Add to `.env` file

## Usage

### Generate Content
```bash
python main.py
# Enter topic when prompted
```

### Post to LinkedIn
```bash
python linkedin_api_poster.py
```

### Schedule Posts
```bash
python linkedin_scheduler.py
```

## Docker Deployment

### Build and Run

```bash
# Build the Docker image
docker build -t linkedin-automation .

# Run the container
docker run -it --env-file .env linkedin-automation
```

### Docker Compose (Recommended)

```yaml
version: '3.8'
services:
  linkedin-bot:
    build: .
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
      - ./generated_posts:/app/generated_posts
```

```bash
docker-compose up -d
```

## Automated Deployment

### Quick Deploy Script

For Linux/macOS:
```bash
./deploy.sh
```

For Windows:
```cmd
deploy.bat
```

This script will:
- Check for Docker installation
- Create `.env` from template if needed
- Build and start the container
- Mount volumes for logs and generated content

## Deployment Options

### 1. Local Server
- Run on VPS or local machine
- Use cron jobs for scheduling: `0 9 * * * /path/to/project/deploy.sh`
- Monitor logs in `./logs/`

### 2. Cloud Platforms

#### Heroku
```bash
# Install Heroku CLI
heroku create your-app-name
heroku config:set $(cat .env | xargs)
git push heroku main
```

#### Railway
1. Connect your GitHub repo
2. Add environment variables in Railway dashboard
3. Deploy automatically on push

#### Render
1. Create new Web Service
2. Connect GitHub repo
3. Set build command: `docker build -t linkedin-automation .`
4. Set start command: `python main.py`

#### AWS/GCP
- **ECS/EKS**: Use Docker Compose with AWS Fargate
- **Cloud Run**: Deploy the container directly
- **Lambda**: Package as ZIP for serverless deployment

### 3. Scheduled Deployment

For automated daily posting:

```bash
# Add to crontab (Linux/macOS)
0 9 * * * cd /path/to/project && ./deploy.sh

# Or use the scheduler container
docker-compose up -d scheduler
```

## Security Notes

- Never commit `.env` file (it's in `.gitignore`)
- Use encrypted credentials for production
- Rotate API keys regularly
- Monitor OpenAI and LinkedIn API usage/costs
- Use Docker secrets in production environments

## Monitoring

### Logs
```bash
# View container logs
docker-compose logs -f linkedin-automation

# View logs directory
ls -la logs/
```

### Health Checks
The application logs all operations to `logs/linkedin_agent.log`

## Troubleshooting

### Common Issues

1. **401 Unauthorized**: Refresh LinkedIn access token
   ```bash
   python linkedin_oauth_handler.py
   ```

2. **OpenAI API errors**: Check API key and credits

3. **Docker build fails**: Ensure Docker Desktop is running

4. **Permission errors**: Check file permissions on `.env` and `.encryption.key`

### Performance Tips

- Run generation and posting separately for better error handling
- Use the scheduler for consistent posting times
- Monitor API rate limits (LinkedIn: 100 posts/day, OpenAI: varies by tier)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## License

MIT License - see LICENSE file for details

Edit the agent files in `agents/` to modify:
- Agent roles and goals
- Task descriptions
- Expected outputs
- Behavior and tone

## Limitations

- LinkedIn API (unofficial) may change and break compatibility
- Rate limiting on LinkedIn API
- OpenAI API costs (GPT-4 is more expensive than GPT-3.5)
- Some LinkedIn features may not be available through the unofficial API

## Future Enhancements

- [ ] Support for image/video attachments
- [ ] Schedule posts for optimal times
- [ ] Analytics tracking for published posts
- [ ] Multiple account support
- [ ] Post templates and customization
- [ ] Integration with LinkedIn official API
- [ ] Batch post creation
- [ ] A/B testing different post variations

## License

This project is provided as-is for personal use.

## Disclaimer

This project uses an unofficial LinkedIn API library. LinkedIn's terms of service may prohibit automated posting. Use at your own risk. Always review generated content before posting.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs in `linkedin_agent.log`
3. Ensure all dependencies are installed correctly
4. Verify API credentials are valid

---

**Happy posting! 🚀**
=======
# LinkedInAutoPosting
That agent will post on linkedin
>>>>>>> 9ea72bfa68e5a8f41f8ccbbebc03b5c131b471bd
