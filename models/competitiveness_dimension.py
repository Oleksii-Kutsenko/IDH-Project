from sqlalchemy import Column, Float, Integer

from models.base import Base


class CompetitivenessDimension(Base):
    __tablename__ = "competitiveness_dimension"
    competitiveness_id = Column(Integer, primary_key=True)
    export_value = Column(Float)
    normalized_score = Column(Float, nullable=True)
