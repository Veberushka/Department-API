from pydantic import BaseModel,Field
from datetime import datetime,date

class EmployeeResponse(BaseModel):
    id: int
    department_id:int
    full_name: str
    position: str
    hired_at:date|None
    created_at:datetime
    
    class Config:
        from_attributes = True 

class EmployeeCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=200,strip_whitespace=True,description='Полное имя сотрудника')
    position: str = Field(..., min_length=1, max_length=200,strip_whitespace=True,description='Должность сотрудника')
    hired_at:date|None = Field(default=None,description='Дата принятия сотрудника на работу')
    class Config:
        extra = 'forbid'