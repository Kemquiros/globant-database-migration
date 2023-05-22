from fastapi import APIRouter
from fastapi.responses import JSONResponse

employee_router = APIRouter()


@employee_router.get(
    '/employees',
    tags=['employees'])
def get_employees():
    """Get the stored employees"""
    return JSONResponse(status_code=200, content={"mesagge": "employees"})
