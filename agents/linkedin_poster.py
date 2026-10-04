"""
LinkedIn Poster Agent - Handles posting to LinkedIn using Official API
"""
import logging
import requests
from crewai import Agent, Task
from config import LINKEDIN_ACCESS_TOKEN, LINKEDIN_USER_ID

logger = logging.getLogger(__name__)


class LinkedInPosterAgent:
    """Agent responsible for posting content to LinkedIn using the official API"""

    @staticmethod
    def create_agent():
        """Create and return a LinkedIn Poster agent"""
        return Agent(
            role="LinkedIn Publisher",
            goal="Successfully publish content to LinkedIn and monitor initial engagement",
            backstory="""You are a social media publishing expert with deep knowledge of LinkedIn's 
            platform mechanics and posting best practices. You understand optimal posting times, 
            format requirements, and how to ensure content reaches the target audience effectively.""",
            verbose=True,
            allow_delegation=False,
        )

    @staticmethod
    def post_to_linkedin(content: str) -> bool:
        """
        Post content to LinkedIn using the official API
        
        Args:
            content (str): The text content to post
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not LINKEDIN_ACCESS_TOKEN or not LINKEDIN_USER_ID:
            logger.error("LinkedIn credentials not configured")
            return False
        
        try:
            url = "https://api.linkedin.com/v2/ugcPosts"
            headers = {
                'Authorization': f'Bearer {LINKEDIN_ACCESS_TOKEN}',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Restli-Protocol-Version': '2.0.0'
            }
            
            author_urn = LINKEDIN_USER_ID if LINKEDIN_USER_ID.startswith("urn:li:") else f"urn:li:person:{LINKEDIN_USER_ID}"
            
            payload = {
                "author": author_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": content},
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
            }
            
            response = requests.post(url, json=payload, headers=headers)
            success = response.status_code == 201
            
            if success:
                logger.info(f"Successfully posted to LinkedIn: {response.json().get('id')}")
            else:
                logger.error(f"Failed to post: {response.status_code} - {response.text}")
            
            return success
            
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return False

    @staticmethod
    def create_posting_task(agent, final_post: str):
        """
        Create a task for the agent to handle LinkedIn posting

        Args:
            agent: The agent instance
            final_post (str): The final post content to publish

        Returns:
            Task: A Crew AI task instance
        """
        return Task(
            description=f"""Prepare the following content for publishing on LinkedIn:

{final_post}

Please:
1. Verify the post meets all LinkedIn requirements
2. Ensure optimal formatting for LinkedIn's platform
3. Confirm all hashtags are properly formatted (#hashtag)
4. Check that links (if any) are properly formatted
5. Provide a summary of posting recommendations (optimal time, audience insights)
6. Confirm the post is ready for immediate publication

Note: The actual publication to LinkedIn will be handled by the Official LinkedIn API.
This task is to prepare and validate the content.""",
            agent=agent,
            expected_output="Validated post ready for publication with posting recommendations"
        )
