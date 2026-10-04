"""
LinkedIn Personal Account Automation using Selenium
For individual users with LinkedIn credentials (email + password)
"""
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import logging
from cryptography.fernet import Fernet

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def get_decrypted_credential(key_name: str) -> str:
    """Decrypt a credential from .env"""
    value = os.getenv(key_name)
    if not value:
        return None
    
    if not value.startswith("encrypted:"):
        return value
    
    encrypted_value = value[10:]
    key_file = ".encryption.key"
    
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            key = f.read()
    else:
        raise ValueError("Encryption key file not found")
    
    cipher = Fernet(key)
    decrypted = cipher.decrypt(encrypted_value.encode())
    return decrypted.decode()


class LinkedInAutomator:
    """Automate LinkedIn posting using Selenium"""
    
    def __init__(self, email: str, password: str, headless: bool = False):
        """Initialize LinkedIn automator with credentials"""
        self.email = email
        self.password = password
        self.driver = None
        self.wait = None
        self.headless = headless
        logger.info("LinkedInAutomator initialized")
    
    def setup_browser(self):
        """Setup Chrome browser with Selenium"""
        logger.info("Setting up Chrome browser...")
        
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Auto-download and use ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        logger.info("Chrome browser ready")
    
    def login(self) -> bool:
        """Login to LinkedIn"""
        try:
            logger.info("Navigating to LinkedIn...")
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(3)
            
            # Enter email
            logger.info("Entering email...")
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(self.email)
            time.sleep(1)
            
            # Enter password
            logger.info("Entering password...")
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(self.password)
            time.sleep(1)
            
            # Click login
            logger.info("Clicking login button...")
            login_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Sign in']")
            login_button.click()
            
            # Wait for page to load (up to 15 seconds)
            logger.info("Waiting for LinkedIn to load...")
            time.sleep(8)
            
            # Check if login successful - look for multiple possible indicators
            try:
                # Try multiple selectors to detect successful login
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "global-nav")), timeout=5)
                logger.info("✅ Login successful!")
                return True
            except:
                try:
                    # Alternative check - look for feed or home
                    current_url = self.driver.current_url
                    if "linkedin.com/feed" in current_url or "linkedin.com/home" in current_url:
                        logger.info("✅ Login successful!")
                        return True
                except:
                    pass
                
                logger.error("❌ Login failed - could not verify login")
                return False
        
        except Exception as e:
            logger.error(f"❌ Login error: {str(e)}")
            return False
    
    def post_content(self, content: str) -> bool:
        """Post content to LinkedIn feed"""
        try:
            logger.info("Starting to post content...")
            
            # Navigate to home if not already there
            self.driver.get("https://www.linkedin.com/feed/")
            time.sleep(4)
            
            # Try multiple selectors for the post button
            post_button = None
            selectors = [
                "//button[contains(@aria-label, 'Start a post')]",
                "//button[contains(., 'Start a post')]",
                "//div[@contenteditable='true']",
            ]
            
            for selector in selectors:
                try:
                    logger.info(f"Trying selector: {selector}")
                    post_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector)),
                        timeout=3
                    )
                    if post_button:
                        logger.info("Found post button!")
                        break
                except:
                    continue
            
            if not post_button:
                logger.error("Could not find post button")
                return False
            
            # Click the button
            logger.info("Clicking post button...")
            self.driver.execute_script("arguments[0].click();", post_button)
            time.sleep(3)
            
            # Find the text area
            logger.info("Finding text area...")
            text_area = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']")),
                timeout=5
            )
            
            # Click and type content
            logger.info("Typing content...")
            text_area.click()
            time.sleep(1)
            text_area.send_keys(content)
            time.sleep(2)
            
            # Find and click Post button
            logger.info("Clicking submit button...")
            post_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Post') or contains(., 'Post')]")),
                timeout=5
            )
            
            # Scroll to button if needed
            self.driver.execute_script("arguments[0].scrollIntoView();", post_btn)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", post_btn)
            
            # Wait for success
            time.sleep(4)
            logger.info("✅ Post published successfully!")
            return True
        
        except Exception as e:
            logger.error(f"❌ Posting error: {str(e)}")
            return False
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")
    
    def __enter__(self):
        """Context manager entry"""
        self.setup_browser()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


def post_to_linkedin(content: str) -> bool:
    """Main function to post content to LinkedIn"""
    
    # Get credentials from .env
    email = get_decrypted_credential("LINKEDIN_EMAIL")
    password = get_decrypted_credential("LINKEDIN_PASSWORD")
    
    if not email or not password:
        logger.error("❌ Missing LinkedIn credentials in .env file")
        logger.error("Add these to .env:")
        logger.error("  LINKEDIN_EMAIL=your_email@gmail.com")
        logger.error("  LINKEDIN_PASSWORD=your_password")
        return False
    
    try:
        with LinkedInAutomator(email, password) as bot:
            # Login
            if not bot.login():
                return False
            
            # Post content
            if not bot.post_content(content):
                return False
            
            return True
    
    except Exception as e:
        logger.error(f"❌ Automation error: {str(e)}")
        return False


def main():
    """Main function for testing"""
    
    post_content = """Did you know that the future of communication is being redefined as we speak? Let me introduce you to the latest release of ChatGPT 5.5, a revolutionary leap in natural language understanding and conversation AI technology.

The company behind OpenAI has just rolled out its latest version, and it is nothing short of groundbreaking. The improvements seen in ChatGPT 5.5 are the result of rigorous research, meticulous engineering, and most importantly, constructive feedback from millions of users globally.

So what makes ChatGPT 5.5 such a gamechanger? Let's dive in:

1. Enhanced Conversation Quality: The algorithm's ability to understand context and respond with increased relevance has been significantly improved. It's almost like talking to another human!

2. Better Error Handling: In previous versions, understanding complex instructions or multi-layered queries was a challenge. ChatGPT 5.5, however, brings a noticeable reduction in such misunderstandings, ensuring a smoother interaction.

3. Contextual Awareness: The new update provides even more accurate responses by considering the broader context of the conversation. Say goodbye to repetitive or irrelevant answers!

#ChatGPT #ArtificialIntelligence #AIInnovation #FutureOfCommunication #TechnologyTrends"""
    
    print("\n" + "="*60)
    print("📱 LinkedIn Personal Account Automation")
    print("="*60 + "\n")
    
    success = post_to_linkedin(post_content)
    
    if success:
        print("\n✅ Post successfully published to LinkedIn!")
    else:
        print("\n❌ Failed to post to LinkedIn")


if __name__ == "__main__":
    main()
