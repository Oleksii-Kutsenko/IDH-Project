from sqlalchemy import Column, Integer, Float

from .base import Base


class MilitaryDimension(Base):
    __tablename__ = "military_dimension"
    military_id = Column(Integer, primary_key=True)
    military_spending = Column(Float, nullable=False)
