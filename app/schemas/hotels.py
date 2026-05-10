from pydantic import BaseModel, ConfigDict



class HotelsAdd(BaseModel):
    title: str
    city: str
    street: str



class Hotels(HotelsAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Hotels_None(BaseModel):
    title: str | None = None
    city: str | None = None
    street: str | None = None



class HotelsSearchNone(BaseModel):
    title: str | None = None
    city: str | None = None
