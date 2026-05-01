from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from app.db import async_session_maker
from app.repositories.users import UsersRepo
from app.schemas.users import UsersRequestAdd, UsersAdd



from passlib.context import CryptContext



router = APIRouter(prefix="/auth", tags=["Авторизация & Аутентификация"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



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
