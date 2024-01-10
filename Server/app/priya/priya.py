import google.auth
from llama_index import ServiceContext, VectorStoreIndex
from llama_index.query_engine import CitationQueryEngine
from .palm_multi import PaLMMultiEmbeddings
from llama_index.llms.vertex import Vertex
from llama_index.vector_stores import PGVectorStore
from vertexai.language_models import InputOutputTextPair
from llama_index.prompts import PromptTemplate
import json
from os import environ


def language_mod_template(language: str):
    return PromptTemplate(
        "Please provide an answer only in the language "
        + language
        + " based solely on the provided sources. "
        "When referencing information from a source, "
        "cite the appropriate source(s) using their corresponding numbers. "
        "Every answer should include at least one source citation. "
        "Only cite a source when you are explicitly referencing it. "
        "If none of the sources are helpful, you should indicate that. "
        "For example:\n"
        "Source 1:\n"
        "The sky is red in the evening and blue in the morning.\n"
        "Source 2:\n"
        "Water is wet when the sky is red.\n"
        "Query: When is water wet?\n"
        "Answer: Water will be wet when the sky is red [2], "
        "which occurs in the evening [1].\n"
        "Now it's your turn. Below are several numbered sources of information:"
        "\n------\n"
        "{context_str}"
        "\n------\n"
        "Query: {query_str}\n"
        "Answer: "
    )


def language_mod_refine_template(language: str):
    return PromptTemplate(
        "Please provide an answer only in the language "
        + language
        + " based solely on the provided sources. "
        "When referencing information from a source, "
        "cite the appropriate source(s) using their corresponding numbers. "
        "Every answer should include at least one source citation. "
        "Only cite a source when you are explicitly referencing it. "
        "If none of the sources are helpful, you should indicate that. "
        "For example:\n"
        "Source 1:\n"
        "The sky is red in the evening and blue in the morning.\n"
        "Source 2:\n"
        "Water is wet when the sky is red.\n"
        "Query: When is water wet?\n"
        "Answer: Water will be wet when the sky is red [2], "
        "which occurs in the evening [1].\n"
        "Now it's your turn. "
        "We have provided an existing answer: {existing_answer}"
        "Below are several numbered sources of information. "
        "Use them to refine the existing answer. "
        "If the provided sources are not helpful, you will repeat the existing answer."
        "\nBegin refining!"
        "\n------\n"
        "{context_msg}"
        "\n------\n"
        "Query: {query_str}\n"
        "Answer: "
    )


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
        context=(
            "You are an expert in US immigration who understands multiple languages. "
            "You need to respond to whatever prompt is given to you by labeling the prompt "
            "language, converting the prompt into standard American English, and responding "
            "with a JSON formatted as: {\"language\": <language>, \"cleaned prompt\":<cleaned prompt>}"
        ),
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
        response = cleaner_model.send_message(prompt, **parameters)
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
        print(self._query_engine.get_prompts())
        self._prompt_cleaner = prompt_cleaner(llm)

    def query(self, prompt: str):
        cleaned = self._prompt_cleaner(prompt)
        language = cleaned["language"]
        self._query_engine.update_prompts(
            {
                "response_synthesizer:text_qa_template": language_mod_template(
                    language
                ),
                "response_synthesizer:refine_template": language_mod_refine_template(
                    language
                ),
            }
        )
        print(self._query_engine.get_prompts())
        response = self._query_engine.query(cleaned["cleaned prompt"])
        sources = []
        for source in response.source_nodes:
            sources.append(
                {
                    "text": source.node.get_text(),
                    "page": source.metadata["page"],
                    "link": source.metadata["link"],
                }
            )
        return {
            "response": response.response.strip(),
            "sources": sources,
            "cleanup": cleaned,
        }
