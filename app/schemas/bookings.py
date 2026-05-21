from pydantic import BaseModel, ConfigDict

from datetime import date



class BookingsAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int



class BookingsAddRequests(BaseModel):
    room_id: int
    date_from: date
    date_to: date



class Bookings(BookingsAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
