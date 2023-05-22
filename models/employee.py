from config.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from department import Department
from job import Job


class Employee(Base):

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    datetime = Column(String)
    department_id = Column(Integer, ForeignKey(Department.id))
    job_id = Column(Integer, ForeignKey(Job.id))
