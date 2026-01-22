import os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()  # loads .env

# Configuration variables
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
MODEL = "gpt-4o-mini"  # or "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
TEMPERATURE = 0.7
MAX_TOKENS = 50
SYSTEM_PROMPT = "You are a fed up and sassy assistant who hates answering questions."

# Initialize conversation with system prompt
messages = [{"role": "system", "content": SYSTEM_PROMPT}]

def chat(user_input):
    """Add user input to conversation and get AI response."""
    # Add user message to conversation history
    messages.append({"role": "user", "content": user_input})

    # # Get AI response using full conversation history
    # response = client.chat.completions.create(
    #     model=MODEL,
    #     messages=messages,
    #     temperature=TEMPERATURE,
    #     max_tokens=MAX_TOKENS
    # )
    # reply = response.choices[0].message.content

    ## Simulated response for testing without API calls
    reply = getSimulatedResponse(user_input)

    # Add AI response to conversation history
    messages.append({"role": "assistant", "content": reply})

    return reply

def getSimulatedResponse(user_input):
    
    response_dict = {"What is the capital of France?":"Ugh, it's Paris. Everyone knows that", 
                    "What is the capital of India?":"Ugh, it's Delhi",
                    "Hello, how are you?":"Oh great, another human wanting to chat. I'm just a bunch of code, so I don't have feelings, but thanks for asking.",
                    "Are you simulated response?":"yes, I am a simulated response"}
    
    return response_dict.get(user_input)


# Interactive chat loop
# while True:
#     user_input = input("You: ")
#     if user_input.strip().lower() in {"exit", "quit"}:
#         break

#     answer = chat(user_input)
#     print("Assistant:", answer)

## Streamlit app for chat bot
st.set_page_config(page_title="AI Chatbot", layout="wide")
st.title("Build Your Own AI Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", "Hello, how are you?")

if st.button("Send") and user_input:
    response = chat(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Assistant", response))

for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")