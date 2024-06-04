from sqlalchemy import Column, Integer

from models.base import Base


class TimeDimension(Base):
    __tablename__ = "time_dimension"
    time_id = Column(Integer, primary_key=True)
    year = Column(Integer, unique=True, nullable=False)
