from langchain_community.embeddings import HuggingFaceEmbeddings
import logging

logger = logging.getLogger(__name__)

class EmbeddingsService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._embeddings = None

    def get_embeddings(self) -> HuggingFaceEmbeddings:
        if self._embeddings is None:
            logger.info(f"Initializing HuggingFaceEmbeddings with model: {self.model_name}")
            self._embeddings = HuggingFaceEmbeddings(model_name=self.model_name)
        return self._embeddings

embeddings_service = EmbeddingsService()
