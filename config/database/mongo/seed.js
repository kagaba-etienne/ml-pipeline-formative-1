// seed.js
use('market_data');

// 1. Clean up existing collections
db.sectors.drop();
db.stocks.drop();
db.stock_prices.drop();

// ============================================================
// Seed 1: Sectors
// ============================================================
const sectorsData = [
  { name: "Technology",       description: "Software, hardware and consumer electronics" },
  { name: "Industrials",      description: "Heavy machinery and manufacturing" },
  { name: "Financials",       description: "Banking and financial services" },
  { name: "Consumer Staples", description: "Essential everyday consumer goods" }
];

db.sectors.insertMany(sectorsData);
print("Sectors inserted.");

// ============================================================
// Seed 2: Stocks (Linked to Sectors)
// ============================================================
// Fetch the newly created sectors so we can use their _ids
const techSector = db.sectors.findOne({ name: "Technology" });
const indSector = db.sectors.findOne({ name: "Industrials" });
const finSector = db.sectors.findOne({ name: "Financials" });
const stapleSector = db.sectors.findOne({ name: "Consumer Staples" });

const stocksData = [
  { ticker: "AAPL", company_name: "Apple Inc", listed_exchange: "NASDAQ", sector_id: techSector._id },
  { ticker: "CAT",  company_name: "Caterpillar Inc", listed_exchange: "NYSE", sector_id: indSector._id },
  { ticker: "JPM",  company_name: "JPMorgan Chase & Co", listed_exchange: "NYSE", sector_id: finSector._id },
  { ticker: "MCD",  company_name: "McDonalds Corporation", listed_exchange: "NYSE", sector_id: stapleSector._id },
  { ticker: "WMT",  company_name: "Walmart Inc", listed_exchange: "NYSE", sector_id: stapleSector._id }
];

db.stocks.insertMany(stocksData);
print("Stocks inserted and linked to sectors.");

// Create unique index for ticker
db.stocks.createIndex({ ticker: 1 }, { unique: true });

// ============================================================
// Seed 3: Stock Prices (Linked to Stocks)
// ============================================================
// Let's insert a sample price for AAPL to show how the linking works
const aaplStock = db.stocks.findOne({ ticker: "AAPL" });

db.stock_prices.insertOne({
  stock_id: aaplStock._id,
  trade_date: new Date("2026-07-05T00:00:00Z"),
  open_price: 150.50,
  high_price: 153.20,
  low_price: 149.80,
  close_price: 152.10,
  volume: 45000000
});
print("Sample stock price inserted and linked to AAPL.");

// Create indexes for efficient querying
db.stock_prices.createIndex({ stock_id: 1, trade_date: -1 });

print("Relational database seeded successfully!");