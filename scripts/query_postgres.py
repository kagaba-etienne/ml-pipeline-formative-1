import os
import urllib.parse
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv()

DATABASE_URL = os.environ.get("POSTGRES_DATABASE_URL")

QUERIES = {
    "Query 1: Latest closing price for each of the 5 stocks": """
        SELECT
            s.ticker,
            s.company_name,
            sp.trade_date AS latest_date,
            sp.close_price AS latest_close,
            sp.volume
        FROM stock_prices sp
        JOIN stocks s ON s.stock_id = sp.stock_id
        WHERE sp.trade_date = (
            SELECT MAX(trade_date) FROM stock_prices sp2
            WHERE sp2.stock_id = sp.stock_id
        )
        ORDER BY s.ticker;
    """,
    "Query 2: Date-range – all AAPL prices in 2017 (First 5 rows)": """
        SELECT
            sp.trade_date,
            sp.open_price, sp.high_price,
            sp.low_price,  sp.close_price,
            sp.volume
        FROM stock_prices sp
        JOIN stocks s ON s.stock_id = sp.stock_id
        WHERE s.ticker = 'AAPL'
          AND sp.trade_date >= '2017-01-01' AND sp.trade_date <= '2017-12-31'
        ORDER BY sp.trade_date
        LIMIT 5;
    """,
    "Query 3: 7-day moving average of close price – JPM (First 5 rows)": """
        SELECT
            sp.trade_date,
            sp.close_price,
            ROUND(
                AVG(sp.close_price) OVER (
                    ORDER BY sp.trade_date
                    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
                )::numeric, 4
            ) AS moving_avg_7d
        FROM stock_prices sp
        JOIN stocks s ON s.stock_id = sp.stock_id
        WHERE s.ticker = 'JPM'
        ORDER BY sp.trade_date
        LIMIT 5;
    """,
    "Query 4: Average annual close price per stock (First 10 rows)": """
        SELECT
            s.ticker,
            EXTRACT(YEAR FROM sp.trade_date) AS year,
            ROUND(AVG(sp.close_price)::numeric, 2) AS avg_close,
            ROUND(MAX(sp.close_price)::numeric, 2) AS max_close,
            ROUND(MIN(sp.close_price)::numeric, 2) AS min_close
        FROM stock_prices sp
        JOIN stocks s ON s.stock_id = sp.stock_id
        GROUP BY s.ticker, EXTRACT(YEAR FROM sp.trade_date)
        ORDER BY s.ticker, year
        LIMIT 10;
    """,
    "Query 5: Most volatile stock (highest std-dev of close price)": """
        SELECT
            s.ticker,
            s.company_name,
            ROUND(STDDEV_SAMP(sp.close_price)::numeric, 4) AS price_std_dev,
            ROUND(AVG(sp.close_price)::numeric, 2) AS avg_close
        FROM stock_prices sp
        JOIN stocks s ON s.stock_id = sp.stock_id
        GROUP BY s.stock_id, s.ticker, s.company_name
        ORDER BY price_std_dev DESC;
    """,
}


def run_queries():
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

    conn = psycopg2.connect(clean_url)

    for title, sql in QUERIES.items():
        print(f"\n{'-'*80}\n{title}\n{'-'*80}")
        df = pd.read_sql_query(sql, conn)
        print(df.to_string(index=False))

    conn.close()


if __name__ == "__main__":
    run_queries()
