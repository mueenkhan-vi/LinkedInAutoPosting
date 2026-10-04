# LinkedIn Official API Setup Guide - Complete

## Step 1: Create LinkedIn Developer App

### 1.1 Go to LinkedIn Developer Portal
1. Visit: https://www.linkedin.com/developers/apps
2. Click "Create app"

### 1.2 Fill App Details
- **App name**: Your choice (e.g., "LinkedIn Auto Poster")
- **LinkedIn Page**: Create or select an existing company page
- **App logo**: Upload any image (required)
- **Legal agreement**: Check the box
- Click "Create app"

### 1.3 Get Your Credentials
After creation, you'll see:
- **Client ID** (save this!)
- **Client Secret** (save this!)

**Keep these safe - you'll use them in the next step**

---

## Step 2: Configure App Settings

### 2.1 Authorized redirect URLs
In your app settings, add:
```
http://localhost:8000/callback
```

### 2.2 Request Access to Sign In with LinkedIn
1. Go to "Products" tab
2. Add "Sign In with LinkedIn"
3. Request access

### 2.3 Request Permission for Share on LinkedIn
1. Go to "Products" tab
2. Add "Share on LinkedIn"
3. In **Requested access scopes**, select:
   - `w_member_social` (Write member social posts)

---

## Step 3: Get Your LinkedIn User ID

### 3.1 Using the API
Run this command (replace TOKEN with any LinkedIn access token):
```bash
curl -X GET https://api.linkedin.com/v2/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response will include:
```json
{
  "id": "XXXXXXXXX"
}
```

Your **LinkedIn User URN** is: `urn:li:person:XXXXXXXXX`

---

## Step 4: Setup Python Scripts

### 4.1 Edit your `.env` file
Add these lines:
```
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
LINKEDIN_REDIRECT_URI=http://localhost:8000/callback
LINKEDIN_ACCESS_TOKEN=will_be_filled_after_oauth
LINKEDIN_USER_ID=urn:li:person:XXXXXXXXX
```

### 4.2 Run OAuth Flow
```bash
python linkedin_oauth_handler.py
```

This will:
1. Open your browser
2. Ask you to authorize the app
3. Get your access token
4. Save it to `.env`

### 4.3 Post to LinkedIn
```bash
python linkedin_api_poster.py
```

This will:
1. Read your post from `linkedin_post_content.txt`
2. Use the API to post it
3. Show success message with post link

---

## Troubleshooting

**"Invalid Client ID"**
- Check your Client ID and Client Secret in `.env`
- Verify they match your app settings

**"Unauthorized"**
- Your access token may have expired
- Run OAuth flow again: `python linkedin_oauth_handler.py`

**"No permission"**
- Make sure `w_member_social` scope is approved
- May take 24 hours for LinkedIn to approve

**"Invalid User ID"**
- Get your ID from LinkedIn API: check Step 3.1

---

## All Files You'll Need

1. ✅ `.env` - Credentials (create/update)
2. ✅ `linkedin_oauth_handler.py` - OAuth flow
3. ✅ `linkedin_api_poster.py` - Post to LinkedIn
4. ✅ `linkedin_post_content.txt` - Your post content
5. ✅ `.encryption.key` - Already have this

---

## Timeline

- **App Creation**: 5 minutes
- **Getting Credentials**: 2 minutes
- **OAuth Setup**: 5 minutes
- **First Post**: 1 minute
- **Total**: ~15 minutes

Let's do this! 🚀
