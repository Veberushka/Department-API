from app.Department.model import Department
from app.base_dao import BaseDAO
from database.postgres import async_session_maker
from sqlalchemy import update
from app.Employee.model import Employee 

class DepartmentDAO(BaseDAO):
    model=Department
    
    @classmethod
    async def update_employees_department(cls, old_department_id: int, new_department_id: int):

        """
        Массовый перенос всех сотрудников из одного департамента в другой.
    
        Выполняет прямое обновление в БД через SQL и SQLAlchemy UPDATE без загрузки объектов
        в память, что оптимально для большого количества сотрудников.
    
        Args:
            old_department_id (int): ID исходного департамента (будет удален)
            new_department_id (int): ID целевого департамента (куда переносятся сотрудники)
    
        Returns:
            None: Метод не возвращает значения
    
        Raises:
            SQLAlchemyError: При ошибках выполнения SQL-запроса
        """

        async with async_session_maker() as session:
            async with session.begin():
                await session.execute(update(Employee)
                                      .where(Employee.department_id == old_department_id)
                                      .values(department_id=new_department_id))
         
    
