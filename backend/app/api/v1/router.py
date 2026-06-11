from fastapi import APIRouter
from app.api.v1.endpoints import topics, debate

api_router = APIRouter()
api_router.include_router(topics.router, prefix="/topics", tags=["topics"])
api_router.include_router(debate.router, prefix="/debate", tags=["debate"])
