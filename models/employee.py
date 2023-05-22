from config.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from .department import DepartmentModel
from .job import JobModel


class EmployeeModel(Base):

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    datetime = Column(String(20))
    department_id = Column(Integer, ForeignKey(DepartmentModel.id))
    job_id = Column(Integer, ForeignKey(JobModel.id))
