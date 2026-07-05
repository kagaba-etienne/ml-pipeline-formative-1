from datetime import datetime, date
from decimal import Decimal
from generated.postgres_client import Prisma
from src.database.clients import postgres_client
from src.schemas.stock_prices import (
    StockPriceCreate,
    StockPriceUpdate,
    StockPriceFilter,
)


class TimeseriesService:
    def __init__(self, db: Prisma):
        self.db = db

    async def create_stock_price(self, data: StockPriceCreate):
        # Insert into Postgres
        # We need to cast Pydantic floats to Decimal for Prisma if required, but Prisma Python usually handles float inputs directly for Decimal fields.
        created = await self.db.stock_prices.create(
            data={
                "stock_id": data.stock_id,
                "trade_date": datetime.combine(data.trade_date, datetime.min.time()),
                "open_price": data.open_price,
                "high_price": data.high_price,
                "low_price": data.low_price,
                "close_price": data.close_price,
                "volume": data.volume,
            }
        )
        return created

    async def get_stock_prices(
        self, filters: StockPriceFilter, skip: int = 0, limit: int = 100
    ):
        # Build where clause
        where = {}

        if filters.stock_id is not None:
            where["stock_id"] = filters.stock_id

        if filters.ticker is not None:
            # Join with stocks table to filter by ticker
            where["stocks"] = {"is": {"ticker": filters.ticker}}

        if filters.start_date is not None or filters.end_date is not None:
            date_filter = {}
            if filters.start_date is not None:
                date_filter["gte"] = datetime.combine(
                    filters.start_date, datetime.min.time()
                )
            if filters.end_date is not None:
                date_filter["lte"] = datetime.combine(
                    filters.end_date, datetime.min.time()
                )
            where["trade_date"] = date_filter

        # Price filters - filtering based on close_price for min/max
        if filters.min_price is not None or filters.max_price is not None:
            price_filter = {}
            if filters.min_price is not None:
                price_filter["gte"] = filters.min_price
            if filters.max_price is not None:
                price_filter["lte"] = filters.max_price
            where["close_price"] = price_filter

        if filters.min_volume is not None or filters.max_volume is not None:
            vol_filter = {}
            if filters.min_volume is not None:
                vol_filter["gte"] = filters.min_volume
            if filters.max_volume is not None:
                vol_filter["lte"] = filters.max_volume
            where["volume"] = vol_filter

        prices = await self.db.stock_prices.find_many(
            where=where, skip=skip, take=limit, order={"trade_date": "desc"}
        )
        return prices

    async def get_stock_price_by_id(self, price_id: int):
        price = await self.db.stock_prices.find_unique(where={"price_id": price_id})
        return price

    async def update_stock_price(self, price_id: int, data: StockPriceUpdate):
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}

        if not update_data:
            return await self.get_stock_price_by_id(price_id)

        updated = await self.db.stock_prices.update(
            where={"price_id": price_id}, data=update_data
        )
        return updated

    async def delete_stock_price(self, price_id: int):
        deleted = await self.db.stock_prices.delete(where={"price_id": price_id})
        return deleted


# Dependency
def get_timeseries_service():
    return TimeseriesService(postgres_client)
