import os
import streamlit as st
import google.auth
from llama_index import StorageContext, load_index_from_storage
from .g_key import write_file

@st.cache_resource
def initialize_services():
    # Authenticate with Google Cloud
    write_file()
    key_path = st.secrets["JSON_PATH"]
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
    credentials, project_id = google.auth.default()

    # Authenticate with OpenAI
    os.environ["OPENAI_API_KEY"] = st.secrets["OPEN_AI_API_KEY"]

    # Load the vector index
    storage_context = StorageContext.from_defaults(
        persist_dir="ask_priya_index")
    vector_index = load_index_from_storage(storage_context)
    query_engine = vector_index.as_query_engine()

    return query_engine
