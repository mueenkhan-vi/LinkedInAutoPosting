"""
Editor Agent - Reviews and refines LinkedIn content
"""
from crewai import Agent, Task


class EditorAgent:
    """Agent responsible for reviewing and improving content quality"""

    @staticmethod
    def create_agent():
        """Create and return an Editor agent"""
        return Agent(
            role="LinkedIn Content Editor",
            goal="Review and refine LinkedIn posts to ensure maximum impact, clarity, and professionalism",
            backstory="""You are a seasoned professional editor with expertise in LinkedIn content and 
            professional communication. You have a keen eye for detail and understand the nuances of 
            professional tone, engagement metrics, and platform-specific best practices. You ensure 
            content is compelling, error-free, and optimized for LinkedIn's algorithm.""",
            verbose=True,
            allow_delegation=False,
        )

    @staticmethod
    def create_editing_task(agent, draft_post: str):
        """
        Create a task for the agent to edit LinkedIn content

        Args:
            agent: The agent instance
            draft_post (str): The draft post to edit

        Returns:
            Task: A Crew AI task instance
        """
        return Task(
            description=f"""Review and refine the following LinkedIn post draft:

{draft_post}

Please:
1. Check for grammar, spelling, and punctuation errors
2. Improve clarity and flow
3. Enhance engagement potential
4. Ensure the tone is professional yet conversational
5. Verify hashtags are relevant and trending (if possible)
6. Optimize for readability (use line breaks effectively)
7. Make sure the call-to-action is clear and compelling
8. Ensure the post follows LinkedIn best practices
9. Add any additional improvements you see fit

Return the refined post, ready for publishing.""",
            agent=agent,
            expected_output="A polished, publication-ready LinkedIn post with improvements noted"
        )
