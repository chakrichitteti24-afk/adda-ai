from app.db.session import SessionLocal
from app.models.domain import Topic, Persona

db = SessionLocal()
topic = db.query(Topic).first()
print(f"Topic: {topic.id if topic else 'None'} - {topic.title if topic else 'None'}")
personas = db.query(Persona).all()
print("Personas:", [p.name for p in personas])
db.close()
