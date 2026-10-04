"""
Content Writer Agent - Creates detailed LinkedIn posts
"""
from crewai import Agent, Task
from crewai_tools import tool


class ContentWriterAgent:
    """Agent responsible for writing detailed LinkedIn content"""

    @staticmethod
    def create_agent():
        """Create and return a Content Writer agent"""
        return Agent(
            role="LinkedIn Content Writer",
            goal="Create engaging, detailed, and professional LinkedIn posts that drive engagement and provide value to the audience",
            backstory="""You are an experienced LinkedIn content strategist with deep knowledge of 
            professional networking best practices. You excel at crafting compelling narratives that 
            resonate with professionals and drive meaningful engagement. You understand how to balance 
            promotional content with valuable insights and actionable information.""",
            verbose=True,
            allow_delegation=False,
        )

    @staticmethod
    def create_writing_task(agent, topic: str):
        """
        Create a task for the agent to write LinkedIn content

        Args:
            agent: The agent instance
            topic (str): The topic for the LinkedIn post

        Returns:
            Task: A Crew AI task instance
        """
        return Task(
            description=f"""Write a detailed and engaging LinkedIn post about the following topic: {topic}

The post should:
1. Start with a compelling hook that captures attention
2. Provide 3-5 key insights or takeaways
3. Include practical tips or actionable advice
4. Be professional yet conversational in tone
5. Include relevant hashtags (3-5 hashtags)
6. End with a call-to-action or thought-provoking question
7. Be between 300-500 words

Format the post in a way that's easy to read on LinkedIn (use line breaks, bullet points where appropriate).""",
            agent=agent,
            expected_output="A complete, well-formatted LinkedIn post ready to be published"
        )
