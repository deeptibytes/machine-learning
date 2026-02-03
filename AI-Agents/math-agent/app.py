import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler
from dotenv import load_dotenv
import os

## Load environment variable
load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")

## Set up the Stramlit app
st.set_page_config(page_title="Text To Math Problem Solver And Data Serach Assistant",page_icon="🧮")
st.title("Text To Math Problem Solver Uing Google Gemma 2")


llm=ChatGroq(model="llama-3.1-8b-instant",groq_api_key=groq_api_key)


## Initializing the tools

# Initializing wikipedia  tool
wikipedia_wrapper=WikipediaAPIWrapper()
wikipedia_tool=Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="Use ONLY to look up factual definitions or concepts."

)

## Initializa the Math tool

def calculator_tool(expression: str):
    return eval(expression)

# math_chain=LLMMathChain.from_llm(llm=llm)
# calculator=Tool(
#     name="Calculator",
#     func=math_chain.run,
#     description="A tools for answering math related questions. Use ONLY for arithmetic calculations like addition, subtraction, multiplication, division."
# )

calculator = Tool(
    name="Calculator",
    func=calculator_tool,
    description="Use ONLY for pure arithmetic expressions. "
        "Input must contain numbers and operators only. "
        "NO words, NO units, NO explanations. "
        "Example: 3+4+12+50"
)

# Create prompt
prompt="""
Your a agent tasked for solving users mathemtical question. Logically arrive at the solution and provide a detailed explanation
and display it point wise for the question below
Question:{question}
Answer:
"""

prompt_template=PromptTemplate(
    input_variables=["question"],
    template=prompt
)

## Combine all the tools into chain to initializa the Reasoning tool
chain=LLMChain(llm=llm,prompt=prompt_template)

reasoning_tool=Tool(
    name="Reasoning tool",
    func=chain.run,
    description="A tool for answering logic-based and reasoning questions."
)

## initialize the agent with all 3 tools

assistant_agent=initialize_agent(
    tools=[wikipedia_tool,calculator,reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    max_iterations=10,
    verbose=True,
    handle_parsing_errors=True
)

if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"assistant","content":"Hi, I'm a Math chatbot who can answer all your maths questions"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

## Lets start the interaction
question=st.text_area("Enter youe question:","I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries. Each pack of blueberries contains 25 berries. How many total pieces of fruit do I have at the end?")

if st.button("find my answer"):
    if question:
        with st.spinner("Generate response.."):
            st.session_state.messages.append({"role":"user","content":question})
            st.chat_message("user").write(question)

            st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response=assistant_agent.run(st.session_state.messages,callbacks=[st_cb]
                                         )
            st.session_state.messages.append({'role':'assistant',"content":response})
            st.write('### Response:')
            st.success(response)

    else:
        st.warning("Please enter the question")









