from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel

from typing import Annotated
from app.services.users import UsersServices

from app.utils.db_manager import DBManager
from app.db import async_session_maker



class PaginationParams(BaseModel):
    page: int = Query(1, description="Страница", gt=0)
    per_page: int = Query(3, description="Колличество элементов на странице", gt=2, lt=50)



PaginationDep = Annotated[PaginationParams, Depends()]



def get_token(request: Request):
    if not (jwt_token := request.cookies.get("access_token", None)):
        raise HTTPException(status_code=401, detail="Вы не авторизованы")
    return jwt_token



def get_current_user_id(token: str = Depends(get_token)):
    user = UsersServices().decode_token(token)
    return user["user_id"]



UserIdDep = Annotated[int, Depends(get_current_user_id)]



async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db



DBDep = Annotated[DBManager, Depends(get_db)]
