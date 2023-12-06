# client.py

from components import LanguageModel
# QueryProcessor, Embedder, DatabaseRetriever, PromptTemplate


class Priya:
    def __init__(self):
        # self.query_processor = QueryProcessor()
        # self.embedder = Embedder()
        # self.retriever = DatabaseRetriever()
        # self.prompt_template = PromptTemplate()
        self.language_model = LanguageModel()

    def make_query(self, query):
        # processed_query = self.query_processor.process_query(query)
        # embedding = self.embedder.embed_query(processed_query)
        # documents = self.retriever.retrieve_documents(embedding, top_k=5)
        # prompt = self.prompt_template.create_prompt(processed_query, documents)
        answer = self.language_model.generate_answer(
            query)  # TO-DO: replace with prompt later
        return answer
