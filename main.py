"""
Main entry point for the LinkedIn Content Generator
Uses OpenAI API directly for simpler, faster content generation
"""
import logging
import sys
import os
import requests
from openai import OpenAI
from utils import setup_logger
from config import OPENAI_API_KEY, LINKEDIN_ACCESS_TOKEN, LINKEDIN_USER_ID

# Setup logger
logger = setup_logger(__name__)


def configure_utf8_output() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def generate_linkedin_content(topic: str) -> str:
    """
    Generate LinkedIn content using OpenAI directly
    
    Args:
        topic (str): The topic for the LinkedIn post
        
    Returns:
        str: The generated LinkedIn post
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not set in environment")
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Step 1: Generate the initial post
    print("[WRITING] Generating LinkedIn post content...")
    
    writer_prompt = f"""Write a detailed and engaging LinkedIn post about the following topic: {topic}

The post should:
1. Start with a compelling hook that captures attention
2. Provide 3-5 key insights or takeaways
3. Include practical tips or actionable advice
4. Be professional yet conversational in tone
5. Include relevant hashtags (3-5 hashtags)
6. End with a call-to-action or thought-provoking question
7. Be between 300-500 words

Format the post in a way that's easy to read on LinkedIn (use line breaks, bullet points where appropriate)."""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": writer_prompt}],
        temperature=0.7,
        max_tokens=1000
    )
    
    draft_post = response.choices[0].message.content
    
    # Step 2: Edit and improve the post
    print("[EDITING] Improving the post...")
    
    editor_prompt = f"""Review and improve this LinkedIn post. Make it more engaging, ensure it follows LinkedIn best practices, 
and optimize for engagement. Keep the same message but enhance the language and structure:

{draft_post}

Return only the improved post without any explanations."""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": editor_prompt}],
        temperature=0.7,
        max_tokens=1000
    )
    
    final_post = response.choices[0].message.content
    
    return final_post


def post_to_linkedin_official(content: str) -> bool:
    """
    Post content to LinkedIn using the official API
    
    Args:
        content (str): The text content to post
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not LINKEDIN_ACCESS_TOKEN or not LINKEDIN_USER_ID:
        logger.error("LinkedIn credentials not configured. Run: python linkedin_oauth_handler.py")
        print("[ERROR] LinkedIn credentials missing. Please set up OAuth first.")
        return False
    
    try:
        # API endpoint - use the official UGC endpoint
        url = "https://api.linkedin.com/v2/ugcPosts"
        
        # Headers
        headers = {
            'Authorization': f'Bearer {LINKEDIN_ACCESS_TOKEN}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        # Format user ID as URN if needed
        author_urn = LINKEDIN_USER_ID if LINKEDIN_USER_ID.startswith("urn:li:") else f"urn:li:person:{LINKEDIN_USER_ID}"
        
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
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 201:
            response_data = response.json()
            post_id = response_data.get('id', 'unknown')
            logger.info(f"Successfully posted to LinkedIn: {post_id}")
            return True
        
        elif response.status_code == 401:
            logger.error("Unauthorized (401) - Access token may have expired")
            print("[ERROR] LinkedIn token expired. Run: python linkedin_oauth_handler.py")
            return False
        
        elif response.status_code == 403:
            logger.error(f"Forbidden (403) - {response.text}")
            print("[ERROR] Permission denied. Check your LinkedIn app settings.")
            return False
        
        else:
            logger.error(f"Failed with status {response.status_code}: {response.text}")
            print(f"[ERROR] Failed to post (Status {response.status_code})")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        print(f"[ERROR] Network error: {e}")
        return False


def main():
    """Main function to run the LinkedIn Content Generator"""
    configure_utf8_output()
    try:
        # Get topic from user
        print("\n" + "="*60)
        print("LinkedIn Content Generator")
        print("="*60)
        
        topic = input("\nEnter the topic for your LinkedIn post: ").strip()
        
        if not topic:
            logger.warning("No topic provided. Exiting.")
            print("[ERROR] Please provide a topic.")
            return
        
        print(f"\nGenerating LinkedIn post for topic: {topic}")
        print("This may take a minute...\n")
        
        # Generate content
        final_post = generate_linkedin_content(topic)
        
        # Save the generated post before printing
        with open("generated_post.txt", "w", encoding="utf-8") as f:
            f.write(final_post)
        print("[INFO] Generated post saved to 'generated_post.txt'")
        
        # Display the generated post
        print("\n" + "="*60)
        print("[SUCCESS] Generated LinkedIn Post:")
        print("="*60)
        print(final_post)
        print("="*60 + "\n")
        
        # Ask if user wants to post to LinkedIn
        post_to_linkedin = input("Do you want to post this to LinkedIn? (yes/no): ").strip().lower()
        
        if post_to_linkedin == "yes":
            print("[POSTING] Attempting to post to LinkedIn...")
            success = post_to_linkedin_official(final_post)
            
            if success:
                print("[SUCCESS] Posted to LinkedIn!")
            else:
                print("[ERROR] Failed to post to LinkedIn. Check .env credentials and run: python linkedin_oauth_handler.py")
        else:
            print("\n[SUCCESS] Post generated successfully. You can copy and paste it manually to LinkedIn.")
            
            # Save post to a text file
            with open("generated_post.txt", "w", encoding="utf-8") as f:
                f.write(final_post)
            print("[INFO] Post saved to 'generated_post.txt'")
    
    except KeyboardInterrupt:
        logger.info("User interrupted the process")
        print("\n\n[INTERRUPTED] Process interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        print(f"\n[ERROR] An error occurred: {str(e)}")
        print("Please check the logs for more details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
