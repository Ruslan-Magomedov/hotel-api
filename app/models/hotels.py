from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.db import Base



class HotelsOrm(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    city: Mapped[str] = mapped_column(String(200))
    street: Mapped[str] = mapped_column(String(200))
