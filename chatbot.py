import streamlit as st
from script import Config
from helpers.llm_helper import chat, stream_parser
from dotenv import load_dotenv

load_dotenv() # loads in environment variables

open_api_key = Config.OPENAI_API_KEY

st.set_page_config(
    page_title="Chatbot",
    initial_sidebar_state="expanded"
)

st.title("my ai chatbot")

# initialize messages if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("# Chat Options")

    model = st.selectbox("What model would you like to use?", ["gpt-3.5-turbo", "gpt-4.0"])

    temperature = st.number_input("Temperature", value=0.7, min_value=0.1, max_value=1.0, step=0.1)

    max_token_length = st.number_input("Max Token Length", value=1000, min_value=100, max_value=1000)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message['content'])
    
if user_prompt := st.chat_input("What questions do you have?"):
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.spinner("Generating response..."):
        llm_response = chat(user_prompt, model=model, 
                            max_tokens=max_token_length, temp=temperature)

        stream_output = st.write_stream(stream_parser(llm_response))

        st.session_state.messages.append({"role": "assistant", 
                                          "content": stream_output})
        
    last_response = st.session_state.messages[len(st.session_state.messages) - 1]['content']

    if str(last_response) != str(stream_output):
        with st.chat_message("assistant"):
            st.markdown(stream_output)

