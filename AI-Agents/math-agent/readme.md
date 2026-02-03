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

## Session State Management
```python
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a Math chatbot who can answer all your maths questions"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])
```

- Initializes chat history with a welcome message
- Maintains conversation state across Streamlit reruns
- Displays all previous messages in the chat interface

## User Interaction Flow
```python
question = st.text_area("Enter youe question:", "I have 5 bananas and 7 grapes...")

if st.button("find my answer"):
    if question:
        with st.spinner("Generate response.."):
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": question})
            st.chat_message("user").write(question)

            # Create callback handler for real-time updates
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)

            # Run agent with callbacks
            response = assistant_agent.run(st.session_state.messages, callbacks=[st_cb])

            # Add assistant response to history
            st.session_state.messages.append({'role': 'assistant', "content": response})

            # Display response
            st.write('### Response:')
            st.success(response)
    else:
        st.warning("Please enter the question")
```

- Uses text area for multi-line math problems
- Includes a sample question about fruit counting
- Shows spinner during processing
- Uses StreamlitCallbackHandler to display intermediate reasoning steps
- Updates chat history and displays final answer


## Example Usage

**Input Question:**
"I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries. Each pack of blueberries contains 25 berries. How many total pieces of fruit do I have at the end?"

**Agent Process:**
1. **Reasoning Tool**: Breaks down the word problem into steps
2. **Calculator Tool**: Performs arithmetic: `5-2+7-3+12+2*25`
3. **Final Answer**: Provides step-by-step explanation with total count

## File Structure
```
math-agent/
├── app.py          # Main Streamlit application
├── readme.md       # This file
└── .env           # API keys (not committed)
```

## Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | API key for Groq service |

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

## Troubleshooting

### "Tool execution failed" Error
- Check that all tools are properly initialized
- Verify API key is valid
- Ensure internet connection for Wikipedia lookups

### Agent gets stuck in loops
- The `max_iterations=10` prevents infinite loops
- If agent seems stuck, try rephrasing the question
- Check verbose output for debugging

### Calculator tool errors
- Ensure input contains only numbers and operators
- No words, units, or explanations in calculator input
- Use the reasoning tool for complex calculations

### Memory issues
- Large conversation histories may consume memory
- Consider clearing session state periodically
- The app maintains chat history across interactions

## Performance Notes
- **Response Time**: 10-30 seconds depending on problem complexity
- **Tool Usage**: Agent automatically selects appropriate tools
- **Iteration Limit**: Maximum 10 reasoning steps to prevent runaway execution
- **Verbose Mode**: Shows intermediate thoughts for educational purposes

## Customization Options

### Add New Tools
```python
from langchain_community.tools import YourTool

new_tool = Tool(
    name="New Tool",
    func=your_function,
    description="Description for tool selection"
)

# Add to tools list
tools = [wikipedia_tool, calculator, reasoning_tool, new_tool]
```

### Change Agent Type
```python
from langchain.agents import AgentType

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,  # Different agent type
    # ... other parameters
)
```

### Modify Reasoning Prompt
```python
custom_prompt = """
Custom instructions for the reasoning tool...
Question: {question}
Answer:
"""
```

## Security Considerations
- Uses `eval()` in calculator tool - ensure input validation in production
- API keys stored in environment variables (not hardcoded)
- No direct user input execution beyond controlled tools

## Future Enhancements
- Add more specialized math tools (algebra, calculus, geometry)
- Integrate with Wolfram Alpha for advanced computations
- Add visualization capabilities for math problems
- Support for multi-language math problems
- Export conversation history
- Batch processing of multiple problems

---

**Last Updated**: February 2, 2026
