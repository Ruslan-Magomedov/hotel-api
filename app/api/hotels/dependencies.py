from fastapi import Depends, Query
from pydantic import BaseModel

from typing import Annotated



class PaginationParams(BaseModel):
    page: int = Query(1, description="Страница", gt=0)
    per_page: int = Query(3, description="Колличество элементов на странице", gt=2, lt=10)



PaginationDep = Annotated[PaginationParams, Depends()]
