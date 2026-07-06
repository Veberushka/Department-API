import pytest
from app.Employee.dao import EmployeeDAO
from app.Department.model import Department
from app.Employee.model import Employee

class TestEmployeeDAO:
    @pytest.mark.asyncio
    async def test_create_employee(self, db_session):
        dept = Department(name="IT")
        db_session.add(dept)
        await db_session.commit()
        await db_session.refresh(dept)
        
        emp = Employee(
            department_id=dept.id,
            full_name="John Doe",
            position="Developer"
        )
        db_session.add(emp)
        await db_session.commit()
        await db_session.refresh(emp)
        
        result = await EmployeeDAO.get_all(id=emp.id)
        assert len(result) == 1
        assert result[0].full_name == "John Doe"