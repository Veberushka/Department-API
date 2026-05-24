from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from database.postgres import Base, int_pk, str_nullnt, Date



# создаем модель таблицы студентов
class Employee(Base):
    id: Mapped[int_pk]
    department_id:Mapped[int]=mapped_column(ForeignKey('departments.id', ondelete='CASCADE'), nullable=False)
    full_name: Mapped[str_nullnt]
    position: Mapped[str_nullnt]
    hired_at:Mapped[Date|None]

    department: Mapped["Department"] = relationship("Department",back_populates="employees")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"name={self.full_name!r})")

    def __repr__(self):
        return str(self)