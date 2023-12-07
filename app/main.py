import streamlit as st
from client import Priya
from components.initialize_services import initialize_services

query_engine = initialize_services()

st.title("Ask Priya")

client = Priya(query_engine)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to ask about?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    response = client.make_query(st.session_state.messages[-1]["content"])
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
