from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.domain import Persona

def seed_personas():
    db = SessionLocal()
    personas = [
        Persona(name="Rabindranath Tagore", system_prompt="You are Rabindranath Tagore. Speak poetically and philosophically.", tone="poetic"),
        Persona(name="Satyajit Ray", system_prompt="You are Satyajit Ray. Speak analytically about aesthetics.", tone="analytical"),
        Persona(name="Subhas Chandra Bose", system_prompt="You are Subhas Chandra Bose. Speak with intense pragmatism and action-orientation.", tone="pragmatic"),
        Persona(name="Moderator", system_prompt="You are the Moderator. Direct the debate and summarize.", tone="neutral")
    ]
    for p in personas:
        existing = db.query(Persona).filter(Persona.name == p.name).first()
        if not existing:
            db.add(p)
    db.commit()
    db.close()

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    seed_personas()
    print("Personas seeded successfully.")
