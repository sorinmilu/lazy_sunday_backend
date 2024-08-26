"""
Rutele pentru task separate pentru claritate

"""


from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, auth
from ..database import get_db
from ..schemas import AppSettings
import logging

router = APIRouter()

@router.post("/tasks/", response_model=schemas.Task)
def create_task(request:Request, task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    logger = logging.getLogger("uvicorn")
    setting_value = request.app.dbsettings.settings.get('Setting1', 'Default Value')
    logger.info("Example route accessed: " + setting_value)
    return crud.create_task(db=db, task=task, user_id=current_user.id)

@router.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(request:Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    tasks = crud.get_tasks_by_user_id(db, user_id=current_user.id, skip=skip, limit=limit)
    return tasks
