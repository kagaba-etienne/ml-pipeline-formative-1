import os
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("MONGODB_DATABASE_URL")
DATABASE_NAME = os.environ.get("MONGODB_DATABASE_NAME", "market_data")


def run_queries():
    if not DATABASE_URL:
        raise ValueError("MONGODB_DATABASE_URL environment variable is missing.")

    client = MongoClient(DATABASE_URL)
    db = client[DATABASE_NAME]

    print(
        f"\n{'-'*80}\nQuery 1: Latest closing price for each of the 5 stocks\n{'-'*80}"
    )
    pipeline_1 = [
        {"$sort": {"ticker": 1, "trade_date": -1}},
        {
            "$group": {
                "_id": "$ticker",
                "latest_date": {"$first": "$trade_date"},
                "latest_close": {"$first": "$close_price"},
                "volume": {"$first": "$volume"},
                "stockId": {"$first": "$stockId"},
            }
        },
        {
            "$lookup": {
                "from": "stocks",
                "localField": "stockId",
                "foreignField": "_id",
                "as": "stock_info",
            }
        },
        {"$unwind": "$stock_info"},
        {
            "$project": {
                "_id": 0,
                "ticker": "$_id",
                "company_name": "$stock_info.company_name",
                "latest_date": 1,
                "latest_close": 1,
                "volume": 1,
            }
        },
        {"$sort": {"ticker": 1}},
    ]
    df1 = pd.DataFrame(list(db.stock_prices.aggregate(pipeline_1)))
    print(df1.to_string(index=False))

    print(
        f"\n{'-'*80}\nQuery 2: Date-range – all AAPL prices in 2017 (First 5 rows)\n{'-'*80}"
    )
    pipeline_2 = [
        {
            "$match": {
                "ticker": "AAPL",
                "trade_date": {
                    "$gte": datetime(2017, 1, 1),
                    "$lte": datetime(2017, 12, 31),
                },
            }
        },
        {"$sort": {"trade_date": 1}},
        {"$limit": 5},
        {"$project": {"_id": 0, "stockId": 0, "ticker": 0}},
    ]
    df2 = pd.DataFrame(list(db.stock_prices.aggregate(pipeline_2)))
    print(df2.to_string(index=False))

    print(
        f"\n{'-'*80}\nQuery 3: 7-day moving average of close price – JPM (First 5 rows)\n{'-'*80}"
    )
    pipeline_3 = [
        {"$match": {"ticker": "JPM"}},
        {
            "$setWindowFields": {
                "partitionBy": "$ticker",
                "sortBy": {"trade_date": 1},
                "output": {
                    "moving_avg_7d": {
                        "$avg": "$close_price",
                        "window": {"documents": [-6, 0]},
                    }
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "trade_date": 1,
                "close_price": 1,
                "moving_avg_7d": {"$round": ["$moving_avg_7d", 4]},
            }
        },
        {"$sort": {"trade_date": 1}},
        {"$limit": 5},
    ]
    df3 = pd.DataFrame(list(db.stock_prices.aggregate(pipeline_3)))
    print(df3.to_string(index=False))

    print(
        f"\n{'-'*80}\nQuery 4: Average annual close price per stock (First 10 rows)\n{'-'*80}"
    )
    pipeline_4 = [
        {
            "$group": {
                "_id": {"ticker": "$ticker", "year": {"$year": "$trade_date"}},
                "avg_close": {"$avg": "$close_price"},
                "max_close": {"$max": "$close_price"},
                "min_close": {"$min": "$close_price"},
            }
        },
        {
            "$project": {
                "_id": 0,
                "ticker": "$_id.ticker",
                "year": "$_id.year",
                "avg_close": {"$round": ["$avg_close", 2]},
                "max_close": {"$round": ["$max_close", 2]},
                "min_close": {"$round": ["$min_close", 2]},
            }
        },
        {"$sort": {"ticker": 1, "year": 1}},
        {"$limit": 10},
    ]
    df4 = pd.DataFrame(list(db.stock_prices.aggregate(pipeline_4)))
    # Reorder columns
    df4 = df4[["ticker", "year", "avg_close", "max_close", "min_close"]]
    print(df4.to_string(index=False))

    print(
        f"\n{'-'*80}\nQuery 5: Most volatile stock (highest std-dev of close price)\n{'-'*80}"
    )
    pipeline_5 = [
        {
            "$group": {
                "_id": {"ticker": "$ticker", "stockId": "$stockId"},
                "price_std_dev": {"$stdDevSamp": "$close_price"},
                "avg_close": {"$avg": "$close_price"},
            }
        },
        {
            "$lookup": {
                "from": "stocks",
                "localField": "_id.stockId",
                "foreignField": "_id",
                "as": "stock_info",
            }
        },
        {"$unwind": "$stock_info"},
        {
            "$project": {
                "_id": 0,
                "ticker": "$_id.ticker",
                "company_name": "$stock_info.company_name",
                "price_std_dev": {"$round": ["$price_std_dev", 4]},
                "avg_close": {"$round": ["$avg_close", 2]},
            }
        },
        {"$sort": {"price_std_dev": -1}},
    ]
    df5 = pd.DataFrame(list(db.stock_prices.aggregate(pipeline_5)))
    print(df5.to_string(index=False))

    client.close()


if __name__ == "__main__":
    run_queries()
