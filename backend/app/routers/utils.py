from datetime import datetime, timedelta, timezone
import os
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.user import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status
from jose import jwt, JWTError


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITH = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


async def get_current_gym(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITH])
        gym_id: int = payload.get('gym_membership_id')
        if gym_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate gym.')
        return {'gym_id': gym_id}
    except JWTError:
        HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                      detail='Could not validate gym.')

