from datetime import date

from app.repositories.utils import rooms_ids_for_bookings
from app.repositories.base import BaseRepo
from app.models.rooms import RoomsOrm
from app.schemas.rooms import Room


class RoomsRepo(BaseRepo):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_bookings(date_from, date_to, hotel_id)
        return await self.get_filtered(self.model.id.in_(rooms_ids_to_get))
