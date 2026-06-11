from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AddaAI API",
    description="API for the AddaAI historical debate platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.v1.router import api_router
from app.services.rag.rag_service import rag_service

@app.on_event("startup")
async def startup_event():
    import asyncio
    await asyncio.to_thread(rag_service.initialize)


@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok", "message": "AddaAI API is running"}

app.include_router(api_router, prefix="/api/v1")
