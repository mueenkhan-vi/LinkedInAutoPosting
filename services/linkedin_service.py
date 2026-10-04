"""
LinkedIn Service for posting content to LinkedIn
"""
import logging
from typing import Optional
from linkedin_api import Linkedin
from config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD

logger = logging.getLogger(__name__)


class LinkedInService:
    """Service to handle LinkedIn API interactions"""

    def __init__(self):
        """Initialize LinkedIn service with credentials"""
        self.client = None
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate with LinkedIn"""
        try:
            self.client = Linkedin(LINKEDIN_EMAIL, LINKEDIN_PASSWORD)
            logger.info("Successfully authenticated with LinkedIn")
        except Exception as e:
            logger.error(f"Failed to authenticate with LinkedIn: {str(e)}")
            raise

    def post_to_linkedin(self, content: str, media_urls: Optional[list] = None) -> Optional[str]:
        """
        Post content to LinkedIn

        Args:
            content (str): The text content to post
            media_urls (Optional[list]): List of media URLs to attach

        Returns:
            Optional[str]: Post ID if successful, None otherwise
        """
        try:
            if media_urls:
                post_result = self.client.post(
                    text_content=content,
                    media=media_urls
                )
            else:
                post_result = self.client.post(text_content=content)

            logger.info(f"Successfully posted to LinkedIn: {post_result}")
            return post_result

        except Exception as e:
            logger.error(f"Failed to post to LinkedIn: {str(e)}")
            return None

    def get_profile(self) -> dict:
        """Get current profile information"""
        try:
            profile = self.client.get_profile()
            logger.info("Successfully retrieved profile information")
            return profile
        except Exception as e:
            logger.error(f"Failed to get profile: {str(e)}")
            return {}
