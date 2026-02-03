# Math Problem Solver Agent

## Project Overview
This Streamlit application creates an intelligent math chatbot that can solve mathematical problems, perform calculations, and look up factual information using multiple specialized tools. The agent combines reasoning capabilities with arithmetic computation and knowledge retrieval to provide comprehensive answers to math-related questions.

## Features
- **Multi-Tool Agent**: Uses Wikipedia, Calculator, and Reasoning tools for comprehensive problem solving
- **Interactive Chat Interface**: Maintains conversation history with session state management
- **Real-time Processing**: Shows intermediate reasoning steps with Streamlit callbacks
- **Error Handling**: Robust parsing error handling and user-friendly warnings
- **Groq Integration**: Uses Llama 3.1-8B model for fast, accurate responses
- **Zero-Shot Reasoning**: Can solve problems it hasn't been explicitly trained on

## Step-by-Step Implementation Details

### 1. **Environment Setup and Imports**
```python
import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler
from dotenv import load_dotenv
import os

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
```

- Imports all necessary LangChain components for agent creation
- Loads Groq API key from environment variables
- Sets up Streamlit for the web interface

### 2. **Streamlit App Configuration**
```python
st.set_page_config(page_title="Text To Math Problem Solver And Data Serach Assistant", page_icon="🧮")
st.title("Text To Math Problem Solver Uing Google Gemma 2")
```

- Configures the page title and calculator emoji icon
- Sets the main title (note: title mentions "Google Gemma 2" but actually uses Llama 3.1)

### 3. **LLM Initialization**
```python
llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=groq_api_key)
```

- Initializes the Groq ChatGroq model with Llama 3.1-8B-Instant
- This model provides fast inference for reasoning and calculation tasks

### 4. **Tool 1: Wikipedia Tool**
```python
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="Use ONLY to look up factual definitions or concepts."
)
```

- Creates a Wikipedia wrapper for factual lookups
- Tool description restricts usage to factual information only
- Helps the agent access general knowledge when needed

### 5. **Tool 2: Calculator Tool**
```python
def calculator_tool(expression: str):
    return eval(expression)

calculator = Tool(
    name="Calculator",
    func=calculator_tool,
    description="Use ONLY for pure arithmetic expressions. "
        "Input must contain numbers and operators only. "
        "NO words, NO units, NO explanations. "
        "Example: 3+4+12+50"
)
```

- Defines a simple calculator function using Python's `eval()`
- Tool description emphasizes pure arithmetic only (no text, units, or explanations)
- Provides basic arithmetic capabilities for the agent

### 6. **Tool 3: Reasoning Tool**
```python
prompt = """
Your a agent tasked for solving users mathemtical question. Logically arrive at the solution and provide a detailed explanation
and display it point wise for the question below
Question:{question}
Answer:
"""

prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)

chain = LLMChain(llm=llm, prompt=prompt_template)

reasoning_tool = Tool(
    name="Reasoning tool",
    func=chain.run,
    description="A tool for answering logic-based and reasoning questions."
)
```

- Creates a custom reasoning tool using LLMChain
- Prompt template instructs the model to provide step-by-step solutions
- Tool handles complex reasoning and multi-step problem solving

### 7. **Agent Initialization with ZERO_SHOT_REACT_DESCRIPTION**
```python
assistant_agent = initialize_agent(
    tools=[wikipedia_tool, calculator, reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    max_iterations=10,
    verbose=True,
    handle_parsing_errors=True
)
```

- Initializes the agent with all three tools
- Uses `ZERO_SHOT_REACT_DESCRIPTION` agent type
- Sets maximum 10 iterations to prevent infinite loops
- Enables verbose output and error handling

## What is ZERO_SHOT_REACT_DESCRIPTION

`ZERO_SHOT_REACT_DESCRIPTION` is one of LangChain's agent types that enables **zero-shot reasoning** with tool usage. Here's what it means:

### **Zero-Shot**
- The agent can use tools it hasn't been explicitly trained on
- No fine-tuning required for new tool combinations
- Learns from tool descriptions alone

### **ReAct (Reasoning + Acting)**
- **Reasoning**: The agent thinks step-by-step about what to do
- **Acting**: The agent executes actions using available tools
- **Observation**: The agent observes results and continues reasoning

### **Description-Based**
- Tools are selected based on their natural language descriptions
- The agent reads tool descriptions to decide which tool to use
- No hardcoded tool selection logic required

### **How ZERO_SHOT_REACT_DESCRIPTION Works**
1. **User Input**: Receives a question
2. **Thought Process**: Reasons about what information/tools are needed
3. **Action Selection**: Chooses appropriate tool based on descriptions
4. **Tool Execution**: Calls the selected tool
5. **Observation**: Analyzes tool output
6. **Iteration**: Continues until solution is found or max iterations reached

### **Example Workflow**
```
Question: "What is 25% of 200, and who discovered penicillin?"

Thought: I need to calculate 25% of 200 and find who discovered penicillin.
Action: Calculator
Action Input: 200 * 0.25

Observation: 50.0

Thought: Now I need to find who discovered penicillin.
Action: Wikipedia
Action Input: penicillin discovery

Observation: Penicillin was discovered by Alexander Fleming in 1928.

Thought: I have both answers now.
Final Answer: 25% of 200 is 50, and penicillin was discovered by Alexander Fleming.
```

## Agent Capabilities

### Calculator Tool
- Basic arithmetic operations (+, -, *, /)
- Pure numerical expressions only
- No text or units in input

### Wikipedia Tool
- Factual information lookup
- Definitions and concepts
- General knowledge queries

### Reasoning Tool
- Complex problem solving
- Step-by-step explanations
- Logic-based questions
- Multi-step mathematical reasoning

**Last Updated**: February 2, 2026
