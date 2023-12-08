
class MakeResponse:
    def __init__(self, llm, query_engine):
        self.llm = llm
        self.query_engine = query_engine

    def final_answer(self, query):
        complete_response = self.query_engine.query(query)
        llm_response = complete_response.response
        try:
            links = [f"[{complete_response.source_nodes[i].metadata['page']}]({complete_response.source_nodes[i].metadata['link']})"
                     for i in range(len(complete_response.source_nodes))]
        except:
            pass
        if links:
            llm_response += "\n\nSources: " + ', '.join(links)
        return llm_response
