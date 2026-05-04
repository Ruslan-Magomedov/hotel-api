from sqlalchemy import select, func
from pydantic import EmailStr


from app.repositories.base import BaseRepo
from app.models.users import UsersOrm
from app.schemas.users import Users, UserWithHashedPass



class UsersRepo(BaseRepo):
    model = UsersOrm
    schema = Users

    async def get_user_with_hashed_pass(self, data_email: EmailStr):
        """Получение данных из базы в размере одного объекта"""
        request = select(self.model).filter(func.lower(self.model.email).like(f"%{data_email.lower()}%"))
        request = await self.session.execute(request)
        request = request.scalars().one_or_none()

        if request is None:
            return None
        return UserWithHashedPass.model_validate(request, from_attributes=True)
