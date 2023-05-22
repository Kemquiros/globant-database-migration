import codecs
import csv
from typing import List
from fastapi import APIRouter, Path
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemes.department import Department
from config.database import Session
from config.upload_file import MIN_ROWS, MAX_ROWS
from services.department import DepartmentService

department_router = APIRouter()


@department_router.get(
    '/departments',
    tags=['departments'])
def get_departments() -> List[Department]:
    """Get the stored departments"""
    db = Session()
    result = DepartmentService(db).get_departments()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@department_router.get(
    '/departments/{department_id}',
    tags=['departments'])
def get_department(department_id: int = Path(ge=1, lt=10000)) -> Department:
    """Get an specific department by id"""
    db = Session()
    result = DepartmentService(db).get_department_by_id(department_id)
    if not result:
        return JSONResponse(status_code=404, content={
            "message": "The department does not exist",
            "id": department_id
        })
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@department_router.post(
    '/departments',
    tags=['departments'],
    response_model=dict)
def create_department(department: Department) -> dict:
    """Create a new department"""
    db = Session()
    result = DepartmentService(db).get_department_by_id(department.id)
    if not result:
        new_department = DepartmentService(db).create_department(department)
        return JSONResponse(status_code=201, content={
            "message": "New department stored",
            "id": new_department.id
        })
    return JSONResponse(status_code=409, content={
        "message": "The department already exists",
        "id": department.id
    })


@department_router.post(
    '/departments/upload',
    tags=['departments'])
def upload_file(file: UploadFile = File(...)):
    """Create departments from CSV file"""
    csv_reader = csv.DictReader(
        codecs.iterdecode(file.file, 'utf-8'),
        delimiter=",",
        fieldnames=['id', "department"])
    departments = list(csv_reader)
    n_departments = len(departments)
    if n_departments < MIN_ROWS:
        file.file.close()
        return JSONResponse(status_code=409, content={
            "message": "The file needs more rows",
            "min_rows": MIN_ROWS
        })
    elif n_departments > MAX_ROWS:
        file.file.close()
        return JSONResponse(status_code=409, content={
            "message": "The file needs less rows",
            "max_rows": MAX_ROWS
        })
    else:
        db = Session()
        departments = [Department(**department) for department in departments]
        DepartmentService(db).create_departments(departments)
        file.file.close()
        return JSONResponse(status_code=201, content={
            "message": "The file has been uploaded"
        })


@department_router.put(
    '/departments/{department_id}',
    tags=['departments'],
    response_model=dict)
def update_department(department_id: int, department: Department) -> dict:
    """Update an specific department by id"""
    db = Session()
    result = DepartmentService(db).update_department(department_id, department)
    if not result:
        return JSONResponse(status_code=404, content={
            "message": "The department does not exist",
            "id": department_id
        })
    return JSONResponse(status_code=200, content={
        "message": "The department has been updated",
        "id": department_id
    })


@department_router.delete(
    '/departments/{department_department_id}',
    tags=['departments'],
    response_model=dict)
def delete_department(department_id: int) -> dict:
    """Delete an specific department by id"""
    db = Session()
    result = DepartmentService(db).get_department_by_id(department_id)
    if not result:
        return JSONResponse(status_code=404, content={
            "message": "The department does not exist",
            "id": department_id
        })
    DepartmentService(db).delete_department(result)
    return JSONResponse(status_code=200, content={
        "message": "The department has been deleted",
        "id": department_id
    })
