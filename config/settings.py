"""
Configuration settings for the LinkedIn Crew AI Agent
"""
import os
from dotenv import load_dotenv
from utils.encryption import decrypt_credential

# Load environment variables
load_dotenv()

# Helper function to get and optionally decrypt credentials
def _get_credential(key: str, decrypt: bool = False) -> str:
    """Get credential from environment and optionally decrypt it"""
    value = os.getenv(key)
    if not value:
        return None
    
    if decrypt and value.startswith("encrypted:"):
        # Remove the 'encrypted:' prefix and decrypt
        encrypted_value = value[10:]  # Remove 'encrypted:' prefix
        try:
            return decrypt_credential(encrypted_value)
        except Exception as e:
            print(f"⚠️  Warning: Failed to decrypt {key}: {str(e)}")
            print(f"   Using as plaintext instead.")
            return encrypted_value
    
    return value


# OpenAI Configuration
OPENAI_API_KEY = _get_credential("OPENAI_API_KEY", decrypt=True)
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4")

# LinkedIn Configuration
LINKEDIN_EMAIL = _get_credential("LINKEDIN_EMAIL", decrypt=True)
LINKEDIN_PASSWORD = _get_credential("LINKEDIN_PASSWORD", decrypt=True)

# LinkedIn API Configuration (if using official API)
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_USER_ID = os.getenv("LINKEDIN_USER_ID")
LINKEDIN_ORGANIZATION_ID = os.getenv("LINKEDIN_ORGANIZATION_ID")

# Agent Configuration
VERBOSE_MODE = True
MAX_ITERATIONS = 10
