from models.job import JobModel
from schemes.job import Job


class JobService():

    def __init__(self, db) -> None:
        # Bind the database session to the instance
        self.db = db

    def get_jobs(self):
        result = self.db.query(JobModel).all()
        return result

    def get_job_by_id(self, id: int):
        result = self.db.query(JobModel).filter(
            JobModel.id == id).first()
        return result

    def create_job(self, job: Job):
        new_job = JobModel(**job.dict())
        self.db.add(new_job)
        self.db.commit()
        return new_job

    def update_job(self, job_id: int, job: Job):
        updating_job = self.db.query(JobModel).filter(
            JobModel.id == job_id).first()
        if not updating_job:
            return None
        updating_job.id = job.id
        updating_job.job = job.job
        self.db.commit()
        return updating_job

    def delete_job(self, job: Job):
        self.db.delete(job)
        self.db.commit()
