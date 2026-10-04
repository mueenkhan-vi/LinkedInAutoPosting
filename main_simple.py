"""
Simple LinkedIn Post Generator using OpenAI (Direct API)
Alternative to CrewAI for better compatibility
"""
import logging
import sys
import requests
from openai import OpenAI
from utils import setup_logger
from config import OPENAI_API_KEY, LINKEDIN_ACCESS_TOKEN, LINKEDIN_USER_ID

# Setup logger
logger = setup_logger(__name__)


class SimpleLinkedInAgent:
    """Simple agent to generate LinkedIn posts using OpenAI directly"""

    def __init__(self):
        """Initialize the agent with OpenAI client"""
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in .env file")
        
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        logger.info("SimpleLinkedInAgent initialized successfully")

    def generate_post(self, topic: str) -> str:
        """
        Generate a LinkedIn post using OpenAI

        Args:
            topic (str): The topic for the LinkedIn post

        Returns:
            str: Generated LinkedIn post
        """
        logger.info(f"Generating post for topic: {topic}")

        prompt = f"""Write a detailed and engaging LinkedIn post about the following topic: {topic}

The post should:
1. Start with a compelling hook that captures attention
2. Provide 3-5 key insights or takeaways
3. Include practical tips or actionable advice
4. Be professional yet conversational in tone
5. Include relevant hashtags (3-5 hashtags)
6. End with a call-to-action or thought-provoking question
7. Be between 300-500 words

Format the post in a way that's easy to read on LinkedIn (use line breaks, bullet points where appropriate).

Return only the post content, nothing else."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an experienced LinkedIn content strategist. You excel at crafting compelling narratives that resonate with professionals and drive meaningful engagement.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=1500,
            )

            post_content = response.choices[0].message.content
            logger.info("Post generated successfully")
            return post_content

        except Exception as e:
            logger.error(f"Failed to generate post: {str(e)}")
            raise

    def edit_post(self, draft_post: str) -> str:
        """
        Refine a LinkedIn post

        Args:
            draft_post (str): The draft post to refine

        Returns:
            str: Refined post
        """
        logger.info("Editing post...")

        prompt = f"""Review and refine the following LinkedIn post draft:

{draft_post}

Please:
1. Check for grammar, spelling, and punctuation errors
2. Improve clarity and flow
3. Enhance engagement potential
4. Ensure the tone is professional yet conversational
5. Verify hashtags are relevant (if possible)
6. Optimize for readability (use line breaks effectively)
7. Make sure the call-to-action is clear and compelling
8. Ensure the post follows LinkedIn best practices
9. Add any additional improvements you see fit

Return the refined post, nothing else."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a seasoned professional editor with expertise in LinkedIn content. You ensure content is compelling, error-free, and optimized for LinkedIn's algorithm.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5,
                max_tokens=1500,
            )

            refined_post = response.choices[0].message.content
            logger.info("Post refined successfully")
            return refined_post

        except Exception as e:
            logger.error(f"Failed to refine post: {str(e)}")
            raise

    def post_to_linkedin(self, content: str) -> bool:
        """
        Post content to LinkedIn using the official API
        
        Args:
            content (str): The text content to post
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not LINKEDIN_ACCESS_TOKEN or not LINKEDIN_USER_ID:
            logger.error("LinkedIn credentials not configured. Run: python linkedin_oauth_handler.py")
            print("❌ LinkedIn credentials missing. Please set up OAuth first.")
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
                print("❌ LinkedIn token expired. Run: python linkedin_oauth_handler.py")
                return False
            
            elif response.status_code == 403:
                logger.error(f"Forbidden (403) - {response.text}")
                print("❌ Permission denied. Check your LinkedIn app settings.")
                return False
            
            else:
                logger.error(f"Failed with status {response.status_code}: {response.text}")
                print(f"❌ Failed to post (Status {response.status_code})")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            print(f"❌ Network error: {e}")
            return False


def main():
    """Main function to run the simple LinkedIn agent"""
    try:
        print("\n" + "="*60)
        print("🚀 LinkedIn Post Generator (Direct OpenAI API)")
        print("="*60)
        
        topic = input("\nEnter the topic for your LinkedIn post: ").strip()
        
        if not topic:
            logger.warning("No topic provided")
            print("❌ Please provide a topic.")
            return
        
        print(f"\n✍️  Generating LinkedIn post for topic: {topic}")
        print("Please wait...\n")
        
        # Initialize agent
        agent = SimpleLinkedInAgent()
        
        # Generate post
        draft_post = agent.generate_post(topic)
        
        print("\n" + "="*60)
        print("📝 Initial Draft:")
        print("="*60)
        print(draft_post)
        
        # Refine post
        print("\n🔍 Refining post...")
        final_post = agent.edit_post(draft_post)
        
        print("\n" + "="*60)
        print("✅ Final LinkedIn Post:")
        print("="*60)
        print(final_post)
        print("="*60 + "\n")
        
        # Ask if user wants to post to LinkedIn
        post_to_linkedin = input("Do you want to post this to LinkedIn? (yes/no): ").strip().lower()
        
        if post_to_linkedin == "yes":
            print("\n📤 Attempting to post to LinkedIn...")
            success = agent.post_to_linkedin(final_post)
            
            if success:
                print("✅ Successfully posted to LinkedIn!")
            else:
                print("❌ Failed to post to LinkedIn. Check .env credentials and run: python linkedin_oauth_handler.py")
        else:
            print("\n✅ Post generated successfully. You can copy and paste it manually to LinkedIn.")
            
            # Save post to a text file
            with open("generated_post.txt", "w", encoding="utf-8") as f:
                f.write(final_post)
            print("📄 Post saved to 'generated_post.txt'")
    
    except KeyboardInterrupt:
        logger.info("User interrupted the process")
        print("\n\n⚠️  Process interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        print(f"\n❌ An error occurred: {str(e)}")
        print("Please check the logs for more details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
