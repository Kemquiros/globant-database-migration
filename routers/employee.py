import codecs
import csv
from typing import List
from fastapi import APIRouter, Path
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemes.employee import Employee
from config.database import Session
from config.upload_file import MIN_ROWS, MAX_ROWS
from services.employee import EmployeeService

employee_router = APIRouter()


@employee_router.get(
    '/employees',
    tags=['employees'])
def get_employees() -> List[Employee]:
    """Get the stored employees"""
    db = Session()
    result = EmployeeService(db).get_employees()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@employee_router.get(
    '/employees/{employee_id}',
    tags=['employees'])
def get_employee(employee_id: int = Path(ge=1, lt=10000)) -> Employee:
    """Get an specific employee by id"""
    db = Session()
    result = EmployeeService(db).get_employee_by_id(employee_id)
    if not result:
        return JSONResponse(status_code=404, content={
            "message": "The employee does not exist",
            "id": employee_id
        })
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@employee_router.post(
    '/employees',
    tags=['employees'],
    response_model=dict)
def create_employee(employee: Employee) -> dict:
    """Create a new employee"""
    db = Session()
    result = EmployeeService(db).get_employee_by_id(employee.id)
    if not result:
        new_employee = EmployeeService(db).create_employee(employee)
        return JSONResponse(status_code=201, content={
            "message": "New employee stored",
            "id": new_employee.id
        })
    return JSONResponse(status_code=409, content={
        "message": "The employee already exists",
        "id": employee.id
    })


@employee_router.post(
    '/employees/upload',
    tags=['employees'])
def upload_file(file: UploadFile = File(...)):
    """Create employees from CSV file"""
    csv_reader = csv.DictReader(
        codecs.iterdecode(file.file, 'utf-8'),
        delimiter=",",
        fieldnames=[
            'id',
            "name",
            "datetime",
            "department_id",
            "job_id"])
    employees = list(csv_reader)
    n_employees = len(employees)
    if n_employees < MIN_ROWS:
        file.file.close()
        return JSONResponse(status_code=409, content={
            "message": "The file needs more rows",
            "min_rows": MIN_ROWS
        })
    elif n_employees > MAX_ROWS:
        file.file.close()
        return JSONResponse(status_code=409, content={
            "message": "The file needs less rows",
            "max_rows": MAX_ROWS
        })
    else:
        db = Session()
        employees = [Employee(**employee) for employee in employees
                     if (employee['name'] and employee['datetime'] and employee['department_id'] and employee['job_id'])]
        EmployeeService(db).create_employees(employees)
        file.file.close()
        return JSONResponse(status_code=201, content={
            "message": "The file has been uploaded"
        })


@employee_router.put(
    '/employees/{employee_id}',
    tags=['employees'],
    response_model=dict)
def update_employee(employee_id: int, employee: Employee) -> dict:
    """Update an specific employee by id"""
    db = Session()
    result, exception = EmployeeService(
        db).update_employee(employee_id, employee)
    if not result and not exception:
        return JSONResponse(status_code=404, content={
            "message": "The employee does not exist",
            "id": employee_id
        })
    elif exception:
        return JSONResponse(status_code=500, content={
            "error": str(exception)
        })
    return JSONResponse(status_code=200, content={
        "message": "The employee has been updated",
        "id": employee_id
    })


@employee_router.delete(
    '/employees/{employee_employee_id}',
    tags=['employees'],
    response_model=dict)
def delete_employee(employee_id: int) -> dict:
    """Delete an specific employee by id"""
    db = Session()
    result = EmployeeService(db).get_employee_by_id(employee_id)
    if not result:
        return JSONResponse(status_code=404, content={
            "message": "The employee does not exist",
            "id": employee_id
        })
    EmployeeService(db).delete_employee(result)
    return JSONResponse(status_code=200, content={
        "message": "The employee has been deleted",
        "id": employee_id
    })
