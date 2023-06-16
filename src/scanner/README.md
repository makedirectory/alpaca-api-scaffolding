
Here's how you can use this class in your trading_bot.py:

```python
from alpaca_api import AlpacaAPI
from symbol_scanner import SymbolScanner

api = AlpacaAPI('<APCA-API-KEY-ID>', '<APCA-API-SECRET-KEY>', 'https://paper-api.alpaca.markets')
scanner = SymbolScanner(api)

# Scan symbols
symbols = ['AAPL', 'GOOGL', 'TSLA', 'AMZN', 'NFLX']
above_avg_symbols = scanner.scan_symbols(symbols)

# Print the symbols with high price
print("Symbols with last close price above 14-day moving average:")
for symbol in above_avg_symbols:
    print(symbol)
```

This will print the symbols where the last close price is above their 14-day moving average. Remember to replace the placeholders with your actual Alpaca API credentials.