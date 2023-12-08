import streamlit as st
from st_pages import add_page_title
from components.include import include

include()

with open("./README.md") as f:
    readme_contents = f.read()

st.markdown(readme_contents)