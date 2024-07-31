from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from ..models import Users
from ..database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

