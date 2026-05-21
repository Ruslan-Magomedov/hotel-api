from fastapi import APIRouter

from app.api.dependencies import DBDep, UserIdDep, PaginationDep
from app.schemas.bookings import BookingsAddRequests, BookingsAdd



router = APIRouter(prefix="/bookings", tags=["Бронирования"])



@router.get("")
async def get_bookings(db: DBDep, paginations: PaginationDep):
    return await db.bookings.get_all_bookings(
        limit=paginations.per_page,
        offset=paginations.per_page * (paginations.page-1)
    )



@router.get("/me")
async def get_my_bookings(db: DBDep, user: UserIdDep, paginations: PaginationDep):
    return await db.bookings.get_all_bookings(
        user_id=user,
        limit=paginations.per_page,
        offset=paginations.per_page * (paginations.page-1)
    )



@router.post("")
async def add_booking(db: DBDep, user: UserIdDep, data: BookingsAddRequests):
    room = await db.rooms.get_one_or_none(id=data.room_id)                              # Получаем комнату по id
    room_price = room.price                                                             # Получаем цену за комнату
    booking_data = BookingsAdd(user_id= user, price=room_price, **data.model_dump())    # Добавляем данные в схему BookingsAdd
    booking = await db.bookings.add(booking_data)                                       # Добавляем данные в бд
    await db.commit()                                                                   # Сохраняем изменения
    return {"status": 200, "booking": booking}
