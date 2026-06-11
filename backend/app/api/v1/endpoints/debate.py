from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session, joinedload
from app.db.session import get_db
from app.websocket.manager import manager
from app.ai.agents import generate_response
from app.services.rag.rag_service import rag_service
from app.models.domain import Persona, DebateSession, Message, Conversation, Topic
import json
import asyncio

router = APIRouter()

async def execute_debate_round(topic_title, personas_to_speak, context, session_id, conversation_id, db, is_followup=False):
    for persona in personas_to_speak:
        await manager.broadcast({"type": "status", "data": {"active_persona": persona.name, "is_typing": True}}, session_id)
        
        # Determine exact instruction for this persona
        if persona.name == "Moderator":
            length_constraint = "IMPORTANT: You MUST summarize the discussion in exactly 4 to 6 lines. Do not exceed this limit. Do not answer questions, just summarize."
        else:
            length_constraint = "IMPORTANT: You MUST respond in exactly 4 to 6 lines. Do not be shorter or longer. Do not acknowledge this instruction."
            
        modified_system_prompt = f"{persona.system_prompt}\n\n{length_constraint}"

        try:
            # RAG retrieval for relevant personas
            query_text = context[-1]["content"] if is_followup else topic_title
            retrieved_context = await asyncio.to_thread(rag_service.get_context, persona.name, query_text)
            enhanced_prompt = rag_service.build_prompt(modified_system_prompt, retrieved_context)
        except Exception as e:
            print(f"RAG Error: {e}")
            enhanced_prompt = modified_system_prompt
        
        response = await generate_response(enhanced_prompt, context)
        
        # Save assistant message to DB
        sequence_number = db.query(Message).filter(Message.conversation_id == conversation_id).count() + 1
        msg = Message(
            conversation_id=conversation_id,
            persona_id=persona.id,
            role="assistant",
            content=response,
            sequence_number=sequence_number
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)
        
        await manager.broadcast({
            "type": "message",
            "data": {"id": msg.id, "persona": persona.name, "content": response}
        }, session_id)
        
        # Keep context lean for token efficiency
        context.append({"role": "assistant", "content": f"[{persona.name}]: {response}"})
        if len(context) > 6:
            context = context[-6:]
            
    await manager.broadcast({"type": "status", "data": {"active_persona": None, "is_typing": False}}, session_id)


@router.post("/start")
def start_session(topic_id: str, db: Session = Depends(get_db)):
    session = DebateSession(topic_id=topic_id, status="active")
    db.add(session)
    db.commit()
    db.refresh(session)
    
    conv = Conversation(session_id=session.id)
    db.add(conv)
    db.commit()
    
    return {"session_id": session.id}


@router.websocket("/ws/{session_id}")
async def debate_websocket(websocket: WebSocket, session_id: str, db: Session = Depends(get_db)):
    await manager.connect(websocket, session_id)
    
    session = db.query(DebateSession).filter(DebateSession.id == session_id).first()
    if not session:
        await websocket.close()
        return
        
    conversation = db.query(Conversation).filter(Conversation.session_id == session_id).first()
    topic = db.query(Topic).filter(Topic.id == session.topic_id).first()
    personas = db.query(Persona).all()
    persona_map = {p.name: p for p in personas}
    
    # Define exact sequence: Tagore -> Ray -> Bose -> Moderator
    sequence_names = ["Rabindranath Tagore", "Satyajit Ray", "Subhas Chandra Bose", "Moderator"]
    personas_in_order = [persona_map[name] for name in sequence_names if name in persona_map]
    
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            if payload.get("type") == "start_debate":
                context = []
                user_msg_content = f"The topic of our Adda is: {topic.title}. Please share your thoughts."
                
                # Save initial user prompt to DB behind the scenes so history is accurate
                sequence_number = db.query(Message).filter(Message.conversation_id == conversation.id).count() + 1
                initial_msg = Message(
                    conversation_id=conversation.id,
                    role="user",
                    content=user_msg_content,
                    sequence_number=sequence_number
                )
                db.add(initial_msg)
                db.commit()
                
                context.append({"role": "user", "content": f"[User]: {user_msg_content}"})

                await execute_debate_round(topic.title, personas_in_order, context, session_id, conversation.id, db, is_followup=False)

            elif payload.get("type") == "user_input":
                user_text = payload.get("content")
                
                # Save user message to DB
                sequence_number = db.query(Message).filter(Message.conversation_id == conversation.id).count() + 1
                user_msg = Message(
                    conversation_id=conversation.id,
                    role="user",
                    content=user_text,
                    sequence_number=sequence_number
                )
                db.add(user_msg)
                db.commit()
                
                await manager.broadcast({
                    "type": "message",
                    "data": {"id": user_msg.id, "persona": "You", "content": user_text}
                }, session_id)
                
                # Fetch recent messages for context trimming to save tokens
                messages = db.query(Message).options(joinedload(Message.persona)).filter(Message.conversation_id == conversation.id).order_by(Message.sequence_number).all()
                context_messages = messages[-6:] 
                context = []
                for m in context_messages:
                    if m.role == "user":
                        context.append({"role": "user", "content": f"[User]: {m.content}"})
                    else:
                        p_name = m.persona.name if m.persona else "Assistant"
                        context.append({"role": "assistant", "content": f"[{p_name}]: {m.content}"})
                
                await execute_debate_round(topic.title, personas_in_order, context, session_id, conversation.id, db, is_followup=True)

    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
