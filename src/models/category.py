from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Category(Base):
    __tablename__ = 'categories'

    name: Mapped[str] = mapped_column(String(25), unique=True)

    polls: Mapped[list["Poll"]] = relationship(
        "Poll",
        back_populates="category"
    )
