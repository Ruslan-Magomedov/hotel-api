from pydantic import BaseModel



class HotelsAdd(BaseModel):
    title: str
    city: str
    street: str



class Hotels(HotelsAdd):
    id: int



class Hotels_None(BaseModel):
    title: str | None = None
    city: str | None = None
    street: str | None = None



class HotelsSearchNone(BaseModel):
    title: str | None = None
    city: str | None = None
