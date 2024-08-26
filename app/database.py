"""
Conexiunea la baza de date
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .settings import settings

# Create the SQLAlchemy engine using the DATABASE_URL from settings
engine = create_engine(settings.DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to get the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
