from sqlalchemy import Column, Integer, String

from .base import Base


class CountryDimension(Base):
    __tablename__ = "country_dimension"
    country_id = Column(Integer, primary_key=True)
    country_code = Column(String, nullable=False)
    country_name = Column(String, nullable=False)
