from sqlalchemy import select, func

from datetime import date

from app.models.bookings import BookingsOrm
from app.repositories.base import BaseRepo
from app.models.rooms import RoomsOrm
from app.schemas.rooms import Room


class RoomsRepo(BaseRepo):
    model = RoomsOrm
    schema = Room

    async def get_filtered_dy_time(self, hotel_id: int, date_from: date, date_to: date, **filter_by):
        rooms_count = (
            select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsOrm) 
            .filter(
                BookingsOrm.date_from <= date_to,
                BookingsOrm.date_to >= date_from,
            )
            .group_by(BookingsOrm.room_id)
            .cte(name="rooms_count")
        )
        rooms_left_table = (
            select(
                self.model.id.label("rooms_id"),
                (self.model.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
            )
            .select_from(self.model)
            .outerjoin(rooms_count, self.model.id == rooms_count.c.room_id)
            .cte(name="rooms_left_table")
        )
        query = (
            select(rooms_left_table).select_from(rooms_left_table)
            .filter(rooms_left_table.c.rooms_left > 0)
        )

        from app.db import engine

        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))
