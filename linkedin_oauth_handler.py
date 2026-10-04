#!/usr/bin/env python3
"""
LinkedIn OAuth 2.0 Handler
Gets access token and saves it to .env
"""

import os
import sys
import json
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, parse_qs, urlparse
import requests
from dotenv import load_dotenv, set_key
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Load environment
load_dotenv()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI", "http://localhost:8000/callback")

# Global to store auth code
auth_code = None
server = None

class OAuth2Handler(BaseHTTPRequestHandler):
    """Handle OAuth 2.0 callback"""
    
    def do_GET(self):
        global auth_code
        
        # Parse the callback URL
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # Get authorization code or error
        if 'code' in query_params:
            auth_code = query_params['code'][0]
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            response = """
            <html>
            <head><title>Authorization Successful</title></head>
            <body>
                <h1>Authorization Successful!</h1>
                <p>You can close this window and return to the terminal.</p>
                <p>Access token is being obtained...</p>
            </body>
            </html>
            """
            self.wfile.write(response.encode())
            
            logger.info("Authorization code received!")
            
        else:
            error = query_params.get('error', ['Unknown error'])[0]
            error_desc = query_params.get('error_description', ['No description'])[0]
            
            # Send error response
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            response = f"""
            <html>
            <head><title>Authorization Failed</title></head>
            <body>
                <h1>Authorization Failed</h1>
                <p>Error: {error}</p>
                <p>Description: {error_desc}</p>
            </body>
            </html>
            """
            self.wfile.write(response.encode())
            
            logger.error(f"Authorization failed: {error} - {error_desc}")
    
    def log_message(self, format, *args):
        """Suppress server logs"""
        pass


def get_authorization_code():
    """Step 1: Get authorization code from user"""
    
    if not CLIENT_ID or not CLIENT_SECRET:
        logger.error("ERROR: LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET not set in .env")
        logger.error("Please add them to .env file first")
        sys.exit(1)
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Step 1: Getting Authorization Code")
    logger.info("=" * 60)
    
    # Build authorization URL
    auth_params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'openid profile email w_member_social',
        'state': 'linkedin_oauth_state'
    }
    
    auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(auth_params)}"
    
    logger.info("")
    logger.info("Opening LinkedIn authorization page in your browser...")
    logger.info("Please authorize the app to access your LinkedIn account.")
    logger.info("")
    
    # Open browser
    webbrowser.open(auth_url)
    
    # Start local server to receive callback
    global server
    server = HTTPServer(('localhost', 8000), OAuth2Handler)
    logger.info("Waiting for authorization...")
    logger.info("(This may take up to 2 minutes)")
    logger.info("")
    
    # Handle requests
    for _ in range(120):  # Wait up to 2 minutes
        server.handle_request()
        if auth_code:
            break
    
    if not auth_code:
        logger.error("ERROR: Authorization timeout!")
        sys.exit(1)
    
    logger.info(f"Authorization code received: {auth_code[:20]}...")
    return auth_code


def get_access_token(auth_code):
    """Step 2: Exchange authorization code for access token"""
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Step 2: Exchanging Code for Access Token")
    logger.info("=" * 60)
    
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    
    # Prepare request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI
    }
    
    logger.info("Sending token request to LinkedIn...")
    
    try:
        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        
        access_token = token_data.get('access_token')
        expires_in = token_data.get('expires_in', 'unknown')
        
        logger.info(f"Access token obtained!")
        logger.info(f"Expires in: {expires_in} seconds")
        logger.info("")
        logger.info("=" * 60)
        logger.info("YOUR ACCESS TOKEN (copy the full line below):")
        logger.info("=" * 60)
        logger.info(f"Token: {access_token}")
        logger.info("=" * 60)
        logger.info("")
        
        return access_token
        
    except requests.exceptions.RequestException as e:
        logger.error(f"ERROR: Failed to get access token: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response: {e.response.text}")
        sys.exit(1)


def get_user_id(access_token):
    """Step 3: Get LinkedIn user ID"""
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Step 3: Getting Your LinkedIn User ID")
    logger.info("=" * 60)
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'LinkedIn-Version': '202404'
    }
    
    logger.info("Fetching your LinkedIn profile information from userinfo endpoint...")
    
    try:
        response = requests.get('https://api.linkedin.com/v2/userinfo', headers=headers)
        response.raise_for_status()
        
        user_data = response.json()
        user_id = user_data.get('sub') or user_data.get('id')
        
        if user_id:
            user_urn = f"urn:li:member:{user_id}"
            logger.info(f"Your LinkedIn User ID: {user_urn}")
            return user_urn
        else:
            logger.error("ERROR: Could not extract user ID from response")
            logger.error(f"Response: {user_data}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        logger.error(f"ERROR: Failed to get user ID: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response: {e.response.text}")
            if e.response.status_code in (401, 403):
                logger.error("Your app may not have the OpenID Connect product or profile scope enabled.")
                logger.error("Make sure the app has Sign In with LinkedIn using OpenID Connect and the scopes: openid profile email.")
        sys.exit(1)


def save_credentials(access_token, user_id):
    """Step 4: Save credentials to .env"""
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Step 4: Saving Credentials")
    logger.info("=" * 60)
    
    env_file = '.env'
    
    # Update .env file
    set_key(env_file, 'LINKEDIN_ACCESS_TOKEN', access_token)
    set_key(env_file, 'LINKEDIN_USER_ID', user_id)
    
    logger.info(f"Credentials saved to {env_file}")
    logger.info("")
    logger.info("✅ OAuth Setup Complete!")
    logger.info("")
    logger.info("You can now run: python linkedin_api_poster.py")
    logger.info("")


def main():
    """Run OAuth flow"""
    
    print("")
    print("=" * 60)
    print("LinkedIn OAuth 2.0 Setup")
    print("=" * 60)
    print("")
    
    try:
        # Step 1: Get authorization code
        auth_code = get_authorization_code()
        
        # Step 2: Exchange for access token
        access_token = get_access_token(auth_code)
        
        # Step 3: Get user ID
        user_id = get_user_id(access_token)
        
        # Step 4: Save to .env
        save_credentials(access_token, user_id)
        
    except KeyboardInterrupt:
        logger.info("Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)
    finally:
        if server:
            server.server_close()


if __name__ == "__main__":
    main()
