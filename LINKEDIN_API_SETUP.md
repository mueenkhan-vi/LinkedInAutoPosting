"""
LinkedIn Official API Integration Setup Guide
"""

LINKEDIN_API_SETUP_GUIDE = """
============================================================
📚 LinkedIn Official API Setup Guide
============================================================

STEP 1: Register Your Application
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Go to: https://www.linkedin.com/developers/apps
2. Click "Create app"
3. Fill in the form:
   - App name: "LinkedIn Content Creator"
   - LinkedIn Page: (Select or create one)
   - App logo: (Upload any image)
   - Legal agreement: Accept and continue

4. After creation, go to your app's Settings:
   - Note your: CLIENT ID and CLIENT SECRET
   - These are sensitive - keep them secure!


STEP 2: Request Access to Marketing Developer Platform
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. In your app settings, click "Request access"
2. Select required products:
   - ✓ Sign In with LinkedIn
   - ✓ Share on LinkedIn
   - ✓ Marketing Developer Platform

3. Request approval (LinkedIn reviews requests, usually 2-5 days)
4. Once approved, you'll have access to post on behalf of your organization


STEP 3: Set Redirect URIs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

In your app settings, add Authorized redirect URLs:
   - http://localhost:8000/auth/callback
   - http://localhost:8000/callback
   - https://yourdomain.com/callback (if you have one)


STEP 4: Update .env File
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Add these to your .env file:

# LinkedIn OAuth2
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
LINKEDIN_REDIRECT_URI=http://localhost:8000/auth/callback
LINKEDIN_ORGANIZATION_ID=your_org_id_here

To get ORGANIZATION_ID:
1. Go to: https://www.linkedin.com/mynetwork/invitation-manager/
2. Look at the URL - it contains your org ID
3. Or check your company LinkedIn page URL


STEP 5: Get Access Token (One-time Setup)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run the authentication script:
   python get_linkedin_token.py

This will:
1. Open your browser
2. Ask you to authorize the app
3. Redirect you back with an access token
4. Save the token to .env automatically


STEP 6: Test the Integration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run: python post_to_linkedin_official.py

This will post your content to LinkedIn!


KEY DIFFERENCES: Official vs Unofficial API
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Official API:
  ✅ Supported by LinkedIn
  ✅ Secure OAuth2 authentication
  ✅ Reliable and stable
  ✅ No bot detection issues
  ⚠️  Slightly more setup required

Unofficial API (linkedin-api):
  ❌ Uses web scraping
  ❌ Blocked frequently
  ❌ Bot detection triggers
  ❌ Against LinkedIn ToS


TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Issue: "Invalid redirect URI"
  → Check your .env LINKEDIN_REDIRECT_URI matches app settings

Issue: "Access not approved"
  → Wait 2-5 days for LinkedIn to review your app request
  → Check app status at developers.linkedin.com

Issue: "401 Unauthorized"
  → Your access token may have expired
  → Run get_linkedin_token.py again

Issue: "403 Forbidden"
  → Your app may not have permission to post
  → Check that you requested the right permissions


SUPPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LinkedIn Developer Docs:
  https://learn.microsoft.com/en-us/linkedin/shared/api-guide/intro

Official Python SDK:
  https://github.com/microsoft/linkedin-sdk-python
"""

if __name__ == "__main__":
    print(LINKEDIN_API_SETUP_GUIDE)
