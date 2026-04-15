from pydantic import BaseModel



class Hotels(BaseModel):
    title: str
    city: str
    street: str



class Hotels_None(BaseModel):
    title: str | None = None
    city: str | None = None
    street: str | None = None



class HotelsSearch(BaseModel):
    title: str
    city: str



class HotelsSearchNone(BaseModel):
    title: str | None = None
    city: str | None = None
