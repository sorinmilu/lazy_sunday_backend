"""
    Functiile care executa operatii pe baza de date. Celelalte componente ale aplicatiei
    apeleaza aceste functii pentru a citi/scrie in db. 
"""

from sqlalchemy.orm import Session
from . import models, schemas
import bcrypt
import secrets

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def generate_api_key():
    return secrets.token_urlsafe(32)

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks_by_user_id(db: Session, user_id, skip: int = 0, limit: int = 10):
    return db.query(models.Task).filter(models.Task.owner_id == user_id).offset(skip).limit(limit).all()

def get_all_users(db: Session):
    return db.query(models.User).all()

def get_db_settings(db: Session) -> schemas.AppSettings:
    settings = db.query(models.DBSettings).all()
    settings_dict = {setting.key: setting.value for setting in settings}
    return schemas.AppSettings(settings=settings_dict)