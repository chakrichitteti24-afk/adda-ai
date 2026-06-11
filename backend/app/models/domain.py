import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base

def generate_uuid():
    return str(uuid.uuid4())

class Persona(Base):
    __tablename__ = "personas"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    system_prompt = Column(Text, nullable=False)
    tone = Column(String, nullable=False)
    metadata_json = Column(JSON, nullable=True)

class Topic(Base):
    __tablename__ = "topics"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    sessions = relationship("DebateSession", back_populates="topic")

class DebateSession(Base):
    __tablename__ = "debate_sessions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    topic_id = Column(String(36), ForeignKey("topics.id"), nullable=False)
    status = Column(String, nullable=False, default="pending")  # pending, active, completed
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ended_at = Column(DateTime, nullable=True)

    topic = relationship("Topic", back_populates="sessions")
    conversation = relationship("Conversation", back_populates="session", uselist=False)

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    session_id = Column(String(36), ForeignKey("debate_sessions.id"), nullable=False)
    summary = Column(Text, nullable=True)

    session = relationship("DebateSession", back_populates="conversation")
    messages = relationship("Message", back_populates="conversation", order_by="Message.sequence_number")

class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=False)
    persona_id = Column(String(36), ForeignKey("personas.id"), nullable=True)
    role = Column(String, nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    sequence_number = Column(Integer, nullable=False)

    conversation = relationship("Conversation", back_populates="messages")
    persona = relationship("Persona")
