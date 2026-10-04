#!/usr/bin/env python3
"""
LinkedIn Official API Poster
Posts content using the official LinkedIn API
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Load environment
load_dotenv()

ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
USER_ID = os.getenv("LINKEDIN_USER_ID")


def validate_credentials():
    """Validate that we have necessary credentials"""
    
    if not ACCESS_TOKEN:
        logger.error("ERROR: LINKEDIN_ACCESS_TOKEN not found in .env")
        logger.error("Run: python linkedin_oauth_handler.py")
        sys.exit(1)
    
    if not USER_ID:
        logger.error("ERROR: LINKEDIN_USER_ID not found in .env")
        logger.error("Run: python linkedin_oauth_handler.py")
        sys.exit(1)
    
    logger.info("Credentials found")
    return True


def get_author_urn():
    """Return a valid LinkedIn author URN."""
    if USER_ID.startswith("urn:li:"):
        return USER_ID
    return f"urn:li:person:{USER_ID}"


def read_post_content():
    """Read post content from file"""
    
    if not os.path.exists("linkedin_post_content.txt"):
        logger.error("ERROR: linkedin_post_content.txt not found!")
        logger.error("Please run: python test_ultra_minimal.py")
        sys.exit(1)
    
    with open("linkedin_post_content.txt", "r", encoding="utf-8") as f:
        content = f.read().strip()
    
    if not content:
        logger.error("ERROR: Post content is empty!")
        sys.exit(1)
    
    logger.info("Post content loaded")
    logger.info(f"   Length: {len(content)} characters")
    return content


def post_to_linkedin(content):
    """Post content to LinkedIn using official API"""
    
    logger.info("Posting to LinkedIn...")
    
    # API endpoint - use the official UGC endpoint
    url = "https://api.linkedin.com/v2/ugcPosts"
    
    # Headers
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    
    author_urn = get_author_urn()
    
    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    logger.info("Sending request to LinkedIn API...")
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        # Check response
        if response.status_code == 201:
            # Success!
            response_data = response.json()
            post_id = response_data.get('id', 'unknown')
            
            logger.info("")
            logger.info("=" * 60)
            logger.info("✅ POST SUCCESSFUL!")
            logger.info("=" * 60)
            logger.info(f"Post ID: {post_id}")
            logger.info("")
            logger.info("Your post is now live on LinkedIn!")
            logger.info("")
            
            return True
        
        elif response.status_code == 401:
            logger.error("ERROR: Unauthorized (401)")
            logger.error("Your access token may have expired.")
            logger.error("Run: python linkedin_oauth_handler.py")
            return False
        
        elif response.status_code == 403:
            logger.error("ERROR: Forbidden (403)")
            logger.error("You may not have permission to post.")
            logger.error("Check your app settings and scopes.")
            logger.error(f"Response: {response.text}")
            return False
        
        elif response.status_code == 400:
            logger.error("ERROR: Bad Request (400)")
            logger.error("The request format may be invalid.")
            logger.error(f"Response: {response.text}")
            return False
        
        else:
            logger.error(f"ERROR: Unexpected status code {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"ERROR: Request failed: {e}")
        return False


def main():
    """Main function"""
    
    print("")
    print("=" * 60)
    print("LinkedIn Official API Poster")
    print("=" * 60)
    print("")
    
    try:
        # Validate credentials
        validate_credentials()
        print("")
        
        # Read content
        content = read_post_content()
        print("")
        
        # Show preview
        logger.info("Preview of post:")
        logger.info("-" * 60)
        if len(content) > 200:
            logger.info(content[:200] + "...")
        else:
            logger.info(content)
        logger.info("-" * 60)
        print("")
        
        # Post to LinkedIn
        success = post_to_linkedin(content)
        
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Posting cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
