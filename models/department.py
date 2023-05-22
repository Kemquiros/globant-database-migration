from config.database import Base
from sqlalchemy import Column, Integer, String


class DepartmentModel(Base):

    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    department = Column(String(100))
