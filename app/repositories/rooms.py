from app.repositories.base import BaseRepo
from app.models.rooms import RoomsOrm



class RoomsRepo(BaseRepo):
    model = RoomsOrm
