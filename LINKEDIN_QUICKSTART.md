"""
Quick Start Guide for LinkedIn Official API Integration
"""

QUICK_START = """
╔════════════════════════════════════════════════════════════════╗
║     LinkedIn Official API - Quick Start Guide                  ║
╚════════════════════════════════════════════════════════════════╝

✅ WHAT YOU NEED TO DO

Step 1️⃣  Create a LinkedIn App (5 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Go to: https://www.linkedin.com/developers/apps
2. Click "Create app"
3. Fill in:
   ├─ App name: "LinkedIn Content Creator"
   ├─ LinkedIn Page: Choose your company page
   ├─ App logo: Upload any image
   └─ Agree to terms

4. Once created, click your app
5. Go to "Settings" tab
6. Copy your:
   ├─ CLIENT ID
   └─ CLIENT SECRET


Step 2️⃣  Add Credentials to .env (2 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Open .env and add:

# LinkedIn OAuth2 (from your app settings)
LINKEDIN_CLIENT_ID=YOUR_CLIENT_ID_HERE
LINKEDIN_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE
LINKEDIN_REDIRECT_URI=http://localhost:8000/auth/callback
LINKEDIN_ORGANIZATION_ID=YOUR_ORG_ID_HERE

To find ORGANIZATION_ID:
- Go to your LinkedIn company page
- URL looks like: linkedin.com/company/YOUR_ORG_ID
- Copy the number at the end


Step 3️⃣  Request API Permissions (varies - 2-5 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. In your app, click "Request access"
2. Select products:
   ✓ Sign In with LinkedIn
   ✓ Share on LinkedIn (IMPORTANT!)
3. Submit for review

LinkedIn will review and approve (usually 1-5 days)


Step 4️⃣  Get Access Token (30 seconds)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run this command:

    python get_linkedin_token.py

This will:
1. Open your browser automatically
2. Ask you to authorize the app
3. Save your access token to .env


Step 5️⃣  Post to LinkedIn! (10 seconds)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run:

    python post_to_linkedin_official.py

Done! Your post is now on LinkedIn! 🎉


📚 FILES CREATED FOR YOU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ get_linkedin_token.py
  └─ Handles OAuth2 authentication
  └─ Gets and saves your access token

✓ post_to_linkedin_official.py
  └─ Posts generated content to LinkedIn
  └─ Uses official LinkedIn API
  └─ Supports both personal and organization posts

✓ LINKEDIN_API_SETUP.md
  └─ Detailed setup guide
  └─ Troubleshooting tips


⏱️  TIMELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1 (Create App):        5 minutes
Step 2 (Add to .env):        2 minutes
Step 3 (Request Access):     2-5 days (automated review)
Step 4 (Get Token):          30 seconds
Step 5 (Post):               10 seconds
                            ─────────────
TOTAL:                       3-6 days


🚀 NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. ✅ Start with Step 1 above
2. 📄 See LINKEDIN_API_SETUP.md for detailed instructions
3. 🔑 Run: python get_linkedin_token.py (Step 4)
4. 📱 Run: python post_to_linkedin_official.py (Step 5)


❓ QUESTIONS?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Common Issues:
• "Client ID not found" → Check .env file
• "Access denied" → Your app might not be approved yet
• "Invalid redirect URI" → Make sure it matches your app settings

LinkedIn Docs:
https://learn.microsoft.com/en-us/linkedin/shared/api-guide/intro
"""

if __name__ == "__main__":
    print(QUICK_START)
