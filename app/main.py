"""
    Fisierul principal al aplicatiei
     - Creaza aplicatia FastAPI
     - initializeaza loggerul
     - Seteaza middleware-ul CORS
     - Citeste setarile din baza de date
     - Include in aplicatia pornita rutele (care sunt functii definite pentru anumite url-uri)

"""

from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy import create_engine
from .settings import settings
from .routers import users, tasks
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, SessionLocal
from . import models
from fastapi.responses import JSONResponse
from fastapi.openapi.models import SecurityScheme
from .crud import get_db_settings
from sqlalchemy.orm import Session
from .schemas import AppSettings
import logging


logging_config = {
    "level": getattr(logging, settings.LOG_LEVEL),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "handlers": [],
}

if settings.LOG_FILE:
    logging_config["handlers"].append(logging.FileHandler(settings.LOG_FILE))

if settings.LOG_STREAM == "true":
    logging_config["handlers"].append(logging.StreamHandler())

logging.basicConfig(**logging_config)

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

settings_cache = None  # Global variable to store settings

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting event")
    
    with SessionLocal() as db:  # Replace SessionLocal with your session factory
        app.dbsettings = get_db_settings(db)



@app.get("/example")
def example_route():
    logger.info(f"example route called" + settings.LOG_STREAM)
    setting_value = app.dbsettings.settings.get('Setting1', 'Default Value')
    logger.info(f"example route called {setting_value}")
    return {"settings": app.dbsettings.settings}

app.include_router(users.router)
app.include_router(tasks.router)
