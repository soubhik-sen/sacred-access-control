from app.database import SessionLocal
from app.seed_data import seed_database

db = SessionLocal()
seed_database(db)
db.close()