from sqlalchemy import Column, Float, Integer

from models.base import Base


class TradeDimension(Base):
    __tablename__ = "trade_dimension"

    trade_id = Column(Integer, primary_key=True)
    total_trade = Column(Float)
