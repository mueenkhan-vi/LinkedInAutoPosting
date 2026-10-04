# LinkedIn Agent - Quick Start Guide

## ⚡ 5-Minute Setup

### What You Need

- **Python 3.8+** - Download from https://www.python.org/
- **OpenAI API Key** - Get from https://platform.openai.com/api-keys
- **LinkedIn Account** - For posting

### Installation

#### Windows
```batch
1. Extract LinkedInAgent_Package.zip
2. Double-click: setup.bat
3. Wait for installation to complete
4. Edit: .env (your credentials)
5. Double-click: startup.bat
```

#### macOS / Linux
```bash
1. Extract LinkedInAgent_Package.zip
2. Run: chmod +x setup.sh && ./setup.sh
3. Edit: .env (your credentials)
4. Run: ./startup.sh
```

## 🔑 Configure Credentials (5 minutes)

### OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in (or create account)
3. Click "Create new secret key"
4. Copy the key
5. Open `.env` file and add:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

### LinkedIn Access

1. Run: `python linkedin_oauth_handler.py`
2. Browser opens automatically
3. Click "Authorize" to approve
4. Token saved to `.env` automatically
5. Done!

## ▶️ First Run (2 minutes)

```bash
python main.py
```

**You'll see:**
```
============================================================
LinkedIn Content Generator
============================================================

Enter the topic for your LinkedIn post: 
```

**Enter a topic**, for example:
```
AI and Machine Learning trends 2026
```

**Wait** 1-2 minutes for content generation...

**Review** the generated post

**Choose** to post or save to file

## 📝 Usage Examples

### Topic Ideas

- "Benefits of remote work"
- "Latest AI technologies"
- "Leadership tips for 2026"
- "Digital transformation strategy"
- "Personal development journey"

### After Generation

```
Do you want to post this to LinkedIn? (yes/no):
```

**Options:**
- `yes` → Posts directly to your LinkedIn feed
- `no` → Saves to `generated_post.txt` (copy manually)

## 🔄 Generate Multiple Posts

```bash
# Run multiple times
python main.py
python main.py
python main.py
```

Each run generates a new unique post for a different topic.

## 📂 File Locations

After first run, you'll have:

```
generated_post.txt     ← Your last generated post
.env                   ← Your credentials (KEEP SECRET!)
logs/                  ← Application logs
```

## ⚠️ Common Issues

### "Python not found"
→ Install Python from https://www.python.org  
→ Add to PATH during installation

### "OPENAI_API_KEY not set"
→ Edit `.env` file  
→ Add your actual API key  
→ Save and try again

### "LinkedIn credentials missing"
→ Run: `python linkedin_oauth_handler.py`  
→ Follow browser authorization  
→ Token saved automatically

### "ModuleNotFoundError"
→ Run: `pip install -r requirements.txt`  
→ Then try again

## 🚀 Advanced Usage

### Different Entry Points

```bash
# Interactive generator (recommended)
python main.py

# Simple/fast version
python main_simple.py

# Setup LinkedIn OAuth
python linkedin_oauth_handler.py

# Direct API test
python linkedin_api_poster.py
```

### Save Posts to File

Posts are automatically saved to:
- `generated_post.txt` - Latest post
- `linkedin_post_content.txt` - Last formatted post

### Batch Processing

Generate multiple posts:
```bash
for topic in "AI" "Leadership" "Tech"
do
    echo $topic | python main.py
done
```

## 🛡️ Security Tips

- ✓ Keep `.env` file private (don't share!)
- ✓ Never commit `.env` to Git
- ✓ Treat API keys like passwords
- ✓ Rotate tokens every 90 days
- ✓ Monitor account activity regularly

## 📞 Getting Help

### Check Logs
```bash
# View recent errors
cat logs/linkedin_agent.log  # macOS/Linux
type logs\linkedin_agent.log  # Windows
```

### Reinstall Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Reset Configuration
```bash
1. Delete .env file
2. Copy .env.example to .env
3. Run setup again
4. Reconfigure credentials
```

## 📚 Full Documentation

For detailed information, see:

- **INSTALLATION_GUIDE.md** - Complete setup guide
- **LINKEDIN_SETUP.md** - LinkedIn authentication
- **DEPLOYMENT_GUIDE.md** - Multi-user deployment
- **README.md** - Full documentation

## 💡 Tips & Tricks

### Faster Posting
```bash
# Use simple version (faster)
python main_simple.py
```

### Copy Content Manually
If posting fails:
1. Open `generated_post.txt`
2. Copy the content
3. Paste to LinkedIn.com directly

### Schedule Posts (Advanced)

**Windows (Task Scheduler):**
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (daily, weekly)
4. Action: Run `startup.bat`

**macOS/Linux (Cron):**
```bash
# Edit cron jobs
crontab -e

# Add line (runs daily at 9 AM)
0 9 * * * cd ~/LinkedInAgent && python main.py
```

## 🎯 Quick Wins

1. **Generate your first post** (2 min)
   ```bash
   python main.py
   ```

2. **Post to LinkedIn** (1 min)
   - Choose "yes" when prompted

3. **Generate 5 different posts** (15 min)
   - Run multiple times with different topics

4. **Schedule daily posts** (10 min)
   - Set up task scheduler (Windows) or cron (Mac/Linux)

## ✅ Checklist

Before you start:
- [ ] Python 3.8+ installed
- [ ] `.env` file created
- [ ] OpenAI API key added
- [ ] LinkedIn OAuth configured
- [ ] First test run successful

## 🎓 Learning Path

1. **Day 1**: Install and generate your first post
2. **Day 2**: Post to LinkedIn, experiment with topics
3. **Day 3**: Batch generate multiple posts
4. **Day 4**: Explore advanced features
5. **Day 5**: Integrate into your workflow

## 🤝 Need Help?

1. **Check this guide** - Most questions answered here
2. **Read INSTALLATION_GUIDE.md** - Detailed setup
3. **Check logs** - Application logs may have clues
4. **Reinstall** - Sometimes a fresh start helps

## 🎉 Success!

You're ready to generate amazing LinkedIn content!

**Next steps:**
1. Run: `python main.py`
2. Enter a topic
3. Review generated content
4. Post to LinkedIn
5. Repeat daily for consistent engagement

---

**Happy posting!** 🚀

**Package Version**: 2.0.0  
**Created**: May 13, 2026  
**Time to Setup**: 5 minutes  
**Time to First Post**: 7-10 minutes total
