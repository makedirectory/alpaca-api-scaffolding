# Historical Data: https://alpaca.markets/docs/python-sdk/market_data.html?highlight=bars#historical-data
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import logging

logger = logging.getLogger()

class AlpacaHistData:
    def __init__(self, api_key, secret_key):
        self.client = StockHistoricalDataClient(api_key, secret_key)

    # multi symbol request
    def get_hist_all_ticker_data(self, symbols):            
        # Example usage
        # gld_latest_ask_price = latest_multisymbol_quotes["GLD"].ask_price
        try: 
            multisymbol_request_params = StockLatestQuoteRequest(symbol_or_symbols=[symbols])
            latest_multisymbol_quotes = self.client.get_stock_latest_quote(multisymbol_request_params)
            for symbol in latest_multisymbol_quotes:
                return symbol
        except Exception as e:
            print(f"error: {e}")
        return None
    
    # single symbol request
    def get_hist_ticker_data(self, symbol):            
        # Example usage: must use symbol to access even though it is single symbol
        # latest_quote["ETH/USD"].ask_price
        try: 
            request_params = StockLatestQuoteRequest(symbol_or_symbols=symbol)
            latest_quotes = self.client.get_stock_latest_quote(request_params)
            return latest_quotes
        except Exception as e:
            print(f"error: {e}")
        return None
    
    # Get candle stick values for single or multiple symbols
    def get_candle_for_all_ticker(self, symbols, start, end, timeframe=TimeFrame.Day):
        # access bars as list - important to note that you must access by symbol key
        # even for a single symbol request - models are agnostic to number of symbols
        # Ex: bars["NVDA", "AAPL"]
        # TODO: Handle single vs multiple request.
        request_params = StockBarsRequest(
            symbol_or_symbols=symbols,
            timeframe=timeframe,
            start=start, # Ex:  datetime(2022, 7, 1),
            end=end # Ex: datetime(2022, 9, 1)
        )
        bars = self.client.get_stock_bars(request_params)
        candles = bars.df
        # convert to dataframe
        return candles
    
    