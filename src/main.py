from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database.clients import postgres_client
from src.api.router import router as stock_prices_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to the Postgres database using Prisma on startup
    await postgres_client.connect()
    yield
    # Disconnect from the database on shutdown
    await postgres_client.disconnect()


app = FastAPI(
    title="Stock Prices Timeseries API",
    description="API for CRUD operations on stock_prices timeseries data.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(stock_prices_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Stock Prices Timeseries API"}
