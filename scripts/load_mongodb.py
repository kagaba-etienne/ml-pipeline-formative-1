import os
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from dotenv import load_dotenv

load_dotenv()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_CSV_PATH = os.path.join(PROJECT_ROOT, "dataset", "all_stocks_2006-01-01_to_2018-01-01.csv")

DATABASE_URL = os.environ.get("MONGODB_DATABASE_URL")
DATABASE_NAME = os.environ.get("MONGODB_DATABASE_NAME", "market_data")
CSV_PATH = os.getenv("CSV_PATH", DEFAULT_CSV_PATH)
TICKERS = {'AAPL', 'CAT', 'JPM', 'MCD', 'WMT'}

def load_data():
    if not DATABASE_URL:
        raise ValueError("MONGODB_DATABASE_URL environment variable is missing.")

    print("Connecting to MongoDB...")
    client = MongoClient(DATABASE_URL)
    db = client[DATABASE_NAME]

    print("Reading CSV...")
    df = pd.read_csv(CSV_PATH, parse_dates=["Date"])
    df.rename(columns={
        "Date": "trade_date",
        "Open": "open_price",
        "High": "high_price",
        "Low": "low_price",
        "Close": "close_price",
        "Volume": "volume",
        "Name": "ticker"
    }, inplace=True)
    
    df = df[df["ticker"].isin(TICKERS)]
    df.dropna(subset=["trade_date", "close_price"], inplace=True)

    stock_docs = list(db.stocks.find({"ticker": {"$in": list(TICKERS)}}, {"_id": 1, "ticker": 1}))
    ticker_map = {doc["ticker"]: doc["_id"] for doc in stock_docs}

    documents = []
    for _, r in df.iterrows():
        if r["ticker"] in ticker_map:
            documents.append({
                "stockId": ticker_map[r["ticker"]],
                "ticker": r["ticker"],
                "trade_date": r["trade_date"],
                "open_price": float(r["open_price"]),
                "high_price": float(r["high_price"]),
                "low_price": float(r["low_price"]),
                "close_price": float(r["close_price"]),
                "volume": int(r["volume"])
            })

    print(f"Preparing batch insert for {len(documents)} documents...")
    
    try:
        db.stock_prices.insert_many(documents, ordered=False)
        print(f"MongoDB load complete: {len(documents)} inserted.")
    except BulkWriteError as bwe:
        inserted = bwe.details['nInserted']
        print(f"MongoDB load complete: {inserted} inserted (ignored duplicates).")
    finally:
        client.close()

if __name__ == "__main__":
    load_data()