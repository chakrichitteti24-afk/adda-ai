import os
import logging
import uuid
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.rag.vector_store import vector_store_service

logger = logging.getLogger(__name__)

# Base directories where PDFs exist
PERSONA_FOLDERS = {
    "tagore": r"d:\tradiction hacks\rag rabindra nath tagore",
    "ray": r"d:\tradiction hacks\rag satyajit ray",
    "bose": r"d:\tradiction hacks\rag  subash chandrabose"
}

class IngestionService:
    def __init__(self):
        self.chunk_size = 1000
        self.chunk_overlap = 200
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len
        )

    def ingest_all(self):
        logger.info("Starting document ingestion pipeline.")
        for persona, path in PERSONA_FOLDERS.items():
            try:
                self._ingest_persona(persona, path)
            except Exception as e:
                logger.error(f"Error ingesting for persona {persona}: {e}")

    def _ingest_persona(self, persona: str, folder_path: str):
        if not os.path.exists(folder_path):
            logger.error(f"Missing folder: {folder_path}")
            return
            
        logger.info(f"Scanning folder for {persona}: {folder_path}")
        try:
            loader = PyPDFDirectoryLoader(folder_path)
            docs = loader.load()
        except Exception as e:
            logger.error(f"Failed to load PDFs from {folder_path}: {e}")
            return

        if not docs:
            logger.warning(f"Empty PDFs or no documents found in {folder_path}")
            return
            
        logger.info(f"Loaded {len(docs)} documents for {persona}. Chunking...")
        chunks = self.text_splitter.split_documents(docs)
        
        # Add required metadata
        for chunk in chunks:
            chunk.metadata["persona"] = persona
            chunk.metadata["source_file"] = chunk.metadata.get("source", "unknown")
            chunk.metadata["chunk_id"] = str(uuid.uuid4())
            
        logger.info(f"Created {len(chunks)} chunks for {persona}. Storing in vector store...")
        try:
            vector_store = vector_store_service.get_collection(persona)
            vector_store.add_documents(chunks)
            logger.info(f"Successfully stored {len(chunks)} vectors for {persona}.")
        except Exception as e:
            logger.error(f"ChromaDB failure for {persona}: {e}")

ingestion_service = IngestionService()
