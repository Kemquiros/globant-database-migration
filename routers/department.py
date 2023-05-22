from fastapi import APIRouter
from fastapi.responses import JSONResponse

department_router = APIRouter()


@department_router.get(
    '/departments',
    tags=['departments'])
def get_departments():
    """Get the stored departments"""
    return JSONResponse(status_code=200, content={"mesagge": "departments"})
