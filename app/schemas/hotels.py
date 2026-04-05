from pydantic import BaseModel





class Hotels(BaseModel):
    city: str
    name: str



class Hotels_id(Hotels):
    id: int



class Hotels_None(BaseModel):
    city: str | None = None
    name: str | None = None
