"""
LinkedIn Crew AI Orchestration
Manages the crew of agents to create and post LinkedIn content
"""
import logging
from crewai import Crew
from agents import ContentWriterAgent, EditorAgent, LinkedInPosterAgent
from config import VERBOSE_MODE, MAX_ITERATIONS

logger = logging.getLogger(__name__)


class LinkedInCrew:
    """Orchestrates the LinkedIn content creation and posting crew"""

    def __init__(self):
        """Initialize the crew with all agents"""
        self.writer_agent = ContentWriterAgent.create_agent()
        self.editor_agent = EditorAgent.create_agent()
        self.poster_agent = LinkedInPosterAgent.create_agent()
        self.crew = None

    def create_crew(self):
        """Create the Crew AI crew"""
        self.crew = Crew(
            agents=[self.writer_agent, self.editor_agent, self.poster_agent],
            verbose=VERBOSE_MODE,
            max_iterations=MAX_ITERATIONS,
        )
        logger.info("Crew created successfully")

    def generate_linkedin_post(self, topic: str) -> str:
        """
        Generate a LinkedIn post for the given topic

        Args:
            topic (str): The topic for the LinkedIn post

        Returns:
            str: The final LinkedIn post ready to be published
        """
        if not self.crew:
            self.create_crew()

        logger.info(f"Starting LinkedIn post generation for topic: {topic}")

        # Create tasks
        writing_task = ContentWriterAgent.create_writing_task(self.writer_agent, topic)
        
        # For now, we'll execute sequentially
        # In a real scenario, you might want to use the results from one task as input to the next
        
        logger.info("Executing writing task...")
        writing_result = self.crew.kickoff(tasks=[writing_task])
        
        draft_post = writing_result if isinstance(writing_result, str) else str(writing_result)
        
        logger.info("Executing editing task...")
        editing_task = EditorAgent.create_editing_task(self.editor_agent, draft_post)
        
        # Create a new crew instance for the editing task
        editing_crew = Crew(
            agents=[self.editor_agent],
            verbose=VERBOSE_MODE,
            max_iterations=MAX_ITERATIONS,
        )
        editing_result = editing_crew.kickoff(tasks=[editing_task])
        
        final_post = editing_result if isinstance(editing_result, str) else str(editing_result)
        
        logger.info("Executing posting validation task...")
        posting_task = LinkedInPosterAgent.create_posting_task(self.poster_agent, final_post)
        
        posting_crew = Crew(
            agents=[self.poster_agent],
            verbose=VERBOSE_MODE,
            max_iterations=MAX_ITERATIONS,
        )
        posting_result = posting_crew.kickoff(tasks=[posting_task])
        
        logger.info("LinkedIn post generation completed successfully")
        
        return final_post
