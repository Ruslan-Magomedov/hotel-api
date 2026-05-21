from sqlalchemy import select

from app.repositories.base import BaseRepo
from app.models.bookings import BookingsOrm
from app.schemas.bookings import Bookings



class BookingsRepo(BaseRepo):
    model = BookingsOrm
    schema = Bookings

    async def get_all_bookings(self, limit, offset, **filt):
        bookings = await select(self.model).fi
    
    async def get_all_bookings(self, limit, offset, **filter_by):
        """Получение всех данных из базы"""
        request = select(self.model).filter_by(**filter_by).limit(limit).offset(offset)
        request = await self.session.execute(request)
        return [self.schema.model_validate(model) for model in request.scalars().all()]