from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel



class BaseRepo:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    
    async def get_filtered(self, **filter_by):
        """Получение всех данных из базы"""
        request = select(self.model).filter_by(**filter_by)
        request = await self.session.execute(request)
        return [self.schema.model_validate(model) for model in request.scalars().all()]
    

    async def get_all(self, *args, **kwargs):
        """Получение всех данных из базы"""
        return await self.get_filtered()
        

    async def get_one_or_none(self, **filter_by):
        """Получение данных из базы в размере одного объекта"""
        request = select(self.model).filter_by(**filter_by)
        request = await self.session.execute(request)
        request = request.scalars().one_or_none()

        if request is None:
            return None
        return self.schema.model_validate(request)
    

    async def add(self, data: BaseModel):
        """Добавление данных в базу"""
        request = insert(self.model).values(**data.model_dump()).returning(self.model)
        request = await self.session.execute(request)
        return self.schema.model_validate(request.scalars().one())
    
    
    async def update(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        """Удаление данных из базы по id"""
        request = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
        request = await self.session.execute(request)

    
    async def delete(self, **filter_by):
        request = delete(self.model).filter_by(**filter_by)
        request = await self.session.execute(request)
