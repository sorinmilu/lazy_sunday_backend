import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import DeclarativeMeta
from pathlib import Path
from app.models import User, Task, DBSettings  # Import your models here
from app.settings import settings  # Import settings from config.py
from passlib.context import CryptContext


# Use DATABASE_URL from settings
DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_all_models(base):
    models = []
    for cls in base._decl_class_registry.values():
        if isinstance(cls, DeclarativeMeta):
            models.append(cls)
    return models

def table_exists(session, table_name):
    try:
        result = session.execute(text(f"SHOW TABLES LIKE :table_name"), {'table_name': table_name}).scalar()
        return result is not None
    except OperationalError:
        print(f"Table {table_name} does not exist, please run initial migration before injecting data")
        return False

def check_migrations(session, table_name):
    if not table_exists(session, table_name):
        return False

    try:
        result = session.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
        return result == 1
    except OperationalError:
        print(f"There has to be exactly one entry in the {table_name} table to inject initial data")
        return False

def load_initial_data(model_name: str) -> list:
    """ Load initial data from a JSON file for a given model. """
    file_path = Path('initial_data') / f"{model_name}.json"
    print(file_path)
    if file_path.exists():
        with open(file_path, 'r') as file:
            return json.load(file)
    return []

def populate_initial_data(session, model_class):
    """ Call the populate_initial function if it exists. """
    if hasattr(model_class, 'populate_initial'):
        print(f"Populating initial data for {model_class.__name__}")
        data = load_initial_data(model_class.__name__.lower())
        if data:
            model_class.populate_initial(session, data)
        else:
            print(f"No initial data found for {model_class.__name__.lower()}")


def populate():
    """ Trecem toate tabelele manual pentru ca trebui importate iar introspectia e dificila """
    session = SessionLocal()
    try:
        # Populate initial data for all models
        if check_migrations(session, 'alembic_version'):
            for model in [User, Task, DBSettings]:  
                populate_initial_data(session, model)
            session.commit()
        else: 
            raise Exception("Incorrect version status")       
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    populate()
