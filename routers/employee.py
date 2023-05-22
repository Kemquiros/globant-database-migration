from typing import List
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from schemes.employee import Employee

employee_router = APIRouter()


@employee_router.get(
    '/employees',
    tags=['employees'])
def get_employees() -> List[Employee]:
    """Get the stored employees"""
    return JSONResponse(status_code=200, content={"mesagge": "employees"})
