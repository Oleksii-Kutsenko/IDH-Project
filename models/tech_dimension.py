from sqlalchemy import Column, Integer, Float

from .base import Base


class TechDimension(Base):
    __tablename__ = "tech_dimension"
    tech_id = Column(Integer, primary_key=True)
    rnd_spending = Column(Float, nullable=False)
    nature_count = Column(Float, nullable=False)
    nature_share = Column(Float, nullable=False)
