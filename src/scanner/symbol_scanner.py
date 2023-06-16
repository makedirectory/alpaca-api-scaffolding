import pandas as pd
import alpaca_trade_api as tradeapi

class SymbolScanner:
    def __init__(self, api):
        self.api = api

    def scan_symbols(self, symbols):
        """Scans symbols and returns those where the last close price is above their 14-day moving average."""
        above_avg_symbols = []

        for symbol in symbols:
            # Get the barset (historical price and volume data) for the symbol
            barset = self.api.get_bars(symbol, tradeapi.rest.TimeFrame.Day, limit=15) # Fetch data for the past 15 days

            if not barset or len(barset[symbol]) < 15:  # Skip symbols with insufficient data
                continue

            # Extract the close prices from the barset
            close_prices = [bar.c for bar in barset[symbol]]

            # Calculate the 14-day moving average
            avg = pd.Series(close_prices).rolling(window=14).mean().iloc[-1]

            # Compare the last close price with the average
            if close_prices[-1] > avg:
                above_avg_symbols.append(symbol)

        return above_avg_symbols
