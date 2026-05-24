from pydantic import BaseModel,Field, field_validator
from datetime import datetime
from typing import List
from app.Employee.schemas import EmployeeResponse

class DepartmentResponse(BaseModel):
    id: int
    name: str
    parent_id:int|None
    created_at:datetime
    employees: List[EmployeeResponse] = Field(default_factory=list)
    children: List['DepartmentResponse'] = Field(default_factory=list)
    
    class Config:
        from_attributes = True 

DepartmentResponse.model_rebuild()

class DepartmentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200,description='Название Департамента')  # обязательное поле
    parent_id: int | None = Field(default=None,ge=1,description='ID родительского департамента')

    @field_validator('name')
    @classmethod
    def strip_name(cls,name:str)->str:
        return name.strip()
    
    class Config:
        extra = 'forbid'

class DepartmentDelete(BaseModel):
    mode:str = Field(..., pattern=r"^(cascade|reassign)$",description='Режим удаления Департамента, cascade- удалить подразделение,' \
    ' всех сотрудников и все дочерние подразделения,' \
    'reassign — удалить подразделение, а сотрудников перевести в reassign_to_department_id ')

    reassign_to_department_id:int|None= Field(default=None,ge=1, description="Департрамент, в который перененосятся дочерние департаменты и сотрудники" )
    
    class Config:
        extra = 'forbid'


class Departmentupdate(BaseModel):
    name:str|None= Field(default=None,description="Изменененное имя департрамента")
    parent_id: int | None = Field(default=None,ge=1,description="Изменение parent_id департрамента")

    class Config:
        extra = 'forbid'