from trulens_eval import TruLlama, FeedbackMode, Feedback, Tru
from trulens_eval.feedback import Groundedness
from trulens_eval import OpenAI as fOpenAI
import numpy as np


class DevLens:
    def __init__(self, query_engine, user_query, response):
        self.query_engine = query_engine
        self.user_query = user_query
        self.response = response
        self.provider = fOpenAI()
        self.context_selection = TruLlama.select_source_nodes().node.text

    def return_answer_relevance(self):
        f_qa_relevance = Feedback(
            self.provider.relevance_with_cot_reasons,
            name="Answer Relevance"
        ).on_input_output()
        return f_qa_relevance(self.user_query, self.response)

    def return_groundedness(self):
        grounded = Groundedness(groundedness_provider=self.provider)
        f_groundedness = (
            Feedback(grounded.groundedness_measure_with_cot_reasons,
                     name="Groundedness"
                     )
            .on(self.context_selection)
            .on_output()
            .aggregate(grounded.grounded_statements_aggregator)
        )
        return f_groundedness(self.user_query, self.response)

    def return_context_relevance(self):
        f_qs_relevance = (
            Feedback(self.provider.qs_relevance_with_cot_reasons,
                     name="Context Relevance")
            .on_input()
            .on(self.context_selection)
            .aggregate(np.mean)
        )
        return f_qs_relevance(self.user_query, self.response)

    def return_rag_triad(self):
        qa_relevance_score = self.return_answer_relevance()
        groundedness_score = self.return_groundedness()
        qs_relevance_score = self.return_context_relevance()

        return {
            "Answer Relevance Score": qa_relevance_score,
            "Context Relevance Score": qs_relevance_score,
            "Groundedness Score": groundedness_score
        }
