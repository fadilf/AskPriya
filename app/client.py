# client.py

from components import LanguageModel, MakeResponse
# QueryProcessor, Embedder, DatabaseRetriever, PromptTemplate


class Priya:
    def __init__(self, query_engine):
        self.query_engine = query_engine
        self.language_model = LanguageModel()
        self.make_response = MakeResponse(
            self.language_model, self.query_engine)

    def make_query(self, query):
        answer = self.make_response.final_answer(query)
        return answer
