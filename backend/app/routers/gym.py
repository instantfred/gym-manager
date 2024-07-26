from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from starlette import status
from ..models.gym import Gym
from ..database import SessionLocal

router = APIRouter(
    prefix='/gyms',
    tags=['gyms']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/{gym_id}')
async def get_gym(db: db_dependency, gym_id: int = Path(gt=0)):
    gym = db.query(Gym).filter(Gym.id == gym_id).first()
    if gym is None:
        raise HTTPException(status_code=404, detail='Gym not found.')
    else:
        return gym

