from fastapi import APIRouter,Depends,HTTPException,Query,Response
from app.Department.dao import DepartmentDAO
from app.Department.schemas import DepartmentResponse,DepartmentCreate,DepartmentDelete,Departmentupdate
from app.logger import logger
from app.tools.custom_exceptions import Error
import traceback

router=APIRouter(prefix='/departments',tags= ['Эндпоинты Департаментов'])


@router.get('/{id}',summary="Получить данные про департамент по id")
async def get_Department(id:int,
                         depth: int = Query(1, ge=1, le=5, description="Глубина вложенных подразделений"),
    include_employees: bool = Query(True, description="Добавить сотрудников в ответ?"))->DepartmentResponse:
    try:
        rez=await DepartmentDAO.get_by_id_with_children(id,depth,include_employees)
        if rez:
            logger.info(f'/GET/departments/{id}->200 OK, depth={depth},include_employees={include_employees}')
            return rez
        logger.warning(f'/GET/departments/{id}->404 Департамент не найден, depth={depth},include_employees={include_employees}')
        raise HTTPException(status_code=404, detail="Департамент не найден")
    except HTTPException:
        raise
    except Error as e:
        logger.warning(f'/GET/departments/{id}->{e.status_code} {e.detail}, depth={depth},include_employees={include_employees}')
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f'/GET/departments/{id}-> Неизвестная ошибка, depth={depth},include_employees={include_employees}')
        logger.error(f'Полный стек вызовов:\n{traceback.format_exc()}')
        raise HTTPException(500, "Внутренняя ошибка сервера")

@router.post('/',response_model=DepartmentResponse,summary="Добавить департамент")
async def register_department(departament:DepartmentCreate) -> DepartmentResponse:
    try:
        check= await DepartmentDAO.add_department(**departament.dict())
        if check:
            logger.info(f'/POST/departments/->200 OK, name={departament.name},parent_id={departament.parent_id}')
            return check
        logger.warning(f'/POST/departments/->400 Ошибка при добавлении департамента, name={departament.name},parent_id={departament.parent_id}')
        raise HTTPException(status_code=400, detail="Ошибка при добавлении департамента")
    except HTTPException:
        raise
    except Error as e:
        logger.warning(f'/POST/departments/->{e.status_code} {e.detail}, name={departament.name},parent_id={departament.parent_id}')
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f'/POST/departments/->Неизвестная ошибка, name={departament.name},parent_id={departament.parent_id}')
        logger.error(f'Полный стек вызовов:\n{traceback.format_exc()}')
        raise HTTPException(500, "Внутренняя ошибка сервера")
    

@router.patch('/{id}',summary="Вывести Департрамент из подчинения одного и передать в подчинение другого")
async def update_parent_id(id:int,body:Departmentupdate)->DepartmentResponse:
    try:
        check=await DepartmentDAO.update_parent_id_with_name(id=id,parent_id=body.parent_id,name=body.name)
        if check:
            logger.info(f'/PATCH/departments/{id}->200 OK, name={body.name},parent_id={body.parent_id}')
            return check
        logger.warning(f'/PATCH/departments/{id}->400 Ошибка при обновлении информации о департаменте, name={body.name},parent_id={body.parent_id}')
        raise HTTPException(status_code=400, detail="Ошибка при обновлении информации о департаменте")
    except HTTPException:
        raise
    except Error as e:
        logger.warning(f'/PATCH/departments/{id}->{e.status_code} {e.detail}, name={body.name},parent_id={body.parent_id}')
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f'/PATCH/departments/{id}->Неизвестная ошибка, name={body.name},parent_id={body.parent_id}')
        logger.error(f'Полный стек вызовов:\n{traceback.format_exc()}')
        raise HTTPException(500, "Внутренняя ошибка сервера")


@router.delete('/{id}',summary="Удалить Департамент")
async def update_delete(id:int,body:DepartmentDelete)->dict:
    try:
        if body.mode == 'cascade' and body.reassign_to_department_id  is not None:
            logger.warning(f'/DELETE/departments/{id}->400 Нельзя выбирать Департамент для переноса при режиме cascade,mode={body.mode},reassign_to_department_id={body.reassign_to_department_id}')
            raise HTTPException(400, "Нельзя выбирать Департамент для переноса при режиме cascade")
        if body.mode == 'reassign' and body.reassign_to_department_id  is None:
            logger.warning(f'/DELETE/departments/{id}->400 При режиме reassign нужно указать reassign_to_department_id,mode={body.mode},reassign_to_department_id={body.reassign_to_department_id}')
            raise HTTPException(400, "При режиме reassign нужно указать reassign_to_department_id")
        rez=await DepartmentDAO.delete_by_id(id,body.mode,body.reassign_to_department_id)
        logger.info(f'/DELETE/departments/{id}->200 OK, mode={body.mode},reassign_to_department_id={body.reassign_to_department_id}')
        return Response(status_code=204)
    except HTTPException:
        raise
    except Error as e:
        logger.info(f'/DELETE/departments/{id}->{e.status_code} {e.detail}, mode={body.mode},reassign_to_department_id={body.reassign_to_department_id}')
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f'/DELETE/departments/{id}->Неизвестная ошибка, mode={body.mode},reassign_to_department_id={body.reassign_to_department_id}')
        logger.error(f'Полный стек вызовов:\n{traceback.format_exc()}')
        raise HTTPException(500, "Внутренняя ошибка сервера")