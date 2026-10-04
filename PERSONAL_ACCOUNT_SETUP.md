"""
Personal LinkedIn Account Setup Guide
For individual users with just email + password
"""

GUIDE = """
╔════════════════════════════════════════════════════════════════╗
║   LinkedIn Personal Account - Automation Setup (SIMPLE!)       ║
╚════════════════════════════════════════════════════════════════╝

✅ YOU ONLY NEED YOUR LINKEDIN CREDENTIALS!

No API keys, no approvals, no waiting! 🎉


STEP 1: Make sure your credentials are in .env (2 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Open .env and add (or update) these lines:

# LinkedIn Personal Account Credentials
LINKEDIN_EMAIL=your_email@gmail.com
LINKEDIN_PASSWORD=your_password

That's it! No encryption needed for personal testing.


STEP 2: Test Single Post (1 minute)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run:
    python linkedin_personal_bot.py

This will:
1. Open your Chrome browser
2. Log in to LinkedIn automatically
3. Post the test content
4. Close the browser

Watch it work in real-time! 👀


STEP 3: Setup Daily Scheduler (2 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run:
    python linkedin_scheduler.py

Follow the prompts:
    1. Enter posting time (e.g., 09:00 for 9 AM)
    2. Choose if you want AI-generated content (yes/no)
    3. It will post automatically every day at that time!

The scheduler will keep running. Press Ctrl+C to stop.


HOW IT WORKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Personal Account Automation (Selenium):
  ✅ Uses your real LinkedIn login
  ✅ No API needed
  ✅ No approval process
  ✅ Works immediately
  ✅ Opens real Chrome browser
  ✅ Mimics human behavior

Content Generation (ChatGPT):
  ✅ Creates unique content daily
  ✅ Professional LinkedIn posts
  ✅ Includes hashtags and CTAs
  ✅ Topic-based or AI-generated


FILES CREATED FOR YOU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

linkedin_personal_bot.py
  └─ Selenium-based LinkedIn automation
  └─ Login + Post functionality
  └─ One-time or on-demand posting

linkedin_scheduler.py
  └─ Daily automatic posting scheduler
  └─ Runs continuously
  └─ Customizable posting time
  └─ Optional AI content generation

test_ultra_minimal.py (existing)
  └─ ChatGPT content generation


QUICK START EXAMPLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Example 1: Post once right now
    python linkedin_personal_bot.py

Example 2: Auto-post daily at 9 AM
    python linkedin_scheduler.py
    (Enter: 09:00)
    (Choose: no for default content)

Example 3: Daily AI-generated posts about AI
    python linkedin_scheduler.py
    (Enter: 09:00)
    (Choose: yes)
    (Enter topic: Artificial Intelligence)


TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"Chrome not found"
  → Install Chrome: https://www.google.com/chrome/
  → Or install ChromeDriver separately

"Login failed"
  → Check LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env
  → Make sure they're correct
  → Try logging in manually first to unlock any security

"2FA/Two-Factor Authentication blocks login"
  → Disable 2FA temporarily for automation
  → Or use an app password if LinkedIn offers it
  → Security note: Keep your .env file private!

"Element not found" 
  → LinkedIn's UI might have changed
  → Manual posting still works with test_ultra_minimal.py

"Connection timeout"
  → LinkedIn is blocking the connection
  → Wait a few minutes and try again
  → Use VPN if needed


IMPORTANT SECURITY NOTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔐 .env file contains your password
   ├─ NEVER commit to Git
   ├─ NEVER share with others
   ├─ Add to .gitignore (should already be there)
   └─ Keep it secure!

🔐 LinkedIn password security
   ├─ Don't use same password as other sites
   ├─ Disable 2FA for automation (risky!)
   ├─ Or use app-specific password if available
   └─ Consider a separate automation account


NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. ✅ Update .env with your credentials
2. ✅ Run: python linkedin_personal_bot.py (test once)
3. ✅ Run: python linkedin_scheduler.py (daily automation)
4. ✅ Keep it running in the background
5. 📊 Check your LinkedIn for daily posts!


KEEPING IT RUNNING 24/7
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Option 1: Windows Task Scheduler
  → Create a task to run linkedin_scheduler.py at startup
  → Script will run in background

Option 2: Screen/tmux (on Linux/Mac)
  → Run in a detached terminal session
  → Won't stop when you close terminal

Option 3: Docker
  → Run as a containerized service
  → Always available


THAT'S IT! 🎉
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You now have:
  ✅ AI-powered content generation (ChatGPT)
  ✅ Automatic LinkedIn posting (Selenium)
  ✅ Daily scheduling (schedule library)
  ✅ No API keys or approvals needed!

Questions? Check the troubleshooting section above.
"""

if __name__ == "__main__":
    print(GUIDE)
