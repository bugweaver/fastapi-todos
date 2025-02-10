from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from typing import Optional


class TodosTable(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    completed: Mapped[bool] = mapped_column(default=False)
