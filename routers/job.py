import codecs
import csv
from typing import List
from fastapi import APIRouter, Path
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemes.job import Job
from config.database import Session
from services.job import JobService
from config.upload_file import MIN_ROWS, MAX_ROWS

job_router = APIRouter()


@job_router.get(
    '/jobs',
    tags=['jobs'])
def get_jobs() -> List[Job]:
    """Get the stored jobs"""
    db = Session()
    result = JobService(db).get_jobs()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@job_router.get(
    '/jobs/{job_id}',
    tags=['jobs'])
def get_job(job_id: int = Path(ge=1, lt=10000)) -> Job:
    """Get an specific job by id"""
    db = Session()
    result = JobService(db).get_job_by_id(job_id)
    if not result:
        return JSONResponse(status_code=404, content={
            "message": "The job does not exist",
            "id": job_id
        })
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@job_router.post(
    '/jobs',
    tags=['jobs'],
    response_model=dict)
def create_job(job: Job) -> dict:
    """Create a new job"""
    db = Session()
    result = JobService(db).get_job_by_id(job.id)
    if not result:
        new_job = JobService(db).create_job(job)
        return JSONResponse(status_code=201, content={
            "message": "New job stored",
            "id": new_job.id
        })
    return JSONResponse(status_code=409, content={
        "message": "The job already exists",
        "id": job.id
    })


@job_router.post(
    '/jobs/upload',
    tags=['jobs'])
def upload_file(file: UploadFile = File(...)):
    """Create jobs from CSV file"""
    csv_reader = csv.DictReader(
        codecs.iterdecode(file.file, 'utf-8'),
        delimiter=",",
        fieldnames=['id', "job"])
    jobs = list(csv_reader)
    n_jobs = len(jobs)
    if n_jobs < MIN_ROWS:
        file.file.close()
        return JSONResponse(status_code=409, content={
            "message": "The file needs more rows",
            "min_rows": MIN_ROWS
        })
    elif n_jobs > MAX_ROWS:
        file.file.close()
        return JSONResponse(status_code=409, content={
            "message": "The file needs less rows",
            "max_rows": MAX_ROWS
        })
    else:
        db = Session()
        jobs = [Job(**job) for job in jobs]
        JobService(db).create_jobs(jobs)
        file.file.close()
        return JSONResponse(status_code=201, content={
            "message": "The file has been uploaded"
        })


@job_router.put(
    '/jobs/{job_id}',
    tags=['jobs'],
    response_model=dict)
def update_job(job_id: int, job: Job) -> dict:
    """Update an specific job by id"""
    db = Session()
    result = JobService(db).update_job(job_id, job)
    if not result:
        return JSONResponse(status_code=404, content={
            "message": "The job does not exist",
            "id": job_id
        })
    return JSONResponse(status_code=200, content={
        "message": "The job has been updated",
        "id": job_id
    })


@job_router.delete(
    '/jobs/{job_job_id}',
    tags=['jobs'],
    response_model=dict)
def delete_job(job_id: int) -> dict:
    """Delete an specific job by id"""
    db = Session()
    result = JobService(db).get_job_by_id(job_id)
    if not result:
        return JSONResponse(status_code=404, content={
            "message": "The job does not exist",
            "id": job_id
        })
    JobService(db).delete_job(result)
    return JSONResponse(status_code=200, content={
        "message": "The job has been deleted",
        "id": job_id
    })
