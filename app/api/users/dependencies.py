from fastapi import Depends, Request, HTTPException

from typing import Annotated
from app.services.users import UsersServices



def get_token(request: Request):
    if not (jwt_token := request.cookies.get("access_token", None)):
        raise HTTPException(status_code=401, detail="Вы не авторизованы")
    return jwt_token



def get_current_user_id(token: str = Depends(get_token)):
    user = UsersServices().decode_token(token)
    return user["user_id"]



UserIdDep = Annotated[int, Depends(get_current_user_id)]
