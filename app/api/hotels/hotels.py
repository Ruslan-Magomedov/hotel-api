from fastapi import Query, Body, APIRouter


from app.db import async_session_maker

from app.schemas.hotels import HotelsAdd, Hotels_None, HotelsSearchNone
from app.api.hotels.dependencies import PaginationDep

from app.repositories.hotels import HotelsRepo
from app.repositories.rooms import RoomsRepo




router = APIRouter(prefix="/hotels", tags=["Отели"])



@router.get("/{hotel_id}")
async def get_hotel_by_id(hotel_id: int):
    """Ручка для получения отеля по id"""
    async with async_session_maker() as session:
        return await HotelsRepo(session).get_one_or_none(id=hotel_id)



@router.get("")
async def get_hotels(paginations: PaginationDep, data: HotelsSearchNone = Query()):
    """Ручка для получения отеля - (отелей) по названию города и названию отеля"""
    async with async_session_maker() as session:
        return await HotelsRepo(session).get_all(
            title=data.title,
            city=data.city,
            limit=paginations.per_page,
            offset=paginations.per_page * (paginations.page-1)
        )



@router.post("")
async def add_hotels(data: HotelsAdd = Body()):
    """Ручка для создания нового объекта отеля"""
    async with async_session_maker() as session:
        obj = await HotelsRepo(session).add(data)
        await session.commit()
    return {"status": 200, "data": obj}



@router.delete("/{hotel_id}")
async def delete_hotels(hotel_id: int):
    """Ручка для удаления отеля по id"""
    async with async_session_maker() as session:
        await HotelsRepo(session).delete(id=hotel_id)
        await session.commit()
    return {"status": 200}



@router.put("/{hotel_id}")
async def modify_hotels(hotel_id: int, data: HotelsAdd = Body()):
    """Ручка для полного изменения объекта по идинтификатору"""
    async with async_session_maker() as session:
        await HotelsRepo(session).update(data, id=hotel_id)
        await session.commit()
    return {"status": 200}
        


@router.patch("/{hotel_id}")
async def partially_mod_hotels(hotel_id: int, data: Hotels_None = Body()):
    """Ручка для частичного изменения объекта по идинтификатору"""
    async with async_session_maker() as session:
        await HotelsRepo(session).update(data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": 200}
