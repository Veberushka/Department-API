from fastapi import APIRouter,Depends,HTTPException,Path
from app.Employee.dao import EmployeeDAO
from app.Employee.schemas import EmployeeResponse,EmployeeCreate
from app.Department.routers import router
from app.Department.dao import DepartmentDAO
from app.logger import logger
import traceback


@router.post('/{id}/employees',response_model=EmployeeResponse,summary="Добавить сотрудника")
async def create_employee(employee:EmployeeCreate,
                              id: int = Path(...,ge=1,description='ID рабочего департамента сотрудника'),) -> EmployeeResponse:
    try:
        departament= await DepartmentDAO.get_all(id=id)
        if not departament:
            logger.warning(f'/POST/departments/{id}/employees->400 Департамент не найден, employee={employee}')
            raise HTTPException(status_code=404, detail="Департамент не найден")
    
        check= await EmployeeDAO.add(department_id=id,**employee.dict())
        if check:
            logger.info(f'/POST/departments/{id}/employees->200 OK, employee={employee}')
            return check
        logger.warning(f'/POST/departments/{id}/employees->400 Ошибка при добавлении сотрудника, employee={employee}')
        raise HTTPException(status_code=400, detail="Ошибка при добавлении сотрудника") 
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'/POST/departments/{id}/employees->Неизвестная ошибка, employee={employee}')
        logger.error(f'Полный стек вызовов:\n{traceback.format_exc()}')
        raise HTTPException(500, "Внутренняя ошибка сервера")