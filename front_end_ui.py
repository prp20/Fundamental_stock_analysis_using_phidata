import streamlit as st
from utils import apply_styles
from finance_agent import get_agent_team, as_stream
agent = get_agent_team()

st.title("Stock Analyzer Based on Stock Symbols")

if st.button("Start a New Chat"):
    st.session_state.messages = []
    st.rerun()

apply_styles()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chunks = agent.run(prompt, stream=True)
        response = st.write_stream(as_stream(chunks))
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
