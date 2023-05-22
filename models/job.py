from config.database import Base
from sqlalchemy import Column, Integer, String


class JobModel(Base):

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    job = Column(String(100))
