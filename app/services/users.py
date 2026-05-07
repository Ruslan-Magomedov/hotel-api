from fastapi import HTTPException
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from app.config import settings



class UsersServices:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        """Создание jwt токена"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(payload=to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt
    
    def decode_token(self, token: str) -> dict:
        """Декодирование jwt токена"""
        try:
            return jwt.decode(jwt=token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
            raise HTTPException(status_code=401, detail="Предоставьте валидный токен")
    
    def hash_password(self, password: str) -> str:
        """Шифрование пароля"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Проверка пароля на валидность"""
        return self.pwd_context.verify(plain_password, hashed_password)
