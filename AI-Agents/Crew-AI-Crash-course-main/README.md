# Crew AI - YouTube Video Content to Blog Post Generator

## Project Overview
This is a **Crew AI** project that automates the process of extracting information from YouTube videos and generating blog posts. It uses a multi-agent system where:
- **Blog Researcher Agent**: Searches YouTube channels, retrieves video transcriptions, and compiles information
- **Blog Writer Agent**: Takes the research and writes engaging blog content

The project demonstrates Crew AI's ability to orchestrate multiple AI agents working together to accomplish complex tasks.

## What is Crew AI?

**Crew AI** is a framework for building autonomous agent teams that can collaborate on complex tasks. Key concepts:

- **Agents**: AI entities with specific roles, goals, and tools
- **Tasks**: Work items assigned to agents with clear descriptions and expected outputs
- **Tools**: External functions/APIs that agents use to gather information
- **Crew**: The team orchestrator that manages agent collaboration and task execution
- **Process**: How tasks are executed (sequential, hierarchical, etc.)

Think of Crew AI as building a small team where:
- Each agent has a specific expertise and responsibility
- Agents have access to tools (like YouTube search)
- Tasks are distributed among agents
- The crew manages how these agents work together

## Project Architecture

### File Structure
```
Crew-AI-Crash-course-main/
├── agents.py          # Define AI agents with roles and goals
├── tasks.py           # Define tasks for agents to complete
├── tools.py           # Define tools agents can use
├── crew.py            # Orchestrate agents and tasks into a crew
├── requirements.txt   # Project dependencies
├── README.md          # Original project README
└── LICENSE            # Project license
```

## Step-by-Step Code Explanation

### 1. **Tools (tools.py)**
```python
from crewai_tools import YoutubeChannelSearchTool

yt_tool = YoutubeChannelSearchTool(youtube_channel_handle='@krishnaik06')
```

- **What it does**: Creates a YouTube search tool that targets a specific channel (@krishnaik06)
- **Purpose**: Allows agents to search and retrieve video information from this channel
- **Usage**: This tool is passed to agents so they can query YouTube data

### 2. **Agents (agents.py)**

#### Blog Researcher Agent
```python
blog_researcher = Agent(
    role='Blog Researcher from Youtube Videos',
    goal='get the relevant video transcription for the topic {topic} from the provided Yt channel',
    verbose=True,
    memory=True,
    backstory=(
       "Expert in understanding videos in AI Data Science, Machine Learning And GEN AI and providing suggestion" 
    ),
    tools=[yt_tool],
    allow_delegation=True
)
```

**Agent Properties:**
- **role**: Defines what the agent does (researcher, writer, etc.)
- **goal**: The objective the agent is trying to achieve (can use `{topic}` placeholder)
- **verbose**: Print detailed logs of agent's reasoning and actions
- **memory**: Enable agent to remember previous interactions (context awareness)
- **backstory**: Agent's "personality" and expertise context
- **tools**: List of tools the agent can access
- **allow_delegation**: Can the agent delegate tasks to other agents? (True for researcher, False for writer)

#### Blog Writer Agent
```python
blog_writer = Agent(
    role='Blog Writer',
    goal='Narrate compelling tech stories about the video {topic} from YT video',
    verbose=True,
    memory=True,
    backstory=(
        "With a flair for simplifying complex topics, you craft "
        "engaging narratives that captivate and educate, bringing new "
        "discoveries to light in an accessible manner."
    ),
    tools=[yt_tool],
    allow_delegation=False
)
```

**Key difference**: 
- Writer has `allow_delegation=False` (works independently, doesn't delegate to others)
- Writer uses the same YouTube tool to access video information

### 3. **Tasks (tasks.py)**

#### Research Task
```python
research_task = Task(
    description=(
        "Identify the video {topic}. "
        "Get detailed information about the video from the channel video."
    ),
    expected_output='A comprehensive 3 paragraphs long report based on the {topic} of video content.',
    tools=[yt_tool],
    agent=blog_researcher,
)
```

**Task Properties:**
- **description**: Clear instructions for what needs to be done
- **expected_output**: What the agent should deliver (helps guide the agent)
- **tools**: Tools available for this specific task
- **agent**: Which agent is responsible for this task

#### Writing Task
```python
write_task = Task(
    description=(
        "get the info from the youtube channel on the topic {topic}."
    ),
    expected_output='Summarize the info from the youtube channel video on the topic {topic} and create the content for the blog',
    tools=[yt_tool],
    agent=blog_writer,
    async_execution=False,
    output_file='new-blog-post.md'  # Save output to file
)
```

**Additional Properties:**
- **async_execution**: Whether this task can run in parallel (False = sequential)
- **output_file**: Save the task output to a markdown file

### 4. **Crew Orchestration (crew.py)**

```python
from crewai import Crew, Process
from agents import blog_researcher, blog_writer
from tasks import research_task, write_task

crew = Crew(
    agents=[blog_researcher, blog_writer],
    tasks=[research_task, write_task],
    process=Process.sequential,  # Tasks execute one after another
    memory=True,                  # Crew remembers all interactions
    cache=True,                   # Cache results for efficiency
    max_rpm=100,                  # Rate limiting (requests per minute)
    share_crew=True               # Share context between agents
)

result = crew.kickoff(inputs={'topic': 'AI VS ML VS DL vs Data Science'})
print(result)
```

**Crew Configuration:**
- **agents**: List of agents in the crew
- **tasks**: List of tasks to execute
- **process**: Task execution strategy
  - `Process.sequential`: Tasks run one after another
  - `Process.hierarchical`: One agent supervises others
- **memory**: Enable crew-wide memory for context sharing
- **cache**: Cache tool responses to avoid repeated API calls
- **max_rpm**: Rate limit to avoid overwhelming APIs
- **share_crew**: Share information between agents

**Execution Flow:**
1. `crew.kickoff()` starts task execution
2. Blog Researcher searches YouTube for "AI VS ML VS DL vs Data Science"
3. Researcher compiles a 3-paragraph report
4. Blog Writer takes that report and creates engaging blog content
5. Output is saved to `new-blog-post.md`

## How It Works - Execution Flow

```
User Input: {'topic': 'AI VS ML VS DL vs Data Science'}
    ↓
Crew Kickoff
    ↓
Research Task (Sequential #1)
    ├─ Agent: blog_researcher
    ├─ Tool: yt_tool searches @krishnaik06 channel
    ├─ Output: 3-paragraph report on the topic
    └─ Saved in memory for next task
    ↓
Writing Task (Sequential #2)
    ├─ Agent: blog_writer
    ├─ Tool: yt_tool (if needed for additional context)
    ├─ Input: Research report from previous task
    ├─ Process: Creates engaging blog narrative
    └─ Output: Saves to 'new-blog-post.md'
    ↓
Final Result
```

## Key Concepts

### Agent Collaboration
- **Memory Sharing**: With `memory=True` in agents and crew, context flows between tasks
- **Task Sequencing**: Tasks are executed in order; later tasks can use outputs from earlier ones
- **Delegation**: Blog Researcher can delegate (ask for help), Writer cannot
- **Tool Access**: Both agents have access to YouTube tool

### Prompting & Directing
- **Backstories** give agents personality and context
- **Goals** with placeholders like `{topic}` get filled in at runtime
- **Expected Outputs** guide agents toward specific formats/lengths
- **Descriptions** provide clear instructions

### Efficiency Features
- **Caching**: Avoid re-running the same tool calls
- **Rate Limiting**: Respect API rate limits
- **Async Execution**: Support parallel task execution (if configured)

## How to Run

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install crewai crewai_tools python-dotenv langchain-huggingface openai
```

### Step 2: Set Up Environment Variables
Create a `.env` file in the project directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

Get your OpenAI API key from: https://platform.openai.com/api-keys

**Note**: The project uses `gpt-4-0125-preview` as the LLM model (specified in `agents.py`)

### Step 3: (Optional) Modify the Topic
Edit `crew.py` to change the topic:
```python
result = crew.kickoff(inputs={'topic': 'Your custom topic here'})
```

### Step 4: Run the Crew
```bash
cd /Users/deepti/Documents/my_ai_projects/Crew-AI-Crash-course-main
python crew.py
```

### Step 5: Check the Output
- Console will print the final result
- Blog post will be saved to `new-blog-post.md` in the same directory

## Configuration Options

### Change YouTube Channel
Edit `tools.py`:
```python
yt_tool = YoutubeChannelSearchTool(youtube_channel_handle='@your_channel_name')
```

### Change Task Execution Order
Edit `crew.py`:
```python
# Hierarchical: One agent supervises others
process=Process.hierarchical,

# Sequential: Default, one after another
process=Process.sequential,
```

### Disable Caching
```python
crew = Crew(
    ...
    cache=False,  # Don't cache results
    ...
)
```

### Change Model
Edit `agents.py`:
```python
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"  # or other models
```

## Troubleshooting

### "API key not found" Error
- Ensure `.env` file exists in the project directory
- Check that `OPENAI_API_KEY` is set correctly
- No extra spaces or quotes around the key

### "YouTube tool failed" Error
- Verify the YouTube channel handle is correct (should start with @)
- Check internet connection
- The channel may have restrictions on API access

### "No output file created"
- Check that the `write_task` has `output_file='new-blog-post.md'`
- Verify write permissions in the project directory
- Check console output for errors during task execution

### Slow Execution
- First run caches results (future runs are faster)
- With `cache=True`, repeated topics reuse previous results
- Large API responses may take time; wait for completion

## Understanding the Output

The generated `new-blog-post.md` will contain:
- Blog title (derived from topic)
- Introduction paragraph (context about the topic)
- Main content (synthesized from multiple videos/sources)
- Conclusion (summary and insights)
- All in Markdown format for easy publishing

## Advanced Features & Ideas

### Add More Agents
```python
# Create a fact-checker agent
fact_checker = Agent(
    role='Fact Checker',
    goal='Verify facts in the blog post',
    backstory='...',
    tools=[search_tool],
)

# Add to crew
crew = Crew(
    agents=[blog_researcher, blog_writer, fact_checker],
    tasks=[research_task, write_task, fact_check_task],
)
```

### Add More Tools
```python
from crewai_tools import WebsiteSearchTool, FileReadTool

tools = [yt_tool, WebsiteSearchTool(), FileReadTool()]
```

### Custom Tool Creation
```python
from crewai_tools import tool

@tool
def my_custom_tool(input: str) -> str:
    """Description of what the tool does"""
    # Implementation here
    return result
```

### Monitor Agent Activity
```python
crew = Crew(
    ...
    verbose=True,  # Enable detailed logs
    ...
)
```

## Dependencies Explained

| Package | Purpose |
|---------|---------|
| `crewai` | Core Crew AI framework |
| `crewai_tools` | Pre-built tools (YouTube, web search, etc.) |
| `python-dotenv` | Load environment variables from `.env` |
| `langchain-huggingface` | HuggingFace integrations with LangChain |
| `openai` | OpenAI API client (implicit dependency) |

## Security Notes
- Never commit `.env` file to git
- Add `.env` to `.gitignore`
- Use environment variables for all sensitive keys
- Keep API keys private and rotate regularly

## Use Cases for Crew AI
- **Content Generation**: Automate blog/article creation from research
- **Data Analysis**: Multiple agents analyzing different aspects
- **Customer Support**: Team of specialized support bots
- **Research**: Automated literature review and synthesis
- **Product Development**: Cross-functional agent teams

## Next Steps
- Customize the backstories for your use case
- Modify task descriptions for different topics
- Add more agents for specialized roles (editor, SEO optimizer, etc.)
- Integrate with publishing platforms to auto-publish blog posts
- Build a web UI to make it accessible

---

**Last Updated**: March 10, 2026