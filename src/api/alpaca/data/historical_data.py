import logging

# Historical Data: https://alpaca.markets/docs/python-sdk/market_data.html?highlight=bars#historical-data
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.requests import StockBarsRequest

logger = logging.getLogger()

class AlpacaHistData:
    def __init__(self, asset_hist_client):
        self.hist_api = asset_hist_client

    # multi symbol request
    def get_hist_ticker_data_multi(self, symbols):   
        if symbols is None:
            logger.error("Missing symbols for ticker history")         
        # Example usage
        # gld_latest_ask_price = latest_multisymbol_quotes["GLD"].ask_price
        try: 
            multisymbol_request_params = StockLatestQuoteRequest(
                symbol_or_symbols=[symbols]

            )
            latest_multisymbol_quotes = self.hist_api.get_stock_latest_quote(multisymbol_request_params)
            for symbol in latest_multisymbol_quotes:
                return symbol
        except Exception as e:
            print(f"error: {e}")
        return None
    
    # single symbol request
    def get_latest_quote(self, symbol):
        if symbol is None:
            logger.error("Missing symbols for ticker quote")               
        # Example usage: must use symbol to access even though it is single symbol
        # latest_quote["ETH/USD"].ask_price
        try: 
            request_params = StockLatestQuoteRequest(
                symbol_or_symbols=symbol
            )
            latest_quotes = self.hist_api.get_stock_latest_quote(request_params)
            return latest_quotes
        except Exception as e:
            print(f"error: {e}")
        return None
    
    # Get candle stick values for single or multiple symbols
    def get_bars_for_ticker(self, symbols, start, end, timeframe):
        # access bars as list - important to note that you must access by symbol key
        # even for a single symbol request - models are agnostic to number of symbols
        # Ex: bars["NVDA", "AAPL"]
        # TODO: Handle single vs multiple request.

        if symbols is None:
            logger.error("Missing symbols for ticker bars")   

        if start is None or end is None:
            logger.error("Missing start or end for ticker bars")   

        # Make sure start is earlier than now
        if timeframe is None:
            raise ValueError("Timeframe is not defined.")

        # Make sure start is earlier than now
        if start > end:
            raise ValueError("Start datetime is after end datetime")
        
        request_params = StockBarsRequest(
            symbol_or_symbols=symbols,
            timeframe=timeframe,
            start=start, # Ex:  datetime(2022, 7, 1),
            end=end, # Ex: datetime(2022, 9, 1)
            limit=500,
            adjustment='split'
        )
        try: 
            bars = self.hist_api.get_stock_bars(request_params)
            candles = bars.df
            # convert to dataframe
            return candles
        except Exception as e:
            logger.error(f"Can't get data for {symbols}.")    
    