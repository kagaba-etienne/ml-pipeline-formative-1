-- ============================================================
-- Stock Prices Database Schema (PostgreSQL)
-- Tickers: AAPL, CAT, JPM, MCD, WMT
-- ============================================================

DROP TABLE IF EXISTS stock_prices CASCADE;
DROP TABLE IF EXISTS stocks CASCADE;
DROP TABLE IF EXISTS sectors CASCADE;

-- Table 1: sectors
CREATE TABLE sectors (
    sector_id   SERIAL PRIMARY KEY,
    sector_name VARCHAR(100) NOT NULL,
    description TEXT
);

-- Table 2: stocks
CREATE TABLE stocks (
    stock_id        SERIAL PRIMARY KEY,
    ticker          VARCHAR(10)  NOT NULL UNIQUE,
    company_name    VARCHAR(150) NOT NULL,
    sector_id       INT NOT NULL,
    listed_exchange VARCHAR(20) DEFAULT 'NASDAQ',
    CONSTRAINT fk_sector FOREIGN KEY (sector_id) REFERENCES sectors(sector_id)
);

-- Table 3: stock_prices (core time-series)
CREATE TABLE stock_prices (
    price_id    BIGSERIAL PRIMARY KEY,
    stock_id    INT           NOT NULL,
    trade_date  DATE          NOT NULL,
    open_price  DECIMAL(12,4) NOT NULL,
    high_price  DECIMAL(12,4) NOT NULL,
    low_price   DECIMAL(12,4) NOT NULL,
    close_price DECIMAL(12,4) NOT NULL,
    volume      BIGINT        NOT NULL,
    CONSTRAINT fk_stock      FOREIGN KEY (stock_id) REFERENCES stocks(stock_id),
    CONSTRAINT uq_stock_date UNIQUE (stock_id, trade_date)
);

CREATE INDEX idx_trade_date ON stock_prices(trade_date);
CREATE INDEX idx_stock_date ON stock_prices(stock_id, trade_date);

-- ============================================================
-- Seed: sectors
-- ============================================================
INSERT INTO sectors (sector_name, description) VALUES
('Technology',       'Software, hardware and consumer electronics'),
('Industrials',      'Heavy machinery and manufacturing'),
('Financials',       'Banking and financial services'),
('Consumer Staples', 'Essential everyday consumer goods');

-- ============================================================
-- Seed: stocks (only the 5 selected tickers)
-- ============================================================
INSERT INTO stocks (ticker, company_name, sector_id, listed_exchange) VALUES
('AAPL', 'Apple Inc',               1, 'NASDAQ'),
('CAT',  'Caterpillar Inc',         2, 'NYSE'),
('JPM',  'JPMorgan Chase & Co',     3, 'NYSE'),
('MCD',  'McDonalds Corporation',   4, 'NYSE'),
('WMT',  'Walmart Inc',             4, 'NYSE');