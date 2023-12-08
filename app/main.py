import streamlit as st
from client import Priya
from components.initialize_services import initialize_services
from include import include


avatar_img = "https://raw.githubusercontent.com/manasvitickoo/ask_divya_img/main/ask_divya.png"
st.set_page_config(page_title="Ask Priya - US Immigration AI Helper", page_icon=avatar_img)

include(home=True)

with open( "app/style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

query_engine = initialize_services()

### Initial message ###
with st.chat_message("assistant", avatar=avatar_img):
    st.write("Hello there, what questions about US immigration can I help you with today?")
    st.write("Examples of questions I can answer:")
#######################

client = Priya(query_engine)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=(avatar_img if message["role"] == "assistant" else None)):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to ask about?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    response = client.make_query(st.session_state.messages[-1]["content"])
    with st.chat_message("assistant", avatar=avatar_img):
        st.markdown(response)
    st.session_state.messages.append(
        {"role": "assistant", "content": response})