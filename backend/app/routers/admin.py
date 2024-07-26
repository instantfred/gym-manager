from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from starlette import status
from ..models.gym import Gym
from ..database import SessionLocal

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


class GymRequest(BaseModel):
    slug: str = Field(min_length=3)
    name: str = Field(min_length=3, max_length=100)
    is_active: bool
    address: str = Field(min_length=3, max_length=100)
    phone_number: str = Field(min_length=8, max_length=12)


@router.get('/gyms')
async def get_all_gyms(db: db_dependency):
    return db.query(Gym).all()


@router.post('/gyms',status_code=status.HTTP_201_CREATED)
async def create_gym(db: db_dependency, gym_request: GymRequest):
    gym = Gym(**gym_request.dict())
    db.add(gym)
    db.commit()
    db.refresh(gym)
    return gym


@router.patch('/gyms/{gym_id}/deactivate')
async def deactivate_gym(db: db_dependency, gym_id: int = Path(gt=0)):
    gym = db.query(Gym).filter(Gym.id == gym_id).first()
    if gym is None:
        raise HTTPException(status_code=404, detail='Gym not found.')
    gym.is_active = False
    db.commit()
    db.refresh(gym)
    return gym


@router.patch('/gyms/{gym_id}/activate')
async def activate_gym(db: db_dependency, gym_id: int = Path(gt=0)):
    gym = db.query(Gym).filter(Gym.id == gym_id).first()
    if gym is None:
        raise HTTPException(status_code=404, detail='Gym not found.')
    gym.is_active = True
    db.commit()
    db.refresh(gym)
    return gym


@router.put('/gyms/{gym_id}')
async def update_gym(db: db_dependency, gym_request: GymRequest, gym_id: int = Path(gt=0)):
    gym = db.query(Gym).filter(Gym.id == gym_id).first()
    if gym is None:
        raise HTTPException(status_code=404, detail='Gym not found.')
    for field, value in gym_request.dict().items():
        setattr(gym, field, value)
    db.commit()
    db.refresh(gym)
    return gym
