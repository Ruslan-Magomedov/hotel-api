from fastapi import APIRouter, Body, Query

from datetime import date, timedelta

from app.api.dependencies import DBDep
from app.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch



router = APIRouter(prefix="/hotels", tags=["Номера"])



@router.get("/{hotel_id}/room/{room_id}")
async def get_room_by_id(db: DBDep, hotel_id: int, room_id: int):
    """Ручка для получения номера по id"""
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)



@router.get("/{hotel_id}/rooms")
async def get_hotel_rooms(db: DBDep, hotel_id: int,
                          date_from: date = Query(example=str(date.today())),
                          date_to: date = Query(example=str(date.today()+timedelta(days=1))),
                          ):
    """Ручка для получения номеров отеля"""
    return await db.rooms.get_filtered_dy_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)



@router.post("/{hotel_id}/rooms")
async def add_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body()):
    """Ручка для создания нового номера для отеля"""
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    obj = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": 200, "data": obj}



@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    """Ручка для удаления номера по id"""
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": 200}



@router.put("/{hotel_id}/rooms/{room_id}")
async def modify_rooms(db: DBDep, hotel_id: int, room_id: int,  room_data: RoomAddRequest = Body()):
    """Ручка для полного изменения номера по идинтификатору"""
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.update(_room_data, id=room_id)
    await db.commit()
    return {"status": 200}
        


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_mod_rooms(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest = Body()):
    """Ручка для частичного изменения номера по идинтификатору"""
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.update(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": 200}
