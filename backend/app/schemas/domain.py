from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class TopicBase(BaseModel):
    title: str
    description: Optional[str] = None

class TopicCreate(TopicBase):
    pass

class TopicResponse(TopicBase):
    id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PersonaResponse(BaseModel):
    id: str
    name: str
    system_prompt: str
    tone: str
    metadata_json: Optional[Dict[str, Any]] = None
    model_config = ConfigDict(from_attributes=True)

class DebateSessionCreate(BaseModel):
    topic_id: str

class DebateSessionResponse(BaseModel):
    id: str
    topic_id: str
    status: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    persona_id: Optional[str]
    role: str
    content: str
    timestamp: datetime
    sequence_number: int
    model_config = ConfigDict(from_attributes=True)

class DebateRespondRequest(BaseModel):
    session_id: str
    user_message: str

class PersonaResponseItem(BaseModel):
    persona: str
    content: str

class DebateRespondResponse(BaseModel):
    responses: List[PersonaResponseItem]

class DebateMessageResponse(BaseModel):
    id: str
    conversation_id: str
    persona_id: Optional[str] = None
    persona_name: Optional[str] = None
    role: str
    content: str
    timestamp: datetime
    sequence_number: int
    model_config = ConfigDict(from_attributes=True)
