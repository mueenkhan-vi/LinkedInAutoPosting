"""
LinkedIn Daily Posting Scheduler
Automatically post content at a specified time each day
"""
import schedule
import time
import logging
from datetime import datetime
from linkedin_personal_bot import post_to_linkedin
from test_ultra_minimal import generate_post

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LinkedInScheduler:
    """Schedule automatic LinkedIn posts"""
    
    def __init__(self, post_time: str = "09:00"):
        """
        Initialize scheduler
        
        Args:
            post_time (str): Time to post daily in HH:MM format (24-hour)
        """
        self.post_time = post_time
        self.is_running = False
        logger.info(f"LinkedIn Scheduler initialized - Post time: {post_time}")
    
    def generate_and_post(self, topic: str = None):
        """Generate and post content"""
        try:
            logger.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting post generation...")
            
            # If topic provided, generate fresh content
            if topic:
                logger.info(f"Generating post for topic: {topic}")
                content = generate_post(topic)
            else:
                # Use default topic
                content = """🚀 Excited to share insights on AI and innovation!

The pace of technological advancement is accelerating at an unprecedented rate. Every day brings new possibilities and opportunities for those ready to embrace change.

Key takeaways for today:
1. Stay curious and keep learning
2. Embrace new technologies
3. Share knowledge with your network
4. Build connections with like-minded professionals

What's your take on the latest in AI and technology? Drop your thoughts below! 👇

#AI #Innovation #Technology #Learning #Growth #LinkedIn"""
            
            logger.info("Post content generated, now publishing to LinkedIn...")
            
            # Post to LinkedIn
            success = post_to_linkedin(content)
            
            if success:
                logger.info(f"✅ Successfully posted at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                logger.error(f"❌ Failed to post at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            return success
        
        except Exception as e:
            logger.error(f"❌ Error during posting: {str(e)}")
            return False
    
    def schedule_daily_post(self, topic: str = None):
        """Schedule daily posting"""
        def job():
            self.generate_and_post(topic)
        
        schedule.every().day.at(self.post_time).do(job)
        logger.info(f"✅ Daily post scheduled at {self.post_time}")
    
    def start(self, topic: str = None):
        """Start the scheduler"""
        self.schedule_daily_post(topic)
        self.is_running = True
        
        logger.info("="*60)
        logger.info("📱 LinkedIn Daily Scheduler Running")
        logger.info("="*60)
        logger.info(f"Posts will be published at {self.post_time} every day")
        logger.info("Press Ctrl+C to stop the scheduler\n")
        
        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        except KeyboardInterrupt:
            logger.info("\n⏹️  Scheduler stopped by user")
            self.is_running = False
    
    def stop(self):
        """Stop the scheduler"""
        self.is_running = False
        logger.info("Scheduler stopped")


def main():
    """Main function"""
    import sys
    from dotenv import load_dotenv
    
    load_dotenv()
    
    print("\n" + "="*60)
    print("📅 LinkedIn Daily Posting Scheduler")
    print("="*60)
    
    # Ask user for post time
    post_time = input("\nEnter posting time (HH:MM in 24-hour format, default 09:00): ").strip()
    if not post_time:
        post_time = "09:00"
    
    # Validate time format
    try:
        time.strptime(post_time, "%H:%M")
    except ValueError:
        print("❌ Invalid time format. Using default 09:00")
        post_time = "09:00"
    
    # Ask for topic or use default
    use_generated = input("Generate fresh content each day? (yes/no, default: no): ").strip().lower()
    
    topic = None
    if use_generated == "yes":
        topic = input("Enter topic for daily posts (or press Enter for random topics): ").strip()
    
    # Start scheduler
    scheduler = LinkedInScheduler(post_time)
    scheduler.start(topic)


if __name__ == "__main__":
    main()
