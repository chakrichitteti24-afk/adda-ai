import logging
from app.services.rag.vector_store import vector_store_service

logger = logging.getLogger(__name__)

class RetrieverService:
    def retrieve(self, persona: str, query: str, k: int = 3) -> str:
        try:
            vector_store = vector_store_service.get_collection(persona)
            docs = vector_store.similarity_search(query, k=k)
            if not docs:
                logger.info(f"No relevant documents found for {persona} query: {query}")
                return ""
            
            logger.info(f"Retrieved {len(docs)} chunks for {persona}")
            context = "\n\n".join([d.page_content for d in docs])
            return context
        except Exception as e:
            logger.error(f"Retrieval error for {persona}: {e}")
            return ""

retriever_service = RetrieverService()
