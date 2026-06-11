import os
import logging
from langchain_community.vectorstores import Chroma
from app.services.rag.embeddings import embeddings_service
from app.core.config import settings

logger = logging.getLogger(__name__)

class VectorStoreService:
    def __init__(self):
        # We can use the configured path, or default to a sibling directory
        self.persist_directory = getattr(settings, 'CHROMA_DB_DIR', "./chroma_db")
        self._collections = {}

    def get_collection(self, collection_name: str) -> Chroma:
        if collection_name not in self._collections:
            logger.info(f"Loading Chroma vector store for collection: {collection_name}")
            self._collections[collection_name] = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=embeddings_service.get_embeddings(),
                collection_name=collection_name
            )
        return self._collections[collection_name]

    def is_empty(self, personas: list[str]) -> bool:
        if not os.path.exists(self.persist_directory):
            return True
        for p in personas:
            try:
                col = self.get_collection(p)
                # Ensure the collection has data
                if col._collection.count() == 0:
                    return True
            except Exception as e:
                logger.warning(f"Error checking collection {p}: {e}")
                return True
        return False

vector_store_service = VectorStoreService()
