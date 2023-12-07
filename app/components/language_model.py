from llama_index.llms.vertex import Vertex
from llama_index.llms.base import ChatMessage, MessageRole, CompletionResponse


class LanguageModel:
    def __init__(self):
        # Initialize the language model
        self.llm = Vertex(model="chat-bison", temperature=0,  # change to chat bison later on
                          additional_kwargs={})

    def generate_answer(self, query):
        # Generate a response to the query
        response = self.llm.complete(query).text
        return response
