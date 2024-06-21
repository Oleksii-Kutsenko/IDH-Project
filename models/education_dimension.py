from sqlalchemy import Column, Float, Integer

from .base import Base


class EducationDimension(Base):
    __tablename__ = "education_dimension"
    education_id = Column(Integer, primary_key=True)
    math_score = Column(Float, nullable=False)
    science_score = Column(Float, nullable=False)
    reading_score = Column(Float, nullable=False)
    pisa_average_score = Column(Float, nullable=False)  # Average of math, science, and reading scores
    normalized_score = Column(Float, nullable=True)
