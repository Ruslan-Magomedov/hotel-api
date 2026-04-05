from fastapi import Query, Body, APIRouter


from app.schemas.hotels import Hotels, Hotels_id, Hotels_None
from app.api.hotels.dependencies import PaginationDep



router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "city": "Sochi", "name": "Super"},
    {"id": 2, "city": "Moscow", "name": "Beluchi"},
    {"id": 3, "city": "Volga", "name": "Volodya"},
    {"id": 4, "city": "Rostov", "name": "Rassos"},
    {"id": 5, "city": "Sochi", "name": "RuRu"},
    {"id": 6, "city": "Sochi", "name": "Super"},
    {"id": 7, "city": "Moscow", "name": "Beluchi"},
    {"id": 8, "city": "Volga", "name": "Volodya"},
    {"id": 9, "city": "Rostov", "name": "Rassos"},
    {"id": 10, "city": "Sochi", "name": "RuRu"},
    {"id": 11, "city": "Sochi", "name": "Super"},
    {"id": 12, "city": "Moscow", "name": "Beluchi"},
    {"id": 13, "city": "Volga", "name": "Volodya"},
    {"id": 14, "city": "Rostov", "name": "Rassos"},
    {"id": 15, "city": "Sochi", "name": "RuRu"},
    {"id": 16, "city": "Sochi", "name": "Super"},
    {"id": 17, "city": "Moscow", "name": "Beluchi"},
    {"id": 18, "city": "Volga", "name": "Volodya"},
    {"id": 19, "city": "Rostov", "name": "Rassos"},
    {"id": 20, "city": "Sochi", "name": "RuRu"},
]



@router.get("")
def get_hotels(paginations: PaginationDep,
               hotel_id: int | None = Query(None, description="Идинтефикатор"),
               city: str | None = Query(None, description="Город")):
    """Поинт для получения отеля - (отелей) по id или названию города и названию отеля"""
    hotels_ = []

    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        if city and hotel["city"] != city:
            continue
        hotels_.append(hotel)
    
    b = paginations.page * paginations.per_page
    a = b - paginations.per_page
    
    return hotels_[a:b]



@router.delete("/{hotel_id}")
def delete_hotels(hotel_id: int):
    """Поинт для удаления отеля по id"""
    global hotels

    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"msg": "OK"}



@router.post("")
def add_hotels(city: str = Body(description="Название города", embed=True)):
    global hotels
    """Поинт для создания нового объекта отеля"""
    hotels.append({"id": hotels[-1]["id"]+1, "city": city})
    return {"msg": "OK"}



@router.put("/{hotel_id}")
def modify_hotels(
    hotel_id: int,
    city: str = Body(description="Город"),
    name: str = Body(description="Отель")
    ):
    """Поинт для полного изменения объекта по идинтификатору"""
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
    """Поинт для частичного изменения объекта по идинтификатору"""
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if city:
                hotels[hotel_id-1]["city"] = city
            if name:
                hotels[hotel_id-1]["name"] = name
            return {"msg": "OK"}
    return {"msg": "Not Found"}
