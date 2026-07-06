import pytest
from sqlalchemy import select,delete
from app.Department.dao import DepartmentDAO
from app.Department.model import Department

class TestDepartmentDAO:

    @pytest.mark.asyncio
    async def test_create_department(self, db_session):
        dept = Department(name="IT")
        db_session.add(dept)
        await db_session.commit()
        await db_session.refresh(dept)
        
        query = select(Department).where(Department.id == dept.id)
        result = await db_session.execute(query)
        departments = result.scalars().all()
        assert len(departments) == 1
        assert departments[0].name == "IT"
    
    @pytest.mark.asyncio
    async def test_delete_department(self, db_session):
        dept = Department(name="IT")
        db_session.add(dept)
        await db_session.commit()
        await db_session.refresh(dept)
        
        query = delete(Department).where(Department.id == dept.id)
        result = await db_session.execute(query)
        rows = result.rowcount
        assert rows == 1
        
        query = select(Department).where(Department.id == dept.id)
        result = await db_session.execute(query)
        departments = result.scalars().all()
        assert len(departments) == 0