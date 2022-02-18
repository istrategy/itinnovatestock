import yfinance as yf

data = yf.download("ABG.JO", start="2022-01-01", end="2022-02-17")

print(data)

# https://finnhub.io/docs/api/stock-symbols