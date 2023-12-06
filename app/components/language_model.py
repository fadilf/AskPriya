import os
import google.auth
import streamlit as st
from llama_index.llms.vertex import Vertex
from llama_index.llms.base import ChatMessage, MessageRole, CompletionResponse


class LanguageModel:
    def __init__(self):
        # Authenticate and initialize the language model
        self._authenticate()
        self.llm = Vertex(model="text-bison", temperature=0,
                          additional_kwargs={})

    def _authenticate(self):
        # Load the JSON key file path from Streamlit secrets
        key_path = st.secrets["JSON_PATH"]

        # Set the environment variable to point to the key file
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

        # Authenticate using the key file
        credentials, project_id = google.auth.default()

    def generate_answer(self, query):
        # Generate a response to the query
        response = self.llm.complete(query).text
        return response
