import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from app.tools.custom_exceptions import Error


class TestDepartmentAPI:

    #######################################
    # Тесты эндпоинта post
    @pytest.mark.asyncio
    async def test_create_department_success(self, client: AsyncClient):
        with patch('app.Department.routers.DepartmentServiсe.add_department') as mock_add:
            mock_add.return_value = {
                "id": 1,
                "name": "IT Department",
                "parent_id": None,
                "created_at": "2025-01-01T00:00:00",
                "employees": [],
                "children": []
            }
            data = {"name": "IT Department", "parent_id": None}
            response = await client.post("/departments/", json=data)
            assert response.status_code == 200
            result = response.json()
            assert result["name"] == "IT Department"
            assert result["parent_id"] is None
            assert "id" in result

    @pytest.mark.asyncio
    async def test_create_department_with_parent(self, client: AsyncClient):

        with patch('app.Department.routers.DepartmentServiсe.add_department') as mock_add:
            mock_add.return_value = {
                "id": 2,
                "name": "Child",
                "parent_id": 1,
                "created_at": "2025-01-01T00:00:00",
                "employees": [],
                "children": []
            }
            
            response = await client.post("/departments/",json={"name": "Child", "parent_id": 1})

            assert response.status_code == 200
            assert response.json()["parent_id"] == 1


    #######################################
    # Тесты эндпоинта get

    @pytest.mark.asyncio
    async def test_get_department_success(self, client: AsyncClient):

        with patch('app.Department.routers.DepartmentServiсe.get_by_id_with_children') as mock_get:
            mock_get.return_value = {
                "id": 1,
                "name": "Test Department",
                "parent_id": None,
                "created_at": "2025-01-01T00:00:00",
                "employees": [],
                "children": []
            }
        
        
            response = await client.get(f"/departments/1")
        
            assert response.status_code == 200
            result = response.json()
            assert result["id"] == 1
            assert result["name"] == "Test Department"
            assert "employees" in result
            assert "children" in result

    @pytest.mark.asyncio
    async def test_get_department_with_depth(self, client: AsyncClient):
        
        with patch('app.Department.routers.DepartmentServiсe.get_by_id_with_children') as mock_get: 

            mock_get.return_value = {
                "id": 1,
                "name": "A",
                "parent_id": None,
                "created_at": "2025-01-01T00:00:00",
                "employees": [],
                "children": [
                    {
                        "id": 2,
                        "name": "B",
                        "parent_id": 1,
                        "created_at": "2025-01-01T00:00:00",
                        "employees": [],
                        "children": [
                            {
                                "id": 3,
                                "name": "C",
                                "parent_id": 2,
                                "created_at": "2025-01-01T00:00:00",
                                "employees": [],
                                "children": []
                            }
                        ]
                    }
                ]
            }
        
            # Тест с depth=1
            response = await client.get(f"/departments/1?depth=1")
            result = response.json()
            assert len(result["children"]) == 1
            assert result["children"][0]["id"] == 2
        
            # Тест с depth=2
            response = await client.get(f"/departments/1?depth=2")
            result = response.json()
            assert result["children"][0]["children"][0]["id"] == 3

    @pytest.mark.asyncio
    async def test_get_department_with_employees(self, client: AsyncClient):
        with patch('app.Department.routers.DepartmentServiсe.get_by_id_with_children') as mock_get:
            mock_get.return_value = {
                "id": 1,
                "name": "IT",
                "parent_id": None,
                "created_at": "2025-01-01T00:00:00",
                "employees": [
                    {
                        "id": 1,
                        "full_name": "Alice",
                        "position": "Developer",
                        "department_id": 1,  
                        "hired_at": None,     
                        "created_at": "2025-01-01T00:00:00"  
                        },
                        {
                        "id": 2,
                        "full_name": "Bob",
                        "position": "Developer",
                        "department_id": 1,  
                        "hired_at": None,     
                        "created_at": "2025-01-01T00:00:00"  
                        },
                        ],
                "children": []
            }
        
        
            response = await client.get(f"/departments/1?include_employees=true")
            assert len(response.json()["employees"]) == 2
        
            mock_get.return_value = {
                "id": 1,
                "name": "IT",
                "parent_id": None,
                "created_at": "2025-01-01T00:00:00",
                "employees": [],
                "children": []
            }

            response = await client.get(f"/departments/1?include_employees=false")
            assert len(response.json()["employees"]) == 0

    @pytest.mark.asyncio
    async def test_get_department_not_found(self, client: AsyncClient):
        with patch('app.Department.routers.DepartmentServiсe.get_by_id_with_children') as mock_get:
            mock_get.return_value = None
            response = await client.get("/departments/999999")
            assert response.status_code == 404
    
    #######################################
    # Тесты эндпоинта patch

    @pytest.mark.asyncio
    async def test_update_department_name(self, client: AsyncClient):
        with patch('app.Department.routers.DepartmentServiсe.update_parent_id_with_name') as mock_update:
            mock_update.return_value = {
                "id": 1,
                "name": "New Name",
                "parent_id": None,
                "created_at": "2025-01-01T00:00:00",
                "employees": [],
                "children": []
            }
       
        
            response = await client.patch(f"/departments/1",json={"name": "New Name"})
        
            assert response.status_code == 200
            assert response.json()["name"] == "New Name"

    @pytest.mark.asyncio
    async def test_update_department_parent(self, client: AsyncClient):
         with patch('app.Department.routers.DepartmentServiсe.update_parent_id_with_name') as mock_update:
            mock_update.return_value = {
                "id": 1,
                "name": "Child",
                "parent_id": 5,
                "created_at": "2025-01-01T00:00:00",
                "employees": [],
                "children": []
            }
       
        
            response = await client.patch(f"/departments/1",
                                        json={"parent_id": 5})
        
            assert response.status_code == 200
            assert response.json()["parent_id"] == 5


    #######################################
    # Тесты эндпоинта delete

    @pytest.mark.asyncio
    async def test_delete_department_cascade(self, client: AsyncClient):
        with patch('app.Department.routers.DepartmentServiсe.delete_by_id') as mock_delete:
            mock_delete.return_value = None
        
            response = await client.delete( f"/departments/1?mode=cascade")
        
            assert response.status_code == 204
            mock_delete.assert_called_once_with(1, "cascade", None)
        
        

    @pytest.mark.asyncio
    async def test_delete_department_reassign(self, client: AsyncClient):
         with patch('app.Department.routers.DepartmentServiсe.delete_by_id') as mock_delete:
            mock_delete.return_value = None
        
            response = await client.delete(f"/departments/1?mode=reassign&reassign_to_department_id=5")
        
            assert response.status_code == 204
            mock_delete.assert_called_once_with(1, "reassign", 5)


    @pytest.mark.asyncio
    async def test_delete_department_not_found(self, client: AsyncClient):
        with patch('app.Department.routers.DepartmentServiсe.delete_by_id') as mock_delete:
            mock_delete.side_effect = Error(status_code=404, detail="Департамент не найден")
            response = await client.delete("/departments/999999?mode=cascade")
            assert response.status_code == 404