from sqlalchemy import Column, Float, Integer

from .base import Base


class PopulationDimension(Base):
    __tablename__ = "population_dimension"
    population_id = Column(Integer, primary_key=True)
    population = Column(Integer, nullable=False)
    normalized_score = Column(Float, nullable=True)
