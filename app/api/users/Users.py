from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from app.db import async_session_maker
from app.repositories.users import UsersRepo
from app.schemas.users import UsersRequestAdd, UsersAdd



from passlib.context import CryptContext

import jwt

from datetime import datetime, timedelta, timezone



router = APIRouter(prefix="/auth", tags=["Авторизация & Аутентификация"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



@router.post("/register")
async def register_users(data: UsersRequestAdd):
    
    hashed_pass = pwd_context.hash(data.password)
    new_user_data = UsersAdd(email=data.email, hashed_pass=hashed_pass)
    
    async with async_session_maker() as session:
        try:
            await UsersRepo(session).add(new_user_data)
            await session.commit()
            return {"status": 200}
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                    status_code=400,
                    detail="Email already exists"
            )



@router.post("/login")
async def login_users(data: UsersRequestAdd):
    
    hashed_pass = pwd_context.hash(data.password)
    new_user_data = UsersAdd(email=data.email, hashed_pass=hashed_pass)
    
    async with async_session_maker() as session:
        try:
            await UsersRepo(session).get_one_or_none(email=data.email)
            await session.commit()
            return {"status": 200}
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                    status_code=400,
                    detail="Email already exists"
            )
