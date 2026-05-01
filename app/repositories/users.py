from app.repositories.base import BaseRepo
from app.models.users import UsersOrm
from app.schemas.users import Users



class UsersRepo(BaseRepo):
    model = UsersOrm
    schema = Users
