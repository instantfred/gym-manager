from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from starlette import status
from ..models.gym import Gym
from ..database import SessionLocal

router = APIRouter(
    prefix='/gym',
    tags=['gym']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/')
async def test(db: db_dependency):
    return db.query(Gym).all()
