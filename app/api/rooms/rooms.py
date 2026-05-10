from fastapi import APIRouter, Body


from app.db import async_session_maker
from app.repositories.rooms import RoomsRepo
from app.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch



router = APIRouter(prefix="/hotels", tags=["Номера"])



@router.get("/{hotel_id}/room/{room_id}")
async def get_room_by_id(hotel_id: int, room_id: int):
    """Ручка для получения номера по id"""
    async with async_session_maker() as session:
        return await RoomsRepo(session).get_one_or_none(hotel_id=hotel_id, id=room_id)



@router.get("/{hotel_id}/rooms")
async def get_hotel_rooms(hotel_id: int):
    """Ручка для получения номеров отеля"""
    async with async_session_maker() as session:
        return await RoomsRepo(session).get_filtered(hotel_id=hotel_id)



@router.post("/{hotel_id}/rooms")
async def add_room(hotel_id: int, room_data: RoomAddRequest = Body()):
    """Ручка для создания нового номера для отеля"""
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        obj = await RoomsRepo(session).add(_room_data)
        await session.commit()
    return {"status": 200, "data": obj}



@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int):
    """Ручка для удаления номера по id"""
    async with async_session_maker() as session:
        await RoomsRepo(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": 200}



@router.put("/{hotel_id}/rooms/{room_id}")
async def modify_rooms(hotel_id: int, room_id: int,  room_data: RoomAddRequest = Body()):
    """Ручка для полного изменения номера по идинтификатору"""
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepo(session).update(_room_data, id=room_id)
        await session.commit()
    return {"status": 200}
        


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_mod_hotels(hotel_id: int, room_id: int, room_data: RoomPatchRequest = Body()):
    """Ручка для частичного изменения номера по идинтификатору"""
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepo(session).update(_room_data, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": 200}
