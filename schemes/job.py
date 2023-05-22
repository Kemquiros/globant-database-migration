from pydantic import BaseModel, Field


class Job(BaseModel):
    id: int = Field(None, gt=0)
    job: str = Field(min_length=2, max_length=100)

    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'job': 'Recruiter'
            }
        }
