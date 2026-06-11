import logging
from app.services.rag.ingest import ingestion_service
from app.services.rag.vector_store import vector_store_service
from app.services.rag.retriever import retriever_service

# Setup basic logging if not already configured
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Map UI persona names to DB collections
PERSONA_MAP = {
    "Rabindranath Tagore": "tagore",
    "Satyajit Ray": "ray",
    "Subhas Chandra Bose": "bose"
}

class RAGServiceFacade:
    def initialize(self):
        logger.info("Initializing RAG System...")
        personas = list(PERSONA_MAP.values())
        if vector_store_service.is_empty(personas):
            logger.info("ChromaDB is empty or missing collections. Starting ingestion...")
            ingestion_service.ingest_all()
        else:
            logger.info("ChromaDB already exists with data. Skipping ingestion.")

    def get_context(self, persona_name: str, query: str) -> str:
        collection_name = PERSONA_MAP.get(persona_name)
        if not collection_name:
            return ""
        return retriever_service.retrieve(collection_name, query)
        
    def build_prompt(self, system_prompt: str, context: str) -> str:
        if not context.strip():
            return system_prompt
            
        injected_prompt = f"""{system_prompt}

Below is some additional knowledge retrieved from your personal writings, speeches, or documents. 
Use this context to inform your perspective if it is relevant to the conversation. 
If it is not relevant, rely on your general persona knowledge.
Never mention that you are reading from "retrieved documents" or "context". 
Incorporate the knowledge naturally as if it comes from your own memory.

### Relevant Context ###
{context}
### End Context ###
"""
        return injected_prompt

rag_service = RAGServiceFacade()
