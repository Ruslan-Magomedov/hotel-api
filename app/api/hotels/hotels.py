from fastapi import Query, Body, APIRouter

from app.api.dependencies import DBDep, PaginationDep
from app.schemas.hotels import HotelsAdd, Hotels_None, HotelsSearchNone



router = APIRouter(prefix="/hotels", tags=["Отели"])



@router.get("/{hotel_id}")
async def get_hotel_by_id(db: DBDep, hotel_id: int):
    """Ручка для получения отеля по id"""
    return await db.hotels.get_one_or_none(id=hotel_id)



@router.get("")
async def get_hotels(db: DBDep, paginations: PaginationDep, data: HotelsSearchNone = Query()):
    """Ручка для получения отеля - (отелей) по названию города и названию отеля"""
    return await db.hotels.get_all(
        title=data.title,
        city=data.city,
        limit=paginations.per_page,
        offset=paginations.per_page * (paginations.page-1)
    )



@router.post("")
async def add_hotels(db: DBDep, data: HotelsAdd = Body()):
    """Ручка для создания нового объекта отеля"""
    obj = await db.hotels.add(data)
    await db.commit()
    return {"status": 200, "data": obj}



@router.delete("/{hotel_id}")
async def delete_hotels(db: DBDep, hotel_id: int):
    """Ручка для удаления отеля по id"""
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": 200}



@router.put("/{hotel_id}")
async def modify_hotels(db: DBDep, hotel_id: int, data: HotelsAdd = Body()):
    """Ручка для полного изменения объекта по идинтификатору"""
    await db.hotels.update(data, id=hotel_id)
    await db.commit()
    return {"status": 200}
        


@router.patch("/{hotel_id}")
async def partially_mod_hotels(db: DBDep, hotel_id: int, data: Hotels_None = Body()):
    """Ручка для частичного изменения объекта по идинтификатору"""
    await db.hotels.update(data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": 200}
