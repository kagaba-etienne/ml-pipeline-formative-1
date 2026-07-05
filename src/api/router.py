from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import date
from src.schemas.stock_prices import (
    StockPriceCreate,
    StockPriceUpdate,
    StockPriceResponse,
    StockPriceFilter,
)
from src.services.timeseries_service import TimeseriesService, get_timeseries_service

router = APIRouter(prefix="/api/stock-prices", tags=["Stock Prices"])


@router.post("/", response_model=StockPriceResponse, status_code=201)
async def create_stock_price(
    data: StockPriceCreate, service: TimeseriesService = Depends(get_timeseries_service)
):
    try:
        return await service.create_stock_price(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[StockPriceResponse])
async def get_stock_prices(
    stock_id: Optional[int] = Query(None, description="Filter by stock ID"),
    ticker: Optional[str] = Query(None, description="Filter by stock ticker"),
    start_date: Optional[date] = Query(
        None, description="Filter by start date (inclusive)"
    ),
    end_date: Optional[date] = Query(
        None, description="Filter by end date (inclusive)"
    ),
    min_price: Optional[float] = Query(
        None, description="Filter by minimum close price"
    ),
    max_price: Optional[float] = Query(
        None, description="Filter by maximum close price"
    ),
    min_volume: Optional[int] = Query(None, description="Filter by minimum volume"),
    max_volume: Optional[int] = Query(None, description="Filter by maximum volume"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    service: TimeseriesService = Depends(get_timeseries_service),
):
    filters = StockPriceFilter(
        stock_id=stock_id,
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        min_price=min_price,
        max_price=max_price,
        min_volume=min_volume,
        max_volume=max_volume,
    )

    try:
        return await service.get_stock_prices(filters, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{price_id}", response_model=StockPriceResponse)
async def get_stock_price(
    price_id: int, service: TimeseriesService = Depends(get_timeseries_service)
):
    price = await service.get_stock_price_by_id(price_id)
    if not price:
        raise HTTPException(status_code=404, detail="Stock price not found")
    return price


@router.put("/{price_id}", response_model=StockPriceResponse)
async def update_stock_price(
    price_id: int,
    data: StockPriceUpdate,
    service: TimeseriesService = Depends(get_timeseries_service),
):
    price = await service.get_stock_price_by_id(price_id)
    if not price:
        raise HTTPException(status_code=404, detail="Stock price not found")

    try:
        return await service.update_stock_price(price_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{price_id}", status_code=204)
async def delete_stock_price(
    price_id: int, service: TimeseriesService = Depends(get_timeseries_service)
):
    price = await service.get_stock_price_by_id(price_id)
    if not price:
        raise HTTPException(status_code=404, detail="Stock price not found")

    try:
        await service.delete_stock_price(price_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
