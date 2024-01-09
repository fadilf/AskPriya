import google.auth
from llama_index import ServiceContext, VectorStoreIndex
from llama_index.query_engine import CitationQueryEngine
from .palm_multi import PaLMMultiEmbeddings
from llama_index.llms.vertex import Vertex
from llama_index.vector_stores import PGVectorStore
from vertexai.language_models import InputOutputTextPair
import json
from dotenv import load_dotenv

from os import environ

# load_dotenv()
def prompt_cleaner(llm: Vertex):
    chat_model = llm._chat_client
    parameters = {
        "temperature": 0,
        "max_output_tokens": 256,
        "top_p": 0.95,
        "top_k": 1,
    }

    cleaner_model = chat_model.start_chat(
        context="You are an expert in US immigration who understands multiple languages. You need to respond to whatever prompt is given to you by labeling the prompt language, converting the prompt into standard American English, and responding with a JSON formatted as: {\"language\": <language>, \"cleaned prompt\":<cleaned prompt>}",
        examples=[
            InputOutputTextPair(
                input_text="What is USCIS?",
                output_text='{"language": "English", "cleaned prompt": "What is USCIS?"}',
            ),
            InputOutputTextPair(
                input_text="Hw do i renew my f1 visa?",
                output_text='{"language": "English", "cleaned prompt": "How do I renew my F-1 Visa?"}',
            ),
            InputOutputTextPair(
                input_text="¿Puedo obtener una visa de opción STEM si voy a una universidad estadounidense?",
                output_text='{"language": "Spanish", "cleaned prompt": "Can I get a STEM OPT visa if I attend a U.S. university?"}',
            ),
        ],
    )
    def cleaner(prompt: str) -> dict[str, str]:
        response = cleaner_model.send_message(
            prompt, **parameters
        )
        return json.loads(response.text)
    return cleaner


class Priya:
    def __init__(self) -> None:
        credentials, project_id = google.auth.default()
        llm = Vertex(model="chat-bison", temperature=0, additional_kwargs={})
        db_user = "postgres"
        db_password = environ["DB_PASSWORD"]
        db_name = "askpriyadb4"
        db_host = environ["DB_HOST"]
        db_port = 5432
        vector_store = PGVectorStore.from_params(
            database=db_name,
            host=db_host,
            password=db_password,
            port=db_port,
            user=db_user,
            table_name="uscis",
            embed_dim=768,
        )
        embed_model = PaLMMultiEmbeddings()
        service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm)
        vector_index = VectorStoreIndex.from_vector_store(vector_store=vector_store, service_context=service_context)
        query_engine = CitationQueryEngine.from_args(
            vector_index,
            similarity_top_k=3,
            citation_chunk_size=512,
        )
        self._query_engine = query_engine
        self._prompt_cleaner = prompt_cleaner(llm)
    
    def query(self, prompt: str):
        cleaned = self._prompt_cleaner(prompt)
        response = self._query_engine.query(cleaned["cleaned prompt"])
        sources = []
        for source in response.source_nodes:
            sources.append({
                "text": source.node.get_text(),
                "page": source.metadata["page"],
                "link": source.metadata["link"]
            })
        return {
            "response": response.response.strip(),
            "sources": sources,
            "cleanup": cleaned
        }