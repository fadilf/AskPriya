from typing import Any, List, Optional

from llama_index.bridge.pydantic import PrivateAttr
from llama_index.embeddings.base import BaseEmbedding


class PaLMMultiEmbeddings(BaseEmbedding):
    _model: Any = PrivateAttr()
    _tei: Any = PrivateAttr()

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        try:
            from vertexai.language_models import TextEmbeddingModel
            from vertexai.language_models import TextEmbeddingInput

        except ImportError:
            raise ImportError(
                "vertexai.language_models not found, please install it."
            )
        self._model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
        self._tei = TextEmbeddingInput
        super().__init__(**kwargs)

    @classmethod
    def class_name(cls) -> str:
        return "instructor"

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)

    def _get_query_embedding(self, query: str) -> List[float]:
        embeddings = self._model.get_embeddings([
            self._tei(
                text=query,
                task_type="RETRIEVAL_QUERY"
            )
        ])

        return embeddings[0].values

    def _get_text_embedding(self, text: str) -> List[float]:
        embeddings = self._model.get_embeddings([
            self._tei(
                text=text,
                task_type="RETRIEVAL_DOCUMENT"
            )
        ])

        return embeddings[0].values

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        inputs = [self._tei(text=text,task_type="RETRIEVAL_DOCUMENT") for text in texts]
        embeddings = self._model.get_embeddings(inputs)
        return [embedding.values for embedding in embeddings]