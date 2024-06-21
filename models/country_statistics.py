from sqlalchemy import Column, ForeignKey, Integer

from models.base import Base


class CountryStatistics(Base):
    __tablename__ = "country_statistics"

    statistics_id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey("country_dimension.country_id"), nullable=False)
    time_id = Column(Integer, ForeignKey("time_dimension.time_id"), nullable=False)
    education_id = Column(Integer, ForeignKey("education_dimension.education_id"))
    technology_id = Column(Integer, ForeignKey("tech_dimension.tech_id"))
    military_id = Column(Integer, ForeignKey("military_dimension.military_id"))
    competitiveness_id = Column(Integer, ForeignKey("competitiveness_dimension.competitiveness_id"))
    trade_id = Column(Integer, ForeignKey("trade_dimension.trade_id"))
    # financial_center_id = Column(Integer, ForeignKey("financial_center_dimension.financial_center_id"))
    economic_id = Column(Integer, ForeignKey("economic_dimension.economic_id"))
    # reserve_currency_id = Column(Integer, ForeignKey("reserve_currency_dimension.reserve_currency_id"))       
