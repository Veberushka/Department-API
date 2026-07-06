from sqlalchemy import select,update,delete
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from database.postgres import async_session_maker


class BaseDAO:
    model=None
    @classmethod
    async def get_all(cls,include_employees=False,**filters):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            if include_employees:
                query = query.options(selectinload(getattr(cls.model, 'employees')))
            data = await session.execute(query)
            return data.scalars().all()


    @classmethod
    async def add(cls,**values):
        async with async_session_maker() as session:
            try:
                async with session.begin():
                    new_data=cls.model(**values)
                    session.add(new_data)
                    return new_data
            except SQLAlchemyError as e:
                raise 
    
    @classmethod
    async def update(cls,filters,**values):
        async with async_session_maker() as session:
            try:
                async with session.begin():
                #Создание модели обновления для полей, которые подходят под определения фильтра,передются значения, которые нужно обновить
                    if 'id__in' in filters:
                        query = (update(cls.model).where(cls.model.id.in_(filters['id__in'])).values(**values)
                        .returning(cls.model).execution_options(synchronize_session="fetch"))
                    else:
                        query=(update(cls.model).where(*[getattr(cls.model,key)== value for key, value in filters.items()])
                            .values(**values).returning(cls.model).execution_options(synchronize_session="fetch"))
                    result = await session.execute(query)
                    return result.scalars().all()
            except SQLAlchemyError as e:
                raise
                
    @classmethod
    async def delete(cls, **filter_by):
        if not filter_by:
            raise ValueError("Необходимо указать хотя бы один параметр для удаления.")
        async with async_session_maker() as session:
            try:
                async with session.begin():
                    query = delete(cls.model).filter_by(**filter_by)
                    result = await session.execute(query)
            except SQLAlchemyError as e:
                    raise 
            return result.rowcount
        