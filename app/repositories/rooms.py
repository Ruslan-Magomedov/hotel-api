from datetime import date

from app.repositories.utils import rooms_ids_for_bookings
from app.repositories.base import BaseRepo
from app.models.rooms import RoomsOrm
from app.schemas.rooms import Room


class RoomsRepo(BaseRepo):
    model = RoomsOrm
    schema = Room

    async def get_filtered_dy_time(self, hotel_id: int, date_from: date, date_to: date, **filter_by):
        rooms_ids_to_get = rooms_ids_for_bookings(hotel_id, date_from, date_to)
        return await self.get_filtered(self.model.id.in_(rooms_ids_to_get))
