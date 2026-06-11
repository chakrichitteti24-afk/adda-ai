from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.domain import Topic
from app.schemas.domain import TopicCreate, TopicResponse

router = APIRouter()

@router.post("/", response_model=TopicResponse)
def create_topic(topic: TopicCreate, db: Session = Depends(get_db)):
    db_topic = Topic(title=topic.title, description=topic.description)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

@router.get("/", response_model=list[TopicResponse])
def get_topics(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    topics = db.query(Topic).offset(skip).limit(limit).all()
    return topics
