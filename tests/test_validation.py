import pytest
from pathlib import Path
import sys

parent_dir=Path(__file__).parent.parent
sys.path.append(str(parent_dir))

from app.Department.schemas import DepartmentDelete,Departmentupdate,DepartmentCreate
from pydantic import ValidationError


def test_DepartmentCreate_required_min_lenght():
    with pytest.raises(ValidationError):
        DepartmentCreate(name='')

def test_DepartmentCreate_name_required_max_lenght():
    with pytest.raises(ValueError):
        DepartmentCreate(name='1'*201)

def test_DepartmentCreate_mising_name():
    with pytest.raises(ValueError):
        DepartmentCreate(parent_id='2')

def test_DepartmentCreate_name_strip():
    test= DepartmentCreate(name='  Test')
    assert test.name=='Test'

def test_DepartmentCreate_validation_parent_id():
    test= DepartmentCreate(name='Test',parent_id='2')
    assert test.parent_id==2

def test_DepartmentCreate_valid_parent_id():
    with pytest.raises(ValidationError):
        DepartmentCreate(name='Test',parent_id='Test')

def test_DepartmentCreate_config():
    with pytest.raises(ValidationError):
        DepartmentCreate(name='Test',Test='2')

def test_DepartamentDelete_mode_valid():
    with pytest.raises(ValidationError):
        DepartmentDelete(mode='Test')

def test_DepartamentDelete_reassign_valid():
    test=DepartmentDelete(mode='reassign',reassign_to_department_id=2)
    assert test.mode == 'reassign' and test.reassign_to_department_id == 2

def test_DepartamentDelete_reassign_to_department_id_invalid():
    with pytest.raises(ValidationError):
        DepartmentDelete(reassign_to_department_id='Test')

def test_DepartamentDelete_config():
    with pytest.raises(ValidationError):
        DepartmentDelete(mode='reassign',Test='2')

def test_Departamentupdate_config():
    with pytest.raises(ValidationError):
        Departmentupdate(Test='2')

def test_Departamentupdate_validation_name():
    with pytest.raises(ValidationError):
        Departmentupdate(name=True)

def test_Departamentupdate_validation_parent_id():
    with pytest.raises(ValidationError):
        Departmentupdate(parent_id='Test')