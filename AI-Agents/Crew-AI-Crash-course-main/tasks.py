from crewai import Task
from tools import yt_tool
from agents import blog_researcher,blog_writer

## Research Task

research_task = Task(
    description=(
        "Search the YouTube channel @krishnaik06 for videos about {topic}. "
        "Use the YouTube search tool to find relevant video transcripts "
        "and extract useful insights."
    ),
    expected_output=(
        "A comprehensive 3 paragraph report summarizing the key concepts "
        "from the videos about {topic}."
    ),
    tools=[yt_tool],
    agent=blog_researcher,
)

# Writing task with language model configuration
write_task = Task(
  description=(
    "get the info from the youtube channel on the topic {topic}."
  ),
  expected_output='Summarize the info from the youtube channel video on the topic{topic} and create the content for the blog',
  tools=[yt_tool],
  agent=blog_writer,
  async_execution=False,
  output_file='new-blog-post.md'  # Example of output customization
)
