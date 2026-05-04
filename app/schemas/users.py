from pydantic import BaseModel, EmailStr



class UsersRequestAdd(BaseModel):
    email: EmailStr
    password: str



class UsersAdd(BaseModel):
    email: EmailStr
    hashed_pass: str



class Users(BaseModel):
    id: int
    email: EmailStr



class UserWithHashedPass(Users):
    hashed_pass: str
