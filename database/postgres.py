
from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from app.config  import get_db_url
from datetime import datetime, date
from typing import Annotated



DATABASE_URL = get_db_url() 

engine = create_async_engine(DATABASE_URL,echo=True,pool_size=2,max_overflow=2)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
Date = Annotated[date, mapped_column(nullable=True)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_nullnt = Annotated[str, mapped_column( nullable=False)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[created_at]

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    def to_dict(self):
        result = {column.name: getattr(self,column.name) for column in self.__table__.columns}
        return result

