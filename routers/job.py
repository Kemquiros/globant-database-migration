from typing import List
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from schemes.job import Job

job_router = APIRouter()


@job_router.get(
    '/jobs',
    tags=['jobs'])
def get_jobs() -> List[Job]:
    """Get the stored jobs"""
    return JSONResponse(status_code=200, content={"mesagge": "jobs"})
