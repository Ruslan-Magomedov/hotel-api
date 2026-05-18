from fastapi import APIRouter, HTTPException, Response
from sqlalchemy.exc import IntegrityError

from app.api.dependencies import DBDep, UserIdDep
from app.schemas.users import UsersRequestAdd, UsersAdd
from app.services.users import UsersServices



router = APIRouter(prefix="/auth", tags=["Авторизация & Аутентификация"])



@router.post("/register")
async def register_users(db: DBDep, data: UsersRequestAdd):
    hashed_pass = UsersServices().hash_password(data.password)
    new_user_data = UsersAdd(email=data.email.lower(), hashed_pass=hashed_pass)
    
    try:
        await db.users.add(new_user_data)
        await db.commit()
        return {"status": 200}
    except IntegrityError:
        raise HTTPException(status_code=400, detail=f"Почта '{data.email}' уже существует")



@router.post("/login")
async def login_users(db: DBDep, data: UsersRequestAdd, response: Response):
    user = await db.users.get_user_with_hashed_pass(data.email)

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
async def get_me(db: DBDep, user_id: UserIdDep):
    return await db.users.get_one_or_none(id=user_id)
