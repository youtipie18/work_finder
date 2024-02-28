from sqlalchemy import Column, String, Integer
from db import Base


class User(Base):
    __tablename__ = "user"
    user_id = Column("user_id", Integer, primary_key=True, unique=True)
    full_name = Column("full_name", String, nullable=False)
    job_title = Column("job", String, nullable=False)

    def __init__(self, user_id, full_name, job_title):
        self.user_id = user_id
        self.full_name = full_name
        self.job_title = job_title


class Job(Base):
    __tablename__ = "job"
    job_id = Column("job_id", Integer, primary_key=True, unique=True)
    title = Column("title", String, nullable=False)
    requirements = Column("requirements", String, nullable=False)
    description = Column("description", String, nullable=False)
    url = Column("url", String, nullable=False, unique=True)

    def __eq__(self, other):
        return isinstance(other, Job) and self.url == other.url
