from app.repositories.base import BaseRepo
from app.models.rooms import RoomsOrm
from app.schemas.rooms import Room


class RoomsRepo(BaseRepo):
    model = RoomsOrm
    schema = Room
