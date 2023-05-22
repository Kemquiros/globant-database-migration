from typing import List
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from schemes.department import Department

department_router = APIRouter()


@department_router.get(
    '/departments',
    tags=['departments'])
def get_departments() -> List[Department]:
    """Get the stored departments"""
    return JSONResponse(status_code=200, content={"mesagge": "departments"})
