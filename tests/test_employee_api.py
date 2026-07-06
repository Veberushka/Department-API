import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from app.tools.custom_exceptions import Error

class TestEmployeeAPI:
    @pytest.mark.asyncio
    async def test_create_employee_success(self, client: AsyncClient):
        with patch('app.Employee.routers.DepartmentDAO.get_all') as mock_dept:
            mock_dept.return_value = [{"id": 1, "name": "IT"}]
            with patch('app.Employee.routers.EmployeeDAO.add') as mock_create:
                mock_create.return_value = {
                "id": 1,
                "department_id": 1,
                "full_name": "John Doe",
                "position": "Senior Developer",
                "hired_at": "2025-01-01",
                "created_at": "2025-01-01T00:00:00"
            }

                response = await client.post(f"/departments/1/employees",
                json={
                "full_name": "John Doe",
                "position": "Senior Developer",
                "hired_at": "2025-01-01"
                }
            )

                assert response.status_code == 200
                result = response.json()
                assert result["full_name"] == "John Doe"
                assert result["position"] == "Senior Developer"
                assert result["department_id"] == 1
                assert result["hired_at"] == "2025-01-01"
                assert "id" in result
                assert "created_at" in result

                mock_create.assert_called_once()

    @pytest.mark.asyncio    
    async def test_create_employee_department_not_found(self, client: AsyncClient):
        with patch('app.Employee.routers.DepartmentDAO.get_all') as mock_dept:
            mock_dept.return_value = []  
            response = await client.post("/departments/999999/employees",
                json={
                    "full_name": "John Doe",
                    "position": "Developer"
                }
            )

            assert response.status_code == 404
            assert "Департамент не найден" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_create_employee_without_hired_at(self, client: AsyncClient):
        with patch('app.Employee.routers.DepartmentDAO.get_all') as mock_dept:
            mock_dept.return_value = [{"id": 1, "name": "IT"}]
            with patch('app.Employee.routers.EmployeeDAO.add') as mock_create:
                mock_create.return_value = {
                    "id": 2,
                    "department_id": 1,
                    "full_name": "Jane Doe",
                    "position": "Developer",
                    "hired_at": None,
                    "created_at": "2025-01-01T00:00:00"
                }
                response = await client.post(f"/departments/1/employees",
                    json={
                    "full_name": "Jane Doe",
                    "position": "Developer"
                    }
                )
                assert response.status_code == 200
                assert response.json()["hired_at"] is None