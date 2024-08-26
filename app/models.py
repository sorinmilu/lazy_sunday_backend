"""
Modelele care reprezinta obiectele din baza de date

"""



from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, MetaData, DateTime, Text, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session  # Import Session
from passlib.context import CryptContext
from datetime import datetime

metadata = MetaData() 
Base = declarative_base(metadata=metadata)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(150), unique=True, index=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)
    tasks = relationship("Task", back_populates="owner")
    added = Column(DateTime, server_default=func.now(), nullable=False)
    
    
    @classmethod
    def populate_initial(cls, session: Session, data: list):
        for item in data:
            if 'hashed_password' in item:
                item['hashed_password'] = hash_password(item['hashed_password'])    

            if not session.query(cls).filter_by(username=item['username']).first():

                user = cls(**item)
                session.add(user)
        session.commit()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(String(500))
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")
    added = Column(DateTime, server_default=func.now(), nullable=False)
    progress = Column(Integer, default=0, nullable=False)


    @classmethod
    def populate_initial(cls, session: Session, data: list):
        for item in data:
            if not session.query(cls).filter_by(title=item['title']).first():
                task = cls(**item)
                session.add(task)
        session.commit()

class DBSettings(Base):
    __tablename__ = 'dbsettings'
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, index=True, nullable=False)
    value = Column(Text, nullable=False)

    @classmethod
    def populate_initial(cls, session: Session, data: list):
        for item in data:
            if not session.query(cls).filter_by(key=item['key']).first():
                task = cls(**item)
                session.add(task)
        session.commit()