from sqlalchemy import select, func

from datetime import date

from app.models.bookings import BookingsOrm
from app.models.rooms import RoomsOrm
from app.repositories.base import BaseRepo




def rooms_ids_for_bookings(hotel_id: int, date_from: date, date_to: date, **filter_by):
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
            RoomsOrm.id.label("rooms_id"),
            (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
        )
        .select_from(RoomsOrm)
        .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
        .cte(name="rooms_left_table")
    )

    rooms_ids_for_hotels = (
        select(RoomsOrm.id)
        .select_from(RoomsOrm)
        .filter_by(hotel_id=hotel_id)
        .subquery(name="rooms_ids_for_hotels")
    )

    rooms_ids_to_get = (
        select(rooms_left_table.c.rooms_id)
        .select_from(rooms_left_table)
        .filter(
            rooms_left_table.c.rooms_left > 0,
            rooms_left_table.c.rooms_id.in_(rooms_ids_for_hotels)
        )
    )

    # from app.db import engine
    # print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

    return BaseRepo.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))