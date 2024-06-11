from sqlalchemy import Column, Float, Integer

from models.base import Base


class EconomicDimension(Base):
    __tablename__ = "economic_dimension"
    economic_id = Column(Integer, primary_key=True)
    country_gdp = Column(Float, nullable=False)
