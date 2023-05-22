from pydantic import BaseModel, Field


class Employee(BaseModel):
    id: int = Field(None, gt=0)
    name: str = Field(min_length=2, max_length=50)
    datetime: str = Field(length=20)
    department_id: int = Field(gt=0, lt=9999)
    job_id: int = Field(gt=0, lt=9999)

    class Config:
        schema_extra = {
            'example': {
                'id': 4535,
                'name': ',Marcelo Gonzalez',
                'datetime': '2021-07-27T16:02:08Z',
                'department_id': 1,
                'job_id': 2
            }
        }
