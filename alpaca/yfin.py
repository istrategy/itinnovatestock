import yfinance as yf

data = yf.download("MTN ABG.JO", start="2022-02-01", end="2022-02-17")

print(data)

# https://finnhub.io/docs/api/stock-symbols