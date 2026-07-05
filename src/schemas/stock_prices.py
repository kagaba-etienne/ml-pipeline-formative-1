from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class StockPriceBase(BaseModel):
    stock_id: int = Field(..., description="The ID of the stock")
    trade_date: date = Field(..., description="Date of the trade")
    open_price: float = Field(..., description="Opening price")
    high_price: float = Field(..., description="Highest price during the trading day")
    low_price: float = Field(..., description="Lowest price during the trading day")
    close_price: float = Field(..., description="Closing price")
    volume: int = Field(..., description="Trading volume")


class StockPriceCreate(StockPriceBase):
    pass


class StockPriceUpdate(BaseModel):
    open_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    close_price: Optional[float] = None
    volume: Optional[int] = None


class StockPriceResponse(StockPriceBase):
    price_id: int

    class Config:
        from_attributes = True


class StockPriceFilter(BaseModel):
    stock_id: Optional[int] = None
    ticker: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_volume: Optional[int] = None
    max_volume: Optional[int] = None
