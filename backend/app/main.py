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
from alembic.config import Config
from alembic import command
from app.db.seed import seed_personas
import logging

logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    import asyncio
    
    # Run database migrations programmatically at startup
    try:
        logger.info("Running database migrations (Alembic upgrade head)...")
        alembic_cfg = Config("alembic.ini")
        await asyncio.to_thread(command.upgrade, alembic_cfg, "head")
        logger.info("Database migrations completed successfully.")
    except Exception as e:
        logger.error(f"Database migration failed, falling back to Base.metadata.create_all: {e}")
        try:
            from app.db.session import engine
            from app.models import Base
            await asyncio.to_thread(Base.metadata.create_all, bind=engine)
            logger.info("Database tables created successfully using Base.metadata.create_all.")
        except Exception as create_err:
            logger.error(f"Base.metadata.create_all fallback failed: {create_err}")

    # Seed the database (idempotent)
    try:
        logger.info("Seeding default database records...")
        await asyncio.to_thread(seed_personas)
        logger.info("Database seeding completed successfully.")
    except Exception as e:
        logger.error(f"Database seeding failed: {e}")

    # Initialize RAG
    await asyncio.to_thread(rag_service.initialize)


@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok", "message": "AddaAI API is running"}

app.include_router(api_router, prefix="/api/v1")
