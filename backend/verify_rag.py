import asyncio
from app.services.rag.rag_service import rag_service

async def test_rag():
    print("Initializing RAG Service (this will check ChromaDB)...")
    rag_service.initialize()
    
    print("\n--- Testing Retrieval ---")
    query = "freedom and education"
    print(f"Query: {query}")
    
    for persona in ["Rabindranath Tagore", "Satyajit Ray", "Subhas Chandra Bose"]:
        print(f"\nRetrieving for {persona}...")
        context = rag_service.get_context(persona, query)
        print(f"Retrieved length: {len(context)}")
        if context:
            print(f"Sample: {context[:200]}...")
        else:
            print("No context retrieved.")

if __name__ == "__main__":
    asyncio.run(test_rag())
