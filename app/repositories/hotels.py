from sqlalchemy import select, func

from datetime import date

from app.repositories.base import BaseRepo
from app.models.hotels import HotelsOrm
from app.models.rooms import RoomsOrm
from app.schemas.hotels import Hotels
from app.repositories.utils import rooms_ids_for_bookings



class HotelsRepo(BaseRepo):
    model = HotelsOrm
    schema = Hotels

    async def get_all(self, title, city, limit, offset):
        obj = select(HotelsOrm)

        if city:
            obj = obj.filter(func.lower(HotelsOrm.city).like(f"%{city.lower()}%"))
            
        if title:
            obj = obj.filter(func.lower(HotelsOrm.title).like(f"%{title.lower()}%"))
        
        obj = obj.limit(limit).offset(offset)
        obj = await self.session.execute(obj)
    
        return [self.schema.model_validate(model, from_attributes=True) for model in obj.scalars().all()]
    

    async def get_filtered_by_time(self, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_bookings(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        return await self.get_filtered(self.model.id.in_(hotels_ids_to_get))
