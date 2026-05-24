from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from database.postgres import Base, int_pk, str_nullnt



# создаем модель таблицы студентов
class Department(Base):
    id: Mapped[int_pk]
    name: Mapped[str_nullnt]
    parent_id:Mapped[int| None]=mapped_column(ForeignKey('departments.id', ondelete='CASCADE'), nullable=True)

    parent: Mapped["Department | None"] = relationship(
    back_populates="children",
    remote_side="Department.id"
    )

    children: Mapped[list["Department"]] = relationship(
        back_populates="parent",
    )
    
    employees: Mapped[list["Employee"]] = relationship("Employee",back_populates="department")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"name={self.name!r})")

    def __repr__(self):
        return str(self)
    