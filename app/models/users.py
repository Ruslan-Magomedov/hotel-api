from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, SmallInteger

from app.db import Base



class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(30))
    age: Mapped[int] = mapped_column()
    location: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    hashed_pass: Mapped[str] = mapped_column(String())
