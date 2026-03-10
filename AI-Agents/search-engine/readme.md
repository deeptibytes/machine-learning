# Search Agent (LangChain + Streamlit)

## Project Overview
This small Streamlit app demonstrates a LangChain agent that can search the web and scholarly articles and answer user queries by combining search tools and an LLM. It uses:
- DuckDuckGo for general web search
- Wikipedia for factual lookups
- arXiv for scholarly article lookups

The app displays the agent's reasoning and actions in real time using `StreamlitCallbackHandler`.

## What the app does (high level)
- Presents a chat UI (Streamlit) where users can type questions.
- Passes the chat history to a LangChain agent configured with three tools (Search, Wikipedia, arXiv).
- The agent reasons (zero-shot), selects a tool when needed, executes it, observes results, and continues until it composes a final answer.
- The Streamlit UI shows the agent's intermediate thoughts and tool outputs (via callbacks) and the final response.

## Files
- `app.py`: Main Streamlit application
- `tools_agents.ipynb`: Notebook with examples (optional)

## Key Components (code walk-through)

### 1) Environment & LLM
```py
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant", streaming=True)
```
- Loads `GROQ_API_KEY` from `.env` and instantiates `ChatGroq` (Groq wrapper).
- `streaming=True` will stream tokens from the model where supported.

### 2) Tools
- `ArxivQueryRun` (wraps `ArxivAPIWrapper`) — used to fetch arXiv search results (scholarly papers). In this app it is initialized with `top_k_results=1` and `doc_content_chars_max=200`.
- `WikipediaQueryRun` (wraps `WikipediaAPIWrapper`) — used for factual lookups; also limited to short content snippets by `doc_content_chars_max`.
- `DuckDuckGoSearchRun` — general web search tool.

They are created as:
```py
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)
arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

search = DuckDuckGoSearchRun(name="Search")
```

These tools provide text results the agent can use as observations.

### 3) Streamlit UI & Session State
- The app uses a chat-style interface using `st.chat_input` and stores messages in `st.session_state["messages"]` so that conversation persists across reruns.
- Messages are rendered using `st.chat_message(role).write(content)`.

### 4) Agent Initialization
```py
search_agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handling_parsing_errors=True,
)
```
- `initialize_agent` wires the LLM and tools together and returns an agent that can decide which tool to call.
- The `AgentType.ZERO_SHOT_REACT_DESCRIPTION` agent uses tool descriptions (natural language) to choose which tool to use and performs ReAct-style reasoning (see below).

### 5) Streaming Callbacks & Execution
- `StreamlitCallbackHandler` is passed as a callback to `agent.run(...)`. It shows the agent's internal steps and tool outputs in the Streamlit chat bubble while the agent is running.
- The final response is appended to `st.session_state.messages` and displayed.

## What is ZERO_SHOT_REACT_DESCRIPTION?
`ZERO_SHOT_REACT_DESCRIPTION` is an agent type provided by LangChain that enables zero-shot tool-using agents based on the ReAct pattern. Briefly:
- Zero-shot: The agent is not specially fine-tuned for the specific tools — it makes tool use decisions based on the tools' natural language descriptions.
- ReAct: "Reason + Act" — the agent alternates between reasoning (thinking) and acting (calling tools). After each action it receives an observation and continues reasoning.
- Description-based: The agent selects tools by reading their descriptions; clear, accurate descriptions help the agent choose the right tool.

This agent type is a good default when you want an agent that can combine LLM reasoning with tool execution without custom training.

## How to run

1. Create a Python virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
# .venv\Scripts\activate  # Windows (PowerShell)
```

2. Install dependencies (adjust versions as needed):
```bash
pip install streamlit langchain langchain-groq langchain-community python-dotenv
# If you plan to run notebook examples:
pip install jupyter
```

3. Create a `.env` file in the `search-engine` folder with your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

4. Run the app:
```bash
cd /Users/deepti/Documents/git/AI-Agents/search-engine
streamlit run app.py
```

5. Use the chat input at the bottom to ask questions (example: "What is the latest on machine learning interpretability?"). The agent will reason and call search / wiki / arXiv as necessary.

## Configuration & Customization
- Increase `top_k_results` when instantiating `ArxivAPIWrapper` or `WikipediaAPIWrapper` to fetch more results.
- Change `doc_content_chars_max` to control how much content is passed from the tools to the agent.
- Switch `AgentType` if you prefer other agent behaviors (e.g., conversational agents).
- Toggle `streaming=True/False` in `ChatGroq` depending on whether you want token streaming.

## Security & Privacy
- API keys should never be committed to source control. Add `.env` to `.gitignore`.
- Tool outputs (web search results) are sent to the LLM — avoid asking for or exposing sensitive user data.

## Troubleshooting
- If the app shows no response: verify `GROQ_API_KEY` is set and valid.
- If a tool returns empty results: check network connectivity and that external services are reachable.
- To debug agent behavior, set `verbose=True` in `initialize_agent` (it will print thoughts/actions).

## Extensions and Ideas
- Add caching for tool results to reduce repeated external calls.
- Integrate a vector store to store and retrieve long-term memory / document context.
- Add more tools (e.g., semantic search, file loaders, PDF readers) to extend capabilities.

---

**Last Updated**: February 21, 2026
