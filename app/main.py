import streamlit as st
from client import Priya
from components.initialize_services import initialize_services
from components.include import include


avatar_img = "https://raw.githubusercontent.com/manasvitickoo/ask_divya_img/main/ask_divya.png"
st.set_page_config(page_title="Ask Priya - US Immigration AI Helper", page_icon=avatar_img)

include(home=True)

with open( "app/style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

query_engine = initialize_services()

client = Priya(query_engine)

def ask_and_respond(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    response = client.make_query(st.session_state.messages[-1]["content"])
    with st.chat_message("assistant", avatar=avatar_img):
        st.markdown(response)
    st.session_state.messages.append(
        {"role": "assistant", "content": response})

### Initial message ###
start_message = st.chat_message("assistant", avatar=avatar_img)
start_message.write("Hello there, what questions about US immigration can I help you with today?")
start_message.write("Examples of questions I can answer:")
examples = [
    "What is USCIS?",
    "How do I check my case status?",
    "¿Puedo obtener una visa de opción STEM si voy a una universidad estadounidense?",
]
example_buttons = [start_message.button(example) for example in examples]
#######################

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=(avatar_img if message["role"] == "assistant" else None)):
        st.markdown(message["content"])

chat_input_box = st.chat_input("What would you like to ask about?")

for example, example_button in zip(examples, example_buttons):
    if example_button:
        ask_and_respond(example)

if chat_input_box:
    ask_and_respond(chat_input_box)