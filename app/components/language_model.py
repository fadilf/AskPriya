from llama_index.llms.vertex import Vertex
from llama_index.llms.base import ChatMessage, MessageRole, CompletionResponse


class LanguageModel:
    def __init__(self):
        # Initialize the language model
        self.llm = Vertex(model="chat-bison", temperature=0,
                          additional_kwargs={})
