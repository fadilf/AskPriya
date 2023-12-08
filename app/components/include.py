import streamlit as st
from st_pages import add_page_title, show_pages_from_config

def include(home=False):
    if home:
        show_pages_from_config()
    # else:
    add_page_title()

    with open( "app/style.css" ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

    with st.sidebar:
        st.expander("ℹ️ Disclaimer").caption(
                "For official immigration advice please consult a certified lawyer."
            )
        st.link_button("View on GitHub", "https://github.com/fadilf/AskPriya")