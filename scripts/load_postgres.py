import os
import pandas as pd
import urllib.parse
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv

load_dotenv()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_CSV_PATH = os.path.join(
    PROJECT_ROOT, "dataset", "stocks_dataset.csv"
)

DATABASE_URL = os.environ.get("POSTGRES_DATABASE_URL")
CSV_PATH = os.getenv("CSV_PATH", DEFAULT_CSV_PATH)
TICKERS = {"AAPL", "CAT", "JPM", "MCD", "WMT"}


def load_data():
    if not DATABASE_URL:
        raise ValueError("POSTGRES_DATABASE_URL environment variable is missing.")

    parsed = urllib.parse.urlparse(DATABASE_URL)
    query_params = urllib.parse.parse_qsl(parsed.query)
    safe_params = [
        (k, v) for k, v in query_params if k not in ("schema", "connection_limit")
    ]
    clean_url = urllib.parse.urlunparse(
        parsed._replace(query=urllib.parse.urlencode(safe_params))
    )

    print("Connecting to PostgreSQL...")
    conn = psycopg2.connect(clean_url)
    cursor = conn.cursor()

    print("Reading CSV...")
    df = pd.read_csv(CSV_PATH, parse_dates=["Date"])
    df.rename(
        columns={
            "Date": "trade_date",
            "Open": "open_price",
            "High": "high_price",
            "Low": "low_price",
            "Close": "close_price",
            "Volume": "volume",
            "Name": "ticker",
        },
        inplace=True,
    )

    df = df[df["ticker"].isin(TICKERS)]
    df.dropna(subset=["trade_date", "close_price"], inplace=True)

    cursor.execute("SELECT stock_id, ticker FROM stocks")
    ticker_map = {row[1]: row[0] for row in cursor.fetchall()}

    insert_sql = """
        INSERT INTO stock_prices
            (stock_id, trade_date, open_price, high_price, low_price, close_price, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (stock_id, trade_date) DO NOTHING
    """

    rows = [
        (
            ticker_map[r["ticker"]],
            r["trade_date"].date(),
            float(r["open_price"]),
            float(r["high_price"]),
            float(r["low_price"]),
            float(r["close_price"]),
            int(r["volume"]),
        )
        for _, r in df.iterrows()
        if r["ticker"] in ticker_map
    ]

    print(f"Executing batch insert for {len(rows)} rows...")
    extras.execute_batch(cursor, insert_sql, rows, page_size=2000)
    conn.commit()

    print("PostgreSQL load complete.")
    cursor.close()
    conn.close()


if __name__ == "__main__":
    load_data()
