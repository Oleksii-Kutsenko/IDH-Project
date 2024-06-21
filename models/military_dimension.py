from sqlalchemy import Column, Float, Integer

from .base import Base


class MilitaryDimension(Base):
    __tablename__ = "military_dimension"
    military_id = Column(Integer, primary_key=True)
    military_spending = Column(Float, nullable=False)
    normalized_score = Column(Float, nullable=True)
