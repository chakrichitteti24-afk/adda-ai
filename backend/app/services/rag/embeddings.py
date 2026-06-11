from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
import logging
import os

logger = logging.getLogger(__name__)

class EmbeddingsService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._embeddings = None

    def get_embeddings(self) -> HuggingFaceInferenceAPIEmbeddings:
        if self._embeddings is None:
            logger.info(f"Initializing API-based HuggingFaceInferenceAPIEmbeddings with model: {self.model_name}")
            hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN") or ""
            self._embeddings = HuggingFaceInferenceAPIEmbeddings(
                api_key=hf_token,
                model_name=f"sentence-transformers/{self.model_name}"
            )
        return self._embeddings

embeddings_service = EmbeddingsService()
