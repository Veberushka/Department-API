from app.Department.model import Department
from app.base_dao import BaseDAO
from app.tools.tree import build_Tree_with_recursion,sort_Tree,collect_department_ids,collect_department_names
from app.tools.custom_exceptions import Error
from sqlalchemy.exc import IntegrityError
from database.postgres import async_session_maker
from sqlalchemy import update
from app.Employee.model import Employee 

class DepartmentDAO(BaseDAO):
    model=Department

    @classmethod
    def departments_to_dicts(cls,departament,include_employees=False):

        """
        Преобразование списка объектов Department в список словарей.
    
        Сериализует ORM-объекты в формат JSON-friendly словарей с возможностью
        включения связанных сотрудников.
    
        Args:
            departments: Список объектов Department из БД
            include_employees: Флаг включения сотрудников в результат.
    
        Returns:
            list[dict]: Список словарей с данными департаментов, каждый содержит:
                - Все поля из модели Department (id, name, parent_id, created_at)
                - 'employees': list[dict] - список словарей сотрудников (если include_employees=True)
    
        """

        all_departments_dicts = []
        for dept in departament:
            dept_dict = dept.to_dict()
        
            if include_employees and hasattr(dept, 'employees'):
                dept_dict['employees'] = [
                    emp.to_dict() for emp in dept.employees
                ]
            else:
                dept_dict['employees'] = []
               
            all_departments_dicts.append(dept_dict)

        return all_departments_dicts
    
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
        
    @classmethod
    async def get_by_id_with_children(cls,id,depth,include_employees):
        """
        Получение департамента с его иерархической структурой.
    
        Рекурсивно строит дерево подразделений до указанной глубины с возможностью
        включения сотрудников в ответ.
    
        Args:
            id : ID корневого департамента для построения дерева
            depth : Глубина вложенности подразделений (1-5)
            include_employees (bool): Флаг включения сотрудников в ответ
                - True: Включает список сотрудников для каждого департамента
                - False: Возвращает только структуру подразделений
    
        Returns:
            dict | None: Дерево подразделений в формате:
                {
                "id": int,
                "name": str,
                "parent_id": int | None,
                "created_at": datetime,
                "employees": [...],  # Если include_employees=True
                "children": [        # Рекурсивная структура до depth
                    {...},
                    {...}
                ]
                }
            Возвращает None, если департамент с id не найден
    
            Note:
            Сотрудники сортируются по полю 'full_name' если include_employees=True
    
        """

        all_department=await cls.get_all(include_employees)
        need_department_with_children=build_Tree_with_recursion(cls.departments_to_dicts(all_department,include_employees),id,depth)
        if include_employees:
            need_department_with_children=sort_Tree(need_department_with_children,'full_name')
        return need_department_with_children
        

    @classmethod
    async def add_department(cls,name,parent_id: int|None=None):
        """
         Создание нового подразделения
    
        Args:
            name: Название подразделения (уникально в рамках parent_id)
            parent_id: ID родительского подразделения (None для корневого)
    
        Returns:
            dict: Данные созданного подразделения
    
        Raises:
            Error(409): Если подразделение с таким именем уже существует
            Error(404): Если parent_id не найден
        """

        existing=None
        if parent_id:
            existing= await cls.get_all(parent_id=parent_id,name=name)
        if existing:
            raise Error(
            status_code=409,
            detail=f"Департрамент '{name}' уже существует в подчинении {parent_id}")
        try:
            new_department = await cls.add(name=name,parent_id=parent_id)
            return {
            "id": new_department.id,
            "name": new_department.name,
            "parent_id": new_department.parent_id,
            "created_at": new_department.created_at,
            "employees": [],
            "children": []
        }
        except IntegrityError as e:
            if "foreign key constraint" in str(e).lower():
                raise Error(status_code=404, detail=f"Департамент с id={parent_id} не найден")
            raise 
    
    @classmethod
    async def update_parent_id_with_name(cls,id,parent_id,name):

        """
        Обновление родительского департамента и/или названия подразделения.
    
        Выполняет комплексную проверку перед обновлением:
        - Защита от циклических ссылок (нельзя переместить департамент внутрь своего поддерева)
        - Проверка уникальности имени в рамках нового родителя
    
        Args:
            id : ID обновляемого департамента
            parent_id : Новый ID родительского департамента (None для корневого)
            name: Новое название департамента
    
        Returns:
            dict: Обновленные данные департамента в формате:
                {
                    "id": int,
                    "name": str,
                    "parent_id": int | None,
                    "created_at": datetime,
                    "employees": [],
                    "children": []
                }
    
        Raises:
            Error(409): Если обнаружена циклическая ссылка или имя уже существует
            Error(404): Если новый родительский департамент не найден
        """
        exception_parent_id=None
        exception_parent_name=None
        if parent_id:
            all_department=cls.departments_to_dicts(await cls.get_all())
            exception_department_ids=build_Tree_with_recursion(all_department,id,depth=5)
            exception_department_names=build_Tree_with_recursion(all_department,parent_id,depth=2)
            if exception_department_ids:
                exception_parent_id=collect_department_ids(exception_department_ids,id)
                exception_parent_name=collect_department_names(exception_department_names,parent_id,depth=2)
            else:
                exception_parent_id = []
        if exception_parent_id and parent_id in exception_parent_id:
            raise Error(status_code=409,detail=f"Департамент не может быть быть в своем подчинении")
        if exception_parent_name and name in exception_parent_name:
            raise Error(status_code=409,detail=f"Департамент c именем {name} уже существует в подчинении")
        try:
            result=await cls.update({'id':id},parent_id=parent_id,name=name)
            obj = result[0]

            return {"id": obj.id,
                    "name": obj.name,
                    "parent_id": obj.parent_id,
                    "created_at": obj.created_at,
                    "employees": [],
                    "children": []  }
        except IntegrityError as e:
            if "foreign key constraint" in str(e).lower():
                raise Error(status_code=404, detail=f"Департамент с id={parent_id} не найден")
            raise 
            
    @classmethod
    async def delete_by_id(cls,id,mode,reassign_to_department_id):
        """
        Удаление департамента с поддержкой двух режимов.
    
        Args:
            id : ID удаляемого департамента
            mode: Режим удаления
                - 'cascade': Полное каскадное удаление (департамент + все подразделения + сотрудники)
                - 'reassign': Перенос всех сотрудников и дочерних подразделений в другой департамент
            reassign_to_department_id (int | None): ID департамента-получателя (обязателен при mode='reassign')
    
        Returns:
            None: Метод не возвращает значения
    
        Raises:
            Error(404): Если удаляемый или целевой департамент не найден
    
        Behavior:
            При mode='cascade':
                - Удаляет департамент, всех его сотрудников и все дочерние подразделения
            -    Использует каскадное удаление на уровне БД (ON DELETE CASCADE)
        
            При mode='reassign':
                - Собирает все ID дочерних подразделений
                - Переназначает их parent_id на reassign_to_department_id
                - Переносит всех сотрудников в reassign_to_department_id
                - Удаляет исходный департамент
    
        """

        if mode =='cascade':
            await cls.delete(id=id)
        elif mode== 'reassign' and reassign_to_department_id:
            all_department=cls.departments_to_dicts(await cls.get_all())
            exception_department=build_Tree_with_recursion(all_department,id,depth=2)
            if exception_department is None:
                raise Error(404, f"Департамент с id={id} не найден")
            child_id=collect_department_ids(exception_department,id)[1:]
            await cls.update({'id__in':child_id}, parent_id=reassign_to_department_id)
            await cls.update_employees_department(id, reassign_to_department_id)
            await cls.delete(id=id)
    
