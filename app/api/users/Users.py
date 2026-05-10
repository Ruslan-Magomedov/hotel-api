from fastapi import APIRouter, HTTPException, Response
from sqlalchemy.exc import IntegrityError

from app.db import async_session_maker
from app.repositories.users import UsersRepo
from app.schemas.users import UsersRequestAdd, UsersAdd
from app.services.users import UsersServices
from app.api.users.dependencies import UserIdDep



router = APIRouter(prefix="/auth", tags=["Авторизация & Аутентификация"])



@router.post("/register")
async def register_users(data: UsersRequestAdd):
    hashed_pass = UsersServices().hash_password(data.password)
    new_user_data = UsersAdd(email=data.email.lower(), hashed_pass=hashed_pass)
    
    async with async_session_maker() as session:
        try:
            await UsersRepo(session).add(new_user_data)
            await session.commit()
            return {"status": 200}
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                    status_code=400,
                    detail=f"Почта '{data.email}' уже существует"
            )



@router.post("/login")
async def login_users(data: UsersRequestAdd, response: Response):
    async with async_session_maker() as session:
        user = await UsersRepo(session).get_user_with_hashed_pass(data.email)
        if not user:
            raise HTTPException(status_code=401, detail=f"Пользователь с почтой '{data.email}' не зарегистрирован")
        if not UsersServices().verify_password(data.password, user.hashed_pass):
            raise HTTPException(status_code=401, detail=f"Неверный пароль")
        access_token = UsersServices().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}



@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status_code": 200}



@router.get("/me")
async def get_me(user_id: UserIdDep):
    async with async_session_maker() as session:
        return await UsersRepo(session).get_one_or_none(id=user_id)
