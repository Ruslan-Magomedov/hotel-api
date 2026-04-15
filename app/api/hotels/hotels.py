from fastapi import Query, Body, APIRouter
from sqlalchemy import insert, select, func


from app.db import async_session_maker

from app.models.hotels import HotelsOrm


from app.schemas.hotels import Hotels, Hotels_None, HotelsSearch, HotelsSearchNone
from app.api.hotels.dependencies import PaginationDep



router = APIRouter(prefix="/hotels", tags=["Отели"])



@router.get("")
async def get_hotels(paginations: PaginationDep, data: HotelsSearchNone = Query()):
    """Ручка для получения отеля - (отелей) по id или названию города и названию отеля"""
    async with async_session_maker() as session:
        obj = select(HotelsOrm)

        if data.city:
            obj = obj.filter(func.lower(HotelsOrm.city).like(f"%{data.city.lower()}%"))
            
        if data.title:
            obj = obj.filter(func.lower(HotelsOrm.title).like(f"%{data.title.lower()}%"))
        
        obj = (
            obj
            .limit(paginations.per_page)
            .offset(paginations.per_page * (paginations.page-1))
        )
        obj = await session.execute(obj)
    
    return obj.scalars().all()



@router.delete("/{hotel_id}")
def delete_hotels(hotel_id: int):
    """Ручка для удаления отеля по id"""
    
    return {"msg": "OK"}



@router.post("")
async def add_hotels(data: Hotels = Body()):
    """Ручка для создания нового объекта отеля"""
    async with async_session_maker() as session:
        obj = insert(HotelsOrm).values(**data.model_dump())
        await session.execute(obj)
        await session.commit()

    return {"message": "OK"}



@router.put("/{hotel_id}")
def modify_hotels(
    hotel_id: int,
    city: str = Body(description="Город"),
    name: str = Body(description="Отель")
    ):
    """Ручка для полного изменения объекта по идинтификатору"""
    global hotels
    
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotels[hotel_id-1] = {"id": hotel_id, "city": city, "name": name}
            return {"msg": "OK"}
    return {"msg": "Not Found"}
        


@router.patch("/{hotel_id}")
def partially_mod_hotels(
    hotel_id: int,
    city: str | None = Body(None, description="Город"),
    name: str | None = Body(None, description="Отель")
    ):
    """Ручка для частичного изменения объекта по идинтификатору"""
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if city:
                hotels[hotel_id-1]["city"] = city
            if name:
                hotels[hotel_id-1]["name"] = name
            return {"msg": "OK"}
    return {"msg": "Not Found"}
