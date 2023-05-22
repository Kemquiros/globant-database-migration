from fastapi import APIRouter
from fastapi.responses import JSONResponse

job_router = APIRouter()


@job_router.get(
    '/jobs',
    tags=['jobs'])
def get_jobs():
    """Get the stored jobs"""
    return JSONResponse(status_code=200, content={"mesagge": "jobs"})
